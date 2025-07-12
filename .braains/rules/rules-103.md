---
alwaysApply: true
version: 1.2
changelog:
  - v1.0: Initial coding ethos and standards
  - v1.1: Enhanced with comprehensive standards and integration with memory system
  - v1.2: Aligned mock usage policy with rules-101 and integrated rule precedence hierarchy
---

# CODING ETHOS v1.2

DOMAIN: software engineering standards
OBJECTIVE: ensure code quality, maintainability, and consistency through comprehensive coding standards, philosophy, and practices across all technologies

VERSION_COMPATIBILITY_MATRIX:

- RULES_101: 'v1.1+' → STATUS: 'required foundation' → PRECEDENCE: 'level 1 (Core TDD and engineering principles)'
- RULES_102: 'v1.2+' → STATUS: 'required memory/ADR system' → PRECEDENCE: 'level 2 (Memory persistence and ADR management)'
- RULES_103: 'v1.2' → STATUS: 'current implementation layer' → PRECEDENCE: 'level 3 (Implementation standards and practices)'

RULE_PRECEDENCE_ACKNOWLEDGMENT:

- DEFERS_TO: 'rules-101 for core TDD and engineering principles'
- DEFERS_TO: 'rules-102 for architectural documentation and memory management'
- AUTHORITY: 'implementation standards, coding practices, tooling configuration'
- CONFLICT_RESOLUTION: 'follow rules-101/102 precedence, document conflicts in ADRs'

## FILE PATH VARIABLES

ETHOS_FILE = '${workspaceFolder}/.braains/CODING-ETHOS.md'
STANDARDS_COMPLIANCE_FILE = '${workspaceFolder}/.braains/STANDARDS-COMPLIANCE.md'
VIOLATIONS_LOG_FILE = '${workspaceFolder}/.braains/VIOLATIONS-LOG.md'

## CORE PHILOSOPHY

PHIL_CONSTRAINTS:

  1. ENTITY: 'regressions' → ACTION/NEGATION: 'fix forward, never introduce' → RESULT: 'continuous improvement'
  2. ENTITY: 'software solutions' → ACTION/NEGATION: 'always aim for elegance' → RESULT: 'high-quality engineering'
  3. ENTITY: 'tests' → ACTION/NEGATION: 'treat as ultimate specification' → RESULT: 'behavior-driven development'
  4. ENTITY: 'test manipulation' → ACTION/NEGATION: 'never bend to make pass' → RESULT: 'correct software implementation'
  5. ENTITY: 'standards' → ACTION/NEGATION: 'always elevate and aspire' → RESULT: 'continuous excellence'
  6. ENTITY: 'files' → ACTION/NEGATION: 'require defined purpose and justification' → RESULT: 'intentional architecture'
  7. ENTITY: 'decisions' → ACTION/NEGATION: 'always document rationale' → RESULT: 'traceable reasoning'
  8. ENTITY: 'codebase patterns' → ACTION/NEGATION: 'maintain consistency' → RESULT: 'predictable architecture'
  9. ENTITY: 'rule precedence' → ACTION/NEGATION: 'respect hierarchy' → RESULT: 'consistent rule application'

## FILE HEADER REQUIREMENTS

HDR_MANDATORY_SECTIONS:

- SECTION: 'filename' → CONTENT: 'exact file name' → STATUS: 'required'
- SECTION: 'filepath' → CONTENT: 'full path from project root' → STATUS: 'required'
- SECTION: 'version' → CONTENT: 'semantic version number' → STATUS: 'required'
- SECTION: 'description' → CONTENT: 'clear purpose statement' → STATUS: 'required'
- SECTION: 'author' → CONTENT: 'creator and creation date' → STATUS: 'required'
- SECTION: 'modified' → CONTENT: 'last modifier and date' → STATUS: 'required'
- SECTION: 'purpose' → CONTENT: 'responsibility and system role' → STATUS: 'required'
- SECTION: 'dependencies' → CONTENT: 'key external dependencies' → STATUS: 'optional'
- SECTION: 'exports' → CONTENT: 'main public interfaces' → STATUS: 'optional'
- SECTION: 'uml' → CONTENT: 'architectural diagram reference' → STATUS: 'conditional'
- SECTION: 'rule_compliance' → CONTENT: 'applicable rule versions' → STATUS: 'recommended'

