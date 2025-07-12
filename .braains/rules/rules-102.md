---
alwaysApply: true
version: 1.2
changelog:
  - v1.0: Initial memory persistence and context awareness system
  - v1.1: Added comprehensive ADR (Architecture Decision Record) management
  - v1.2: Added rule precedence hierarchy and version compatibility matrix
---

# rules-102-v1.2

DOMAIN: software engineering
OBJECTIVE: ensure code quality and maintainability through adherence to engineering principles, persistent context awareness, and comprehensive architectural decision documentation

RULE_PRECEDENCE_HIERARCHY:

- PRECEDENCE_LEVEL_1: 'rules-101 (Core TDD and engineering principles)' → AUTHORITY: 'TDD workflow, testing principles, SOLID/DRY adherence'
- PRECEDENCE_LEVEL_2: 'rules-102 (Memory persistence and ADR management)' → AUTHORITY: 'architectural documentation, context preservation, ADR lifecycle'
- PRECEDENCE_LEVEL_3: 'rules-103 (Implementation standards and practices)' → AUTHORITY: 'coding standards, tooling, language-specific practices'
- CONFLICT_RESOLUTION: 'higher precedence level takes priority in case of conflicts'
- INTEGRATION_PRINCIPLE: 'all rules work together, precedence only applies to direct conflicts'

VERSION_COMPATIBILITY_MATRIX:

- RULES_101: 'v1.1+' → STATUS: 'required foundation'
- RULES_102: 'v1.2' → STATUS: 'current version'
- RULES_103: 'v1.1+' → STATUS: 'required implementation layer'
- COMPATIBILITY_CHECK: 'verify version compatibility before applying rules'

## FILE PATH VARIABLES

PROJECT_ROOT = '${workspaceFolder}'
BRAAINS_ROOT = '${workspaceFolder}/.braains'
AI_MEMORY_FILE = '${workspaceFolder}/.braains/AI-MEMORY.md'
AI_NOTES_FILE = '${workspaceFolder}/.braains/AI-NOTES-2-SELF.md'
PATTERN_REGISTRY_FILE = '${workspaceFolder}/.braains/PATTERN-REGISTRY.md'
ADR_DIRECTORY = '${workspaceFolder}/.braains/adrs'
ADR_INDEX_FILE = '${workspaceFolder}/.braains/adrs/ADR-INDEX.md'
ADR_TEMPLATE_FILE = '${workspaceFolder}/.braains/adrs/ADR-TEMPLATE.md'

## MEMORY PERSISTENCE LAYER

MEMORY_MANAGEMENT:
  FILES:
    - NAME: '${AI_MEMORY_FILE}'
      PURPOSE: 'persistent architectural decisions and patterns'
      UPDATE: 'after each significant implementation'
    - NAME: '${AI_NOTES_FILE}'
      PURPOSE: 'context-aware instructions and learnings'
      UPDATE: 'continuously during development'
    - NAME: '${PATTERN_REGISTRY_FILE}'
      PURPOSE: 'established patterns and their usage'
      UPDATE: 'when new patterns are introduced or modified'
    - NAME: '${ADR_INDEX_FILE}'
      PURPOSE: 'centralized index of all architectural decision records'
      UPDATE: 'whenever new ADRs are created or statuses change'

ADR_MANAGEMENT:
  DIRECTORY_STRUCTURE:
    - '${ADR_DIRECTORY}/' → 'root directory for all ADRs'
    - '${ADR_DIRECTORY}/ADR-001-[title].md' → 'individual ADR files'
    - '${ADR_DIRECTORY}/ADR-INDEX.md' → 'master index of all ADRs'
    - '${ADR_DIRECTORY}/ADR-TEMPLATE.md' → 'template for new ADRs'

  NUMBERING_SYSTEM:
    - FORMAT: 'ADR-{NNN}-{kebab-case-title}.md'
    - SEQUENCE: 'sequential numbering starting from 001'
    - EXAMPLES: 'ADR-001-database-selection.md', 'ADR-002-authentication-strategy.md'

PRE_EXECUTION_PROTOCOL:
  MANDATORY_ACTIONS:
    1. ACTION: 'verify' → OBJECT: 'version compatibility' → STATUS: 'prerequisite for execution'
    2. ACTION: 'read' → FILES: ['${AI_MEMORY_FILE}', '${AI_NOTES_FILE}', '${PATTERN_REGISTRY_FILE}', '${ADR_INDEX_FILE}']
    3. ACTION: 'scan' → TARGET: 'repository structure' → OUTPUT: 'file list and architecture'
    4. ACTION: 'analyze' → TARGET: 'existing patterns' → OUTPUT: 'pattern compliance check'
    5. ACTION: 'verify' → TARGET: 'test suite integrity' → OUTPUT: 'test corruption prevention'
    6. ACTION: 'review' → TARGET: 'recent ADRs' → OUTPUT: 'architectural decision awareness'

