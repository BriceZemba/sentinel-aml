"""CrewAI investigation crew - a role-based team of specialist analysts.

Imported only when an LLM is available (see runner.py). The crew mirrors how a
real financial-intelligence unit is staffed: specialists gather evidence with
deterministic tools, a lead investigator weighs it and recommends. The *tools*
carry the auditable logic; the LLM agents orchestrate and narrate - it never
invents the risk score.
"""
from __future__ import annotations

import json
import os

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool

import analysis

# ---- tools (thin wrappers over the framework-free analysis core) ----


@tool("Resolve entity and screen sanctions/PEP")
def resolve_entity_tool(customer_id: str) -> str:
    """Resolve the subject customer + beneficial owners and screen them against
    sanctions and PEP lists. Returns JSON with customer, evidence, red_flags."""
    return json.dumps(analysis.resolve_entity(customer_id))


@tool("Analyze account transactions for AML typologies")
def analyze_transactions_tool(account_id: str, customer_json: str) -> str:
    """Detect structuring, layering, high-risk geography and profile deviation on
    an account. Pass the resolved customer as JSON. Returns JSON evidence."""
    customer = json.loads(customer_json) if customer_json else {}
    return json.dumps(analysis.analyze_transactions(account_id, customer))


@tool("Screen adverse media for subject and counterparties")
def adverse_media_tool(customer_json: str, transactions_json: str) -> str:
    """Negative-news screen over the subject and its counterparties. Returns JSON evidence."""
    return json.dumps(analysis.screen_adverse_media(json.loads(customer_json or "{}"), json.loads(transactions_json or "[]")))


def _llm() -> LLM:
    return LLM(model=os.getenv("SENTINEL_CREW_MODEL", "anthropic/claude-opus-4-8"), temperature=0.1)


def build_crew() -> Crew:
    llm = _llm()
    entity_analyst = Agent(
        role="KYC & Sanctions Analyst",
        goal="Resolve the customer and its owners and surface any sanctions/PEP exposure.",
        backstory="A meticulous CDD specialist who never lets a beneficial owner go unscreened.",
        tools=[resolve_entity_tool], llm=llm, verbose=False, allow_delegation=False,
    )
    txn_analyst = Agent(
        role="Transaction Analyst",
        goal="Identify laundering typologies in the account's activity with cited evidence.",
        backstory="A former bank examiner who can spot structuring and layering in their sleep.",
        tools=[analyze_transactions_tool], llm=llm, verbose=False, allow_delegation=False,
    )
    osint_analyst = Agent(
        role="OSINT Analyst",
        goal="Find adverse media on the subject and counterparties.",
        backstory="An open-source intelligence researcher focused on financial-crime signals.",
        tools=[adverse_media_tool], llm=llm, verbose=False, allow_delegation=False,
    )
    lead = Agent(
        role="Lead Investigator",
        goal="Weigh all evidence and recommend FILE_SAR, ESCALATE, REQUEST_INFO, or DISMISS with a clear rationale.",
        backstory="A seasoned MLRO-track investigator who writes defensible, regulator-ready conclusions.",
        llm=llm, verbose=False, allow_delegation=False,
    )

    t_entity = Task(description="Resolve and screen customer {customer_id}.",
                    expected_output="JSON from the entity tool.", agent=entity_analyst)
    t_txn = Task(description="Analyze transactions for account {account_id} using the resolved customer.",
                 expected_output="JSON from the transaction tool.", agent=txn_analyst, context=[t_entity])
    t_osint = Task(description="Screen adverse media for the subject and counterparties.",
                   expected_output="JSON from the adverse-media tool.", agent=osint_analyst, context=[t_entity, t_txn])
    t_lead = Task(
        description=(
            "Combine all evidence for alert {alert_id} (rule {rule}, priority {priority}). "
            "Produce a final recommendation. Sanctions exposure must ESCALATE. "
            "Return strictly the InvestigationOutput JSON schema."
        ),
        expected_output="InvestigationOutput JSON.", agent=lead, context=[t_entity, t_txn, t_osint],
    )
    return Crew(agents=[entity_analyst, txn_analyst, osint_analyst, lead],
                tasks=[t_entity, t_txn, t_osint, t_lead], process=Process.sequential, verbose=False)