HDR_LANGUAGE_TEMPLATES:
  PYTHON_TEMPLATE: |
    """
    File: {filename}
    Path: {filepath}
    Version: {version}
    Created: {date} by {author}
    Modified: {date} by {modifier}

    Purpose: {clear description of file purpose}
    
    Dependencies: {list key dependencies}
    Exports: {list main exports/classes/functions}
    
    UML: {optional UML diagram or reference}
    Rule Compliance: rules-101 v{version}, rules-102 v{version}, rules-103 v{version}
    """
  
  TYPESCRIPT_TEMPLATE: |
    /**
     *File: {filename}
     * Path: {filepath}
     *Version: {version}
     * Created: {date} by {author}
     *Modified: {date} by {modifier}
     *
     *Purpose: {clear description of file purpose}
     *
     *Dependencies: {list key dependencies}
     * Exports: {list main exports/interfaces/types}
     *
     * UML: {optional UML diagram or reference}
     *Rule Compliance: rules-101 v{version}, rules-102 v{version}, rules-103 v{version}
     */

## GENERAL DESIGN PRINCIPLES

GEN_CONSTRAINTS:

  1. ENTITY: 'SOLID principles' → ACTION/NEGATION: 'always apply' → RESULT: 'maintainable architecture' → PRECEDENCE: 'defers to rules-101'
  2. ENTITY: 'code duplication' → ACTION/NEGATION: 'eliminate through DRY' → RESULT: 'single source of truth' → PRECEDENCE: 'defers to rules-101'
  3. ENTITY: 'design patterns' → ACTION/NEGATION: 'use contextually appropriate' → RESULT: 'proven solutions'
  4. ENTITY: 'file placement' → ACTION/NEGATION: 'match responsibility to structure' → RESULT: 'logical organization'
  5. ENTITY: 'versioning' → ACTION/NEGATION: 'follow semantic versioning' → RESULT: 'predictable releases'
  6. ENTITY: 'concerns' → ACTION/NEGATION: 'maintain clear separation' → RESULT: 'modular design'
  7. ENTITY: 'data structures' → ACTION/NEGATION: 'prefer immutable' → RESULT: 'predictable state'
  8. ENTITY: 'errors' → ACTION/NEGATION: 'implement comprehensive handling' → RESULT: 'robust systems'
  9. ENTITY: 'performance' → ACTION/NEGATION: 'consider in all decisions' → RESULT: 'efficient software'
  10. ENTITY: 'security' → ACTION/NEGATION: 'apply by default' → RESULT: 'secure systems'
  11. ENTITY: 'maintainability' → ACTION/NEGATION: 'prioritize in design' → RESULT: 'long-term sustainability'
  12. ENTITY: 'architectural decisions' → ACTION/NEGATION: 'document in ADRs' → RESULT: 'traceable architecture' → PRECEDENCE: 'defers to rules-102'
  13. ENTITY: 'code language' → ACTION/NEGATION: 'write all code and comments in English' → RESULT: 'universal understanding' → PRECEDENCE: 'applies globally'

## TESTING STANDARDS

TEST_CONSTRAINTS:

  1. ENTITY: 'test coverage' → ACTION/NEGATION: 'maintain minimum 80%' → RESULT: 'comprehensive verification'
  2. ENTITY: 'test pyramid' → ACTION/NEGATION: 'follow unit > integration > E2E' → RESULT: 'efficient test strategy'
  3. ENTITY: 'test isolation' → ACTION/NEGATION: 'ensure complete independence' → RESULT: 'reliable tests'
  4. ENTITY: 'test names' → ACTION/NEGATION: 'make descriptive and clear' → RESULT: 'self-documenting tests'
  5. ENTITY: 'test structure' → ACTION/NEGATION: 'follow Arrange-Act-Assert' → RESULT: 'consistent test format'
  6. ENTITY: 'mocking' → ACTION/NEGATION: 'use sparingly for external dependencies only' → RESULT: 'realistic testing' → PRECEDENCE: 'aligns with rules-101 mock policy'
  7. ENTITY: 'test data' → ACTION/NEGATION: 'use factories for consistency' → RESULT: 'maintainable test data'
  8. ENTITY: 'performance tests' → ACTION/NEGATION: 'include for critical components' → RESULT: 'performance assurance'
  9. ENTITY: 'TDD workflow' → ACTION/NEGATION: 'follow RED-GREEN-REFACTOR' → RESULT: 'test-driven development' → PRECEDENCE: 'defers to rules-101'
  10. ENTITY: 'test-first principle' → ACTION/NEGATION: 'no implementation without failing test' → RESULT: 'TDD compliance' → PRECEDENCE: 'defers to rules-101'