POST_EXECUTION_PROTOCOL:
  MANDATORY_ACTIONS:
    1. ACTION: 'document' → TARGET: 'architectural decisions' → FILE: '${AI_MEMORY_FILE}'
    2. ACTION: 'record' → TARGET: 'pattern usage' → FILE: '${PATTERN_REGISTRY_FILE}'
    3. ACTION: 'note' → TARGET: 'context and rationale' → FILE: '${AI_NOTES_FILE}'
    4. ACTION: 'evaluate' → TARGET: 'ADR creation necessity' → RESULT: 'create ADR if architectural decision made'
    5. ACTION: 'update' → TARGET: 'ADR index' → FILE: '${ADR_INDEX_FILE}'
    6. ACTION: 'log' → TARGET: 'rule precedence usage' → PURPOSE: 'conflict resolution tracking'

## ADR CREATION TRIGGERS

MANDATORY_ADR_CREATION_SCENARIOS:

  1. TRIGGER: 'new architectural pattern introduction' → ACTION: 'create ADR' → RATIONALE: 'document pattern choice and alternatives'
  2. TRIGGER: 'technology stack decision' → ACTION: 'create ADR' → RATIONALE: 'capture technology evaluation and selection'
  3. TRIGGER: 'significant refactoring decision' → ACTION: 'create ADR' → RATIONALE: 'document refactoring approach and trade-offs'
  4. TRIGGER: 'breaking change implementation' → ACTION: 'create ADR' → RATIONALE: 'justify breaking change and migration strategy'
  5. TRIGGER: 'security approach selection' → ACTION: 'create ADR' → RATIONALE: 'document security model and considerations'
  6. TRIGGER: 'testing strategy change' → ACTION: 'create ADR' → RATIONALE: 'capture testing approach rationale'
  7. TRIGGER: 'integration pattern decision' → ACTION: 'create ADR' → RATIONALE: 'document integration choices and protocols'
  8. TRIGGER: 'performance optimization strategy' → ACTION: 'create ADR' → RATIONALE: 'record performance decisions and trade-offs'
  9. TRIGGER: 'rule precedence conflict resolution' → ACTION: 'create ADR' → RATIONALE: 'document how conflicts were resolved'

ADR_CREATION_WORKFLOW:
  STEP_1: 'identify decision scope' → OUTPUT: 'clear problem statement'
  STEP_2: 'generate next ADR number' → SOURCE: '${ADR_INDEX_FILE}' → FORMAT: 'ADR-{NNN}'
  STEP_3: 'create ADR file' → LOCATION: '${ADR_DIRECTORY}' → TEMPLATE: '${ADR_TEMPLATE_FILE}'
  STEP_4: 'populate ADR content' → SECTIONS: 'all required sections per template'
  STEP_5: 'update ADR index' → FILE: '${ADR_INDEX_FILE}' → ACTION: 'add new entry'
  STEP_6: 'reference ADR' → FILES: ['${AI_MEMORY_FILE}', related code files] → ACTION: 'create bidirectional links'

## ADR TEMPLATE STRUCTURE

ADR_TEMPLATE_CONTENT: |

# ADR-{NNN}: {Title}
  
## Metadata

- **Status**: Proposed | Accepted | Rejected | Deprecated | Superseded
- **Date**: {YYYY-MM-DD}
- **Deciders**: {List of people involved in decision}
- **Consulted**: {List of people consulted}
- **Informed**: {List of people informed}
- **Tags**: {Relevant tags for categorization}
- **Rule Precedence**: {If applicable, note which rule precedence level applies}
  
## Context and Problem Statement

  {Describe the architectural problem or decision that needs to be made}
  
## Decision Drivers

- {List key factors that influence the decision}
- {Technical constraints}
- {Business requirements}
- {Quality attributes}
- {Rule system constraints}
  
## Considered Options

- **Option 1**: {Description}
- **Option 2**: {Description}
- **Option 3**: {Description}
  
## Decision Outcome

  **Chosen Option**: {Selected option with brief rationale}
  
## Pros and Cons Analysis
  
### Option 1: {Name}

  **Pros:**

- {Advantage 1}
- {Advantage 2}
  
  **Cons:**

- {Disadvantage 1}
- {Disadvantage 2}
  
