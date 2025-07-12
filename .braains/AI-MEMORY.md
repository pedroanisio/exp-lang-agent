# Architectural Memory - AI Linguistics Agent

## Current Patterns
- **Pydantic-AI Agent Pattern**: Core AI agent using Anthropic Claude models with structured responses
- **FastAPI REST Pattern**: RESTful API design with automatic OpenAPI documentation
- **ANTLR Integration Pattern**: Grammar parsing and analysis using ANTLR4 Python runtime
- **TDD Workflow Pattern**: Red-Green-Refactor cycle with git tagging for traceability
- **Memory Persistence Pattern**: Context preservation using .braains/ directory structure

## Design Decisions
- **2025-07-12**: **AI Framework Selection**: Chose Pydantic-AI for structured AI responses and type safety
- **2025-07-12**: **Web Framework Selection**: Chose FastAPI over Flask for automatic documentation and async support
- **2025-07-12**: **Grammar Processing**: Selected ANTLR4 for robust parser generation and language recognition
- **2025-07-12**: **Database Strategy**: SQLite for development, PostgreSQL for production with session management
- **2025-07-12**: **Frontend Framework**: React with TypeScript for type-safe UI development

## Constraints
- **Rule Compliance**: Must follow Rules 101-106 precedence hierarchy
- **TDD Methodology**: No implementation without failing tests (Rules-101)
- **Type Safety**: Comprehensive type hints and validation (Pydantic + TypeScript)
- **Documentation**: All architectural decisions must have ADRs (Rules-102)
- **Code Quality**: Comprehensive linting and formatting (Rules-106)

## Technology Stack
- **Backend**: Python 3.11+, FastAPI, Pydantic-AI, SQLAlchemy, Alembic
- **AI Integration**: Anthropic API (Claude 3.5 Sonnet)
- **Grammar Processing**: ANTLR4 Python runtime
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: React 18+, TypeScript 5+, Vite
- **Testing**: pytest, Jest, React Testing Library
- **Quality**: Ruff, Black, ESLint, Prettier, MyPy



## Neo4j Knowledge Graph Integration

### Architecture Enhancement
- **Date**: 2024-12-07
- **Decision**: Integrate Neo4j as knowledge graph database for linguistic and compiler knowledge
- **Rationale**: Hybrid approach combining LLM semantic understanding with structured knowledge retrieval

### Knowledge Graph Structure
- **Linguistic Articles**: Parsed academic papers, research articles, linguistic theories
- **Compiler Knowledge**: ANTLR grammars, EBNF specifications, parsing techniques
- **Relationships**: Semantic connections between concepts, citations, dependencies
- **Retrieval**: Graph-based queries for precise knowledge access

### Integration Points
- **Pydantic-AI**: Enhanced with graph-based context retrieval
- **Anthropic API**: Augmented with structured knowledge from Neo4j
- **Session Management**: Include graph query history and knowledge paths
- **Web Interface**: Knowledge graph visualization and exploration

### Technical Components
- **Neo4j Database**: Graph storage and querying
- **Knowledge Parser**: Article and document processing pipeline
- **Graph Builder**: Relationship extraction and graph construction
- **Retrieval System**: Hybrid LLM + graph query system
- **Visualization**: Interactive knowledge graph exploration



## Enhanced Architecture: Hybrid Database + Docker

### Database Strategy
- **Neo4j**: Graph relationships, formal grammar structures, concept hierarchies
- **ChromaDB**: Vector embeddings, semantic similarity, content-based retrieval
- **Query Routing**: Intelligent selection based on query type and use case
- **Synchronization**: Maintain consistency between graph and vector representations

### Docker Containerization
- **Multi-container Architecture**: Separate containers for each service
- **Service Isolation**: Clean separation of concerns and dependencies
- **Scalability**: Independent scaling of database and application components
- **Development**: Consistent environment across team and deployment stages

### Container Architecture
```
├── neo4j/              # Graph database container
├── chromadb/           # Vector database container  
├── app/                # FastAPI + Pydantic-AI container
├── frontend/           # React web interface container
├── nginx/              # Reverse proxy container
└── docker-compose.yml  # Orchestration configuration
```

### Knowledge Processing Pipeline
1. **Article Parsing**: Extract content from linguistic and compiler literature
2. **Relationship Extraction**: Identify semantic and structural relationships
3. **Vector Embedding**: Generate embeddings for similarity search
4. **Graph Construction**: Build knowledge graph with extracted relationships
5. **Dual Storage**: Store in both Neo4j (relationships) and ChromaDB (vectors)

### Query Processing Flow
1. **Query Analysis**: Determine optimal database(s) for query type
2. **Parallel Retrieval**: Query relevant databases simultaneously
3. **Result Fusion**: Merge and rank results from multiple sources
4. **Context Enhancement**: Augment LLM context with retrieved knowledge
5. **Response Generation**: Generate informed responses using hybrid knowledge