MOCK_USAGE_ALIGNMENT:

- ALIGNED_WITH: 'rules-101 v1.1+ mock usage policy'
- PERMITTED: 'mocks for external dependencies in tests (databases, APIs, file systems)'
- PERMITTED: 'mocks for isolation of unit under test from external concerns'
- PROHIBITED: 'mocks in implementation code'
- PROHIBITED: 'mocks to avoid writing real business logic'
- PRINCIPLE: 'prefer real implementations over mocks whenever feasible'

## DOCUMENTATION STANDARDS

DOC_CONSTRAINTS:

  1. ENTITY: 'README files' → ACTION/NEGATION: 'make comprehensive for every project' → RESULT: 'clear project understanding'
  2. ENTITY: 'public APIs' → ACTION/NEGATION: 'document with examples' → RESULT: 'usable interfaces'
  3. ENTITY: 'architectural decisions' → ACTION/NEGATION: 'maintain decision records' → RESULT: 'traceable architecture' → PRECEDENCE: 'defers to rules-102'
  4. ENTITY: 'changelogs' → ACTION/NEGATION: 'keep detailed for all releases' → RESULT: 'transparent evolution'
  5. ENTITY: 'complex logic' → ACTION/NEGATION: 'explain with inline comments' → RESULT: 'understandable code'
  6. ENTITY: 'functionality examples' → ACTION/NEGATION: 'provide working examples' → RESULT: 'practical documentation'
  7. ENTITY: 'troubleshooting' → ACTION/NEGATION: 'document common issues' → RESULT: 'self-service support'
  8. ENTITY: 'rule compliance' → ACTION/NEGATION: 'document in file headers' → RESULT: 'version traceability'

## PYTHON STANDARDS

PY_CONSTRAINTS:

  1. ENTITY: 'code style' → ACTION/NEGATION: 'follow PEP 8 strictly' → RESULT: 'consistent Python style'
  2. ENTITY: 'type hints' → ACTION/NEGATION: 'apply PEP 484 throughout' → RESULT: 'type-safe code'
  3. ENTITY: 'code formatting' → ACTION/NEGATION: 'use Black formatter' → RESULT: 'uniform formatting'
  4. ENTITY: 'import organization' → ACTION/NEGATION: 'organize with isort' → RESULT: 'clean imports'
  5. ENTITY: 'linting' → ACTION/NEGATION: 'enforce with Flake8' → RESULT: 'style compliance'
  6. ENTITY: 'type checking' → ACTION/NEGATION: 'verify with MyPy' → RESULT: 'type correctness'
  7. ENTITY: 'testing' → ACTION/NEGATION: 'implement with pytest' → RESULT: 'robust testing' → PRECEDENCE: 'defers to rules-101 TDD workflow'
  8. ENTITY: 'documentation' → ACTION/NEGATION: 'use PEP 257 docstrings' → RESULT: 'documented code'
  9. ENTITY: 'test coverage' → ACTION/NEGATION: 'measure with coverage.py' → RESULT: 'coverage visibility'
  10. ENTITY: 'environments' → ACTION/NEGATION: 'isolate with venv/poetry/uv' → RESULT: 'dependency isolation'
  11. ENTITY: 'dependencies' → ACTION/NEGATION: 'pin with lock files' → RESULT: 'reproducible builds'
  12. ENTITY: 'configuration' → ACTION/NEGATION: 'centralize in pyproject.toml' → RESULT: 'unified config'
  13. ENTITY: 'project structure' → ACTION/NEGATION: 'use src/ or package layout' → RESULT: 'clear organization'
  14. ENTITY: 'automation' → ACTION/NEGATION: 'setup pre-commit hooks' → RESULT: 'automated quality'
  15. ENTITY: 'data models' → ACTION/NEGATION: 'use Pydantic 2.11.4+' → RESULT: 'validated data'
  16. ENTITY: 'logging' → ACTION/NEGATION: 'implement structured logging' → RESULT: 'traceable execution'
  17. ENTITY: 'async operations' → ACTION/NEGATION: 'use async/await properly' → RESULT: 'efficient I/O'
  18. ENTITY: 'resource management' → ACTION/NEGATION: 'use context managers' → RESULT: 'clean resource handling'
  19. ENTITY: 'data structures' → ACTION/NEGATION: 'use dataclasses/Pydantic' → RESULT: 'structured data'

