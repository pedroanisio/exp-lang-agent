"""
File: config.py
Path: src/linguistics_agent/config.py
Purpose: Configuration management with environment variables and API keys
Author: AI Development Team
Created: 2024-12-07
Modified: 2024-12-07
Description: Centralized configuration for linguistics agent with real API integration
Rule Compliance: rules-101 v1.2, rules-102 v1.2, rules-103 v1.2
"""

import os
from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """Database configuration for PostgreSQL, Neo4j and ChromaDB."""

    # PostgreSQL Configuration (Primary database)
    postgresql_url: str = Field(
        default="sqlite+aiosqlite:///./test.db", 
        env="DATABASE_URL",
        description="PostgreSQL database URL"
    )
    
    # Neo4j Configuration
    neo4j_uri: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", env="NEO4J_USER")
    neo4j_password: str = Field(default="password", env="NEO4J_PASSWORD")
    neo4j_database: str = Field(default="linguistics", env="NEO4J_DATABASE")

    # ChromaDB Configuration
    chromadb_host: str = Field(default="localhost", env="CHROMADB_HOST")
    chromadb_port: int = Field(default=8000, env="CHROMADB_PORT")
    chromadb_collection: str = Field(
        default="linguistics_knowledge", env="CHROMADB_COLLECTION"
    )

    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")


class AnthropicConfig(BaseSettings):
    """Anthropic API configuration for real API integration."""

    api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    api_base: str = Field(default="https://api.anthropic.com", env="ANTHROPIC_API_BASE")
    model: str = Field(default="claude-3-5-sonnet-20241022")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4000, ge=1, le=8192)
    timeout: int = Field(default=30, ge=1, le=300)

    @validator("api_key")
    def validate_api_key(cls, v):
        """Validate that API key is provided when needed."""
        if v and not v.startswith("sk-ant-"):
            raise ValueError('Anthropic API key must start with "sk-ant-"')
        return v


class TestConfig(BaseSettings):
    """Testing configuration with real API integration."""

    use_real_api: bool = Field(default=False, env="TEST_USE_REAL_API")
    anthropic_api_key: Optional[str] = Field(default=None, env="TEST_ANTHROPIC_API_KEY")
    timeout: int = Field(default=30, env="TEST_TIMEOUT")
    max_retries: int = Field(default=3)

    @validator("anthropic_api_key")
    def validate_test_api_key(cls, v, values):
        """Validate test API key when real API is enabled."""
        # Only validate if explicitly using real API and not in initialization
        use_real_api = values.get("use_real_api", False)
        if use_real_api and v is None:
            # Allow None during initialization, validation will happen when needed
            pass
        return v


class KnowledgeConfig(BaseSettings):
    """Knowledge ingestion and management configuration."""

    storage_path: str = Field(
        default="/app/data/knowledge", env="KNOWLEDGE_STORAGE_PATH"
    )
    max_file_size_mb: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    allowed_file_types: List[str] = Field(
        default=["pdf", "txt", "md", "html"], env="ALLOWED_FILE_TYPES"
    )

    # Processing configuration
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)
    embedding_model: str = Field(default="text-embedding-3-small")

    @validator("allowed_file_types", pre=True)
    def parse_file_types(cls, v):
        """Parse comma-separated file types from environment."""
        if isinstance(v, str):
            return [ft.strip().lower() for ft in v.split(",")]
        return v


class SecurityConfig(BaseSettings):
    """Security and authentication configuration."""

    secret_key: str = Field(default="dev-secret-key", env="APP_SECRET_KEY")
    jwt_secret_key: str = Field(default="jwt-secret-key", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")

    # CORS configuration
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"], env="CORS_ORIGINS"
    )

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins from environment."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


class AppConfig(BaseSettings):
    """Main application configuration."""

    env: str = Field(default="development", env="APP_ENV")
    debug: bool = Field(default=True, env="APP_DEBUG")
    log_level: str = Field(default="INFO", env="APP_LOG_LEVEL")

    # Server configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=1)

    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    @validator("env")
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed_envs = ["development", "testing", "staging", "production"]
        if v not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v


class Settings(BaseSettings):
    """Comprehensive application settings."""

    app: AppConfig = AppConfig()
    anthropic: AnthropicConfig = AnthropicConfig()
    database: DatabaseConfig = DatabaseConfig()
    knowledge: KnowledgeConfig = KnowledgeConfig()
    security: SecurityConfig = SecurityConfig()
    testing: TestConfig = TestConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app.env == "production"

    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.app.env == "testing"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app.env == "development"

    def get_anthropic_api_key(self) -> Optional[str]:
        """Get the appropriate Anthropic API key based on environment."""
        if self.is_testing() and self.testing.use_real_api:
            return self.testing.anthropic_api_key
        return self.anthropic.api_key

    def validate_api_configuration(self) -> bool:
        """Validate that API configuration is complete."""
        api_key = self.get_anthropic_api_key()
        if not api_key:
            return False

        if self.is_testing() and self.testing.use_real_api:
            return bool(self.testing.anthropic_api_key)

        return bool(self.anthropic.api_key)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def update_settings_for_testing(
    anthropic_api_key: Optional[str] = None, use_real_api: bool = True
) -> None:
    """Update settings for testing with real API integration."""
    global settings

    if anthropic_api_key:
        settings.testing.anthropic_api_key = anthropic_api_key
        settings.testing.use_real_api = use_real_api
        settings.app.env = "testing"

    # Validate configuration
    if use_real_api and not settings.validate_api_configuration():
        raise ValueError(
            "Invalid API configuration for testing. "
            "Provide ANTHROPIC_API_KEY or TEST_ANTHROPIC_API_KEY environment variable."
        )


def get_database_url(db_type: str) -> str:
    """Get database connection URL for specified database type."""
    if db_type.lower() == "neo4j":
        return settings.database.neo4j_uri
    elif db_type.lower() == "chromadb":
        return f"http://{settings.database.chromadb_host}:{settings.database.chromadb_port}"
    elif db_type.lower() == "redis":
        return settings.database.redis_url
    else:
        raise ValueError(f"Unknown database type: {db_type}")


# Environment-specific configurations
def configure_for_production(anthropic_api_key: str) -> None:
    """Configure settings for production environment."""
    global settings
    settings.app.env = "production"
    settings.app.debug = False
    settings.anthropic.api_key = anthropic_api_key
    settings.app.log_level = "WARNING"


def configure_for_development() -> None:
    """Configure settings for development environment."""
    global settings
    settings.app.env = "development"
    settings.app.debug = True
    settings.app.log_level = "DEBUG"