### Option 2: {Name}

  **Pros:**

- {Advantage 1}
- {Advantage 2}
  
  **Cons:**

- {Disadvantage 1}
- {Disadvantage 2}
  
## Consequences
  
### Positive Consequences

- {Benefit 1}
- {Benefit 2}
  
### Negative Consequences

- {Risk 1}
- {Risk 2}
  
### Neutral Consequences

- {Neutral impact 1}
- {Neutral impact 2}
  
## Implementation Notes

- {Key implementation details}
- {Migration strategy if applicable}
- {Rollback plan if needed}
- {Rule compliance considerations}
  
## Validation and Success Metrics

- {How to measure success of this decision}
- {Validation criteria}
- {Review timeline}
  
## Links and References

- {Related ADRs}
- {External documentation}
- {Code references}
- {Issue/ticket numbers}
- {Applicable rules references}
  
## Notes

- {Additional context}
- {Future considerations}
- {Lessons learned}
- {Rule precedence conflicts and resolutions}

ADR_INDEX_STRUCTURE: |

# Architecture Decision Records Index
  
## ADR Statistics

- **Total ADRs**: {count}
- **Accepted**: {count}
- **Proposed**: {count}
- **Rejected**: {count}
- **Deprecated**: {count}
- **Superseded**: {count}
  
## ADR List
  
  | ID | Title | Status | Date | Tags | Rule Level |
  |---|-------|--------|------|------|------------|
  | ADR-001 | {Title} | {Status} | {Date} | {Tags} | {Rule Precedence} |
  | ADR-002 | {Title} | {Status} | {Date} | {Tags} | {Rule Precedence} |
  
## ADR Categories
  
### Technology Decisions

- {List of technology-related ADRs}
  
### Architecture Patterns

- {List of architecture pattern ADRs}
  
### Security Decisions

- {List of security-related ADRs}
  
### Performance Optimizations

- {List of performance-related ADRs}

### Rule Precedence Conflicts

- {List of ADRs documenting rule conflicts and resolutions}
  
## Recently Modified

- {List of recently created/updated ADRs}
  
## Superseded Chain

- {Show superseded relationships}

## Rule Compliance Matrix

- {Track which rules are referenced by which ADRs}

## Memory file templates

MEMORY_FILE_STRUCTURE:
  AI_MEMORY_TEMPLATE: |
    # Architectural Memory
    ## Current Patterns
    - [Pattern Name]: [Usage Context]

    ## Design Decisions
    - [Date]: [Decision]: [Rationale]
    
    ## Constraints
    - [Constraint]: [Reason]
    
  AI_NOTES_TEMPLATE: |
    # Context Notes
    ## Current Sprint/Feature
    - Working on: [feature]
    - Key decisions: [list]

    ## Watch Points
    - [Area]: [Concern]
    
    ## Learned Patterns
    - [Pattern]: [When to use]
    
  PATTERN_REGISTRY_TEMPLATE: |
    # Pattern Registry
    ## Established Patterns
    - [Pattern Name]: [Description]
      - Usage: [When to use]
      - Location: [Where implemented]
      - Examples: [Code references]

    ## Pattern Evolution
    - [Date]: [Pattern Change]: [Reason]
    
    ## Anti-Patterns
    - [Anti-Pattern]: [Why to avoid]

CONTEXT_PRESERVATION_RULES:
  ARCHITECTURAL_MEMORY:
    - RULE: 'never violate documented patterns in ${AI_MEMORY_FILE}'
    - RULE: 'maintain consistency with previous architectural decisions'
    - RULE: 'update memory files before context is lost'
    - RULE: 'always reference relevant ADRs when making architectural decisions'
    - RULE: 'respect rule precedence hierarchy in all decisions'

  PATTERN_CONTINUITY:
    - RULE: 'reference ${PATTERN_REGISTRY_FILE} before implementing new features'
    - RULE: 'ensure new code follows established patterns'
    - RULE: 'document any pattern deviations with justification'
    - RULE: 'create ADR for any new patterns introduced'

  ADR_CONSISTENCY:
    - RULE: 'never contradict accepted ADRs without creating superseding ADR'
    - RULE: 'always check ADR index before making architectural decisions'
    - RULE: 'update ADR status when implementation changes'
    - RULE: 'maintain bidirectional links between ADRs and code'