## TYPESCRIPT STANDARDS

TS_CONSTRAINTS:

  1. ENTITY: 'type safety' → ACTION/NEGATION: 'enable strict mode' → RESULT: 'maximum type safety'
  2. ENTITY: 'any types' → ACTION/NEGATION: 'avoid, use unknown alternative' → RESULT: 'type-safe code'
  3. ENTITY: 'data structures' → ACTION/NEGATION: 'prefer interfaces and type aliases' → RESULT: 'clear type definitions'
  4. ENTITY: 'code quality' → ACTION/NEGATION: 'enforce with ESLint + @typescript-eslint' → RESULT: 'consistent quality'
  5. ENTITY: 'code formatting' → ACTION/NEGATION: 'standardize with Prettier' → RESULT: 'uniform style'
  6. ENTITY: 'testing' → ACTION/NEGATION: 'implement with Jest/Vitest + RTL' → RESULT: 'comprehensive testing' → PRECEDENCE: 'defers to rules-101 TDD workflow'
  7. ENTITY: 'configuration' → ACTION/NEGATION: 'keep tsconfig.json clean' → RESULT: 'optimized builds'
  8. ENTITY: 'imports' → ACTION/NEGATION: 'use path aliases' → RESULT: 'clean import statements'
  9. ENTITY: 'code organization' → ACTION/NEGATION: 'structure in components/hooks/utils/services' → RESULT: 'logical organization'
  10. ENTITY: 'build tools' → ACTION/NEGATION: 'use Vite or Next.js' → RESULT: 'fast development'
  11. ENTITY: 'dependencies' → ACTION/NEGATION: 'manage with pnpm/yarn/npm + lockfile' → RESULT: 'consistent installs'
  12. ENTITY: 'environment variables' → ACTION/NEGATION: 'validate with zod' → RESULT: 'type-safe configuration'
  13. ENTITY: 'automation' → ACTION/NEGATION: 'setup Husky + lint-staged' → RESULT: 'automated quality checks'
  14. ENTITY: 'component documentation' → ACTION/NEGATION: 'use Storybook' → RESULT: 'isolated component testing'
  15. ENTITY: 'accessibility' → ACTION/NEGATION: 'ensure a11y compliance' → RESULT: 'inclusive interfaces'
  16. ENTITY: 'component structure' → ACTION/NEGATION: 'follow atomic design patterns' → RESULT: 'scalable UI'
  17. ENTITY: 'styling' → ACTION/NEGATION: 'adopt consistent CSS-in-JS/Tailwind' → RESULT: 'maintainable styles'
  18. ENTITY: 'prop validation' → ACTION/NEGATION: 'validate with Zod when needed' → RESULT: 'runtime safety'
  19. ENTITY: 'component documentation' → ACTION/NEGATION: 'document with Typedoc' → RESULT: 'API documentation'
  20. ENTITY: 'performance' → ACTION/NEGATION: 'optimize with useMemo/useCallback/React.memo' → RESULT: 'efficient rendering'
  21. ENTITY: 'state management' → ACTION/NEGATION: 'choose appropriate solution' → RESULT: 'scalable state'
  22. ENTITY: 'error handling' → ACTION/NEGATION: 'implement error boundaries' → RESULT: 'robust error handling'
  23. ENTITY: 'bundle size' → ACTION/NEGATION: 'analyze and optimize regularly' → RESULT: 'efficient bundles'

