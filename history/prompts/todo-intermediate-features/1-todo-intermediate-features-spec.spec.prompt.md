---
id: 1
title: todo-intermediate-features-spec
stage: spec
date: 2026-01-01
surface: agent
model: Claude Sonnet 4.5
feature: todo-intermediate-features
branch: 003-todo-intermediate-features
user: default_user
command: /sp.specify
labels: ["specification", "todo", "cli", "intermediate-features"]
links:
  spec: specs/003-todo-intermediate-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/003-todo-intermediate-features/spec.md
 - specs/003-todo-intermediate-features/checklists/requirements.md
tests:
 - specs/003-todo-intermediate-features/spec.md validated against quality checklist
---

## Prompt

```text
Your task is to produce a **new specification** that extends the
**existing Phase I Basic Todo CLI application**
to support **INTERMEDIATE LEVEL features only**.

---

## Context
- Project: Evolution of Todo
- Phase: Phase I
- Level: Intermediate (Organization & Usability)
- Interface: Python Console (CLI)
- Storage: In-memory only
- Language: Python 3.13+
- Environment Manager: UV
- Code Generator: Claude Code
- Manual code writing is strictly forbidden

This specification must **build on top of the already completed Basic Level**.
Do NOT redesign or remove existing basic functionality.

---

## Scope Boundary (VERY IMPORTANT)

### INCLUDED (Intermediate Only)
- Priorities
- Tags / Categories
- Search
- Filter
- Sorting
- Menu-based CLI interaction

### EXCLUDED (Must NOT appear)
- aration of concerns
- Business logic must not leak into CLI layer
- In-memory storage only

---

## Non-Functional Requirements
- Clear and readable CLI output
- Graceful handling of invalid menu choices
- Friendly error messages
- Clean, maintainable Python code

---

## Acceptance Criteria
- User can add tasks with priority and tags
- User can search tasks by keyword
- User can filter tasks by status, priority, or tag
- User can sort tasks using menu options
- Menu-based CLI works reliably
- No advanced-level features are present

---

## DelRecurring tasks
- Due dates
- Notifications
- Any AI features
- Any persistence or database

---

## Existing Basic Features (Already Implemented)
- Add Task
- View Tasks
- Update Task
- Delete Task
- Mark Task Complete / Incomplete

These must continue working without breaking changes.

---

## New Intermediate Features (REQUIRED)

### 1. Task Priorities
- Each task must support a priority level:
  - High
  - Medium
  - Low
- Default priority: Medium
- Priority must be editable during task update

---

### 2. Tags / Categories
- Tasks may have zero or more tags
- Tags are short strings (e.g., `work`, `home`, `study`)
- Tags are optional
- Multiple tags allowed per task

---

### 3. Search Functionality
- User can search tasks by keyword
- Search applies to:
  - Title
  - Description
  - Tags

---

### 4. Filter Functionality
User must be able to filter tasks by:
- Completion status (completed / incomplete)
- Priority level
- Tag

---

### 5. Sorting
User must be able to sort task list by:
- Priority
- Alphabetical order (title)
- Creation order (default)

---

## CLI UX REQUIREMENTS (MANDATORY)

The CLI must switch from free-text commands to a **menu-driven interface**.

### Main Menu Output Format (Exact Style Required)

--- Todo Application ---

Add Task

View All Tasks

Update Task

Delete Task

Mark Task Complete

Mark Task Incomplete

Search Tasks

Filter Tasks

Sort Tasks

Exit

Enter your choice (1-10):

yaml
Copy code

---

### Add Task Flow (Example)

Enter task title:
Enter task description:
Select priority (High / Medium / Low):
Enter tags (comma-separated, optional):

yaml
Copy code

---

### View Task Output Requirements
Each task must display:
- ID
- Title
- Completion status
- Priority
- Tags

Example (format flexible but must include all fields):

[1] Buy groceries
Status: Incomplete
Priority: High
Tags: home, errands

yaml
Copy code

---

## Data Model Changes

Extend the existing Task model to include:
- priority: enum/string (High | Medium | Low)
- tags: list of strings

Do NOT remove existingiverable
Return **only the Intermediate Level specification**
in **well-structured Markdown**.

Do NOT:
- Generate code
- Modify Basic Level behavior
- Include Advanced Level features
```

## Response snapshot

Created comprehensive specification for intermediate todo CLI features including:
- Task priorities (High/Medium/Low)
- Tags/Categories support
- Search functionality
- Filter capabilities
- Sorting options
- Menu-driven CLI interface
- All requirements documented with user stories, functional requirements, and success criteria

## Outcome

- ✅ Impact: New feature specification created for intermediate todo CLI features
- 🧪 Tests: Specification validated against quality checklist criteria
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Successfully extended basic todo functionality with intermediate features while maintaining existing functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase