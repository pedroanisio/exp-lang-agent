---
alwaysApply: true
version: 1.2
changelog:
  - v1.0: Initial TDD and engineering principles
  - v1.1: Clarified mock usage policy for consistency with rules-103
  - v1.2: Enhanced TDD workflow with git tagging strategies for robustness
---

# rules-101-v1.2

DOMAIN: software engineering
OBJECTIVE: ensure code quality and maintainability through adherence to engineering principles and test-driven development with git-based workflow enforcement

CONSTRAINTS:

1. ENTITY: 'poor architecture decisions' → ACTION/NEGATION: 'avoid' → RESULT: 'best practices compliance'
2. ENTITY: 'spaghetti code' → ACTION/NEGATION: 'avoid' → RESULT: 'clean code structure'
3. ENTITY: 'DRY violations' → ACTION/NEGATION: 'avoid' → RESULT: 'code maintainability'
4. ENTITY: 'SOLID principle violations' → ACTION/NEGATION: 'avoid' → RESULT: 'solid design adherence'
5. ENTITY: 'mocks or placeholders' → ACTION/NEGATION: 'do not use for implementation logic' → RESULT: 'avoid fake implementations' → EXCEPTION: 'mocks for external dependencies in tests allowed when necessary for isolation'
6. ENTITY: 'solution' → ACTION/NEGATION: 'do not overcomplicate' → RESULT: 'elegant working solution'
7. ENTITY: 'redline' → ACTION/NEGATION: 'do not cross' → RESULT: 'compliance maintenance'
8. ENTITY: 'implementation without failing test' → ACTION/NEGATION: 'never write' → RESULT: 'TDD compliance'
9. ENTITY: 'test writing after implementation' → ACTION/NEGATION: 'prohibit' → RESULT: 'test-first development'
10. ENTITY: 'DoD criteria' → ACTION/NEGATION: 'never compromise' → RESULT: 'quality assurance'
11. ENTITY: 'TDD phase without git tag' → ACTION/NEGATION: 'prohibit' → RESULT: 'traceable development cycles'
12. ENTITY: 'git tag without phase verification' → ACTION/NEGATION: 'avoid' → RESULT: 'validated phase transitions'

MOCK_USAGE_CLARIFICATION:

- PROHIBITED: 'mocks in implementation code'
- PROHIBITED: 'mocks to avoid writing real business logic'
- PROHIBITED: 'mocks as permanent replacements for actual implementations'
- ALLOWED: 'mocks for external dependencies in unit tests (databases, APIs, file systems)'
- ALLOWED: 'mocks for isolation of unit under test from external concerns'
- PRINCIPLE: 'prefer real implementations over mocks whenever feasible'

TDD_WORKFLOW_WITH_GIT_INTEGRATION:

RED_PHASE:

- ACTION: 'write' → OBJECT: 'failing test' → STATUS: 'mandatory'
- ACTION: 'verify' → OBJECT: 'test failure' → STATUS: 'required before proceeding'
- ACTION: 'define' → OBJECT: 'expected behavior' → STATUS: 'complete specification'
- ACTION: 'commit' → OBJECT: 'failing test' → GIT_TAG: 'tdd-red-{feature}-{timestamp}'
- ACTION: 'verify' → OBJECT: 'test execution fails' → CONSTRAINT: 'automated verification before tag creation'

GREEN_PHASE:

- ACTION: 'implement' → OBJECT: 'minimal code' → CONSTRAINT: 'only to pass test'
- ACTION: 'verify' → OBJECT: 'test passes' → CONSTRAINT: 'no additional functionality'
- ACTION: 'maintain' → OBJECT: 'DoD compliance' → CONSTRAINT: 'all criteria met'
- ACTION: 'commit' → OBJECT: 'passing implementation' → GIT_TAG: 'tdd-green-{feature}-{timestamp}'
- ACTION: 'verify' → OBJECT: 'all tests pass' → CONSTRAINT: 'automated verification before tag creation'

REFACTOR_PHASE:

- ACTION: 'improve' → OBJECT: 'code structure' → CONSTRAINT: 'tests remain green'
- ACTION: 'apply' → OBJECT: 'SOLID principles' → CONSTRAINT: 'maintain test coverage'
- ACTION: 'commit' → OBJECT: 'refactored code' → GIT_TAG: 'tdd-refactor-{feature}-{timestamp}'
- ACTION: 'verify' → OBJECT: 'tests still pass' → CONSTRAINT: 'automated verification before tag creation'

GIT_TAGGING_STRATEGY:

