"""
File: __init__.py
Path: src/linguistics_agent/__init__.py
Version: 1.0.0
Created: 2025-07-12 by AI Agent
Modified: 2025-07-12 by AI Agent

Purpose: Main package initialization for AI Linguistics Agent

Dependencies: pydantic-ai, fastapi, antlr4-python3-runtime
Exports: LinguisticsAgent, GrammarAnalyzer, EBNFProcessor

Rule Compliance: rules-101 v1.1+, rules-102 v1.2+, rules-103 v1.2+
"""

from .agent import LinguisticsAgent
from .grammar.ebnf_processor import EBNFProcessor
from .grammar.antlr_integration import GrammarAnalyzer

__version__ = "1.0.0"
__author__ = "AI Agent"
__email__ = "agent@linguistics.ai"

__all__ = [
    "LinguisticsAgent",
    "GrammarAnalyzer", 
    "EBNFProcessor",
]

