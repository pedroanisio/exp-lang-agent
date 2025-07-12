---
alwaysApply: false
version: 1.0
changelog:

- v1.0: Initial software requirements engineering standards

---

# rules-104-v1.0

DOMAIN: software requirements engineering
OBJECTIVE: ensure requirements quality, testability, and traceability through systematic requirements development aligned with TDD principles

VERSION_COMPATIBILITY_MATRIX:

- RULES_101: 'v1.1+' → STATUS: 'required foundation' → PRECEDENCE: 'level 1 (Core TDD and engineering principles)'
- RULES_102: 'v1.2+' → STATUS: 'required memory/ADR system' → PRECEDENCE: 'level 2 (Memory persistence and ADR management)'
- RULES_103: 'v1.2+' → STATUS: 'required implementation layer' → PRECEDENCE: 'level 3 (Implementation standards and practices)'
- RULES_104: 'v1.0' → STATUS: 'requirements engineering layer' → PRECEDENCE: 'level 4 (Requirements engineering and specification)'

RULE_PRECEDENCE_ACKNOWLEDGMENT:

- DEFERS_TO: 'rules-101 for TDD workflow adaptation to requirements'
- DEFERS_TO: 'rules-102 for requirements documentation and ADR management'
- DEFERS_TO: 'rules-103 for requirements formatting and standards'
- AUTHORITY: 'requirements engineering, acceptance criteria, user story structure'

## FILE PATH VARIABLES

REQ_ROOT = '${workspaceFolder}/requirements'
REQ_MEMORY_FILE = '${workspaceFolder}/.braains/REQUIREMENTS-MEMORY.md'
REQ_REGISTRY_FILE = '${workspaceFolder}/.braains/REQUIREMENTS-REGISTRY.md'
ACCEPTANCE_CRITERIA_DIR = '${workspaceFolder}/requirements/acceptance-criteria'
USER_STORIES_DIR = '${workspaceFolder}/requirements/user-stories'
REQ_ADR_DIR = '${workspaceFolder}/.braains/adrs/requirements'

## REQUIREMENTS TDD WORKFLOW

RTDD_WORKFLOW:

  REQUIREMENTS_RED_PHASE:
    - ACTION: 'write' → OBJECT: 'failing acceptance test' → STATUS: 'mandatory before requirements'
    - ACTION: 'define' → OBJECT: 'measurable acceptance criteria' → STATUS: 'must be testable'
    - ACTION: 'verify' → OBJECT: 'test failure' → STATUS: 'required before proceeding'
    - ACTION: 'document' → OBJECT: 'expected behavior' → STATUS: 'complete specification'

  REQUIREMENTS_GREEN_PHASE:
    - ACTION: 'write' → OBJECT: 'minimal requirement' → CONSTRAINT: 'only to satisfy acceptance criteria'
    - ACTION: 'verify' → OBJECT: 'acceptance criteria met' → CONSTRAINT: 'no additional functionality'
    - ACTION: 'maintain' → OBJECT: 'INVEST principles' → CONSTRAINT: 'all criteria met'

  REQUIREMENTS_REFACTOR_PHASE:
    - ACTION: 'improve' → OBJECT: 'requirement clarity' → CONSTRAINT: 'acceptance criteria remain valid'
    - ACTION: 'apply' → OBJECT: 'requirements standards' → CONSTRAINT: 'maintain testability'
    - ACTION: 'eliminate' → OBJECT: 'ambiguity and redundancy' → CONSTRAINT: 'preserve intent'

## REQUIREMENTS ENGINEERING CONSTRAINTS

REQ_CONSTRAINTS:

  1. ENTITY: 'requirements without acceptance criteria' → ACTION/NEGATION: 'never write' → RESULT: 'testable requirements'
  2. ENTITY: 'ambiguous language' → ACTION/NEGATION: 'eliminate' → RESULT: 'clear specifications'
  3. ENTITY: 'untestable requirements' → ACTION/NEGATION: 'reject' → RESULT: 'verifiable specifications'
  4. ENTITY: 'requirements without business value' → ACTION/NEGATION: 'question and remove' → RESULT: 'value-driven development'
  5. ENTITY: 'conflicting requirements' → ACTION/NEGATION: 'resolve before implementation' → RESULT: 'consistent system'
  6. ENTITY: 'requirements changes' → ACTION/NEGATION: 'document with ADRs' → RESULT: 'traceable evolution'
  7. ENTITY: 'assumptions' → ACTION/NEGATION: 'make explicit' → RESULT: 'transparent constraints'
  8. ENTITY: 'non-functional requirements' → ACTION/NEGATION: 'quantify with metrics' → RESULT: 'measurable quality'
  9. ENTITY: 'requirements dependencies' → ACTION/NEGATION: 'map explicitly' → RESULT: 'clear relationships'
  10. ENTITY: 'stakeholder approval' → ACTION/NEGATION: 'obtain before implementation' → RESULT: 'validated requirements'