TAG_NAMING_CONVENTION:

- RED_PHASE: 'tdd-red-{feature-name}-{yyyymmdd-hhmmss}'
- GREEN_PHASE: 'tdd-green-{feature-name}-{yyyymmdd-hhmmss}'
- REFACTOR_PHASE: 'tdd-refactor-{feature-name}-{yyyymmdd-hhmmss}'
- CYCLE_COMPLETE: 'tdd-cycle-{feature-name}-{yyyymmdd-hhmmss}'
- BUG_FIX_RED: 'tdd-bugfix-red-{bug-id}-{yyyymmdd-hhmmss}'
- BUG_FIX_GREEN: 'tdd-bugfix-green-{bug-id}-{yyyymmdd-hhmmss}'

TAG_METADATA:

- REQUIRED_FIELDS: ['phase', 'feature', 'timestamp', 'test_status', 'commit_hash']
- OPTIONAL_FIELDS: ['author', 'reviewer', 'dod_compliance', 'coverage_percentage']
- ANNOTATION_FORMAT: 'structured metadata in JSON format'

AUTOMATED_VERIFICATION:

PRE_COMMIT_HOOKS:

- HOOK: 'verify-red-phase' → REQUIREMENT: 'at least one test fails' → ACTION: 'prevent commit if no failing tests'
- HOOK: 'verify-green-phase' → REQUIREMENT: 'all tests pass' → ACTION: 'prevent commit if any test fails'
- HOOK: 'verify-refactor-phase' → REQUIREMENT: 'all tests pass + no new functionality' → ACTION: 'prevent commit if test status changed'

PRE_TAG_HOOKS:

- HOOK: 'validate-tdd-red-tag' → VERIFICATION: 'test suite contains failing tests' → ACTION: 'reject tag if tests pass'
- HOOK: 'validate-tdd-green-tag' → VERIFICATION: 'test suite passes completely' → ACTION: 'reject tag if tests fail'
- HOOK: 'validate-tdd-refactor-tag' → VERIFICATION: 'test suite passes + code quality metrics improved' → ACTION: 'reject tag if quality degraded'

WORKFLOW_ENFORCEMENT:

PHASE_TRANSITION_RULES:

- TRANSITION: 'RED → GREEN' → REQUIREMENT: 'tdd-red-* tag exists' → VERIFICATION: 'previous phase tagged'
- TRANSITION: 'GREEN → REFACTOR' → REQUIREMENT: 'tdd-green-* tag exists' → VERIFICATION: 'previous phase tagged'
- TRANSITION: 'REFACTOR → RED' → REQUIREMENT: 'tdd-refactor-* tag exists' → VERIFICATION: 'cycle completion'

ROLLBACK_STRATEGY:

- ROLLBACK_POINT: 'tdd-red-*' → SAFETY: 'return to failing test state'
- ROLLBACK_POINT: 'tdd-green-*' → SAFETY: 'return to minimal working implementation'
- ROLLBACK_POINT: 'tdd-refactor-*' → SAFETY: 'return to clean, working code'
- ROLLBACK_VERIFICATION: 'automated test execution' → REQUIREMENT: 'verify rollback state integrity'

PATTERN_RULES:

RED_TO_GREEN_PATTERN:

- NAME: 'Minimal Implementation Pattern'
- RULE: 'implement only enough code to make the test pass'
- SEQUENCE: 'RED → tag → minimal code → GREEN → tag → refactor'
- CONSTRAINT: 'no anticipatory code'
- GIT_INTEGRATION: 'each phase must be tagged before transition'

BUG_IN_CODE_PATTERN:

- NAME: 'Test-First Bug Fix Pattern'
- RULE: 'write failing test that reproduces bug before fixing'
- SEQUENCE: 'reproduce bug in test → RED tag → fix implementation → GREEN tag'
- CONSTRAINT: 'bug must be captured in test before fix'
- GIT_INTEGRATION: 'bug fix cycles follow same tagging strategy'

BUG_IN_TEST_PATTERN:

- NAME: 'Test Correction Pattern'
- RULE: 'fix test to properly specify intended behavior'
- SEQUENCE: 'identify test issue → correct test → verify implementation still passes'
- CONSTRAINT: 'maintain existing functionality coverage'
- GIT_INTEGRATION: 'test corrections require separate commit and tag'

AUDIT_AND_TRACEABILITY:

CYCLE_TRACKING:

