---
alwaysApply: true
version: 1.0
changelog:
  - v1.0: Initial comprehensive linting standards with multi-language support
---

# rules-106-v1.0

DOMAIN: code quality and linting standards
OBJECTIVE: ensure consistent code quality through comprehensive linting across all supported languages and frameworks

VERSION_COMPATIBILITY_MATRIX:

- RULES_101: 'v1.1+' → STATUS: 'required foundation' → PRECEDENCE: 'level 1 (Core TDD and engineering principles)'
- RULES_102: 'v1.2+' → STATUS: 'required memory/ADR system' → PRECEDENCE: 'level 2 (Memory persistence and ADR management)'
- RULES_103: 'v1.2+' → STATUS: 'required implementation layer' → PRECEDENCE: 'level 3 (Implementation standards and practices)'
- RULES_104: 'v1.0+' → STATUS: 'optional requirements layer' → PRECEDENCE: 'level 4 (Requirements engineering and specification)'
- RULES_106: 'v1.0' → STATUS: 'linting and quality enforcement' → PRECEDENCE: 'level 5 (Code quality and linting standards)'

RULE_PRECEDENCE_ACKNOWLEDGMENT:

- DEFERS_TO: 'rules-101 for TDD workflow integration and core engineering principles'
- DEFERS_TO: 'rules-102 for linting configuration ADRs and memory management'
- DEFERS_TO: 'rules-103 for implementation standards and coding practices'
- DEFERS_TO: 'rules-104 for requirements-driven linting when applicable'
- AUTHORITY: 'linting tool selection, configuration, automation, and quality metrics'

## FILE PATH VARIABLES

LINTING_ROOT = '${workspaceFolder}/.linting'
LINTING_CONFIG_DIR = '${workspaceFolder}/.linting/configs'
LINTING_REPORTS_DIR = '${workspaceFolder}/.linting/reports'
LINTING_MEMORY_FILE = '${workspaceFolder}/.braains/LINTING-MEMORY.md'
LINTING_METRICS_FILE = '${workspaceFolder}/.braains/LINTING-METRICS.md'
LINTING_VIOLATIONS_LOG = '${workspaceFolder}/.braains/LINTING-VIOLATIONS.md'

## COMPREHENSIVE LINTING STANDARDS

LINTING_PHILOSOPHY:

- PRINCIPLE: 'language-agnostic quality foundation' → IMPLEMENTATION: 'broad engineering principles'
- PRINCIPLE: 'language-specific excellence' → IMPLEMENTATION: 'complete tooling when needed'
- PRINCIPLE: 'project-appropriate depth' → IMPLEMENTATION: 'scale linting to project complexity'
- PRINCIPLE: 'AI agent adaptability' → IMPLEMENTATION: 'context-aware rule application'

LINT_CONSTRAINTS:

  1. ENTITY: 'linting violations' → ACTION/NEGATION: 'never commit code with violations' → RESULT: 'clean code baseline'
  2. ENTITY: 'linting configuration' → ACTION/NEGATION: 'centralize and version control' → RESULT: 'consistent standards'
  3. ENTITY: 'auto-fixable issues' → ACTION/NEGATION: 'automatically resolve' → RESULT: 'efficient cleanup'
  4. ENTITY: 'linting rules' → ACTION/NEGATION: 'align with coding standards' → RESULT: 'integrated quality'
  5. ENTITY: 'linting bypasses' → ACTION/NEGATION: 'justify and document' → RESULT: 'controlled exceptions'
  6. ENTITY: 'linting metrics' → ACTION/NEGATION: 'track and report' → RESULT: 'quality visibility'
  7. ENTITY: 'custom linting rules' → ACTION/NEGATION: 'create for project-specific patterns' → RESULT: 'tailored quality'
  8. ENTITY: 'linting performance' → ACTION/NEGATION: 'optimize for fast feedback' → RESULT: 'efficient development'
  9. ENTITY: 'linting integration' → ACTION/NEGATION: 'embed in TDD workflow' → RESULT: 'seamless quality' → PRECEDENCE: 'defers to rules-101'
  10. ENTITY: 'linting configuration changes' → ACTION/NEGATION: 'document in ADRs' → RESULT: 'traceable standards evolution' → PRECEDENCE: 'defers to rules-102'

