"""
Code Analysis Engine for quality assessment and improvement suggestions.
"""

import ast
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CodeQualityLevel(Enum):
    """Code quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


@dataclass
class CodeIssue:
    """Represents a code quality issue."""
    severity: str  # 'critical', 'warning', 'info'
    line: Optional[int]
    message: str
    suggestion: str


@dataclass
class CodeAnalysisResult:
    """Result of code analysis."""
    quality_level: CodeQualityLevel
    score: float  # 0.0 to 1.0
    issues: List[CodeIssue]
    metrics: Dict[str, Any]
    suggestions: List[str]


class CodeAnalyzer:
    """
    Analyzes code quality and provides improvement suggestions.
    """

    def __init__(self):
        """Initialize code analyzer."""
        self.metrics = {}

    def analyze(self, code: str, language: str = "python") -> CodeAnalysisResult:
        """
        Analyze code quality.

        Args:
            code: Source code to analyze
            language: Programming language

        Returns:
            CodeAnalysisResult
        """
        if language == "python":
            return self._analyze_python(code)
        else:
            return self._generic_analysis(code)

    def _analyze_python(self, code: str) -> CodeAnalysisResult:
        """Analyze Python code."""
        issues = []
        metrics = {
            'lines_of_code': 0,
            'num_functions': 0,
            'num_classes': 0,
            'complexity': 0,
            'has_docstrings': False,
            'has_type_hints': False,
        }

        lines = code.split('\n')
        metrics['lines_of_code'] = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

        # Try to parse the code
        try:
            tree = ast.parse(code)

            # Count functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics['num_functions'] += 1

                    # Check for docstring
                    if ast.get_docstring(node):
                        metrics['has_docstrings'] = True

                    # Check for type hints
                    if node.returns or any(arg.annotation for arg in node.args.args):
                        metrics['has_type_hints'] = True

                elif isinstance(node, ast.ClassDef):
                    metrics['num_classes'] += 1

            # Check for common issues
            if not metrics['has_docstrings'] and metrics['num_functions'] > 0:
                issues.append(CodeIssue(
                    severity='warning',
                    line=None,
                    message='Missing docstrings',
                    suggestion='Add docstrings to functions and classes for better documentation'
                ))

            if not metrics['has_type_hints'] and metrics['num_functions'] > 0:
                issues.append(CodeIssue(
                    severity='info',
                    line=None,
                    message='Missing type hints',
                    suggestion='Add type hints to improve code clarity and catch errors'
                ))

        except SyntaxError as e:
            issues.append(CodeIssue(
                severity='critical',
                line=e.lineno,
                message=f'Syntax error: {e.msg}',
                suggestion='Fix syntax errors before proceeding'
            ))

        # Check for code smells
        if metrics['lines_of_code'] > 300:
            issues.append(CodeIssue(
                severity='warning',
                line=None,
                message='File is too long',
                suggestion='Consider breaking into smaller modules'
            ))

        # Check for naming conventions
        if re.search(r'def [A-Z]', code):
            issues.append(CodeIssue(
                severity='warning',
                line=None,
                message='Function names should be lowercase',
                suggestion='Use snake_case for function names'
            ))

        # Calculate score
        score = self._calculate_score(metrics, issues)

        # Determine quality level
        if score >= 0.9:
            quality_level = CodeQualityLevel.EXCELLENT
        elif score >= 0.7:
            quality_level = CodeQualityLevel.GOOD
        elif score >= 0.5:
            quality_level = CodeQualityLevel.FAIR
        else:
            quality_level = CodeQualityLevel.POOR

        # Generate suggestions
        suggestions = self._generate_suggestions(metrics, issues)

        return CodeAnalysisResult(
            quality_level=quality_level,
            score=score,
            issues=issues,
            metrics=metrics,
            suggestions=suggestions
        )

    def _generic_analysis(self, code: str) -> CodeAnalysisResult:
        """Generic code analysis for non-Python code."""
        lines = code.split('\n')
        loc = len([l for l in lines if l.strip()])

        metrics = {
            'lines_of_code': loc,
            'has_comments': any('//' in l or '#' in l or '/*' in code for l in lines)
        }

        issues = []
        if loc > 500:
            issues.append(CodeIssue(
                severity='warning',
                line=None,
                message='File is very long',
                suggestion='Consider refactoring into smaller files'
            ))

        score = 0.7 if metrics['has_comments'] else 0.5

        return CodeAnalysisResult(
            quality_level=CodeQualityLevel.GOOD if score >= 0.7 else CodeQualityLevel.FAIR,
            score=score,
            issues=issues,
            metrics=metrics,
            suggestions=['Add more code documentation']
        )

    def _calculate_score(self, metrics: Dict[str, Any], issues: List[CodeIssue]) -> float:
        """Calculate overall code quality score."""
        score = 1.0

        # Penalize for issues
        for issue in issues:
            if issue.severity == 'critical':
                score -= 0.3
            elif issue.severity == 'warning':
                score -= 0.1
            elif issue.severity == 'info':
                score -= 0.05

        # Bonus for good practices
        if metrics.get('has_docstrings'):
            score += 0.1
        if metrics.get('has_type_hints'):
            score += 0.1

        # Ensure score is in valid range
        return max(0.0, min(1.0, score))

    def _generate_suggestions(self, metrics: Dict[str, Any], issues: List[CodeIssue]) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []

        # From issues
        for issue in issues:
            if issue.suggestion not in suggestions:
                suggestions.append(issue.suggestion)

        # General suggestions
        if metrics['lines_of_code'] < 10:
            suggestions.append('Code seems minimal - ensure all functionality is implemented')

        if metrics['num_functions'] == 0 and metrics['num_classes'] == 0:
            suggestions.append('Consider organizing code into functions or classes')

        if not suggestions:
            suggestions.append('Code looks good! Consider adding more comprehensive tests')

        return suggestions