## SECURITY STANDARDS

SEC_CONSTRAINTS:

  1. ENTITY: 'dependencies' → ACTION/NEGATION: 'audit and update regularly' → RESULT: 'secure dependencies'
  2. ENTITY: 'secrets' → ACTION/NEGATION: 'never commit to version control' → RESULT: 'protected credentials'
  3. ENTITY: 'inputs' → ACTION/NEGATION: 'validate all, sanitize outputs' → RESULT: 'injection prevention'
  4. ENTITY: 'authentication' → ACTION/NEGATION: 'implement proper auth/authz' → RESULT: 'access control'
  5. ENTITY: 'communications' → ACTION/NEGATION: 'use HTTPS in production' → RESULT: 'encrypted transport'
  6. ENTITY: 'security events' → ACTION/NEGATION: 'log without exposing sensitive data' → RESULT: 'security monitoring'
  7. ENTITY: 'permissions' → ACTION/NEGATION: 'apply least privilege principle' → RESULT: 'minimal access'
  8. ENTITY: 'sensitive data' → ACTION/NEGATION: 'encrypt at rest and in transit' → RESULT: 'data protection'
  9. ENTITY: 'security decisions' → ACTION/NEGATION: 'document in ADRs' → RESULT: 'traceable security architecture' → PRECEDENCE: 'defers to rules-102'

## PERFORMANCE STANDARDS

PERF_CONSTRAINTS:

  1. ENTITY: 'bottlenecks' → ACTION/NEGATION: 'identify through profiling' → RESULT: 'performance optimization'
  2. ENTITY: 'caching' → ACTION/NEGATION: 'implement appropriate strategies' → RESULT: 'improved response times'
  3. ENTITY: 'resources' → ACTION/NEGATION: 'use lazy loading for non-critical' → RESULT: 'faster initial load'
  4. ENTITY: 'database queries' → ACTION/NEGATION: 'optimize and minimize API calls' → RESULT: 'efficient data access'
  5. ENTITY: 'performance metrics' → ACTION/NEGATION: 'monitor in production' → RESULT: 'performance visibility'
  6. ENTITY: 'memory usage' → ACTION/NEGATION: 'manage and prevent leaks' → RESULT: 'stable memory consumption'
  7. ENTITY: 'algorithms' → ACTION/NEGATION: 'choose appropriate data structures' → RESULT: 'optimal performance'
  8. ENTITY: 'performance decisions' → ACTION/NEGATION: 'document in ADRs' → RESULT: 'traceable performance architecture' → PRECEDENCE: 'defers to rules-102'

## VERSION CONTROL STANDARDS

GIT_CONSTRAINTS:

  1. ENTITY: 'commit messages' → ACTION/NEGATION: 'write clear and descriptive' → RESULT: 'traceable history'
  2. ENTITY: 'branching' → ACTION/NEGATION: 'use feature branches with Git/GitHub flow' → RESULT: 'organized development'
  3. ENTITY: 'code reviews' → ACTION/NEGATION: 'require through pull requests' → RESULT: 'quality assurance'
  4. ENTITY: 'commit history' → ACTION/NEGATION: 'maintain clean and meaningful' → RESULT: 'clear evolution'
  5. ENTITY: 'releases' → ACTION/NEGATION: 'use semantic versioning for tags' → RESULT: 'predictable releases'
  6. ENTITY: 'automation' → ACTION/NEGATION: 'use Git hooks for checks' → RESULT: 'automated quality'
  7. ENTITY: 'ignore files' → ACTION/NEGATION: 'maintain appropriate .gitignore' → RESULT: 'clean repository'
  8. ENTITY: 'merge strategy' → ACTION/NEGATION: 'prefer merge commits for traceability' → RESULT: 'clear merge history'
  9. ENTITY: 'rule compliance' → ACTION/NEGATION: 'include version info in commits' → RESULT: 'version traceability'

## CODE REVIEW STANDARDS

