"""
File: ebnf_processor.py
Path: src/linguistics_agent/tools/ebnf_processor.py
Purpose: EBNF grammar processing and validation tool
Author: AI Development Team
Created: 2024-12-07
Modified: 2024-12-07
Description: Tool for processing, validating, and analyzing EBNF grammars
Rule Compliance: rules-101 v1.2, rules-102 v1.2, rules-103 v1.2
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(str, Enum):
    """Validation strictness levels."""

    STRICT = "strict"
    MODERATE = "moderate"
    LENIENT = "lenient"


@dataclass
class ValidationResult:
    """Result of EBNF validation."""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]


class EBNFProcessor:
    """
    EBNF (Extended Backus-Naur Form) processor for grammar validation and analysis.

    This tool provides comprehensive EBNF grammar processing capabilities including:
    - Syntax validation
    - Structure analysis
    - Optimization suggestions
    - Format conversion
    """

    def __init__(self) -> None:
        """Initialize the EBNF processor."""
        self._setup_patterns()

    def _setup_patterns(self) -> None:
        """Set up regex patterns for EBNF parsing."""
        # Basic EBNF syntax patterns
        self.rule_pattern = re.compile(
            r"^([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*(.+?)\s*;?\s*$", re.MULTILINE
        )

        self.terminal_pattern = re.compile(r'"([^"]*)"')
        self.non_terminal_pattern = re.compile(r"[a-zA-Z][a-zA-Z0-9_]*")
        self.optional_pattern = re.compile(r"\[([^\[\]]*)\]")
        self.repetition_pattern = re.compile(r"\{([^\{\}]*)\}")
        self.grouping_pattern = re.compile(r"\(([^\(\)]*)\)")
        self.alternation_pattern = re.compile(r"\|")

        # Comment patterns
        self.comment_pattern = re.compile(r"//.*$|/\*.*?\*/", re.MULTILINE | re.DOTALL)

        # Invalid character patterns
        self.invalid_chars = re.compile(r'[^\w\s=\[\]\{\}\(\)\|";,\-\+\*\?\.\\]')

    def validate_grammar(
        self, grammar_text: str, level: ValidationLevel = ValidationLevel.STRICT
    ) -> str:
        """
        Validate an EBNF grammar and return validation results.

        Args:
            grammar_text: The EBNF grammar text to validate
            level: Validation strictness level

        Returns:
            String representation of validation results
        """
        try:
            result = self._perform_validation(grammar_text, level)

            if result.is_valid:
                return f"Grammar validation successful. {len(result.warnings)} warnings found."
            else:
                return f"Grammar validation failed. {len(result.errors)} errors found."

        except Exception as e:
            return f"Validation error: {str(e)}"

    def _perform_validation(
        self, grammar_text: str, level: ValidationLevel
    ) -> ValidationResult:
        """
        Perform comprehensive EBNF validation.

        Args:
            grammar_text: The EBNF grammar text to validate
            level: Validation strictness level

        Returns:
            ValidationResult with detailed analysis
        """
        errors: List[str] = []
        warnings: List[str] = []
        suggestions: List[str] = []

        # Clean the grammar text
        cleaned_text = self._clean_grammar(grammar_text)

        # Basic syntax validation
        syntax_errors = self._validate_syntax(cleaned_text)
        errors.extend(syntax_errors)

        # Rule structure validation
        structure_errors, structure_warnings = self._validate_structure(
            cleaned_text, level
        )
        errors.extend(structure_errors)
        warnings.extend(structure_warnings)

        # Semantic validation
        semantic_errors, semantic_warnings = self._validate_semantics(
            cleaned_text, level
        )
        errors.extend(semantic_errors)
        warnings.extend(semantic_warnings)

        # Generate suggestions
        suggestions = self._generate_suggestions(cleaned_text, errors, warnings)

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={
                "validation_level": level.value,
                "rule_count": len(self._extract_rules(cleaned_text)),
                "terminal_count": len(self._extract_terminals(cleaned_text)),
                "non_terminal_count": len(self._extract_non_terminals(cleaned_text)),
            },
        )

    def _clean_grammar(self, grammar_text: str) -> str:
        """Clean grammar text by removing comments and normalizing whitespace."""
        # Remove comments
        cleaned = self.comment_pattern.sub("", grammar_text)

        # Normalize whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)
        cleaned = re.sub(r"\s*=\s*", " = ", cleaned)
        cleaned = re.sub(r"\s*;\s*", ";\n", cleaned)

        return cleaned.strip()

    def _validate_syntax(self, grammar_text: str) -> List[str]:
        """Validate basic EBNF syntax."""
        errors: List[str] = []

        # Check for invalid characters
        invalid_matches = self.invalid_chars.findall(grammar_text)
        if invalid_matches:
            errors.append(f"Invalid characters found: {set(invalid_matches)}")

        # Check for balanced brackets
        bracket_errors = self._check_balanced_brackets(grammar_text)
        errors.extend(bracket_errors)

        # Check rule format
        lines = grammar_text.split("\n")
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            if "=" in line and not self.rule_pattern.match(line):
                errors.append(f"Line {i}: Invalid rule format")

        return errors

    def _check_balanced_brackets(self, text: str) -> List[str]:
        """Check for balanced brackets in the grammar."""
        errors: List[str] = []
        brackets = {"(": ")", "[": "]", "{": "}"}
        stack: List[Tuple[str, int]] = []

        for i, char in enumerate(text):
            if char in brackets:
                stack.append((char, i))
            elif char in brackets.values():
                if not stack:
                    errors.append(f"Unmatched closing bracket '{char}' at position {i}")
                else:
                    open_bracket, _ = stack.pop()
                    if brackets[open_bracket] != char:
                        errors.append(f"Mismatched brackets at position {i}")

        for bracket, pos in stack:
            errors.append(f"Unmatched opening bracket '{bracket}' at position {pos}")

        return errors

    def _validate_structure(
        self, grammar_text: str, level: ValidationLevel
    ) -> Tuple[List[str], List[str]]:
        """Validate grammar structure and organization."""
        errors: List[str] = []
        warnings: List[str] = []

        rules = self._extract_rules(grammar_text)

        if not rules:
            errors.append("No valid rules found in grammar")
            return errors, warnings

        # Check for duplicate rule definitions
        rule_names = [rule[0] for rule in rules]
        duplicates = set([name for name in rule_names if rule_names.count(name) > 1])
        if duplicates:
            errors.append(f"Duplicate rule definitions: {duplicates}")

        # Check for undefined non-terminals
        defined_rules = set(rule_names)
        used_non_terminals = self._extract_non_terminals(grammar_text)
        undefined = used_non_terminals - defined_rules

        if undefined and level in [ValidationLevel.STRICT, ValidationLevel.MODERATE]:
            if level == ValidationLevel.STRICT:
                errors.append(f"Undefined non-terminals: {undefined}")
            else:
                warnings.append(f"Undefined non-terminals: {undefined}")

        # Check for unused rules
        unused_rules = defined_rules - used_non_terminals
        if unused_rules and level == ValidationLevel.STRICT:
            warnings.append(f"Unused rules: {unused_rules}")

        return errors, warnings

    def _validate_semantics(
        self, grammar_text: str, level: ValidationLevel
    ) -> Tuple[List[str], List[str]]:
        """Validate semantic aspects of the grammar."""
        errors: List[str] = []
        warnings: List[str] = []

        # Check for left recursion
        left_recursive = self._detect_left_recursion(grammar_text)
        if left_recursive:
            if level == ValidationLevel.STRICT:
                errors.append(f"Left recursive rules detected: {left_recursive}")
            else:
                warnings.append(f"Left recursive rules detected: {left_recursive}")

        # Check for empty productions
        empty_productions = self._detect_empty_productions(grammar_text)
        if empty_productions and level == ValidationLevel.STRICT:
            warnings.append(f"Empty productions found: {empty_productions}")

        return errors, warnings

    def _extract_rules(self, grammar_text: str) -> List[Tuple[str, str]]:
        """Extract all rules from the grammar text."""
        return self.rule_pattern.findall(grammar_text)

    def _extract_terminals(self, grammar_text: str) -> set[str]:
        """Extract all terminal symbols from the grammar."""
        return set(self.terminal_pattern.findall(grammar_text))

    def _extract_non_terminals(self, grammar_text: str) -> set[str]:
        """Extract all non-terminal symbols used in the grammar."""
        # Remove terminals first
        text_without_terminals = self.terminal_pattern.sub("", grammar_text)

        # Find all non-terminals
        non_terminals = set()
        for match in self.non_terminal_pattern.finditer(text_without_terminals):
            # Skip rule names (left side of =)
            before_match = text_without_terminals[: match.start()]
            if "=" not in before_match.split("\n")[-1]:
                non_terminals.add(match.group())

        return non_terminals

    def _detect_left_recursion(self, grammar_text: str) -> List[str]:
        """Detect left recursive rules in the grammar."""
        left_recursive: List[str] = []
        rules = self._extract_rules(grammar_text)

        for rule_name, rule_body in rules:
            # Simple left recursion detection
            alternatives = rule_body.split("|")
            for alt in alternatives:
                alt = alt.strip()
                if alt.startswith(rule_name):
                    left_recursive.append(rule_name)
                    break

        return left_recursive

    def _detect_empty_productions(self, grammar_text: str) -> List[str]:
        """Detect rules with empty productions."""
        empty_productions: List[str] = []
        rules = self._extract_rules(grammar_text)

        for rule_name, rule_body in rules:
            alternatives = rule_body.split("|")
            for alt in alternatives:
                if not alt.strip() or alt.strip() == '""':
                    empty_productions.append(rule_name)
                    break

        return empty_productions

    def _generate_suggestions(
        self, grammar_text: str, errors: List[str], warnings: List[str]
    ) -> List[str]:
        """Generate optimization and improvement suggestions."""
        suggestions: List[str] = []

        if errors:
            suggestions.append("Fix syntax errors before proceeding with optimization")

        if warnings:
            suggestions.append(
                "Consider addressing warnings for better grammar quality"
            )

        # Analyze complexity
        rules = self._extract_rules(grammar_text)
        if len(rules) > 50:
            suggestions.append("Consider breaking down large grammars into modules")

        # Check for optimization opportunities
        terminals = self._extract_terminals(grammar_text)
        if len(terminals) > 100:
            suggestions.append("Consider using token classes for similar terminals")

        return suggestions

    def analyze_complexity(self, grammar_text: str) -> Dict[str, Any]:
        """
        Analyze the complexity of an EBNF grammar.

        Args:
            grammar_text: The EBNF grammar to analyze

        Returns:
            Dictionary with complexity metrics
        """
        rules = self._extract_rules(grammar_text)
        terminals = self._extract_terminals(grammar_text)
        non_terminals = self._extract_non_terminals(grammar_text)

        # Calculate complexity metrics
        rule_count = len(rules)
        terminal_count = len(terminals)
        non_terminal_count = len(non_terminals)

        # Average rule length
        avg_rule_length = sum(len(rule[1]) for rule in rules) / max(rule_count, 1)

        # Nesting depth
        max_nesting = self._calculate_max_nesting(grammar_text)

        # Complexity score (0.0 to 1.0)
        complexity_score = min(
            1.0,
            (
                rule_count * 0.01
                + terminal_count * 0.005
                + non_terminal_count * 0.01
                + avg_rule_length * 0.001
                + max_nesting * 0.1
            ),
        )

        return {
            "rule_count": rule_count,
            "terminal_count": terminal_count,
            "non_terminal_count": non_terminal_count,
            "average_rule_length": avg_rule_length,
            "max_nesting_depth": max_nesting,
            "complexity_score": complexity_score,
            "complexity_level": self._get_complexity_level(complexity_score),
        }

    def _calculate_max_nesting(self, grammar_text: str) -> int:
        """Calculate maximum nesting depth in the grammar."""
        max_depth = 0
        current_depth = 0

        for char in grammar_text:
            if char in "([{":
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in ")]}":
                current_depth = max(0, current_depth - 1)

        return max_depth

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
