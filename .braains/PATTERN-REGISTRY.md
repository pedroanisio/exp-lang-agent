# Pattern Registry - AI Linguistics Agent

## Established Patterns

### Pydantic-AI Agent Pattern
- **Description**: Structured AI agent using Pydantic-AI framework with type-safe responses
- **Usage**: When creating AI agents that need structured, validated outputs
- **Location**: src/linguistics_agent/agent.py
- **Examples**: LinguisticsAgent with GrammarAnalysis response models

### FastAPI REST Pattern
- **Description**: RESTful API design with automatic OpenAPI documentation
- **Usage**: When exposing AI agent functionality via HTTP endpoints
- **Location**: src/linguistics_agent/api/
- **Examples**: /api/analyze, /api/grammar/parse endpoints

### ANTLR Integration Pattern
- **Description**: Grammar parsing using ANTLR4 with Python runtime
- **Usage**: When processing formal grammars and language structures
- **Location**: src/linguistics_agent/grammar/
- **Examples**: EBNF parser, syntax tree generation

### TDD Workflow Pattern
- **Description**: Red-Green-Refactor cycle with git tagging for traceability
- **Usage**: For all feature development following Rules-101
- **Location**: tests/ directory structure
- **Examples**: test_linguistics_agent.py with structured test cases

### Memory Persistence Pattern
- **Description**: Context preservation using .braains/ directory structure
- **Usage**: Maintaining architectural decisions and development context
- **Location**: .braains/ directory
- **Examples**: AI-MEMORY.md, ADR files, pattern documentation

## Pattern Evolution
- **2025-07-12**: **Initial Pattern Establishment**: Core patterns defined for linguistics agent architecture
- **2025-07-12**: **Rule Integration Pattern**: Comprehensive rule system (101-106) integration approach

## Anti-Patterns
- **Mock Overuse**: Avoid mocks in implementation code, use only for external dependencies in tests
- **Rule Precedence Violations**: Never violate Rules-101 TDD principles for convenience
- **Context Loss**: Always update memory files to prevent architectural drift
- **Undocumented Decisions**: Create ADRs for all significant architectural choices