## UNIVERSAL LINTING PRINCIPLES

UNIVERSAL_CONSTRAINTS:

  1. ENTITY: 'code complexity' → ACTION/NEGATION: 'limit cyclomatic complexity < 10' → RESULT: 'maintainable code'
  2. ENTITY: 'function length' → ACTION/NEGATION: 'limit to reasonable size' → RESULT: 'focused functions'
  3. ENTITY: 'duplicate code' → ACTION/NEGATION: 'detect and eliminate' → RESULT: 'DRY compliance'
  4. ENTITY: 'unused code' → ACTION/NEGATION: 'remove automatically' → RESULT: 'clean codebase'
  5. ENTITY: 'security vulnerabilities' → ACTION/NEGATION: 'detect and prevent' → RESULT: 'secure code'
  6. ENTITY: 'performance anti-patterns' → ACTION/NEGATION: 'identify and optimize' → RESULT: 'efficient code'
  7. ENTITY: 'accessibility issues' → ACTION/NEGATION: 'detect and fix' → RESULT: 'inclusive interfaces'
  8. ENTITY: 'naming conventions' → ACTION/NEGATION: 'enforce consistently' → RESULT: 'readable code'

## COMPREHENSIVE PYTHON LINTING

PYTHON_LINTING_STACK:
  
  MODERN_PYTHON_TOOLS:
    - PRIMARY: 'Ruff' → PURPOSE: 'ultra-fast Python linter and formatter' → ADVANTAGE: 'speed + comprehensive rules'
    - FORMATTER: 'Black' → PURPOSE: 'uncompromising code formatting' → INTEGRATION: 'auto-fix'
    - IMPORT_SORTER: 'isort' → PURPOSE: 'import organization' → INTEGRATION: 'auto-fix'
    - TYPE_CHECKER: 'mypy' → PURPOSE: 'static type checking' → REQUIREMENT: 'mandatory for type hints'
    - SECURITY: 'bandit' → PURPOSE: 'security vulnerability detection' → PRIORITY: 'high'
    - COMPLEXITY: 'radon' → PURPOSE: 'code complexity metrics' → MONITORING: 'continuous'
    - DOCSTRING: 'pydocstyle' → PURPOSE: 'docstring style enforcement' → STANDARD: 'PEP 257'
    - DEAD_CODE: 'vulture' → PURPOSE: 'unused code detection' → CLEANUP: 'automated removal'

  PYTHON_RULE_CATEGORIES:

    STYLE_ENFORCEMENT:
      - ENTITY: 'PEP 8 compliance' → ACTION: 'enforce strictly' → RESULT: 'consistent Python style'
      - ENTITY: 'line length' → ACTION: 'limit to 88 characters' → RESULT: 'readable code'
      - ENTITY: 'indentation' → ACTION: 'enforce 4 spaces' → RESULT: 'consistent formatting'
      - ENTITY: 'string quotes' → ACTION: 'normalize consistently' → RESULT: 'uniform strings'
      - ENTITY: 'trailing commas' → ACTION: 'enforce where appropriate' → RESULT: 'clean diffs'

    PYTHON_QUALITY_RULES:
      - ENTITY: 'f-string usage' → ACTION: 'prefer over .format()' → RESULT: 'modern Python'
      - ENTITY: 'comprehensions' → ACTION: 'optimize where appropriate' → RESULT: 'efficient code'
      - ENTITY: 'exception handling' → ACTION: 'use specific exceptions' → RESULT: 'precise error handling'
      - ENTITY: 'magic methods' → ACTION: 'implement consistently' → RESULT: 'proper protocols'
      - ENTITY: 'context managers' → ACTION: 'use for resource management' → RESULT: 'safe resource handling'

    PYTHON_TYPE_SAFETY:
      - ENTITY: 'type hints' → ACTION: 'require for all public interfaces' → RESULT: 'type-safe code'
      - ENTITY: 'Any type usage' → ACTION: 'minimize and justify' → RESULT: 'specific types'
      - ENTITY: 'generic types' → ACTION: 'use appropriately' → RESULT: 'type-safe generics'
      - ENTITY: 'optional handling' → ACTION: 'handle None explicitly' → RESULT: 'null safety'
      - ENTITY: 'union types' → ACTION: 'use modern syntax (|)' → RESULT: 'modern type annotations'

    PYTHON_FRAMEWORK_SPECIFIC:
      
      DJANGO_LINTING:
        - TOOLS: 'flake8-django, django-stubs' → PURPOSE: 'Django-specific linting and typing'
        - RULES: 'model validation, URL patterns, template usage' → QUALITY: 'Django best practices'
        - SECURITY: 'Django security patterns' → PROTECTION: 'framework vulnerabilities'
        - PERFORMANCE: 'ORM optimization patterns' → EFFICIENCY: 'database performance'

      FASTAPI_LINTING:
        - TOOLS: 'flake8-fastapi' → PURPOSE: 'FastAPI-specific linting'
        - RULES: 'dependency injection, response models, async patterns' → QUALITY: 'API best practices'
        - VALIDATION: 'Pydantic model usage' → CORRECTNESS: 'data validation'
        - DOCUMENTATION: 'OpenAPI schema compliance' → USABILITY: 'API documentation'

      PYTEST_LINTING:
        - TOOLS: 'flake8-pytest-style' → PURPOSE: 'pytest-specific linting'
        - RULES: 'fixture usage, assertion patterns, parametrization' → QUALITY: 'effective testing'
        - NAMING: 'test function conventions' → CLARITY: 'descriptive tests'
        - ORGANIZATION: 'test file structure' → MAINTAINABILITY: 'organized tests'

      DATA_SCIENCE_LINTING:
        - TOOLS: 'flake8-pandas, flake8-numpy' → PURPOSE: 'data science linting'
        - RULES: 'DataFrame operations, array usage' → PERFORMANCE: 'efficient data processing'
        - DEPRECATION: 'deprecated methods' → MAINTENANCE: 'modern library usage'
        - BEST_PRACTICES: 'vectorization patterns' → PERFORMANCE: 'optimized computations'

