"""
File: test_linguistics_agent.py
Path: tests/unit/test_linguistics_agent.py
Version: 1.0.0
Created: 2025-07-12 by AI Agent
Modified: 2025-07-12 by AI Agent

Purpose: Unit tests for core linguistics agent functionality following TDD principles

Dependencies: pytest, pytest-asyncio, pydantic
Exports: TestLinguisticsAgent test class

Rule Compliance: rules-101 v1.1+, rules-102 v1.2+, rules-103 v1.2+
"""

import pytest
from typing import Dict, List, Any
from unittest.mock import Mock, patch, AsyncMock

# Import the actual classes
from linguistics_agent.agent import LinguisticsAgent
from linguistics_agent.models.requests import LinguisticsQuery
from linguistics_agent.models.responses import LinguisticsResponse


class TestLinguisticsAgent:
    """Test suite for linguistics agent core functionality."""

    @pytest.fixture
    def sample_query(self) -> Dict[str, Any]:
        """Sample linguistics query for testing.

        Returns:
            Dict containing sample query data for testing
        """
        return {
            "text": "The quick brown fox jumps over the lazy dog",
            "analysis_type": "syntactic",
            "context": {"language": "english"},
        }

    @pytest.fixture
    def sample_ebnf_grammar(self) -> str:
        """Sample EBNF grammar for testing.

        Returns:
            String containing valid EBNF grammar definition
        """
        return """
        digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
        number = digit, { digit } ;
        expression = number, [ ( "+" | "-" ), number ] ;
        """

    async def test_agent_initialization(self) -> None:
        """Test that linguistics agent initializes correctly.

        GIVEN: No existing agent instance
        WHEN: LinguisticsAgent is instantiated
        THEN: Agent should be properly configured with Anthropic model
        """
        # This test will fail initially - RED phase
        agent = LinguisticsAgent()

        assert agent is not None
        assert hasattr(agent, "model")
        assert hasattr(agent, "system_prompt")
        assert "anthropic" in str(agent.model).lower()

    async def test_agent_response_structure(self, sample_query: Dict[str, Any]) -> None:
        """Test that agent returns properly structured response.

        GIVEN: A valid linguistics query
        WHEN: Agent processes the query
        THEN: Response should have required structure and types
        """
        # This test will fail initially - RED phase
        agent = LinguisticsAgent()

        with patch("linguistics_agent.agent.get_dependencies") as mock_deps:
            mock_deps.return_value = Mock()

            result = await agent.run(sample_query["text"])

            # Validate response structure
            assert hasattr(result.output, "analysis_results")
            assert hasattr(result.output, "grammar_insights")
            assert hasattr(result.output, "recommendations")
            assert hasattr(result.output, "confidence_score")

            # Validate data types
            assert isinstance(result.output.analysis_results, dict)
            assert isinstance(result.output.grammar_insights, list)
            assert isinstance(result.output.recommendations, list)
            assert isinstance(result.output.confidence_score, float)
            assert 0.0 <= result.output.confidence_score <= 1.0

    async def test_ebnf_processing_tool(self, sample_ebnf_grammar: str) -> None:
        """Test EBNF grammar processing tool.

        GIVEN: A valid EBNF grammar string
        WHEN: Agent processes the grammar using EBNF tool
        THEN: Should return structured grammar analysis
        """
        # This test will fail initially - RED phase
        agent = LinguisticsAgent()

        with patch("linguistics_agent.agent.get_dependencies") as mock_deps:
            mock_deps.return_value = Mock()

            result = await agent.run_tool(
                "process_ebnf", ebnf_content=sample_ebnf_grammar
            )

            assert "syntax_tree" in result
            assert "grammar_type" in result
            assert "complexity_score" in result
            assert "optimization_suggestions" in result

            # Validate types
            assert isinstance(result["syntax_tree"], dict)
            assert isinstance(result["grammar_type"], str)
            assert isinstance(result["complexity_score"], (int, float))
            assert isinstance(result["optimization_suggestions"], list)

    async def test_grammar_analysis_tool(self) -> None:
        """Test grammar analysis tool functionality.

        GIVEN: A text sample for grammatical analysis
        WHEN: Agent analyzes the grammar structure
        THEN: Should return detailed grammatical insights
        """
        # This test will fail initially - RED phase
        agent = LinguisticsAgent()
        sample_text = "The student reads the book carefully."

        with patch("linguistics_agent.agent.get_dependencies") as mock_deps:
            mock_deps.return_value = Mock()

            result = await agent.run_tool("analyze_grammar", grammar_text=sample_text)

            assert "parse_tree" in result
            assert "pos_tags" in result
            assert "syntactic_structure" in result
            assert "linguistic_features" in result

            # Validate structure
            assert isinstance(result["parse_tree"], dict)
            assert isinstance(result["pos_tags"], list)
            assert isinstance(result["syntactic_structure"], dict)
            assert isinstance(result["linguistic_features"], list)

    async def test_agent_error_handling(self) -> None:
        """Test agent error handling for invalid inputs.

        GIVEN: Invalid or malformed input
        WHEN: Agent processes the input
        THEN: Should handle errors gracefully and return meaningful messages
        """
        # This test will fail initially - RED phase
        agent = LinguisticsAgent()

        with patch("linguistics_agent.agent.get_dependencies") as mock_deps:
            mock_deps.return_value = Mock()

            # Test empty input
            with pytest.raises(ValueError, match="Input text cannot be empty"):
                await agent.run("")

            # Test invalid analysis type
            invalid_query = {
                "text": "Valid text",
                "analysis_type": "invalid_type",
                "context": {},
            }

            result = await agent.run(invalid_query["text"])
            assert (
                result.output.confidence_score < 0.5
            )  # Low confidence for invalid input

    async def test_agent_context_preservation(
        self, sample_query: Dict[str, Any]
    ) -> None:
        """Test that agent preserves context across interactions.

        GIVEN: Multiple sequential queries
        WHEN: Agent processes queries in sequence
        THEN: Should maintain context and improve responses
        """
        # This test will fail initially - RED phase
        agent = LinguisticsAgent()

        with patch("linguistics_agent.agent.get_dependencies") as mock_deps:
            mock_deps.return_value = Mock()

            # First query
            result1 = await agent.run("Analyze this sentence structure.")

            # Second related query
            result2 = await agent.run("What about the previous sentence's complexity?")

            # Should reference previous analysis
            assert result2.output.confidence_score > 0.5
            assert len(result2.output.analysis_results) > 0

    def test_agent_configuration_validation(self) -> None:
        """Test agent configuration validation.

        GIVEN: Agent configuration parameters
        WHEN: Agent is initialized with configuration
        THEN: Should validate configuration and set appropriate defaults
        """
        # This test will fail initially - RED phase
        config = {
            "model": "anthropic:claude-3-5-sonnet",
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        agent = LinguisticsAgent(config=config)

        assert agent.config["model"] == "anthropic:claude-3-5-sonnet"
        assert agent.config["temperature"] == 0.7
        assert agent.config["max_tokens"] == 2000

        # Test invalid configuration
        with pytest.raises(ValueError, match="Invalid model configuration"):
            LinguisticsAgent(config={"model": "invalid_model"})


class TestLinguisticsModels:
    """Test suite for Pydantic models used by the agent."""

    def test_linguistics_query_validation(self) -> None:
        """Test LinguisticsQuery model validation.

        GIVEN: Query data with various formats
        WHEN: LinguisticsQuery model validates the data
        THEN: Should accept valid data and reject invalid data
        """
        # This test will fail initially - RED phase
        from linguistics_agent.models.requests import LinguisticsQuery

        # Valid query
        valid_data = {
            "text": "Sample text for analysis",
            "query_type": "general",
            "context": {"language": "english"},
        }

        query = LinguisticsQuery(**valid_data)
        assert query.text == "Sample text for analysis"
        assert query.query_type == "general"
        assert query.context["language"] == "english"

        # Invalid query - empty text
        with pytest.raises(ValueError):
            LinguisticsQuery(text="", query_type="general")

    def test_linguistics_response_validation(self) -> None:
        """Test LinguisticsResponse model validation.

        GIVEN: Response data from agent
        WHEN: LinguisticsResponse model validates the data
        THEN: Should ensure proper structure and types
        """
        # This test will fail initially - RED phase
        from linguistics_agent.models.responses import LinguisticsResponse

        valid_response_data = {
            "content": "Analysis completed successfully",
            "confidence": 0.85,
            "sources": [],
            "tools_used": [],
            "context_preserved": True,
        }

        response = LinguisticsResponse(**valid_response_data)
        assert response.content == "Analysis completed successfully"
        assert response.confidence == 0.85
        assert isinstance(response.sources, list)
        assert isinstance(response.tools_used, list)
        assert response.context_preserved is True

        # Invalid confidence score
        with pytest.raises(
            ValueError, match="Confidence score must be between 0 and 1"
        ):
            LinguisticsResponse(
                analysis_results={},
                grammar_insights=[],
                recommendations=[],
                confidence_score=1.5,
            )