## REQUIREMENTS QUALITY STANDARDS

REQ_QUALITY_CONSTRAINTS:

  1. ENTITY: 'INVEST principles' → ACTION/NEGATION: 'apply to all user stories' → RESULT: 'quality stories'
     - Independent: Can be developed in any order
     - Negotiable: Details can be discussed
     - Valuable: Provides business value
     - Estimable: Can be sized
     - Small: Fits in a sprint
     - Testable: Has acceptance criteria
  
  2. ENTITY: 'acceptance criteria' → ACTION/NEGATION: 'follow Given-When-Then format' → RESULT: 'behavioral specifications'
  3. ENTITY: 'requirements language' → ACTION/NEGATION: 'use consistent terminology' → RESULT: 'clear communication'
  4. ENTITY: 'requirements prioritization' → ACTION/NEGATION: 'apply MoSCoW method' → RESULT: 'focused development'
  5. ENTITY: 'requirements traceability' → ACTION/NEGATION: 'maintain bidirectional links' → RESULT: 'impact analysis'
  6. ENTITY: 'requirements versioning' → ACTION/NEGATION: 'track all changes' → RESULT: 'change management'
  7. ENTITY: 'requirements coverage' → ACTION/NEGATION: 'ensure complete system coverage' → RESULT: 'comprehensive specifications'
  8. ENTITY: 'requirements validation' → ACTION/NEGATION: 'verify with stakeholders' → RESULT: 'accurate requirements'

## REQUIREMENTS DOCUMENTATION STANDARDS

REQ_DOC_CONSTRAINTS:

  1. ENTITY: 'user story format' → ACTION/NEGATION: 'follow standard template' → RESULT: 'consistent stories'
  2. ENTITY: 'acceptance criteria format' → ACTION/NEGATION: 'use Gherkin syntax' → RESULT: 'executable specifications'
  3. ENTITY: 'requirements hierarchy' → ACTION/NEGATION: 'maintain epic → story → task structure' → RESULT: 'organized requirements'
  4. ENTITY: 'requirements metadata' → ACTION/NEGATION: 'include all required fields' → RESULT: 'complete documentation'
  5. ENTITY: 'requirements reviews' → ACTION/NEGATION: 'conduct before approval' → RESULT: 'quality assurance'
  6. ENTITY: 'requirements baseline' → ACTION/NEGATION: 'establish before development' → RESULT: 'stable foundation'
  7. ENTITY: 'requirements glossary' → ACTION/NEGATION: 'maintain domain terminology' → RESULT: 'consistent language'
  8. ENTITY: 'requirements models' → ACTION/NEGATION: 'use visual representations' → RESULT: 'clear understanding'

## REQUIREMENTS TEMPLATES

USER_STORY_TEMPLATE: |

# User Story: [US-XXX] - [Title]
  
## Metadata

