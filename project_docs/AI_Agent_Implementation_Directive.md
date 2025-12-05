AI AGENT IMPLEMENTATION DIRECTIVE — MAJED VANNA PROJECT
Authoritative Execution Blueprint for the Autonomous Agent

Version: 1.1 — January 2026
Status: Active
Scope: Mandatory for all automated development inside the Majed Vanna project

1. Purpose of This Directive

This document defines the only permitted execution boundaries for the autonomous AI Agent responsible for development, stabilization, and enhancement of the Majed Vanna Enterprise System.

It specifies:

Allowed and forbidden operations

Phase-based execution workflow

Security and safety hard requirements

Integration rules for Oracle, SQLite, LM Studio, and Vanna

Documentation, audit, and compliance duties

The agent MUST treat this directive as law and MUST NOT act outside its scope.

2. Database Architecture Rules
✔ Primary Database (MANDATORY): Oracle

Oracle is the official production backend.
All performance, stability, and metadata extraction work MUST target Oracle as the priority integration.

✔ Secondary Database (Optional for Local Testing): SQLite

SQLite may be used ONLY for:

Local development

Rapid prototyping

Unit tests

Behavior simulation

✖ The agent MUST NOT:

Add support for PostgreSQL, MySQL, MSSQL, or any third-party database

Introduce new DB abstraction layers

Modify the existing DB provider architecture

3. LLM Provider Rules
✔ Default LLM Provider: LM Studio (OpenAI-Compatible REST)

The agent MUST retain the current approach.
The model must behave as an OpenAI-compatible endpoint.

Allowed:

LM Studio REST-compliant LLMs

No schema modification

No provider switching logic added

Forbidden:

Adding new LLM providers

Changing model-selection architecture

Altering Vanna’s LLM execution mechanisms

4. Security Mode System

The system exposes a required environment variable:

ENV_SECURITY_MODE=on    # Enable enhanced security features
ENV_SECURITY_MODE=off   # Default project mode


Enhanced features MUST only activate when explicitly set to "on".

5. Security Requirements

Security is mandatory and phase-gated.

5.1 Baseline Security (Always Active)
Mandatory Rules:
✔ SQL Safety

Single-statement queries only

Parameterized execution

Destructive verbs blocked unless whitelisted

✔ Prompt Safety

Block role-change attempts

Block system override patterns

Block instruction-hijacking phrases

✔ Error Safety

Never expose stack traces to users

Display safe, generic messages

Write full technical errors only to logs

✔ Secrets Management

No secrets in source code

All sensitive values MUST come from .env

✔ Logging Safety

No logging of passwords, tokens, credentials, or sensitive metadata

5.2 Enhanced Security (Active Only When ENV_SECURITY_MODE=on)

When security mode = on, the agent MUST enable:

🔒 Advanced SQL Guard

Lightweight AST analysis

Query-shape validation

Suspicious-statement detection

🔒 Advanced Prompt Guard

Semantic pattern detection

Anti-jailbreaking heuristics

Output validation after LLM generation

🔒 Enhanced DB Safety

Optional read-only execution

Mandatory fetch limits

High-risk query detection

🔒 Structured Logging

JSON-formatted logs

Correlation ID injection

Sensitive field masking

6. Vanna Framework Compliance

The agent MUST preserve all native Vanna features.

✔ Mandatory Features to Support

ask()

explain()

summarize_results()

generate_followup_questions()

get_results()

train(ddl, documentation, sql, df)

vector retrieval

visualization tools

UI component streaming

✖ Forbidden Actions

Rewriting Vanna internals

Replacing core Vanna capabilities

Creating parallel LLM/DB workflows

Removing built-in Vanna UI components

7. UI Implementation Rules
✔ Allowed:

Serve the default embedded Vanna UI

Style adjustments or bug fixes ONLY

✖ Forbidden:

Building a new frontend

Introducing React, Vue, Angular, Svelte, etc.

Adding complex client-side frameworks

8. Deployment Rules
Allowed NOW:

Local development using:

uvicorn app.main:app --reload

Forbidden until Phase 4:

Docker

Nginx reverse proxy

System services (Windows/Linux)

Production infra

9. Phase 1 — Authorized Tasks (Executable Now)

The agent MUST execute Phase 1 tasks in order, and MUST pause after each phase.

Phase 1.A — Input Safety Layer

Validate payloads

Enforce strict schemas

Sanitize user input

Phase 1.B — SQL Safety Layer

Validate SQL structure

Block multistatement execution

Introduce SQL guardrail

Phase 1.C — Prompt Safety Layer

Regex-based injection blocker

Prompt structure enforcement

Phase 1.D — Error Handling

Unified exception handling

User-safe response mapping

Internal logging enhancements

Phase 1.E — Secrets & Environment

Remove ALL secrets from code

Ensure configuration comes from .env

Repository audit for plaintext secrets

10. Phase 2 — Stabilization & Performance

Starts only after explicit authorization.

Phase 2.A — Operational Stabilization

Oracle connection pooling

SQLite mode refinement

API health probes

Phase 2.B — Performance Improvements

LLM latency optimization

Database query roundtrip tuning

Phase 2.C — Test Coverage

20–30% minimum coverage

ask() pipeline tests

DB providers integration tests

11. Forbidden Actions (Critical Section)

The agent MUST NOT:

Modify architecture

Change folder structure

Begin semantic layer implementation

Modify semantic_model.yaml

Add new DB/LLM providers

Deploy Docker/Nginx early

Rewrite any Vanna-provided function

Enable advanced RBAC

Add caching layers

Remove files without explicit instruction

If uncertainty arises → STOP and request clarification.

12. Completion Requirements Before Next Phase

The agent MUST confirm:

✔ Security

Input, prompt, and SQL safety validated

No leakage of sensitive information

✔ Stability

Oracle workflow stable

SQLite dev-mode reliable

No runtime crashes

✔ Functionality

ask(), explain(), summarize_results(), generate_followup_questions() work end-to-end

✔ Configuration

ENV_SECURITY_MODE toggles all enhanced systems correctly

13. Final Rule

Any action outside this directive is strictly prohibited unless the human owner updates this file.

The agent MUST re-read this document before every change.

✅ End of AI Agent Implementation Directive

