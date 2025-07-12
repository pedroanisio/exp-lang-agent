# ADR-007: Test-Driven Development (TDD) Methodology Implementation

## Metadata
- **Status**: Accepted
- **Date**: 2025-07-12
- **Deciders**: AI Agent, Development Team
- **Technical Story**: Cross-cutting concern for all user stories
- **Rule Compliance**: rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+

## Context and Problem Statement

The AI Linguistics Agent project requires a robust development methodology that ensures high code quality, comprehensive test coverage, and reliable functionality. Given the complexity of AI integration, database management, and multi-service architecture, we need a disciplined approach to development that catches issues early and maintains system reliability.

**Key Requirements:**
- High code quality and reliability
- Comprehensive test coverage (80%+ target)
- Early detection of integration issues
- Maintainable and refactorable codebase
- Real API integration testing (no mocks as per user requirement)
- Continuous validation of requirements compliance

## Decision Drivers

- **Quality Assurance**: Ensure high-quality, bug-free code
- **User Requirement**: Explicit request for "no mocked, non placeholder" implementation
- **Complexity Management**: Handle complex AI and database integrations
- **Maintainability**: Enable safe refactoring and feature additions
- **Rule Compliance**: Adherence to rules-101 TDD requirements
- **Continuous Integration**: Support for automated testing pipelines

## Considered Options

### Option 1: Test-Driven Development (TDD) with Real API Integration
- **Pros**:
  - Ensures comprehensive test coverage
  - Drives better design through test-first approach
  - Catches integration issues early
  - Aligns with user requirement for real API testing
  - Supports continuous refactoring
  - Enforces requirements compliance
- **Cons**:
  - Slower initial development
  - Requires API keys for testing
  - More complex test setup

### Option 2: Test-After Development with Mocks
- **Pros**:
  - Faster initial development
  - No external dependencies for testing
  - Simpler test setup
- **Cons**:
  - Contradicts user requirement for "no mocks"
  - May miss integration issues
  - Lower confidence in system reliability

### Option 3: Behavior-Driven Development (BDD)
- **Pros**:
  - Strong focus on user requirements
  - Natural language test specifications
  - Good stakeholder communication
- **Cons**:
  - Additional tooling complexity
  - Steeper learning curve
  - May not align with technical testing needs

### Option 4: Traditional Testing (Unit + Integration)
- **Pros**:
  - Familiar approach
  - Flexible testing strategy
- **Cons**:
  - No guarantee of test coverage
  - May lead to design issues
  - Less disciplined approach

## Decision Outcome

**Chosen option**: Option 1 - Test-Driven Development (TDD) with Real API Integration

**Rationale:**
1. **User Alignment**: Directly addresses user requirement for "no mocked, non placeholder"
2. **Quality Assurance**: TDD ensures high code quality and comprehensive coverage
3. **Design Benefits**: Test-first approach leads to better architecture
4. **Integration Confidence**: Real API testing provides confidence in system behavior
5. **Rule Compliance**: Fully complies with rules-101 TDD requirements
6. **Maintainability**: Enables safe refactoring and feature evolution

## Positive Consequences

- **High Quality**: Comprehensive test coverage ensures reliable code
- **Better Design**: Test-first approach drives cleaner architecture
- **Integration Confidence**: Real API testing validates actual system behavior
- **Refactoring Safety**: Comprehensive tests enable safe code changes
- **Requirements Traceability**: Tests directly validate requirements compliance
- **Continuous Validation**: Automated testing provides ongoing quality assurance

## Negative Consequences

- **Development Speed**: Initial development may be slower
- **Test Complexity**: Real API integration requires more complex test setup
- **External Dependencies**: Tests depend on external API availability
- **Cost Implications**: API usage costs for testing
- **Learning Curve**: Team needs TDD discipline and practices

## Implementation Details