REVIEW_CONSTRAINTS:

  1. ENTITY: 'code changes' → ACTION/NEGATION: 'require review before merging' → RESULT: 'quality gate'
  2. ENTITY: 'feedback' → ACTION/NEGATION: 'provide constructive suggestions' → RESULT: 'collaborative improvement'
  3. ENTITY: 'review timing' → ACTION/NEGATION: 'complete within 24 hours' → RESULT: 'fast feedback loop'
  4. ENTITY: 'review process' → ACTION/NEGATION: 'use consistent checklist' → RESULT: 'thorough review'
  5. ENTITY: 'test verification' → ACTION/NEGATION: 'ensure adequate and passing tests' → RESULT: 'test coverage' → PRECEDENCE: 'defers to rules-101 TDD requirements'
  6. ENTITY: 'documentation' → ACTION/NEGATION: 'verify updates as needed' → RESULT: 'current documentation'
  7. ENTITY: 'performance impact' → ACTION/NEGATION: 'consider implications' → RESULT: 'performance awareness'
  8. ENTITY: 'security review' → ACTION/NEGATION: 'check for vulnerabilities' → RESULT: 'security assurance'
  9. ENTITY: 'rule compliance' → ACTION/NEGATION: 'verify adherence to all applicable rules' → RESULT: 'standards compliance'
  10. ENTITY: 'ADR consistency' → ACTION/NEGATION: 'verify alignment with architectural decisions' → RESULT: 'architectural compliance' → PRECEDENCE: 'defers to rules-102'

## DEPLOYMENT STANDARDS

DEPLOY_CONSTRAINTS:

  1. ENTITY: 'deployments' → ACTION/NEGATION: 'automate with CI/CD pipelines' → RESULT: 'consistent deployments'
  2. ENTITY: 'failed deployments' → ACTION/NEGATION: 'implement rollback strategies' → RESULT: 'quick recovery'
  3. ENTITY: 'applications' → ACTION/NEGATION: 'monitor and infrastructure' → RESULT: 'operational visibility'
  4. ENTITY: 'observability' → ACTION/NEGATION: 'implement comprehensive logging' → RESULT: 'troubleshooting capability'
  5. ENTITY: 'data' → ACTION/NEGATION: 'maintain backups and recovery' → RESULT: 'data protection'
  6. ENTITY: 'scaling' → ACTION/NEGATION: 'design for horizontal scaling' → RESULT: 'scalable architecture'
  7. ENTITY: 'environments' → ACTION/NEGATION: 'separate dev/staging/production' → RESULT: 'safe deployment pipeline'
  8. ENTITY: 'secrets' → ACTION/NEGATION: 'manage configuration securely' → RESULT: 'secure operations'
  9. ENTITY: 'deployment decisions' → ACTION/NEGATION: 'document in ADRs' → RESULT: 'traceable deployment architecture' → PRECEDENCE: 'defers to rules-102'

## QUALITY ASSURANCE STANDARDS

QA_CONSTRAINTS:

  1. ENTITY: 'definition of done' → ACTION/NEGATION: 'define and maintain criteria' → RESULT: 'quality gate' → PRECEDENCE: 'defers to rules-101'
  2. ENTITY: 'continuous integration' → ACTION/NEGATION: 'implement with automated testing' → RESULT: 'early issue detection'
  3. ENTITY: 'static analysis' → ACTION/NEGATION: 'use tools for early issue detection' → RESULT: 'proactive quality'
  4. ENTITY: 'quality metrics' → ACTION/NEGATION: 'track and measure technical debt' → RESULT: 'quality visibility'
  5. ENTITY: 'code refactoring' → ACTION/NEGATION: 'perform regularly for quality' → RESULT: 'maintainable codebase'
  6. ENTITY: 'technical debt' → ACTION/NEGATION: 'track and prioritize' → RESULT: 'debt management'
  7. ENTITY: 'standards compliance' → ACTION/NEGATION: 'ensure adherence to practices' → RESULT: 'consistent quality'
  8. ENTITY: 'rule precedence' → ACTION/NEGATION: 'verify compliance with hierarchy' → RESULT: 'consistent rule application'

## ENFORCEMENT PROTOCOLS