## COMPREHENSIVE TYPESCRIPT LINTING

TYPESCRIPT_LINTING_STACK:
  
  MODERN_TYPESCRIPT_TOOLS:
    - PRIMARY: 'ESLint + @typescript-eslint' → PURPOSE: 'TypeScript-aware linting'
    - FORMATTER: 'Prettier' → PURPOSE: 'code formatting' → INTEGRATION: 'auto-fix'
    - TYPE_CHECKER: 'TypeScript compiler' → PURPOSE: 'type safety validation'
    - SECURITY: 'eslint-plugin-security' → PURPOSE: 'security best practices'
    - PERFORMANCE: 'eslint-plugin-sonarjs' → PURPOSE: 'performance and complexity'
    - ACCESSIBILITY: 'eslint-plugin-jsx-a11y' → PURPOSE: 'accessibility compliance'
    - IMPORTS: 'eslint-plugin-import' → PURPOSE: 'import/export validation'
    - UNUSED_IMPORTS: 'eslint-plugin-unused-imports' → PURPOSE: 'clean imports'

  TYPESCRIPT_RULE_CATEGORIES:

    TYPE_SAFETY_ENFORCEMENT:
      - ENTITY: 'strict mode' → ACTION: 'enable all strict flags' → RESULT: 'maximum type safety'
      - ENTITY: 'any type usage' → ACTION: 'avoid, use unknown' → RESULT: 'type-safe code'
      - ENTITY: 'explicit return types' → ACTION: 'require for functions' → RESULT: 'clear contracts'
      - ENTITY: 'null/undefined handling' → ACTION: 'handle explicitly' → RESULT: 'null safety'
      - ENTITY: 'type assertions' → ACTION: 'minimize and justify' → RESULT: 'safe type assertions'

    TYPESCRIPT_QUALITY_RULES:
      - ENTITY: 'interface vs type' → ACTION: 'prefer interfaces for objects' → RESULT: 'consistent type definitions'
      - ENTITY: 'enum usage' → ACTION: 'prefer const assertions' → RESULT: 'efficient enums'
      - ENTITY: 'generic constraints' → ACTION: 'use appropriate bounds' → RESULT: 'safe generics'
      - ENTITY: 'utility types' → ACTION: 'leverage built-in utilities' → RESULT: 'type manipulation'
      - ENTITY: 'module declarations' → ACTION: 'use proper ambient declarations' → RESULT: 'type-safe modules'

    JAVASCRIPT_INTEROP:
      - ENTITY: 'JS file types' → ACTION: 'provide proper declarations' → RESULT: 'typed JavaScript'
      - ENTITY: 'third-party types' → ACTION: 'use @types packages' → RESULT: 'typed dependencies'
      - ENTITY: 'gradual typing' → ACTION: 'incrementally add types' → RESULT: 'migration strategy'
      - ENTITY: 'type-only imports' → ACTION: 'use type imports' → RESULT: 'optimized bundles'

    TYPESCRIPT_FRAMEWORK_SPECIFIC:
      
      REACT_LINTING:
        - TOOLS: 'eslint-plugin-react, eslint-plugin-react-hooks' → PURPOSE: 'React-specific linting'
        - RULES: 'hook dependencies, component patterns, prop validation' → QUALITY: 'React best practices'
        - TYPES: 'React.FC vs function components' → CONSISTENCY: 'component definitions'
        - PERFORMANCE: 'memo usage, callback optimization' → EFFICIENCY: 'render optimization'

      NEXTJS_LINTING:
        - TOOLS: 'eslint-config-next' → PURPOSE: 'Next.js-specific linting'
        - RULES: 'page structure, API routes, image optimization' → QUALITY: 'Next.js best practices'
        - PERFORMANCE: 'bundle optimization, SSR patterns' → EFFICIENCY: 'optimized applications'
        - SEO: 'meta tags, structured data' → VISIBILITY: 'search optimization'

      NODE_LINTING:
        - TOOLS: 'eslint-plugin-node' → PURPOSE: 'Node.js-specific linting'
        - RULES: 'module resolution, async patterns' → QUALITY: 'Node.js best practices'
        - SECURITY: 'secure coding patterns' → PROTECTION: 'server-side security'
        - PERFORMANCE: 'efficient I/O patterns' → EFFICIENCY: 'server performance'

      TESTING_LINTING:
        - TOOLS: 'eslint-plugin-jest, eslint-plugin-testing-library' → PURPOSE: 'testing linting'
        - RULES: 'test structure, assertion patterns, mock usage' → QUALITY: 'effective testing'
        - ASYNC: 'async test patterns' → RELIABILITY: 'proper async testing'
        - COVERAGE: 'test coverage patterns' → COMPLETENESS: 'comprehensive testing'

