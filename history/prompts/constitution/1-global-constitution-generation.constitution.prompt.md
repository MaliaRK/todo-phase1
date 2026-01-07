---
id: 1
title: "Global Constitution Generation"
stage: "constitution"
date_iso: "2026-01-04"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "003-todo-intermediate-features"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "spec", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "sp.constitution.md"
tests_yaml: []
---

# Prompt History Record: Global Constitution Generation

## Prompt Text
```
Your task is to generate a **GLOBAL Markdown Constitution (`sp.constitution.md`)`
for the full project:

"The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI"

This Constitution is the **highest governing document** for ALL phases:
Phase I → Phase V.

────────────────────────────────────────
ABSOLUTE AUTHORITY RULE
────────────────────────────────────────

This Constitution overrides:
- All feature specs
- All component specs
- All generated code
- All future refinements

No specification or implementation may violate this Constitution.

────────────────────────────────────────
PROJECT SCOPE (ALL PHASES)
────────────────────────────────────────

The project evolves a Todo application through five phases:

Phase I   – In-memory Python console application
Phase II  – Full-stack web application with persistence
Phase III – AI-powered conversational Todo agent
Phase IV  – Local Kubernetes deployment
Phase V   – Cloud-native, event-driven AI system

The Constitution must support **evolution without rewrite**.

────────────────────────────────────────
DEVELOPMENT PHILOSOPHY
────────────────────────────────────────

- The human developer acts as a **System Architect**, not a coder
- Claude Code acts as the **Implementation Engine**
- All software is derived from **explicit written specifications**
- Manual code writing is **strictly forbidden**
- Correctness is achieved by **spec refinement, not patching code**

────────────────────────────────────────
SPEC-DRIVEN DEVELOPMENT LAWS
────────────────────────────────────────

1. No code may exist without a governing spec
2. Specs must define behavior, not implementation tricks
3. Code is disposable; specs are canonical
4. Iteration happens by refining specs, never editing code
5. Generated output must be reproducible from specs alone

────────────────────────────────────────
ARCHITECTURAL EVOLUTION PRINCIPLES
────────────────────────────────────────

- Each phase extends capabilities without breaking prior contracts
- Architectural decisions must enable:
  - Persistence
  - Distribution
  - AI agency
  - Cloud-native execution
- Early phases must not block later phases
- Backward compatibility of intent is mandatory

────────────────────────────────────────
DOMAIN-FIRST DESIGN
────────────────────────────────────────

- The Todo domain is the core abstraction
- UI, API, agents, ──────────────────
OUTPUT REQUIREMENTS
────────────────────────────────────────

- Output valid Markdown only
- File name: `sp.constitution.md`
- Tone: strict, authoritative, architectural
- No code blocks
- No implementation details
- No phase-specific features

Generate the GLOBAL Constitution now.
```

## Response Text
Generated a comprehensive global constitution document that serves as the highest governing document for all five phases of the "Evolution of Todo" project. The constitution establishes core principles for spec-driven development, system architect role definition, evolution without rewrite, todo domain primacy, and forward compatibility architecture. It includes governance sections for development practices, architectural evolution, AI integration readiness, cloud-native foundation, compliance, and phase-specific constraints.

## Outcome
Successfully created the global constitution file `sp.constitution.md` that will govern all phases of the project from the in-memory console application through the cloud-native AI system. The constitution ensures evolution without rewrite and maintains architectural coherence across all phases.