ANTI_ISOLATION_CONSTRAINTS:

  1. ENTITY: 'isolated decision making' → ACTION/NEGATION: 'prohibit' → RESULT: 'context-aware development'
  2. ENTITY: 'memory files' → ACTION/NEGATION: 'always consult' → RESULT: 'persistent context'
  3. ENTITY: 'architectural drift' → ACTION/NEGATION: 'prevent' → RESULT: 'pattern consistency'
  4. ENTITY: 'context loss between sessions' → ACTION/NEGATION: 'eliminate' → RESULT: 'continuous awareness'
  5. ENTITY: 'undocumented architectural decisions' → ACTION/NEGATION: 'prohibit' → RESULT: 'comprehensive ADR coverage'
  6. ENTITY: 'ADR creation avoidance' → ACTION/NEGATION: 'prevent' → RESULT: 'mandatory architectural documentation'
  7. ENTITY: 'rule precedence violations' → ACTION/NEGATION: 'detect and resolve' → RESULT: 'consistent rule application'

## Enhanced constraints with ADR requirements

CONSTRAINTS:
  1-10. [inherits from rules-101 v1.1+]
  11. ENTITY: 'undocumented decisions' → ACTION/NEGATION: 'never make' → RESULT: 'traceable architecture'
  12. ENTITY: 'memory files' → ACTION/NEGATION: 'never ignore' → RESULT: 'context preservation'
  13. ENTITY: 'pattern violations' → ACTION/NEGATION: 'detect and prevent' → RESULT: 'architectural integrity'
  14. ENTITY: 'architectural decisions' → ACTION/NEGATION: 'always create ADR' → RESULT: 'complete decision documentation'
  15. ENTITY: 'ADR numbering' → ACTION/NEGATION: 'never skip or duplicate' → RESULT: 'sequential ADR tracking'
  16. ENTITY: 'ADR template deviation' → ACTION/NEGATION: 'avoid unless justified' → RESULT: 'consistent ADR format'
  17. ENTITY: 'ADR index updates' → ACTION/NEGATION: 'never skip' → RESULT: 'accurate ADR tracking'
  18. ENTITY: 'version compatibility' → ACTION/NEGATION: 'always verify' → RESULT: 'compatible rule application'
  19. ENTITY: 'rule precedence conflicts' → ACTION/NEGATION: 'resolve systematically' → RESULT: 'consistent rule hierarchy'

## Enhanced TDD workflow with ADR integration

TDD_WORKFLOW:
  COMPATIBILITY_CHECK_PHASE:
    - ACTION: 'verify' → OBJECT: 'rules version compatibility' → STATUS: 'mandatory before execution'
    - ACTION: 'load' → OBJECT: 'rule precedence hierarchy' → STATUS: 'required for conflict resolution'

  MEMORY_CHECK_PHASE:
    - ACTION: 'read' → OBJECT: '${AI_MEMORY_FILE}' → STATUS: 'mandatory before RED'
    - ACTION: 'review' → OBJECT: '${ADR_INDEX_FILE}' → STATUS: 'mandatory before RED'
    - ACTION: 'verify' → OBJECT: 'pattern compliance' → STATUS: 'required'
    - ACTION: 'check' → OBJECT: 'relevant ADRs' → STATUS: 'mandatory for architectural decisions'

  RED_PHASE: [inherits from rules-101 with ADR consideration]
  
  GREEN_PHASE_ENHANCED:
    - ACTION: 'implement' → OBJECT: 'minimal code' → CONSTRAINT: 'consistent with ${AI_MEMORY_FILE} and relevant ADRs'
    - ACTION: 'verify' → OBJECT: 'pattern adherence' → CONSTRAINT: 'no architectural violations'
    - ACTION: 'evaluate' → OBJECT: 'ADR creation need' → CONSTRAINT: 'create if architectural decision made'
    - ACTION: 'apply' → OBJECT: 'rule precedence' → CONSTRAINT: 'resolve conflicts systematically'

  REFACTOR_PHASE_ENHANCED:
    - ACTION: 'refactor' → OBJECT: 'code structure' → CONSTRAINT: 'maintain ADR compliance'
    - ACTION: 'document' → OBJECT: 'architectural changes' → CONSTRAINT: 'create ADR if significant'

  DOCUMENTATION_PHASE:
    - ACTION: 'update' → OBJECT: '${AI_MEMORY_FILE}' → TIMING: 'immediately after GREEN'
    - ACTION: 'create' → OBJECT: 'ADR if needed' → TIMING: 'during or immediately after implementation'
    - ACTION: 'document' → OBJECT: 'design rationale' → FILE: '${AI_NOTES_FILE}'
    - ACTION: 'update' → OBJECT: '${ADR_INDEX_FILE}' → TIMING: 'when ADR created or modified'
    - ACTION: 'log' → OBJECT: 'rule precedence usage' → TIMING: 'if conflicts were resolved'