### TDD Cycle Implementation
```python
# RED-GREEN-REFACTOR Cycle

# 1. RED Phase: Write failing test
def test_linguistics_agent_analyzes_text():
    """Test that agent can analyze linguistic content."""
    agent = LinguisticsAgent()
    query = LinguisticsQuery(
        text="The quick brown fox jumps over the lazy dog.",
        analysis_type="comprehensive"
    )

    # This should fail initially (RED)
    response = await agent.analyze(query)

    assert response.success is True
    assert response.analysis is not None
    assert "syntax" in response.analysis
    assert "semantics" in response.analysis

# 2. GREEN Phase: Implement minimal code to pass
class LinguisticsAgent:
    async def analyze(self, query: LinguisticsQuery) -> LinguisticsResponse:
        # Minimal implementation to make test pass
        return LinguisticsResponse(
            success=True,
            analysis={
                "syntax": "basic_syntax_analysis",
                "semantics": "basic_semantic_analysis"
            }
        )

# 3. REFACTOR Phase: Improve implementation
class LinguisticsAgent:
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.ebnf_processor = EBNFProcessor()

    async def analyze(self, query: LinguisticsQuery) -> LinguisticsResponse:
        # Enhanced implementation with real AI integration
        ai_response = await self.anthropic_client.analyze_text(query.text)

        analysis = {
            "syntax": self._extract_syntax_analysis(ai_response),
            "semantics": self._extract_semantic_analysis(ai_response),
            "grammar": self._analyze_grammar_structure(query.text)
        }

        return LinguisticsResponse(
            success=True,
            analysis=analysis,
            confidence_score=ai_response.confidence
        )
```

### Test Structure and Organization
```python
# tests/conftest.py - Test configuration
import pytest
import asyncio
from linguistics_agent.config import get_test_settings

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_settings():
    """Provide test configuration."""
    return get_test_settings()

@pytest.fixture
async def linguistics_agent(test_settings):
    """Create linguistics agent for testing."""
    agent = LinguisticsAgent(settings=test_settings)
    await agent.initialize()
    yield agent
    await agent.cleanup()

@pytest.fixture
async def test_database():
    """Create test database."""
    # Setup test database
    engine = create_test_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### Real API Integration Testing
```python
# tests/integration/test_anthropic_integration.py
import pytest
from linguistics_agent.services.anthropic_service import AnthropicService

