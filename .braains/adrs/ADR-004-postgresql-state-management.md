# ADR-004: PostgreSQL for State Management and Session Persistence

## Metadata
- **Status**: Accepted
- **Date**: 2025-07-12
- **Deciders**: AI Agent, Database Architect
- **Technical Story**: US-004 - PostgreSQL State Management, US-006 - Session Management
- **Rule Compliance**: rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+

## Context and Problem Statement

The AI Linguistics Agent requires robust state management for user sessions, conversation history, project organization, and system configuration. We need a database solution that provides ACID compliance, excellent performance, and integrates well with our Python/FastAPI stack while supporting complex relational data models.

**Key Requirements:**
- ACID compliance for data integrity
- High-performance concurrent access for 100+ users
- Complex relational data modeling capabilities
- Session and conversation history persistence
- Project organization and user workspace management
- Integration with SQLAlchemy ORM
- Production-ready reliability and backup capabilities

## Decision Drivers

- **Data Integrity**: ACID compliance for critical user data
- **Performance**: Sub-second query response times
- **Scalability**: Support for growing user base and data volume
- **Reliability**: Production-grade availability and durability
- **Integration**: Seamless Python/SQLAlchemy integration
- **Features**: Advanced SQL features for complex queries
- **Operational**: Mature tooling for backup, monitoring, maintenance

## Considered Options

### Option 1: PostgreSQL
- **Pros**:
  - Full ACID compliance with excellent data integrity
  - Advanced SQL features (JSON, arrays, full-text search)
  - Excellent performance and scalability
  - Mature ecosystem with extensive tooling
  - Strong SQLAlchemy integration
  - JSON support for flexible schema evolution
  - Robust backup and replication capabilities
- **Cons**:
  - More complex setup than simpler databases
  - Requires PostgreSQL-specific knowledge

### Option 2: MySQL
- **Pros**:
  - Widely adopted and well-documented
  - Good performance characteristics
  - Strong community support
  - Familiar to many developers
- **Cons**:
  - Less advanced SQL features than PostgreSQL
  - Weaker JSON support
  - Some ACID compliance limitations in certain configurations

### Option 3: SQLite
- **Pros**:
  - Zero configuration and maintenance
  - Perfect for development and testing
  - Excellent performance for single-user scenarios
- **Cons**:
  - Limited concurrent access capabilities
  - No network access (file-based only)
  - Not suitable for production multi-user systems

### Option 4: MongoDB (NoSQL)
- **Pros**:
  - Flexible schema design
  - Good horizontal scaling
  - JSON-native storage
- **Cons**:
  - No ACID transactions across documents
  - Less mature Python ecosystem integration
  - Overkill for our relational data needs

## Decision Outcome

**Chosen option**: Option 1 - PostgreSQL

**Rationale:**
1. **Data Integrity**: Full ACID compliance ensures reliable state management
2. **Advanced Features**: JSON support, full-text search, and complex queries
3. **Performance**: Excellent concurrent access and query optimization
4. **Python Integration**: Outstanding SQLAlchemy support and ecosystem
5. **Production Ready**: Mature tooling for backup, monitoring, and maintenance
6. **Future-Proof**: Advanced features support evolving requirements

## Positive Consequences

- **Data Reliability**: ACID compliance ensures consistent state
- **Performance Excellence**: Optimized queries and concurrent access
- **Feature Rich**: Advanced SQL features for complex requirements
- **Operational Maturity**: Excellent tooling for production operations
- **Ecosystem Integration**: Seamless Python/SQLAlchemy integration
- **Scalability**: Proven performance at scale

## Negative Consequences

- **Complexity**: More complex setup and configuration than simpler options
- **Resource Usage**: Higher memory and CPU requirements
- **Learning Curve**: Requires PostgreSQL-specific optimization knowledge
- **Operational Overhead**: Requires database administration expertise

## Implementation Details

### Database Schema Design
```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Projects and Organization
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sessions and Conversations
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    title VARCHAR(255),
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversation Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Knowledge Base Entries
CREATE TABLE knowledge_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- 'url', 'pdf', 'text', 'file'
    source_url VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### SQLAlchemy Models
```python
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    projects = relationship("Project", back_populates="user")
    sessions = relationship("Session", back_populates="user")

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    settings = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="projects")
    sessions = relationship("Session", back_populates="project")
```

### Database Configuration
```python
# Database connection configuration
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/linguistics_agent"

# SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### Migration Management with Alembic
```python
# alembic/env.py configuration
from alembic import context
from sqlalchemy import engine_from_config, pool
from linguistics_agent.models import Base

target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

## Performance Optimization

### Indexing Strategy
```sql
-- Performance indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_project_id ON sessions(project_id);
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_knowledge_entries_source_type ON knowledge_entries(source_type);