ENFORCEMENT_WORKFLOW:
  VERSION_COMPATIBILITY_CHECK:
    - ACTION: 'verify' → OBJECT: 'rules version compatibility' → STATUS: 'mandatory before execution'
    - ACTION: 'load' → OBJECT: 'rule precedence hierarchy' → STATUS: 'required for conflict resolution'

  PRE_EXECUTION_CHECKS:
    - ACTION: 'validate' → OBJECT: 'standards compliance' → STATUS: 'mandatory before coding'
    - ACTION: 'verify' → OBJECT: 'tool configuration' → STATUS: 'required for automation'
    - ACTION: 'check' → OBJECT: 'environment setup' → STATUS: 'prerequisite for development'
    - ACTION: 'confirm' → OBJECT: 'rule precedence understanding' → STATUS: 'conflict prevention'

  DURING_EXECUTION_CHECKS:
    - ACTION: 'monitor' → OBJECT: 'standard adherence' → STATUS: 'continuous validation'
    - ACTION: 'enforce' → OBJECT: 'automated checks' → STATUS: 'real-time feedback'
    - ACTION: 'document' → OBJECT: 'violations and resolutions' → STATUS: 'compliance tracking'
    - ACTION: 'apply' → OBJECT: 'rule precedence' → STATUS: 'conflict resolution'

  POST_EXECUTION_CHECKS:
    - ACTION: 'review' → OBJECT: 'compliance status' → STATUS: 'completion validation'
    - ACTION: 'update' → OBJECT: 'violations log' → STATUS: 'tracking maintenance'
    - ACTION: 'report' → OBJECT: 'compliance metrics' → STATUS: 'visibility reporting'
    - ACTION: 'document' → OBJECT: 'rule precedence usage' → STATUS: 'precedence tracking'

ENFORCEMENT_CONSTRAINTS:

  1. ENTITY: 'standard enforcement' → ACTION/NEGATION: 'automate through tooling' → RESULT: 'consistent application'
  2. ENTITY: 'peer review' → ACTION/NEGATION: 'use for compliance verification' → RESULT: 'human validation'
  3. ENTITY: 'standards evolution' → ACTION/NEGATION: 'review and update regularly' → RESULT: 'current practices'
  4. ENTITY: 'training' → ACTION/NEGATION: 'provide on standards and practices' → RESULT: 'team competency'
  5. ENTITY: 'exceptions' → ACTION/NEGATION: 'document deviations with rationale' → RESULT: 'justified exceptions'
  6. ENTITY: 'compliance metrics' → ACTION/NEGATION: 'measure and report' → RESULT: 'progress tracking'
  7. ENTITY: 'feedback collection' → ACTION/NEGATION: 'gather for improvement' → RESULT: 'continuous improvement'
  8. ENTITY: 'rule conflicts' → ACTION/NEGATION: 'resolve through precedence hierarchy' → RESULT: 'consistent rule application'
  9. ENTITY: 'precedence violations' → ACTION/NEGATION: 'document and resolve' → RESULT: 'maintained rule hierarchy'

## CONTINUOUS IMPROVEMENT PROTOCOLS

IMPROVEMENT_WORKFLOW:
  RETROSPECTIVE_PROCESS:
    - ACTION: 'conduct' → OBJECT: 'regular retrospectives' → FREQUENCY: 'every sprint'
    - ACTION: 'identify' → OBJECT: 'improvement opportunities' → RESULT: 'actionable insights'
    - ACTION: 'implement' → OBJECT: 'improvement actions' → TIMELINE: 'next sprint'
    - ACTION: 'review' → OBJECT: 'rule effectiveness' → RESULT: 'rule system optimization'

  LEARNING_PROCESS:
    - ACTION: 'encourage' → OBJECT: 'continuous learning' → RESULT: 'skill development'
    - ACTION: 'experiment' → OBJECT: 'new technologies and practices' → CONSTRAINT: 'controlled environment'
    - ACTION: 'share' → OBJECT: 'knowledge and best practices' → RESULT: 'team growth'
    - ACTION: 'evolve' → OBJECT: 'rule system' → RESULT: 'adaptive standards'

  FEEDBACK_PROCESS:
    - ACTION: 'implement' → OBJECT: 'fast feedback loops' → RESULT: 'rapid improvement'
    - ACTION: 'collect' → OBJECT: 'feedback on processes' → RESULT: 'process optimization'
    - ACTION: 'evolve' → OBJECT: 'standards based on experience' → RESULT: 'adaptive practices'
    - ACTION: 'refine' → OBJECT: 'rule precedence' → RESULT: 'optimized rule hierarchy'

