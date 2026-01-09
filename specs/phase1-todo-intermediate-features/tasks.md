---
description: "Task list for Todo CLI with Intermediate Features implementation"
---

# Tasks: Todo CLI with Intermediate Features

**Input**: Design documents from `/specs/003-todo-intermediate-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test requirements in the specification, so tests are not included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan ensuring clean architecture
- [ ] T002 Initialize Python 3.13+ project with UV package manager (no manual code writing - use Claude Code)
- [ ] T003 [P] Configure linting and formatting tools to ensure code quality
- [ ] T004 Set up in-memory data storage structure (no file/database persistence)
- [ ] T005 Create /src directory structure for modular code organization
- [ ] T006 Configure development environment with specified technology stack (UV, Python 3.13+, Claude Code, Spec-Kit Plus)
- [ ] T007 Establish Product Architect development approach with specification-driven implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 [P] Extend Task model with priority and tags in src/models.py
- [ ] T009 [P] Update Task constructor to accept priority and tags parameters in src/models.py
- [ ] T010 [P] Add validation for priority values (High/Medium/Low) in src/models.py
- [ ] T011 [P] Add default priority value (Medium) in src/models.py
- [X] T012 Create basic service functions structure in src/services.py
- [ ] T013 Create main CLI structure in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Enhanced Task Management with Priorities and Tags (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with priority levels and tags, and these attributes will be properly stored and displayed when viewing tasks

**Independent Test**: Users can add a new task, select a priority level (High/Medium/Low) and add tags (comma-separated), and see the priority and tags for the task clearly displayed when viewing tasks

### Implementation for User Story 1

- [X] T014 [P] [US1] Update Task model to include priority and tags attributes in src/models.py
- [X] T015 [P] [US1] Update Task string representation to include priority and tags in src/models.py
- [X] T016 [US1] Update task creation in services to accept priority and tags in src/services.py
- [X] T017 [US1] Update task viewing to display priority and tags in src/services.py
- [X] T018 [US1] Update task updating to modify priority and tags in src/services.py
- [X] T019 [US1] Modify CLI to prompt for priority during task creation in src/main.py
- [X] T020 [US1] Modify CLI to prompt for tags during task creation in src/main.py
- [X] T021 [US1] Update task display format to show priority and tags in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Search Functionality (Priority: P1)

**Goal**: Users can enter a search term and see filtered results that match the keyword in title, description, or tags

**Independent Test**: Users can enter a search keyword and see only tasks containing that keyword in title, description, or tags; when search is cleared, all tasks are displayed again

### Implementation for User Story 2

- [X] T022 [P] [US2] Implement search_tasks function in src/services.py to search across title, description, and tags
- [X] T023 [P] [US2] Add search algorithm that checks all three fields case-insensitively in src/services.py
- [X] T024 [US2] Create search menu option in CLI in src/main.py
- [X] T025 [US2] Implement search input flow in CLI in src/main.py
- [X] T026 [US2] Display search results in CLI in src/main.py
- [X] T027 [US2] Handle empty search query case in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Filtering Capabilities (Priority: P2)

**Goal**: Users can apply filters for completion status, priority level, or specific tags and see only matching tasks

**Independent Test**: Users can apply filters for completion status, priority level, or specific tags and see only matching tasks; this delivers value by allowing targeted task views

### Implementation for User Story 3

- [X] T028 [P] [US3] Implement filter_by_status function in src/services.py
- [X] T029 [P] [US3] Implement filter_by_priority function in src/services.py
- [X] T030 [P] [US3] Implement filter_by_tag function in src/services.py
- [X] T031 [US3] Create filtering menu option in CLI in src/main.py
- [X] T032 [US3] Implement filter selection flow in CLI in src/main.py
- [X] T033 [US3] Display filtered results in CLI in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Task Sorting Options (Priority: P2)

**Goal**: Users can select different sorting options and see the task list reorder accordingly

**Independent Test**: Users can select different sorting options (by priority, alphabetically by title, or by creation order) and see the task list reorder accordingly; this delivers value by making it easier to find important tasks

### Implementation for User Story 4

- [X] T034 [P] [US4] Implement sort_by_priority function in src/services.py
- [X] T035 [P] [US4] Implement sort_alphabetically function in src/services.py
- [X] T036 [P] [US4] Maintain default sort by creation order in src/services.py
- [X] T037 [US4] Create sorting menu option in CLI in src/main.py
- [X] T038 [US4] Implement sort selection flow in CLI in src/main.py
- [X] T039 [US4] Display sorted results in CLI in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Menu-Driven CLI Interface (Priority: P1)

**Goal**: Users can navigate through clearly labeled menu options to perform all available actions with a consistent and intuitive user interface

**Independent Test**: Users can see the main menu with numbered options 1-10, select an option, and be guided through the appropriate workflow with clear prompts; when entering invalid menu choices, they receive friendly error messages

### Implementation for User Story 5

- [X] T040 [P] [US5] Replace command-line argument parsing with menu system in src/main.py
- [X] T041 [P] [US5] Implement main menu loop with options 1-10 in src/main.py
- [X] T042 [P] [US5] Map menu options to service layer operations in src/main.py
- [X] T043 [US5] Add input validation for menu selections in src/main.py
- [X] T044 [US5] Implement friendly error handling for invalid menu choices in src/main.py
- [X] T045 [US5] Implement graceful exit functionality in src/main.py
- [X] T046 [US5] Format main menu display with consistent styling in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T047 [P] Update documentation in README.md
- [X] T048 Code cleanup and refactoring across all modules
- [X] T049 Performance optimization for search/filter/sort operations
- [X] T050 [P] Add error handling for edge cases (empty lists, invalid inputs)
- [X] T051 Security validation (input sanitization)
- [X] T052 Run validation against success criteria from specification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all model updates for User Story 1 together:
Task: "Update Task model to include priority and tags attributes in src/models.py"
Task: "Update Task string representation to include priority and tags in src/models.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify functionality after each task or logical group
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence