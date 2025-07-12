# AI Linguistics Agent

A specialized Python AI agent focused on linguistics, compilers, EBNF, and ANTLR analysis with web interface capabilities.

## Features

- **Linguistics Analysis**: Advanced natural language processing and grammatical analysis
- **Grammar Processing**: EBNF and ANTLR integration for formal grammar analysis
- **AI-Powered Insights**: Anthropic Claude integration for intelligent recommendations
- **Session Management**: Persistent conversation history and project organization
- **Web Interface**: Modern React-based frontend for interactive analysis
- **Type Safety**: Comprehensive Pydantic validation and TypeScript integration

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic-AI
- **AI Integration**: Anthropic API (Claude 3.5 Sonnet)
- **Grammar Processing**: ANTLR4 Python runtime
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: React 18+, TypeScript 5+
- **Testing**: pytest with TDD methodology
- **Quality**: Comprehensive linting with Ruff, Black, ESLint

## Development Approach

This project follows Test-Driven Development (TDD) methodology with comprehensive rule compliance:

- **Rules-101**: Core TDD and engineering principles
- **Rules-102**: Memory persistence and ADR management
- **Rules-103**: Implementation standards and practices
- **Rules-104**: Requirements engineering and specification
- **Rules-106**: Code quality and linting standards

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd ai-linguistics-agent

# Install dependencies
pip install -e ".[dev,test]"

# Run tests
pytest

# Start development server
uvicorn src.linguistics_agent.api.main:app --reload
```

## Project Structure

```
ai-linguistics-agent/
├── .braains/                    # Memory system and ADRs
├── src/linguistics_agent/       # Core application code
├── tests/                       # Test suite
├── frontend/                    # React frontend
├── requirements/                # Requirements documentation
└── .linting/                    # Linting configurations
```

## License

MIT License - see LICENSE file for details.

## Contributing

Please follow the established TDD workflow and rule compliance system. See `.braains/` directory for architectural decisions and development patterns.

