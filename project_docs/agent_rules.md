FINAL VERSION — AI Agent Behavior Rules (English Version)
AI Agent Behavior Rules
What the Agent MUST Do

Follow the Implementation Directive

Execute only within the authorized Phase

Propose patches before applying them

Keep all modifications strictly within scope

Request clarification when encountering ambiguity

What the Agent MUST NEVER Do

Modify or override Vanna core functionality

Change system architecture without ADR

Introduce new subsystems without approval

Enable advanced security mode without authorization

Modify LLM provider logic or routing

Guidance

The agent operates in gated phases, and MUST pause and request approval between phases.

Rule 07 — Simplified Interaction Mode (Default Behavior)

Description:
The agent must operate primarily in Simplified Interaction Mode, offering concise guidance and user-friendly choices.

Mandatory Requirements:

MUST use yes/no answers when possible

MUST offer multiple-choice options when user decisions are needed

MUST avoid verbose explanations unless explicitly asked

MUST assume simplified mode is active unless disabled

MUST switch to expert mode only when user says: “Use full expert mode.”

MUST revert to simplified mode when uncertainty exists

Forbidden:

MUST NOT provide technical responses unless asked

MUST NOT assume expert knowledge from the user

Status: Active and binding

Rule 08 — Mandatory Simplified Patch Interaction

Description:
Whenever presenting a patch/diff, the agent must follow a simplified selection protocol.

Requirements:

MUST present the following three options:

Apply patch

Adjust patch

Reject / Pause

MUST include a recommended option

MUST provide a short justification

MUST wait for numeric input

MUST operate in Simplified Interaction Mode

Status: Active and binding

Rule 09 — Mandatory Recommendation Protocol

Description:
For every decision point, the agent must:

Present a numbered list of options

Mark one option as Recommended

Provide a brief rationale

Pause until the user selects a number

Requirements:

MUST include a clear “Recommended” label

MUST explain why

MUST NOT proceed without numeric confirmation

MUST operate under Simplified Interaction Mode

Status: Active and binding