## ADR Quality Gates

ADR_QUALITY_REQUIREMENTS:
  COMPLETENESS:
    - RULE: 'all template sections must be populated'
    - RULE: 'at least 2 options must be considered'
    - RULE: 'consequences must be explicitly stated'
    - RULE: 'success metrics must be defined'
    - RULE: 'rule precedence level must be noted if applicable'

  TRACEABILITY:
    - RULE: 'ADRs must be linked to relevant code'
    - RULE: 'superseded ADRs must be properly linked'
    - RULE: 'related ADRs must be cross-referenced'
    - RULE: 'ADR index must be updated'
    - RULE: 'rule references must be accurate'

  CLARITY:
    - RULE: 'problem statement must be clear and specific'
    - RULE: 'decision rationale must be explicit'
    - RULE: 'implementation notes must be actionable'
    - RULE: 'technical jargon must be explained'
    - RULE: 'rule conflicts must be clearly documented'

ADR_REVIEW_PROCESS:
  SELF_REVIEW:
    - ACTION: 'validate' → OBJECT: 'ADR completeness' → CRITERIA: 'all sections populated'
    - ACTION: 'verify' → OBJECT: 'decision logic' → CRITERIA: 'rationale is clear'
    - ACTION: 'check' → OBJECT: 'links and references' → CRITERIA: 'all links functional'
    - ACTION: 'confirm' → OBJECT: 'ADR index update' → CRITERIA: 'entry added correctly'
    - ACTION: 'verify' → OBJECT: 'rule precedence' → CRITERIA: 'conflicts properly resolved'

ENFORCEMENT:

- STAGE: 'initialization' → REQUIREMENT: 'ADR directory exists and ADR index is read' → VERIFICATION: 'ADR context loaded'
- STAGE: 'initialization' → REQUIREMENT: 'memory files exist and are read' → VERIFICATION: 'context loaded'
- STAGE: 'pre-implementation' → REQUIREMENT: 'context awareness verified' → VERIFICATION: 'no isolation'
- STAGE: 'pre-implementation' → REQUIREMENT: 'relevant ADRs reviewed' → VERIFICATION: 'no architectural conflicts'
- STAGE: 'implementation' → REQUIREMENT: 'ADR compliance maintained' → VERIFICATION: 'decisions align with ADRs'
- STAGE: 'post-implementation' → REQUIREMENT: 'ADR created if architectural decision made' → VERIFICATION: 'decision documented'
- STAGE: 'post-implementation' → REQUIREMENT: 'memory updated' → VERIFICATION: 'context preserved'
- STAGE: 'session-end' → REQUIREMENT: 'ADR index updated' → VERIFICATION: 'all new ADRs registered'

## ADR Lifecycle Management

ADR_LIFECYCLE:
  CREATION:
    - TRIGGER: 'architectural decision identified'
    - ACTION: 'create ADR from template'
    - STATUS: 'Proposed'
    - VALIDATION: 'completeness check including rule precedence'

  ACCEPTANCE:
    - TRIGGER: 'decision implemented and validated'
    - ACTION: 'update status to Accepted'
    - VALIDATION: 'implementation matches ADR and rule compliance'

  SUPERSESSION:
    - TRIGGER: 'better solution identified'
    - ACTION: 'create new ADR and mark old as Superseded'
    - VALIDATION: 'proper linking between ADRs and rule precedence updated'

  DEPRECATION:
    - TRIGGER: 'decision no longer relevant'
    - ACTION: 'update status to Deprecated'
    - VALIDATION: 'reason for deprecation documented'

ADR_MAINTENANCE:
  PERIODIC_REVIEW:
    - FREQUENCY: 'every major release'
    - ACTION: 'review ADR relevance and rule compatibility'
    - OUTCOME: 'update status or create superseding ADR'

  CONSISTENCY_CHECK:
    - FREQUENCY: 'every sprint'
    - ACTION: 'verify code matches ADRs and rule precedence'
    - OUTCOME: 'flag inconsistencies for resolution'

  VERSION_COMPATIBILITY_CHECK:
    - FREQUENCY: 'when rules are updated'
    - ACTION: 'verify ADR compatibility with new rule versions'
    - OUTCOME: 'update ADRs if necessary for compatibility'

COMPATIBILITY:

- REQUIRES: 'rules-101 v1.1+'
- EXTENDS: 'rules-103 v1.1+'
- CURRENT_VERSION: 'v1.2'
- PRECEDENCE_LEVEL: '2 (Memory persistence and ADR management)'

