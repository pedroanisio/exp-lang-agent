"""
File: __init__.py
Path: src/linguistics_agent/models/__init__.py
Purpose: Models package for request/response data structures
Author: AI Development Team
Created: 2024-12-07
Modified: 2024-12-07
Description: Pydantic models for linguistics agent data structures
Rule Compliance: rules-101 v1.2, rules-102 v1.2, rules-103 v1.2
"""

from .requests import LinguisticsQuery
from .responses import LinguisticsResponse

__all__ = ["LinguisticsQuery", "LinguisticsResponse"]

