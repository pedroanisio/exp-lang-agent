"""
File: grammar_analyzer.py
Path: src/linguistics_agent/tools/grammar_analyzer.py
Purpose: Grammar structure analysis and optimization tool
Author: AI Development Team
Created: 2024-12-07
Modified: 2024-12-07
Description: Tool for analyzing grammar structures, patterns, and optimization opportunities
Rule Compliance: rules-101 v1.2, rules-102 v1.2, rules-103 v1.2
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, Counter


class AnalysisDepth(str, Enum):
    """Analysis depth levels."""

    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"


@dataclass
class GrammarPattern:
    """Represents a detected grammar pattern."""

    pattern_type: str
    description: str
    occurrences: int
    examples: List[str]
    optimization_potential: float


@dataclass
class AnalysisResult:
    """Result of grammar analysis."""

    structure_metrics: Dict[str, Any]
    patterns: List[GrammarPattern]
    optimization_suggestions: List[str]
    complexity_analysis: Dict[str, Any]
    metadata: Dict[str, Any]


class GrammarAnalyzer:
    """
    Grammar structure analyzer for linguistic and formal grammar analysis.

    This tool provides comprehensive grammar analysis capabilities including:
    - Structural pattern detection
    - Complexity analysis
    - Optimization suggestions
    - Performance predictions
    """

    def __init__(self) -> None:
        """Initialize the grammar analyzer."""
        self._setup_patterns()

    def _setup_patterns(self) -> None:
        """Set up pattern recognition for grammar analysis."""
        # Common grammar patterns
        self.pattern_definitions = {
            "left_recursion": {
                "regex": r"^(\w+)\s*=\s*\1",
                "description": "Left recursive rule",
                "optimization_impact": 0.8,
            },
            "right_recursion": {
                "regex": r"(\w+)\s*$",
                "description": "Right recursive rule",
                "optimization_impact": 0.3,
            },
            "optional_groups": {
                "regex": r"\[([^\[\]]*)\]",
                "description": "Optional elements",
                "optimization_impact": 0.2,
            },
            "repetition_groups": {
                "regex": r"\{([^\{\}]*)\}",
                "description": "Repetition elements",
                "optimization_impact": 0.4,
            },
            "alternation": {
                "regex": r"\|",
                "description": "Choice alternatives",
                "optimization_impact": 0.3,
            },
            "nested_groups": {
                "regex": r"\(([^\(\)]*\([^\(\)]*\)[^\(\)]*)\)",
                "description": "Nested grouping",
                "optimization_impact": 0.6,
            },
        }

        # Rule extraction patterns
        self.rule_pattern = re.compile(
            r"^([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*(.+?)\s*;?\s*$", re.MULTILINE
        )

        self.terminal_pattern = re.compile(r'"([^"]*)"')
        self.non_terminal_pattern = re.compile(r"[a-zA-Z][a-zA-Z0-9_]*")

    def analyze_structure(
        self, grammar_text: str, depth: AnalysisDepth = AnalysisDepth.COMPREHENSIVE
    ) -> str:
        """
        Analyze grammar structure and return analysis results.

        Args:
            grammar_text: The grammar text to analyze
            depth: Analysis depth level

        Returns:
            String representation of analysis results
        """
        try:
            result = self._perform_analysis(grammar_text, depth)

            complexity = result.complexity_analysis.get("complexity_score", 0.0)
            pattern_count = len(result.patterns)
            suggestion_count = len(result.optimization_suggestions)

            return (
                f"Grammar analysis completed. "
                f"Complexity: {complexity:.2f}, "
                f"Patterns: {pattern_count}, "
                f"Suggestions: {suggestion_count}"
            )

        except Exception as e:
            return f"Analysis error: {str(e)}"

    def _perform_analysis(
        self, grammar_text: str, depth: AnalysisDepth
    ) -> AnalysisResult:
        """
        Perform comprehensive grammar analysis.

        Args:
            grammar_text: The grammar text to analyze
            depth: Analysis depth level

        Returns:
            AnalysisResult with detailed analysis
        """
        # Clean the grammar text
        cleaned_text = self._clean_grammar(grammar_text)

        # Extract basic structure
        structure_metrics = self._analyze_structure_metrics(cleaned_text)

        # Detect patterns
        patterns = self._detect_patterns(cleaned_text, depth)

        # Analyze complexity
        complexity_analysis = self._analyze_complexity(cleaned_text, patterns)

        # Generate optimization suggestions
        optimization_suggestions = self._generate_optimization_suggestions(
            cleaned_text, patterns, complexity_analysis
        )

        return AnalysisResult(
            structure_metrics=structure_metrics,
            patterns=patterns,
            optimization_suggestions=optimization_suggestions,
            complexity_analysis=complexity_analysis,
            metadata={
                "analysis_depth": depth.value,
                "grammar_length": len(cleaned_text),
                "analysis_timestamp": "2024-12-07T00:00:00Z",  # Simplified for testing
            },
        )

    def _clean_grammar(self, grammar_text: str) -> str:
        """Clean and normalize grammar text."""
        # Remove comments
        cleaned = re.sub(
            r"//.*$|/\*.*?\*/", "", grammar_text, flags=re.MULTILINE | re.DOTALL
        )

        # Normalize whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)
        cleaned = re.sub(r"\s*=\s*", " = ", cleaned)

        return cleaned.strip()

    def _analyze_structure_metrics(self, grammar_text: str) -> Dict[str, Any]:
        """Analyze basic structural metrics of the grammar."""
        rules = self.rule_pattern.findall(grammar_text)
        terminals = set(self.terminal_pattern.findall(grammar_text))

        # Extract non-terminals
        non_terminals = set()
        for rule_name, rule_body in rules:
            # Add rule name
            non_terminals.add(rule_name)
            # Find non-terminals in rule body
            text_without_terminals = self.terminal_pattern.sub("", rule_body)
            for match in self.non_terminal_pattern.finditer(text_without_terminals):
                non_terminals.add(match.group())

        # Calculate metrics
        rule_count = len(rules)
        terminal_count = len(terminals)
        non_terminal_count = len(non_terminals)

        # Rule length statistics
        rule_lengths = [len(rule[1]) for rule in rules]
        avg_rule_length = sum(rule_lengths) / max(rule_count, 1)
        max_rule_length = max(rule_lengths) if rule_lengths else 0

        # Branching factor (average alternatives per rule)
        total_alternatives = sum(rule[1].count("|") + 1 for rule in rules)
        avg_branching_factor = total_alternatives / max(rule_count, 1)

        return {
            "rule_count": rule_count,
            "terminal_count": terminal_count,
            "non_terminal_count": non_terminal_count,
            "average_rule_length": avg_rule_length,
            "max_rule_length": max_rule_length,
            "average_branching_factor": avg_branching_factor,
            "grammar_size": len(grammar_text),
            "rule_density": rule_count
            / max(len(grammar_text), 1)
            * 1000,  # Rules per 1000 chars
        }

    def _detect_patterns(
        self, grammar_text: str, depth: AnalysisDepth
    ) -> List[GrammarPattern]:
        """Detect structural patterns in the grammar."""
        patterns: List[GrammarPattern] = []

        for pattern_name, pattern_def in self.pattern_definitions.items():
            if (
                depth == AnalysisDepth.BASIC
                and pattern_def["optimization_impact"] < 0.5
            ):
                continue

            regex = pattern_def["regex"]
            matches = re.findall(regex, grammar_text, re.MULTILINE)

            if matches:
                examples = (
                    matches[:5]
                    if isinstance(matches[0], str)
                    else [str(m) for m in matches[:5]]
                )

                pattern = GrammarPattern(
                    pattern_type=pattern_name,
                    description=pattern_def["description"],
                    occurrences=len(matches),
                    examples=examples,
                    optimization_potential=pattern_def["optimization_impact"],
                )
                patterns.append(pattern)

        # Advanced pattern detection for detailed/comprehensive analysis
        if depth in [AnalysisDepth.DETAILED, AnalysisDepth.COMPREHENSIVE]:
            patterns.extend(self._detect_advanced_patterns(grammar_text))

        return patterns

    def _detect_advanced_patterns(self, grammar_text: str) -> List[GrammarPattern]:
        """Detect advanced structural patterns."""
        patterns: List[GrammarPattern] = []

        # Detect common sub-expressions
        subexpressions = self._find_common_subexpressions(grammar_text)
        if subexpressions:
            patterns.append(
                GrammarPattern(
                    pattern_type="common_subexpressions",
                    description="Repeated sub-expressions that could be factored",
                    occurrences=len(subexpressions),
                    examples=list(subexpressions.keys())[:5],
                    optimization_potential=0.7,
                )
            )

        # Detect deep nesting
        max_nesting = self._calculate_max_nesting(grammar_text)
        if max_nesting > 5:
            patterns.append(
                GrammarPattern(
                    pattern_type="deep_nesting",
                    description=f"Deep nesting detected (depth: {max_nesting})",
                    occurrences=1,
                    examples=[f"Maximum nesting depth: {max_nesting}"],
                    optimization_potential=0.6,
                )
            )

        # Detect potential ambiguities
        ambiguities = self._detect_potential_ambiguities(grammar_text)
        if ambiguities:
            patterns.append(
                GrammarPattern(
                    pattern_type="potential_ambiguities",
                    description="Rules that may cause parsing ambiguities",
                    occurrences=len(ambiguities),
                    examples=ambiguities[:5],
                    optimization_potential=0.9,
                )
            )

        return patterns

    def _find_common_subexpressions(self, grammar_text: str) -> Dict[str, int]:
        """Find commonly repeated sub-expressions."""
        # Extract all sub-expressions (simplified)
        subexpressions = Counter()

        # Look for patterns in parentheses, brackets, and braces
        for pattern in [r"\(([^\(\)]+)\)", r"\[([^\[\]]+)\]", r"\{([^\{\}]+)\}"]:
            matches = re.findall(pattern, grammar_text)
            for match in matches:
                if len(match) > 5:  # Only consider substantial sub-expressions
                    subexpressions[match] += 1

        # Return only sub-expressions that appear multiple times
        return {expr: count for expr, count in subexpressions.items() if count > 1}

    def _calculate_max_nesting(self, grammar_text: str) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0
        current_depth = 0

        for char in grammar_text:
            if char in "([{":
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in ")]}":
                current_depth = max(0, current_depth - 1)

        return max_depth

    def _detect_potential_ambiguities(self, grammar_text: str) -> List[str]:
        """Detect rules that may cause parsing ambiguities."""
        ambiguities: List[str] = []
        rules = self.rule_pattern.findall(grammar_text)

        # Simple ambiguity detection: rules with similar prefixes
        rule_bodies = {name: body for name, body in rules}

        for rule_name, rule_body in rules:
            alternatives = [alt.strip() for alt in rule_body.split("|")]

            # Check for alternatives with common prefixes
            for i, alt1 in enumerate(alternatives):
                for alt2 in alternatives[i + 1 :]:
                    if self._have_common_prefix(alt1, alt2):
                        ambiguities.append(f"{rule_name}: '{alt1}' vs '{alt2}'")

        return ambiguities

    def _have_common_prefix(self, alt1: str, alt2: str, min_length: int = 3) -> bool:
        """Check if two alternatives have a significant common prefix."""
        words1 = alt1.split()
        words2 = alt2.split()

        common_length = 0
        for w1, w2 in zip(words1, words2):
            if w1 == w2:
                common_length += len(w1)
            else:
                break

        return common_length >= min_length

    def _analyze_complexity(
        self, grammar_text: str, patterns: List[GrammarPattern]
    ) -> Dict[str, Any]:
        """Analyze grammar complexity based on structure and patterns."""
        rules = self.rule_pattern.findall(grammar_text)

        # Base complexity from structure
        rule_count = len(rules)
        avg_rule_length = sum(len(rule[1]) for rule in rules) / max(rule_count, 1)
        max_nesting = self._calculate_max_nesting(grammar_text)

        # Pattern-based complexity
        pattern_complexity = sum(
            pattern.occurrences * pattern.optimization_potential for pattern in patterns
        ) / max(len(patterns), 1)

        # Calculate overall complexity score (0.0 to 1.0)
        complexity_score = min(
            1.0,
            (
                rule_count * 0.01
                + avg_rule_length * 0.001
                + max_nesting * 0.1
                + pattern_complexity * 0.2
            ),
        )

        return {
            "complexity_score": complexity_score,
            "complexity_level": self._get_complexity_level(complexity_score),
            "rule_complexity": rule_count * 0.01,
            "structural_complexity": max_nesting * 0.1,
            "pattern_complexity": pattern_complexity,
            "maintainability_score": max(0.0, 1.0 - complexity_score),
            "performance_prediction": self._predict_performance(complexity_score),
        }

    def _get_complexity_level(self, score: float) -> str:
        """Get human-readable complexity level."""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Medium"
        elif score < 0.8:
            return "High"
        else:
            return "Very High"

    def _predict_performance(self, complexity_score: float) -> str:
        """Predict parsing performance based on complexity."""
        if complexity_score < 0.3:
            return "Excellent"
        elif complexity_score < 0.5:
            return "Good"
        elif complexity_score < 0.7:
            return "Fair"
        else:
            return "Poor"

    def _generate_optimization_suggestions(
        self,
        grammar_text: str,
        patterns: List[GrammarPattern],
        complexity_analysis: Dict[str, Any],
    ) -> List[str]:
        """Generate optimization suggestions based on analysis."""
        suggestions: List[str] = []

        # Complexity-based suggestions
        complexity_score = complexity_analysis.get("complexity_score", 0.0)
        if complexity_score > 0.7:
            suggestions.append(
                "Consider breaking down complex rules into simpler components"
            )

        # Pattern-based suggestions
        for pattern in patterns:
            if pattern.optimization_potential > 0.6:
                if pattern.pattern_type == "left_recursion":
                    suggestions.append(
                        "Eliminate left recursion to improve parsing performance"
                    )
                elif pattern.pattern_type == "common_subexpressions":
                    suggestions.append(
                        "Factor out common sub-expressions into separate rules"
                    )
                elif pattern.pattern_type == "deep_nesting":
                    suggestions.append(
                        "Reduce nesting depth to improve readability and performance"
                    )
                elif pattern.pattern_type == "potential_ambiguities":
                    suggestions.append("Resolve potential parsing ambiguities")

        # Structure-based suggestions
        rules = self.rule_pattern.findall(grammar_text)
        if len(rules) > 100:
            suggestions.append("Consider modularizing large grammars")

        # Performance suggestions
        performance = complexity_analysis.get("performance_prediction", "")
        if performance in ["Fair", "Poor"]:
            suggestions.append(
                "Optimize grammar structure for better parsing performance"
            )

        return suggestions

    def get_optimization_report(self, grammar_text: str) -> Dict[str, Any]:
        """
        Generate a comprehensive optimization report.

        Args:
            grammar_text: The grammar text to analyze

        Returns:
            Dictionary with optimization recommendations
        """
        analysis = self._perform_analysis(grammar_text, AnalysisDepth.COMPREHENSIVE)

        return {
            "summary": {
                "complexity_level": analysis.complexity_analysis.get(
                    "complexity_level", "Unknown"
                ),
                "performance_prediction": analysis.complexity_analysis.get(
                    "performance_prediction", "Unknown"
                ),
                "optimization_priority": self._calculate_optimization_priority(
                    analysis
                ),
            },
            "metrics": analysis.structure_metrics,
            "patterns": [
                {
                    "type": p.pattern_type,
                    "description": p.description,
                    "count": p.occurrences,
                    "impact": p.optimization_potential,
                }
                for p in analysis.patterns
            ],
            "suggestions": analysis.optimization_suggestions,
            "complexity": analysis.complexity_analysis,
        }

    def _calculate_optimization_priority(self, analysis: AnalysisResult) -> str:
        """Calculate optimization priority based on analysis results."""
        complexity_score = analysis.complexity_analysis.get("complexity_score", 0.0)
        high_impact_patterns = sum(
            1 for p in analysis.patterns if p.optimization_potential > 0.7
        )

        if complexity_score > 0.8 or high_impact_patterns > 3:
            return "High"
        elif complexity_score > 0.5 or high_impact_patterns > 1:
            return "Medium"
        else:
            return "Low"
