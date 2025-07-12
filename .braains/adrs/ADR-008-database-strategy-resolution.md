# ADR-008: Database Strategy Resolution - SQLite vs PostgreSQL

## Metadata
- **Status**: Proposed
- **Date**: 2025-07-12
- **Deciders**: AI Agent, Database Architect
- **Technical Story**: Resolve ADR-004 compliance gap
- **Rule Compliance**: rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+
- **Supersedes**: Clarifies ADR-004 implementation approach

## Context and Problem Statement

A critical compliance gap exists between ADR-004 (PostgreSQL State Management) and the current implementation which uses SQLite. This creates confusion about the actual database strategy and violates architectural consistency. We need to resolve this mismatch and establish a clear database strategy that supports both development and production needs.

**Current State:**
- ADR-004 specifies PostgreSQL for production
- Implementation uses SQLite for testing
- No PostgreSQL configuration for production
- Database abstraction layer supports both but defaults to SQLite

**Key Requirements:**
- Resolve ADR-004 compliance gap
- Support development workflow efficiency
- Maintain production reliability requirements
- Enable seamless testing and deployment
- Support TDD methodology with real database testing

## Decision Drivers

- **ADR Compliance**: Must resolve ADR-004 specification vs implementation gap
- **Development Efficiency**: Fast test execution and easy setup
- **Production Requirements**: ACID compliance, concurrent access, reliability
- **TDD Methodology**: Real database testing without mocks
- **Deployment Simplicity**: Easy setup across environments
- **Performance**: Sub-second query response times
- **Scalability**: Support for growing user base

## Considered Options

### Option 1: Full PostgreSQL (Production + Development + Testing)
**Description**: Use PostgreSQL for all environments including testing

### Option 2: Hybrid Strategy (PostgreSQL Production, SQLite Development/Testing)
**Description**: PostgreSQL for production, SQLite for development and testing

### Option 3: SQLite-First with PostgreSQL Migration Path
**Description**: Start with SQLite, migrate to PostgreSQL when scaling needs require it

### Option 4: Database-Agnostic with Configuration-Driven Selection
**Description**: Support both databases with environment-based configuration

## Decision Outcome

**Chosen Option**: Option 4 - Database-Agnostic with Configuration-Driven Selection

**Rationale:**
1. **Flexibility**: Supports both development efficiency and production requirements
2. **ADR Compliance**: Maintains PostgreSQL as production standard per ADR-004
3. **TDD Support**: Enables fast SQLite testing while supporting PostgreSQL integration tests
4. **Migration Path**: Smooth transition from development to production
5. **Environment Consistency**: Same codebase works across all environments

## Pros and Cons Analysis

### Option 4: Database-Agnostic with Configuration-Driven Selection

**Pros:**
- Resolves ADR-004 compliance while maintaining development efficiency
- Fast SQLite testing for TDD workflow
- PostgreSQL production deployment per original ADR-004
- Database abstraction layer already supports both
- Environment-specific configuration flexibility
- Smooth development-to-production pipeline

**Cons:**
- Slight complexity in configuration management
- Need to test against both database types
- Potential for environment-specific bugs

## Implementation Strategy

### Database Configuration Matrix
```python
# Development Environment
DATABASE_URL = "sqlite+aiosqlite:///./dev.db"

# Testing Environment  
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Production Environment
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/linguistics_db"
```

### Environment Detection Logic
```python
def get_database_config() -> DatabaseConfig:
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return PostgreSQLConfig()
    elif env == "testing":
        return SQLiteMemoryConfig()
    else:  # development
        return SQLiteFileConfig()
```

### Migration Strategy
1. **Phase 1**: Implement configuration-driven database selection
2. **Phase 2**: Add PostgreSQL production configuration
3. **Phase 3**: Create database migration scripts
4. **Phase 4**: Deploy PostgreSQL in production environment
5. **Phase 5**: Validate production performance and reliability

## Consequences

### Positive Consequences
- **ADR Compliance**: Resolves ADR-004 implementation gap
- **Development Speed**: Fast SQLite testing maintains TDD efficiency
- **Production Reliability**: PostgreSQL provides ACID compliance and scalability
- **Flexibility**: Environment-appropriate database selection
- **Testing Strategy**: Supports both unit tests (SQLite) and integration tests (PostgreSQL)

### Negative Consequences
- **Configuration Complexity**: Need to manage multiple database configurations
- **Testing Overhead**: Should test against both database types for critical features
- **Deployment Complexity**: Need PostgreSQL setup in production

### Neutral Consequences
- **Code Maintenance**: Database abstraction layer already handles differences
- **Documentation**: Need to update deployment guides for PostgreSQL setup

## Validation and Success Metrics

### Compliance Metrics
- ADR-004 compliance: 100% (PostgreSQL in production)
- Test execution time: <30 seconds for full test suite (SQLite)
- Production query performance: <200ms for 95% of queries (PostgreSQL)

### Quality Metrics
- Database abstraction layer test coverage: 100%
- Cross-database compatibility test coverage: 90%
- Production deployment success rate: 100%

## Implementation Notes

### Configuration Management
- Environment variables for database selection
- Docker Compose configurations for each environment
- Database migration scripts for PostgreSQL setup
- Health checks for both database types

### Testing Strategy
- Unit tests: SQLite in-memory for speed
- Integration tests: PostgreSQL for production compatibility
- Performance tests: Both databases for comparison
- Migration tests: SQLite to PostgreSQL data migration

### Deployment Considerations
- PostgreSQL Docker container for production
- Database initialization scripts
- Backup and recovery procedures
- Monitoring and alerting setup

## Links and References

- **Related ADRs**: ADR-004 (PostgreSQL State Management), ADR-006 (Docker Deployment)
- **Technical Documentation**: SQLAlchemy async documentation, PostgreSQL setup guides
- **Code References**: `src/linguistics_agent/database.py`, `src/linguistics_agent/config.py`

## Notes

### Future Considerations
- Database performance monitoring and optimization
- Potential migration to cloud database services (AWS RDS, Google Cloud SQL)
- Read replica setup for scaling read operations
- Database sharding strategy for large-scale deployment

### Rule Compliance
- **TDD Approach**: Test database configuration switching
- **Memory Management**: Document database selection rationale
- **Quality Standards**: Maintain database abstraction layer quality

---

**Status**: ✅ Resolves ADR-004 compliance gap
**Impact**: High - Affects all data persistence operations
**Review Date**: 2025-08-12