-- Full-text search indexes
CREATE INDEX idx_knowledge_entries_content_fts ON knowledge_entries
USING gin(to_tsvector('english', content));
```

### Connection Pooling
```python
# Production connection pool configuration
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Base pool size
    max_overflow=30,       # Additional connections under load
    pool_pre_ping=True,    # Validate connections before use
    pool_recycle=3600,     # Recycle connections every hour
    echo=False             # Disable SQL logging in production
)
```

### Query Optimization
```python
# Efficient query patterns
async def get_user_sessions_with_messages(user_id: UUID) -> List[Session]:
    """Get user sessions with eager loading of messages."""
    async with async_session() as session:
        result = await session.execute(
            select(Session)
            .options(selectinload(Session.messages))
            .where(Session.user_id == user_id)
            .order_by(Session.updated_at.desc())
        )
        return result.scalars().all()
```

## Backup and Recovery Strategy

### Automated Backups
```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/linguistics_agent"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U postgres linguistics_agent > "$BACKUP_DIR/backup_$DATE.sql"

# Retention policy: keep 30 days of backups
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
```

### Point-in-Time Recovery
```bash
# Enable WAL archiving for point-in-time recovery
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/wal_archive/%f'
wal_level = replica
```

## Monitoring and Maintenance

### Performance Monitoring
```sql
-- Query performance monitoring
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Connection monitoring
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;
```

### Maintenance Tasks
```python
# Automated maintenance tasks
async def run_maintenance():
    """Run routine database maintenance."""
    async with async_session() as session:
        # Update table statistics
        await session.execute(text("ANALYZE;"))

        # Vacuum old data
        await session.execute(text("VACUUM ANALYZE messages;"))

        # Clean up old sessions (older than 90 days)
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        await session.execute(
            delete(Session).where(Session.updated_at < cutoff_date)
        )
        await session.commit()
```

## Security Considerations

### Access Control
```sql
-- Database user roles
CREATE ROLE linguistics_app_user LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE linguistics_agent TO linguistics_app_user;
GRANT USAGE ON SCHEMA public TO linguistics_app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO linguistics_app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO linguistics_app_user;
```

### Data Encryption
```python
# Connection with SSL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/linguistics_agent?ssl=require"

# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

## Compliance and Validation

### Rule Compliance
- **rules-101**: TDD approach with comprehensive database testing
- **rules-102**: Documented architectural decision with rationale
- **rules-103**: Implementation follows coding standards and patterns
- **rules-104**: Addresses US-004 and US-006 requirements completely

### Performance Requirements
- Query response time: <100ms for 95% of queries
- Concurrent users: Support 100+ simultaneous connections
- Data integrity: 100% ACID compliance
- Availability: 99.9% uptime target

### Data Requirements
- Session persistence across application restarts
- Conversation history retention (configurable)
- Project organization and user workspaces
- Audit trail for critical operations

## Testing Strategy

### Unit Testing
```python
# Database model testing
@pytest.mark.asyncio
async def test_user_creation():
    async with async_session() as session:
        user = User(username="test", email="test@example.com")
        session.add(user)
        await session.commit()
        assert user.id is not None
```

### Integration Testing
```python
# Database integration testing
@pytest.mark.asyncio
async def test_session_with_messages():
    # Test complete session workflow
    user = await create_test_user()
    session = await create_test_session(user.id)
    message = await create_test_message(session.id)

    # Verify relationships
    loaded_session = await get_session_with_messages(session.id)
    assert len(loaded_session.messages) == 1
```

## Related Decisions

- **ADR-001**: Knowledge Database Architecture (complementary data storage)
- **ADR-003**: FastAPI Framework Selection (database integration layer)
- **ADR-005**: Authentication Strategy (user management)
- **ADR-007**: Docker Deployment (database containerization)

## Migration Strategy

If migration from PostgreSQL becomes necessary:
1. **Schema Export**: Export complete schema and data
2. **Data Transformation**: Convert data to target database format
3. **Application Updates**: Update SQLAlchemy models and queries
4. **Testing Validation**: Comprehensive testing of migrated system
5. **Gradual Cutover**: Phased migration with rollback capability

## Notes

- Consider PostgreSQL version upgrades and compatibility
- Monitor query performance and optimize as needed
- Evaluate partitioning strategies for large tables
- Plan for read replicas if read scalability becomes an issue

---

**Decision Status**: ✅ Accepted
**Implementation Status**: Ready for Development
**Next Review**: 2025-08-12 (monthly review)
**Rule Compliance**: ✅ rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+
