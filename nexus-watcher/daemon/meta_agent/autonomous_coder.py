"""
Autonomous Coder - Self-improving code generation system.

This module implements an autonomous coding agent that can:
- Generate code from specifications
- Test generated code
- Iteratively improve code based on feedback
- Learn from failures and successes
"""

import ast
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .code_analyzer import CodeAnalyzer, CodeQualityLevel
from .strategies import ReasoningStrategy, ChainOfThoughtStrategy


@dataclass
class CodeGenerationTask:
    """Represents a code generation task."""
    task_id: str
    description: str
    language: str
    constraints: List[str]
    created_at: str


@dataclass
class CodeGenerationResult:
    """Result of code generation."""
    task_id: str
    code: str
    quality_score: float
    iterations: int
    reasoning_trace: List[str]
    improvements: List[str]
    success: bool
    error: Optional[str] = None


class AutonomousCoder:
    """
    Autonomous code generation and improvement system.
    """

    def __init__(self, max_iterations: int = 3):
        """
        Initialize autonomous coder.

        Args:
            max_iterations: Maximum improvement iterations
        """
        self.max_iterations = max_iterations
        self.analyzer = CodeAnalyzer()
        self.strategy = ChainOfThoughtStrategy()
        self.generation_history: List[CodeGenerationResult] = []

    async def generate_code(self, task: CodeGenerationTask) -> CodeGenerationResult:
        """
        Generate code for a given task with iterative improvement.

        Args:
            task: Code generation task

        Returns:
            CodeGenerationResult
        """
        reasoning_trace = []
        improvements = []
        current_code = ""

        for iteration in range(self.max_iterations):
            reasoning_trace.append(
                f"[Iteration {iteration + 1}] Generating code for: {task.description}"
            )

            # Generate code (simulated - in real implementation would call LLM)
            if iteration == 0:
                current_code = self._generate_initial_code(task)
                reasoning_trace.append(
                    f"[Iteration {iteration + 1}] Initial code generated"
                )
            else:
                current_code = self._improve_code(current_code, analysis, task)
                reasoning_trace.append(
                    f"[Iteration {iteration + 1}] Code improved based on analysis"
                )

            # Analyze code
            analysis = self.analyzer.analyze(current_code, task.language)
            reasoning_trace.append(
                f"[Iteration {iteration + 1}] Quality: {analysis.quality_level.value}, "
                f"Score: {analysis.score:.2f}"
            )

            # Record improvements
            if iteration > 0:
                improvements.append(
                    f"Iteration {iteration + 1}: {', '.join(analysis.suggestions[:2])}"
                )

            # Check if code is good enough
            if analysis.quality_level in [CodeQualityLevel.EXCELLENT, CodeQualityLevel.GOOD]:
                reasoning_trace.append(
                    f"[Iteration {iteration + 1}] Code quality acceptable, stopping"
                )
                break

            if iteration < self.max_iterations - 1:
                reasoning_trace.append(
                    f"[Iteration {iteration + 1}] Issues found: {len(analysis.issues)}, "
                    f"continuing improvement..."
                )

        # Test the generated code
        test_result = self._test_code(current_code, task)
        reasoning_trace.append(f"[Testing] {test_result}")

        result = CodeGenerationResult(
            task_id=task.task_id,
            code=current_code,
            quality_score=analysis.score,
            iterations=iteration + 1,
            reasoning_trace=reasoning_trace,
            improvements=improvements,
            success=analysis.score >= 0.5
        )

        self.generation_history.append(result)
        return result

    def _generate_initial_code(self, task: CodeGenerationTask) -> str:
        """Generate initial code based on task description."""
        # This is a simulation - in reality would use LLM API

        if "fibonacci" in task.description.lower():
            return '''def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example usage
print(fibonacci(10))
'''

        elif "sort" in task.description.lower():
            return '''def quicksort(arr):
    """Sort array using quicksort algorithm."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Example usage
data = [3, 6, 8, 10, 1, 2, 1]
print(quicksort(data))
'''

        elif "prime" in task.description.lower():
            return '''def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(limit):
    """Generate all prime numbers up to limit."""
    return [n for n in range(2, limit + 1) if is_prime(n)]

# Example usage
print(generate_primes(50))
'''

        elif "calculator" in task.description.lower():
            return '''class Calculator:
    """Simple calculator class."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# Example usage
calc = Calculator()
print(f"10 + 5 = {calc.add(10, 5)}")
print(f"10 - 5 = {calc.subtract(10, 5)}")
print(f"10 * 5 = {calc.multiply(10, 5)}")
print(f"10 / 5 = {calc.divide(10, 5)}")
'''

        else:
            # Generic template
            return '''def solve_problem():
    """
    Solves the given problem.

    This is a placeholder implementation that would be
    replaced with actual logic based on the specific task.
    """
    result = "Task completed successfully"
    return result

# Main execution
if __name__ == "__main__":
    output = solve_problem()
    print(f"Result: {output}")
'''

    def _improve_code(
        self,
        code: str,
        analysis: Any,
        task: CodeGenerationTask
    ) -> str:
        """Improve code based on analysis feedback."""
        # Simulated improvement - in reality would use LLM with feedback

        # Add type hints if missing
        if not analysis.metrics.get('has_type_hints'):
            code = code.replace('def fibonacci(n):', 'def fibonacci(n: int) -> int:')
            code = code.replace('def quicksort(arr):', 'def quicksort(arr: list) -> list:')
            code = code.replace('def is_prime(n):', 'def is_prime(n: int) -> bool:')
            code = code.replace('def generate_primes(limit):', 'def generate_primes(limit: int) -> list:')

        # Add error handling
        if 'try' not in code and 'calculator' in task.description.lower():
            code = code.replace(
                'def divide(self, a, b):',
                'def divide(self, a: float, b: float) -> float:'
            )

        # Improve docstrings
        code = code.replace(
            '"""Calculate the nth Fibonacci number."""',
            '"""Calculate the nth Fibonacci number using recursion.\n\n    Args:\n        n: The position in Fibonacci sequence.\n\n    Returns:\n        The nth Fibonacci number.\n    """'
        )

        return code

    def _test_code(self, code: str, task: CodeGenerationTask) -> str:
        """Test generated code."""
        try:
            # Try to parse the code
            ast.parse(code)

            # Try to execute it (in a controlled way)
            # In production, this would use sandboxing
            namespace = {}
            exec(compile(code, '<string>', 'exec'), namespace)

            return "Code executed successfully without errors"

        except SyntaxError as e:
            return f"Syntax error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return f"Runtime error: {str(e)}"

    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics."""
        if not self.generation_history:
            return {
                'total_tasks': 0,
                'success_rate': 0.0,
                'average_quality': 0.0,
                'average_iterations': 0.0
            }

        successful = [r for r in self.generation_history if r.success]

        return {
            'total_tasks': len(self.generation_history),
            'successful_tasks': len(successful),
            'success_rate': len(successful) / len(self.generation_history),
            'average_quality': sum(r.quality_score for r in self.generation_history) / len(self.generation_history),
            'average_iterations': sum(r.iterations for r in self.generation_history) / len(self.generation_history),
            'total_improvements': sum(len(r.improvements) for r in self.generation_history)
        }