## LINTING WORKFLOW INTEGRATION

LINTING_TDD_INTEGRATION:

  RED_PHASE_LINTING:
    - ACTION: 'verify' → OBJECT: 'test file linting' → STATUS: 'mandatory before commit'
    - ACTION: 'apply' → OBJECT: 'auto-fix rules' → STATUS: 'automatic cleanup'
    - ACTION: 'validate' → OBJECT: 'language-specific configuration' → STATUS: 'standards compliance'
    - ACTION: 'check' → OBJECT: 'framework-specific test patterns' → STATUS: 'best practices'

  GREEN_PHASE_LINTING:
    - ACTION: 'lint' → OBJECT: 'implementation code' → STATUS: 'mandatory before commit'
    - ACTION: 'fix' → OBJECT: 'auto-fixable violations' → STATUS: 'automatic resolution'
    - ACTION: 'review' → OBJECT: 'manual fix requirements' → STATUS: 'manual intervention'
    - ACTION: 'optimize' → OBJECT: 'performance patterns' → STATUS: 'efficiency validation'

  REFACTOR_PHASE_LINTING:
    - ACTION: 'verify' → OBJECT: 'refactored code quality' → STATUS: 'maintained standards'
    - ACTION: 'optimize' → OBJECT: 'linting performance' → STATUS: 'efficient execution'
    - ACTION: 'update' → OBJECT: 'custom rules if needed' → STATUS: 'evolving standards'
    - ACTION: 'validate' → OBJECT: 'cross-language consistency' → STATUS: 'unified standards'

## MULTI-LANGUAGE PROJECT LINTING