- **ID**: US-XXX
- **Epic**: [Epic Name/ID]
- **Priority**: [Must/Should/Could/Won't]
- **Story Points**: [Estimation]
- **Stakeholder**: [Primary stakeholder]
- **Created**: [Date] by [Author]
- **Status**: [Draft/Review/Approved/In Development/Testing/Done]
- **Rule Compliance**: rules-101 v1.1+, rules-102 v1.2+, rules-103 v1.2+, rules-104 v1.0
  
## Story

  **As a** [type of user/persona]
  **I want** [goal/desire]
  **So that** [benefit/value]
  
## Acceptance Criteria
  
### Scenario 1: [Scenario Name]

  ```gherkin
  Given [initial context]
  When [event occurs]
  Then [expected outcome]
  ```
  
### Scenario 2: [Scenario Name]

  ```gherkin
  Given [initial context]
  And [additional context]
  When [event occurs]
  Then [expected outcome]
  And [additional outcome]
  ```
  
## Definition of Done

- [ ] All acceptance criteria pass
- [ ] Unit tests written and passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Accessibility requirements met
- [ ] Performance requirements met
- [ ] Security requirements validated
  
## Dependencies

- [List any dependencies on other stories/components]
  
## Assumptions

- [List any assumptions made]
  
## Notes

- [Additional context, constraints, or considerations]
  
## Test Cases

- [Link to detailed test cases if needed]
  
## Mockups/Wireframes

- [Link to design assets if applicable]

EPIC_TEMPLATE: |

# Epic: [E-XXX] - [Title]
  
## Metadata

- **ID**: E-XXX
- **Theme**: [Business theme/area]
- **Priority**: [Must/Should/Could/Won't]
- **Effort**: [T-shirt size or story points]
- **Stakeholder**: [Primary stakeholder]
- **Created**: [Date] by [Author]
- **Status**: [Draft/Review/Approved/In Development/Testing/Done]
- **Rule Compliance**: rules-101 v1.1+, rules-102 v1.2+, rules-103 v1.2+, rules-104 v1.0
  
## Epic Description

  **As a** [type of user/organization]
  **I want** [high-level goal]
  **So that** [business value/outcome]
  
## Success Criteria

- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]
  
## User Stories

- [US-XXX]: [Story title]
- [US-XXX]: [Story title]
- [US-XXX]: [Story title]
  
## Non-Functional Requirements

- **Performance**: [Specific metrics]
- **Security**: [Security requirements]
- **Accessibility**: [Accessibility standards]
- **Usability**: [Usability requirements]
  
## Dependencies

- [External dependencies]
- [Technical dependencies]
  
## Assumptions

- [Business assumptions]
- [Technical assumptions]
  
## Risks

- [Risk 1]: [Mitigation strategy]
- [Risk 2]: [Mitigation strategy]
  
## Definition of Done

- [ ] All user stories completed
- [ ] Success criteria met
- [ ] Non-functional requirements validated
- [ ] Stakeholder acceptance obtained
- [ ] Documentation complete

## REQUIREMENTS WORKFLOW

REQUIREMENTS_WORKFLOW:

  DISCOVERY_PHASE:
    - ACTION: 'conduct' → OBJECT: 'stakeholder interviews' → STATUS: 'mandatory for understanding'
    - ACTION: 'analyze' → OBJECT: 'business processes' → STATUS: 'required for context'
    - ACTION: 'identify' → OBJECT: 'user personas' → STATUS: 'mandatory for user stories'
    - ACTION: 'document' → OBJECT: 'business rules' → STATUS: 'required for validation'

  REQUIREMENTS_RED_PHASE:
    - ACTION: 'write' → OBJECT: 'failing acceptance test' → STATUS: 'mandatory before requirements'
    - ACTION: 'define' → OBJECT: 'testable acceptance criteria' → STATUS: 'must be executable'
    - ACTION: 'verify' → OBJECT: 'test failure' → STATUS: 'required before proceeding'

  REQUIREMENTS_GREEN_PHASE:
    - ACTION: 'write' → OBJECT: 'minimal user story' → CONSTRAINT: 'only to satisfy acceptance criteria'
    - ACTION: 'verify' → OBJECT: 'INVEST principles' → CONSTRAINT: 'all criteria met'
    - ACTION: 'validate' → OBJECT: 'stakeholder approval' → CONSTRAINT: 'business value confirmed'

  REQUIREMENTS_REFACTOR_PHASE:
    - ACTION: 'improve' → OBJECT: 'story clarity' → CONSTRAINT: 'acceptance criteria remain valid'
    - ACTION: 'eliminate' → OBJECT: 'ambiguity' → CONSTRAINT: 'preserve business intent'
    - ACTION: 'optimize' → OBJECT: 'story size' → CONSTRAINT: 'maintain testability'

  VALIDATION_PHASE:
    - ACTION: 'review' → OBJECT: 'requirements with stakeholders' → STATUS: 'mandatory for approval'
    - ACTION: 'validate' → OBJECT: 'acceptance criteria' → STATUS: 'must be testable'
    - ACTION: 'verify' → OBJECT: 'requirements completeness' → STATUS: 'comprehensive coverage'
    - ACTION: 'approve' → OBJECT: 'requirements baseline' → STATUS: 'development ready'

## REQUIREMENTS MANAGEMENT

REQ_MANAGEMENT_CONSTRAINTS:

  1. ENTITY: 'requirements changes' → ACTION/NEGATION: 'control through change process' → RESULT: 'managed evolution'
  2. ENTITY: 'requirements traceability' → ACTION/NEGATION: 'maintain throughout lifecycle' → RESULT: 'impact analysis'
  3. ENTITY: 'requirements status' → ACTION/NEGATION: 'track and report' → RESULT: 'progress visibility'
  4. ENTITY: 'requirements conflicts' → ACTION/NEGATION: 'resolve before implementation' → RESULT: 'consistent system'
  5. ENTITY: 'requirements coverage' → ACTION/NEGATION: 'ensure complete testing' → RESULT: 'verified system'
  6. ENTITY: 'requirements metrics' → ACTION/NEGATION: 'collect and analyze' → RESULT: 'process improvement'
  7. ENTITY: 'requirements repository' → ACTION/NEGATION: 'maintain centralized' → RESULT: 'single source of truth'
  8. ENTITY: 'requirements reviews' → ACTION/NEGATION: 'conduct regularly' → RESULT: 'quality assurance'

## INTEGRATION WITH EXISTING RULES

INTEGRATION_CONSTRAINTS:

  1. ENTITY: 'requirements ADRs' → ACTION/NEGATION: 'create for significant requirements decisions' → RESULT: 'documented rationale' → PRECEDENCE: 'defers to rules-102'
  2. ENTITY: 'requirements testing' → ACTION/NEGATION: 'follow TDD principles' → RESULT: 'test-driven requirements' → PRECEDENCE: 'defers to rules-101'
  3. ENTITY: 'requirements documentation' → ACTION/NEGATION: 'follow formatting standards' → RESULT: 'consistent documentation' → PRECEDENCE: 'defers to rules-103'
  4. ENTITY: 'requirements memory' → ACTION/NEGATION: 'update context files' → RESULT: 'persistent requirements knowledge' → PRECEDENCE: 'defers to rules-102'
  5. ENTITY: 'requirements patterns' → ACTION/NEGATION: 'document in pattern registry' → RESULT: 'reusable requirements patterns' → PRECEDENCE: 'defers to rules-102'

## REQUIREMENTS QUALITY GATES

QUALITY_GATES:

  GATE_1_COMPLETENESS:
    - CRITERION: 'all acceptance criteria defined' → STATUS: 'mandatory'
    - CRITERION: 'business value articulated' → STATUS: 'mandatory'
    - CRITERION: 'stakeholder identified' → STATUS: 'mandatory'
    - CRITERION: 'dependencies mapped' → STATUS: 'mandatory'

  GATE_2_QUALITY:
    - CRITERION: 'INVEST principles satisfied' → STATUS: 'mandatory'
    - CRITERION: 'acceptance criteria testable' → STATUS: 'mandatory'
    - CRITERION: 'language clear and unambiguous' → STATUS: 'mandatory'
    - CRITERION: 'assumptions documented' → STATUS: 'mandatory'

  GATE_3_VALIDATION:
    - CRITERION: 'stakeholder approval obtained' → STATUS: 'mandatory'
    - CRITERION: 'acceptance criteria validated' → STATUS: 'mandatory'
    - CRITERION: 'conflicts resolved' → STATUS: 'mandatory'
    - CRITERION: 'traceability established' → STATUS: 'mandatory'

  GATE_4_IMPLEMENTATION_READY:
    - CRITERION: 'development team understands requirements' → STATUS: 'mandatory'
    - CRITERION: 'acceptance tests automated' → STATUS: 'mandatory'
    - CRITERION: 'definition of done agreed' → STATUS: 'mandatory'
    - CRITERION: 'requirements baseline approved' → STATUS: 'mandatory'

## ENFORCEMENT PROTOCOLS

ENFORCEMENT_WORKFLOW:

  PRE_REQUIREMENTS_CHECKS:
    - ACTION: 'verify' → OBJECT: 'stakeholder availability' → STATUS: 'mandatory for discovery'
    - ACTION: 'prepare' → OBJECT: 'requirements templates' → STATUS: 'standardization ready'
    - ACTION: 'establish' → OBJECT: 'acceptance criteria format' → STATUS: 'testing ready'

  DURING_REQUIREMENTS_CHECKS:
    - ACTION: 'validate' → OBJECT: 'INVEST principles' → STATUS: 'continuous checking'
    - ACTION: 'verify' → OBJECT: 'acceptance criteria testability' → STATUS: 'real-time validation'
    - ACTION: 'check' → OBJECT: 'stakeholder alignment' → STATUS: 'ongoing verification'

  POST_REQUIREMENTS_CHECKS:
    - ACTION: 'review' → OBJECT: 'requirements quality' → STATUS: 'completion validation'
    - ACTION: 'verify' → OBJECT: 'traceability completeness' → STATUS: 'impact analysis ready'
    - ACTION: 'confirm' → OBJECT: 'implementation readiness' → STATUS: 'development ready'

COMPATIBILITY:

- REQUIRES: 'rules-101 v1.1+'
- REQUIRES: 'rules-102 v1.2+'
- REQUIRES: 'rules-103 v1.2+'
- CURRENT_VERSION: 'v1.0'
- PRECEDENCE_LEVEL: '4 (Requirements engineering and specification)'