class TestAnthropicIntegration:
    """Integration tests with real Anthropic API."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_real_api_text_analysis(self, test_settings):
        """Test real Anthropic API integration."""
        if not test_settings.ANTHROPIC_API_KEY:
            pytest.skip("Anthropic API key not provided")

        service = AnthropicService(api_key=test_settings.ANTHROPIC_API_KEY)

        response = await service.analyze_text(
            "Analyze the syntactic structure of this sentence."
        )

        assert response is not None
        assert response.content is not None
        assert len(response.content) > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_ebnf_grammar_validation(self, linguistics_agent):
        """Test EBNF grammar validation with real AI."""
        grammar = """
        expression = term { ("+" | "-") term } ;
        term = factor { ("*" | "/") factor } ;
        factor = number | "(" expression ")" ;
        number = digit { digit } ;
        digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
        """

        query = EBNFValidationQuery(grammar=grammar)
        response = await linguistics_agent.validate_ebnf(query)

        assert response.is_valid is True
        assert response.analysis is not None
        assert "rules" in response.analysis
```

### Test Categories and Markers
```python
# pytest.ini configuration
[tool:pytest]
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (real API calls)
    e2e: End-to-end tests (full system)
    slow: Slow tests (may take longer to run)
    api: Tests requiring API keys
    database: Tests requiring database

# Run different test categories
# pytest -m unit                    # Fast unit tests only
# pytest -m integration            # Integration tests with real APIs
# pytest -m "not slow"             # Skip slow tests
# pytest --cov=linguistics_agent   # With coverage report
```

### Test Data Management
```python
# tests/factories.py - Test data factories
import factory
from linguistics_agent.models import User, Project, Session

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password_hash = factory.LazyFunction(lambda: hash_password("testpass123"))
    role = "user"

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    user = factory.SubFactory(UserFactory)

# Usage in tests
@pytest.mark.asyncio
async def test_project_creation():
    user = await UserFactory.create_async()
    project = await ProjectFactory.create_async(user=user)

    assert project.user_id == user.id
    assert project.name is not None
```

### Performance Testing
```python
# tests/performance/test_api_performance.py
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

class TestAPIPerformance:
    """Performance tests for API endpoints."""

    @pytest.mark.asyncio
    @pytest.mark.performance
    async def test_concurrent_analysis_requests(self, test_client):
        """Test API performance under concurrent load."""
        async def make_request():
            start_time = time.time()
            response = await test_client.post(
                "/api/v1/analyze",
                json={"text": "Test linguistic analysis", "analysis_type": "basic"}
            )
            end_time = time.time()
            return response.status_code, end_time - start_time

        # Run 50 concurrent requests
        tasks = [make_request() for _ in range(50)]
        results = await asyncio.gather(*tasks)

        # Validate performance requirements
        response_times = [result[1] for result in results]
        avg_response_time = sum(response_times) / len(response_times)
        p95_response_time = sorted(response_times)[int(0.95 * len(response_times))]

        assert avg_response_time < 1.0  # Average < 1 second
        assert p95_response_time < 2.0  # 95th percentile < 2 seconds
        assert all(result[0] == 200 for result in results)  # All successful
```

### Test Coverage and Quality Gates
```python
# .github/workflows/test.yml - CI/CD integration
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -r requirements/test.txt

    - name: Run linting
      run: |
        ruff check src/ tests/
        black --check src/ tests/
        mypy src/

    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=linguistics_agent --cov-report=xml

    - name: Run integration tests
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        pytest tests/integration/ -v

    - name: Check coverage threshold
      run: |
        coverage report --fail-under=80

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
```

### Test Documentation and Reporting
```python
# tests/test_documentation.py
def test_all_endpoints_have_tests():
    """Ensure all API endpoints have corresponding tests."""
    from linguistics_agent.main import app

    # Get all routes from FastAPI app
    routes = [route.path for route in app.routes if hasattr(route, 'path')]

    # Check that each route has a test
    test_files = glob.glob("tests/**/test_*.py", recursive=True)

    for route in routes:
        if route.startswith("/api/"):
            # Verify test exists for this route
            test_name = f"test_{route.replace('/', '_').replace('{', '').replace('}', '')}"
            assert any(test_name in open(f).read() for f in test_files), \
                f"No test found for route: {route}"
```

## Quality Gates and Metrics

### Coverage Requirements
- **Unit Tests**: 90%+ coverage for core business logic
- **Integration Tests**: 80%+ coverage for API endpoints
- **End-to-End Tests**: 100% coverage for critical user journeys
- **Overall Coverage**: 80%+ minimum threshold

### Performance Requirements
- **Unit Tests**: <100ms per test
- **Integration Tests**: <5 seconds per test
- **API Tests**: <2 seconds response time for 95% of requests
- **Load Tests**: Support 100 concurrent users

### Quality Metrics
```python
# Quality metrics tracking
def test_code_quality_metrics():
    """Track and validate code quality metrics."""
    # Cyclomatic complexity
    assert get_average_complexity() < 10

    # Test-to-code ratio
    assert get_test_to_code_ratio() > 1.5

    # Documentation coverage
    assert get_docstring_coverage() > 80
```

## Compliance and Validation

### Rule Compliance
- **rules-101**: Full TDD implementation with RED-GREEN-REFACTOR cycle
- **rules-102**: Documented methodology with architectural rationale
- **rules-103**: Implementation follows testing best practices
- **rules-104**: Addresses quality requirements across all user stories

### TDD Process Validation
1. **RED Phase**: All new features start with failing tests
2. **GREEN Phase**: Minimal implementation to pass tests
3. **REFACTOR Phase**: Code improvement while maintaining test coverage
4. **Continuous Integration**: Automated test execution on all changes

## Related Decisions

- **ADR-002**: Anthropic API Integration (real API testing)
- **ADR-003**: FastAPI Framework Selection (API testing framework)
- **ADR-004**: PostgreSQL State Management (database testing)
- **ADR-006**: Docker Deployment (containerized testing)

## Testing Strategy Evolution

### Phase 1: Core TDD Implementation
- Unit tests for all business logic
- Integration tests for AI services
- Database integration tests

### Phase 2: Advanced Testing
- Performance and load testing
- Security testing
- End-to-end user journey tests

### Phase 3: Continuous Improvement
- Test automation optimization
- Advanced coverage analysis
- Mutation testing for test quality

## Notes

- API keys required for integration testing (provided by user)
- Consider test data management strategy for large datasets
- Monitor test execution time and optimize slow tests
- Regular review of test coverage and quality metrics

---

**Decision Status**: ✅ Accepted
**Implementation Status**: In Progress
**Next Review**: 2025-08-12 (monthly review)
**Rule Compliance**: ✅ rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+