MULTI_LANGUAGE_CONSTRAINTS:

  1. ENTITY: 'language mixing' → ACTION/NEGATION: 'maintain separate configurations' → RESULT: 'language-specific quality'
  2. ENTITY: 'shared standards' → ACTION/NEGATION: 'align where possible' → RESULT: 'consistent principles'
  3. ENTITY: 'polyglot projects' → ACTION/NEGATION: 'coordinate linting workflows' → RESULT: 'unified quality'
  4. ENTITY: 'language boundaries' → ACTION/NEGATION: 'respect interface contracts' → RESULT: 'clean integration'
  5. ENTITY: 'build integration' → ACTION/NEGATION: 'coordinate linting in CI/CD' → RESULT: 'comprehensive validation'

LANGUAGE_DETECTION_WORKFLOW:

- ACTION: 'detect' → OBJECT: 'primary project language' → METHOD: 'file analysis'
- ACTION: 'configure' → OBJECT: 'appropriate linting stack' → METHOD: 'context-aware setup'
- ACTION: 'apply' → OBJECT: 'language-specific rules' → METHOD: 'targeted enforcement'
- ACTION: 'coordinate' → OBJECT: 'multi-language projects' → METHOD: 'unified workflow'

## CONFIGURATION MANAGEMENT

CONFIGURATION_STRATEGY:

  CENTRALIZED_CONFIGURATION:
    - PYTHON_CONFIG: 'pyproject.toml' → CENTRALIZATION: 'single Python configuration'
    - TYPESCRIPT_CONFIG: 'eslint.config.js' → CENTRALIZATION: 'single TypeScript configuration'
    - SHARED_CONFIG: 'shared base configurations' → CONSISTENCY: 'common standards'
    - PROJECT_CONFIG: 'project-specific overrides' → FLEXIBILITY: 'contextual customization'

  CONFIGURATION_INHERITANCE:
    - BASE_RULES: 'universal quality principles' → FOUNDATION: 'consistent quality'
    - LANGUAGE_RULES: 'language-specific extensions' → SPECIALIZATION: 'targeted quality'
    - FRAMEWORK_RULES: 'framework-specific additions' → OPTIMIZATION: 'best practices'
    - PROJECT_RULES: 'project-specific customizations' → ADAPTATION: 'contextual fit'

## LINTING AUTOMATION

AUTOMATION_WORKFLOW:

  PRE_COMMIT_LINTING:
    - ACTION: 'detect' → OBJECT: 'changed file languages' → STATUS: 'context awareness'
    - ACTION: 'run' → OBJECT: 'appropriate linting tools' → STATUS: 'targeted validation'
    - ACTION: 'auto-fix' → OBJECT: 'fixable violations' → STATUS: 'automatic resolution'
    - ACTION: 'block' → OBJECT: 'commits with violations' → STATUS: 'quality enforcement'

  EDITOR_INTEGRATION:
    - ACTION: 'configure' → OBJECT: 'language-specific extensions' → STATUS: 'optimal tooling'
    - ACTION: 'enable' → OBJECT: 'real-time linting' → STATUS: 'immediate feedback'
    - ACTION: 'coordinate' → OBJECT: 'multi-language projects' → STATUS: 'unified experience'
    - ACTION: 'optimize' → OBJECT: 'performance for large projects' → STATUS: 'efficient development'

  CI_CD_LINTING:
    - ACTION: 'validate' → OBJECT: 'all project languages' → STATUS: 'comprehensive validation'
    - ACTION: 'parallelize' → OBJECT: 'language-specific linting' → STATUS: 'efficient execution'
    - ACTION: 'aggregate' → OBJECT: 'linting results' → STATUS: 'unified reporting'
    - ACTION: 'fail' → OBJECT: 'builds with violations' → STATUS: 'quality gate'

## LINTING METRICS AND REPORTING