## INTEGRATION WITH MEMORY SYSTEM

MEMORY_INTEGRATION_CONSTRAINTS:

  1. ENTITY: 'ethos compliance' → ACTION/NEGATION: 'verify against memory files' → RESULT: 'consistent standards' → PRECEDENCE: 'defers to rules-102'
  2. ENTITY: 'standards violations' → ACTION/NEGATION: 'track in AI-NOTES-2-SELF.md' → RESULT: 'violation awareness' → PRECEDENCE: 'defers to rules-102'
  3. ENTITY: 'pattern compliance' → ACTION/NEGATION: 'document in PATTERN-REGISTRY.md' → RESULT: 'pattern consistency' → PRECEDENCE: 'defers to rules-102'
  4. ENTITY: 'ethos deviations' → ACTION/NEGATION: 'justify in ADRs' → RESULT: 'documented exceptions' → PRECEDENCE: 'defers to rules-102'
  5. ENTITY: 'compliance verification' → ACTION/NEGATION: 'include in pre-execution protocol' → RESULT: 'proactive compliance'
  6. ENTITY: 'rule precedence conflicts' → ACTION/NEGATION: 'document in ADRs' → RESULT: 'traceable conflict resolution' → PRECEDENCE: 'defers to rules-102'

MEMORY_INTEGRATION_WORKFLOW:
  INITIALIZATION_PHASE:
    - ACTION: 'verify' → OBJECT: 'version compatibility' → STATUS: 'mandatory before execution'
    - ACTION: 'load' → OBJECT: 'ethos standards' → STATUS: 'mandatory before coding'
    - ACTION: 'verify' → OBJECT: 'compliance history' → STATUS: 'context awareness'
    - ACTION: 'establish' → OBJECT: 'rule precedence context' → STATUS: 'conflict prevention'

  EXECUTION_PHASE:
    - ACTION: 'validate' → OBJECT: 'standard adherence' → STATUS: 'continuous checking'
    - ACTION: 'document' → OBJECT: 'violations and resolutions' → STATUS: 'real-time tracking'
    - ACTION: 'apply' → OBJECT: 'rule precedence' → STATUS: 'conflict resolution'

  COMPLETION_PHASE:
    - ACTION: 'update' → OBJECT: 'compliance records' → STATUS: 'completion requirement'
    - ACTION: 'report' → OBJECT: 'standards metrics' → STATUS: 'visibility maintenance'
    - ACTION: 'document' → OBJECT: 'rule precedence usage' → STATUS: 'precedence tracking'

## ENFORCEMENT VERIFICATION

VERIFICATION_STAGES:

- STAGE: 'initialization' → REQUIREMENT: 'version compatibility verified and ethos standards loaded' → VERIFICATION: 'compatible versions and standards context available'
- STAGE: 'pre-coding' → REQUIREMENT: 'compliance tools configured and rule precedence established' → VERIFICATION: 'automation enabled and hierarchy understood'
- STAGE: 'during-coding' → REQUIREMENT: 'standards adherence maintained and precedence applied' → VERIFICATION: 'real-time validation and conflict resolution'
- STAGE: 'post-coding' → REQUIREMENT: 'compliance verified and precedence documented' → VERIFICATION: 'quality gate passed and hierarchy maintained'
- STAGE: 'completion' → REQUIREMENT: 'violations documented and precedence tracked' → VERIFICATION: 'compliance tracked and hierarchy preserved'

COMPATIBILITY:

- REQUIRES: 'rules-101 v1.1+'
- REQUIRES: 'rules-102 v1.2+'
- CURRENT_VERSION: 'v1.2'
- PRECEDENCE_LEVEL: '3 (Implementation standards and practices)'
- ALIGNMENT: 'Mock usage policy aligned with rules-101 v1.1+'