- METRIC: 'cycle_duration' → MEASUREMENT: 'time between RED and REFACTOR tags'
- METRIC: 'cycle_frequency' → MEASUREMENT: 'number of complete cycles per feature'
- METRIC: 'rollback_frequency' → MEASUREMENT: 'number of phase rollbacks'
- METRIC: 'phase_compliance' → MEASUREMENT: 'percentage of proper phase transitions'

REPORTING:

- REPORT: 'tdd_compliance_report' → CONTENT: 'phase transition history, cycle metrics, rollback analysis'
- REPORT: 'feature_development_timeline' → CONTENT: 'complete TDD cycle history for each feature'
- REPORT: 'quality_metrics' → CONTENT: 'test coverage, code quality trends per cycle'

CI_CD_INTEGRATION:

PIPELINE_TRIGGERS:

- TRIGGER: 'tdd-green-*' → PIPELINE: 'integration_tests' → ACTION: 'run integration test suite'
- TRIGGER: 'tdd-refactor-*' → PIPELINE: 'code_quality_analysis' → ACTION: 'run static analysis and quality gates'
- TRIGGER: 'tdd-cycle-*' → PIPELINE: 'deployment_candidate' → ACTION: 'mark as deployment ready'

QUALITY_GATES:

- GATE: 'red_phase_gate' → REQUIREMENT: 'at least one failing test' → ACTION: 'proceed to implementation'
- GATE: 'green_phase_gate' → REQUIREMENT: 'all tests pass + DoD compliance' → ACTION: 'proceed to refactor'
- GATE: 'refactor_phase_gate' → REQUIREMENT: 'improved code quality + tests pass' → ACTION: 'complete cycle'

REQUIREMENTS:

- ACTION: 'follow' → OBJECT: 'software engineering principles' → ATTRIBUTES: ['best practices', 'poor practice avoidance']
- ACTION: 'maintain' → OBJECT: 'elegant working solution' → ATTRIBUTES: ['simplicity', 'functionality']
- ACTION: 'ensure' → OBJECT: 'code quality' → ATTRIBUTES: ['DRY compliance', 'SOLID adherence', 'clean architecture']
- ACTION: 'enforce' → OBJECT: 'TDD cycle' → ATTRIBUTES: ['RED-GREEN-REFACTOR', 'test-first', 'pattern compliance']
- ACTION: 'preserve' → OBJECT: 'DoD integrity' → ATTRIBUTES: ['no shortcuts', 'full compliance', 'quality gates']
- ACTION: 'maintain' → OBJECT: 'git workflow traceability' → ATTRIBUTES: ['tagged phases', 'automated verification', 'audit trails']

PRINCIPLES:

- PRINCIPLE: 'software engineering principles' → TYPE: 'best practices' → ACTION: 'follow consistently'
- PRINCIPLE: 'DRY' → TYPE: 'code organization' → ACTION: 'eliminate repetition'
- PRINCIPLE: 'SOLID' → TYPE: 'design pattern' → ACTION: 'apply to architecture'
- PRINCIPLE: 'TDD' → TYPE: 'development methodology' → ACTION: 'mandatory application'
- PRINCIPLE: 'Test-First' → TYPE: 'workflow enforcement' → ACTION: 'no code without failing test'
- PRINCIPLE: 'Git-Driven TDD' → TYPE: 'workflow traceability' → ACTION: 'every phase must be tagged and verified'

ENFORCEMENT:

- STAGE: 'pre-implementation' → REQUIREMENT: 'failing test exists' → VERIFICATION: 'test runs and fails' → GIT_ACTION: 'commit with tdd-red-* tag'
- STAGE: 'implementation' → REQUIREMENT: 'minimal code only' → VERIFICATION: 'test passes' → GIT_ACTION: 'commit with tdd-green-* tag'
- STAGE: 'completion' → REQUIREMENT: 'DoD satisfied' → VERIFICATION: 'all criteria met' → GIT_ACTION: 'commit with tdd-refactor-* tag'
- STAGE: 'cycle-completion' → REQUIREMENT: 'full TDD cycle' → VERIFICATION: 'all phases tagged' → GIT_ACTION: 'create tdd-cycle-* tag'

COMPATIBILITY:

- EXTENDS: 'rules-102 (memory + ADR management)'
- EXTENDS: 'rules-103 (comprehensive standards)'
- PRECEDENCE: 'rules-101 takes precedence for core TDD principles'
- VERSION_COMPATIBILITY: 'rules-102 v1.1+, rules-103 v1.1+'
- GIT_REQUIREMENTS: 'git hooks, automated tagging, CI/CD integration'