METRICS_TRACKING:

  QUALITY_METRICS:
    - METRIC: 'violation_count' → MEASUREMENT: 'total violations per commit/PR'
    - METRIC: 'violation_severity' → MEASUREMENT: 'error/warning/info distribution'
    - METRIC: 'fix_rate' → MEASUREMENT: 'auto-fixed vs manual-fixed violations'
    - METRIC: 'compliance_score' → MEASUREMENT: 'percentage of clean commits'
    - METRIC: 'rule_effectiveness' → MEASUREMENT: 'violations caught per rule'
    - METRIC: 'language_quality' → MEASUREMENT: 'quality metrics per language'
    - METRIC: 'framework_compliance' → MEASUREMENT: 'framework-specific adherence'

  REPORTING_WORKFLOW:
    - ACTION: 'generate' → OBJECT: 'linting reports' → FREQUENCY: 'per commit/PR/build'
    - ACTION: 'track' → OBJECT: 'quality trends' → FREQUENCY: 'weekly/monthly'
    - ACTION: 'alert' → OBJECT: 'quality degradation' → TRIGGER: 'threshold breaches'
    - ACTION: 'update' → OBJECT: 'memory files with linting insights' → INTEGRATION: 'context preservation'
    - ACTION: 'analyze' → OBJECT: 'violation patterns' → PURPOSE: 'rule optimization'

## LINTING MEMORY INTEGRATION

MEMORY_INTEGRATION:

  LINTING_MEMORY_TRACKING:
    - ACTION: 'document' → OBJECT: 'linting configuration decisions' → FILE: '${LINTING_MEMORY_FILE}'
    - ACTION: 'track' → OBJECT: 'recurring violation patterns' → FILE: '${AI_NOTES_FILE}'
    - ACTION: 'register' → OBJECT: 'custom linting rules' → FILE: '${PATTERN_REGISTRY_FILE}'
    - ACTION: 'record' → OBJECT: 'linting tool changes' → STATUS: 'ADR creation trigger'
    - ACTION: 'maintain' → OBJECT: 'violation history' → FILE: '${LINTING_VIOLATIONS_LOG}'

  LINTING_CONTEXT_PRESERVATION:
    - CONTEXT: 'linting configuration evolution' → PRESERVATION: 'maintain decision history'
    - CONTEXT: 'violation pattern analysis' → PRESERVATION: 'learn from recurring issues'
    - CONTEXT: 'rule effectiveness tracking' → PRESERVATION: 'optimize rule sets'
    - CONTEXT: 'project-specific customizations' → PRESERVATION: 'maintain consistency'
    - CONTEXT: 'language-specific patterns' → PRESERVATION: 'cross-project learning'

## LINTING EXCEPTION HANDLING

EXCEPTION_MANAGEMENT:

  VIOLATION_BYPASSES:
    - JUSTIFICATION: 'document reason for disable' → FORMAT: 'inline comments'
    - SCOPE: 'minimize disable scope' → PRINCIPLE: 'surgical exceptions'
    - REVIEW: 'periodic review of disabled rules' → MAINTENANCE: 'exception hygiene'
    - TRACKING: 'monitor exception usage' → OVERSIGHT: 'prevent abuse'
    - DOCUMENTATION: 'ADR for systematic exceptions' → TRACEABILITY: 'decision documentation'

  LEGACY_CODE_HANDLING:
    - STRATEGY: 'gradual improvement approach' → IMPLEMENTATION: 'incremental cleanup'
    - ISOLATION: 'separate legacy from new code rules' → CONTROL: 'focused improvement'
    - MIGRATION: 'systematic rule application' → PLANNING: 'managed technical debt'
    - DOCUMENTATION: 'ADR for legacy handling strategy' → TRACEABILITY: 'approach documentation'

## LINTING TOOL EVOLUTION

TOOL_EVOLUTION:

  TOOL_EVALUATION:
    - FREQUENCY: 'quarterly tool assessment' → PURPOSE: 'stay current with best practices'
    - CRITERIA: 'performance, accuracy, maintainability' → EVALUATION: 'comprehensive assessment'
    - DOCUMENTATION: 'ADR for tool changes' → TRACEABILITY: 'decision documentation'
    - MIGRATION: 'systematic tool transition' → PLANNING: 'smooth adoption'

  RULE_EVOLUTION:
    - REVIEW: 'periodic rule effectiveness review' → FREQUENCY: 'monthly assessment'
    - ADJUSTMENT: 'rule severity and scope tuning' → OPTIMIZATION: 'balanced enforcement'
    - DOCUMENTATION: 'ADR for rule changes' → TRACEABILITY: 'standards evolution'
    - COMMUNICATION: 'team notification of changes' → ADOPTION: 'change management'

## LINTING INTEGRATION POINTS

INTEGRATION_POINTS:

  GIT_INTEGRATION:
    - HOOK: 'pre-commit linting' → ENFORCEMENT: 'mandatory quality gate'
    - HOOK: 'pre-push validation' → VERIFICATION: 'comprehensive check'
    - TAGGING: 'linting status in git tags' → TRACEABILITY: 'quality tracking'
    - WORKFLOW: 'linting in TDD phase transitions' → INTEGRATION: 'seamless quality'

  EDITOR_INTEGRATION:
    - REAL_TIME: 'live linting feedback' → EFFICIENCY: 'immediate correction'
    - AUTO_FIX: 'format on save' → AUTOMATION: 'consistent application'
    - CONFIGURATION: 'shared editor settings' → CONSISTENCY: 'team alignment'
    - EXTENSIONS: 'required linting extensions' → STANDARDIZATION: 'tool consistency'

  CI_CD_INTEGRATION:
    - PIPELINE: 'linting in build process' → ENFORCEMENT: 'automated quality gate'
    - REPORTING: 'linting results in build reports' → VISIBILITY: 'quality metrics'
    - FAILURE: 'fail builds on violations' → ENFORCEMENT: 'quality standards'
    - ARTIFACTS: 'linting reports as build artifacts' → PRESERVATION: 'historical data'

## ENFORCEMENT PROTOCOLS

ENFORCEMENT_WORKFLOW:

  PRE_EXECUTION_CHECKS:
    - ACTION: 'verify' → OBJECT: 'linting tools availability' → STATUS: 'mandatory before execution'
    - ACTION: 'validate' → OBJECT: 'linting configuration' → STATUS: 'standards compliance'
    - ACTION: 'load' → OBJECT: 'language-specific rules' → STATUS: 'context awareness'
    - ACTION: 'check' → OBJECT: 'framework detection' → STATUS: 'specialized rules'

  DURING_EXECUTION_CHECKS:
    - ACTION: 'monitor' → OBJECT: 'linting performance' → STATUS: 'efficiency tracking'
    - ACTION: 'apply' → OBJECT: 'auto-fix rules' → STATUS: 'automatic resolution'
    - ACTION: 'track' → OBJECT: 'violation patterns' → STATUS: 'learning insights'
    - ACTION: 'coordinate' → OBJECT: 'multi-language linting' → STATUS: 'unified quality'

  POST_EXECUTION_CHECKS:
    - ACTION: 'report' → OBJECT: 'linting results' → STATUS: 'quality visibility'
    - ACTION: 'update' → OBJECT: 'memory files' → STATUS: 'context preservation'
    - ACTION: 'analyze' → OBJECT: 'quality trends' → STATUS: 'continuous improvement'
    - ACTION: 'document' → OBJECT: 'significant violations' → STATUS: 'learning documentation'

ENFORCEMENT_CONSTRAINTS:

  1. ENTITY: 'linting automation' → ACTION/NEGATION: 'implement consistently' → RESULT: 'reliable quality'
  2. ENTITY: 'manual linting bypasses' → ACTION/NEGATION: 'minimize and document' → RESULT: 'controlled exceptions'
  3. ENTITY: 'linting performance' → ACTION/NEGATION: 'optimize for speed' → RESULT: 'efficient development'
  4. ENTITY: 'cross-language consistency' → ACTION/NEGATION: 'maintain where applicable' → RESULT: 'unified standards'
  5. ENTITY: 'linting evolution' → ACTION/NEGATION: 'adapt to best practices' → RESULT: 'current standards'

## COMPATIBILITY

- REQUIRES: 'rules-101 v1.1+'
- REQUIRES: 'rules-102 v1.2+'
- REQUIRES: 'rules-103 v1.2+'
- OPTIONAL: 'rules-104 v1.0+'
- CURRENT_VERSION: 'v1.0'
- PRECEDENCE_LEVEL: '5 (Code quality and linting standards)'

