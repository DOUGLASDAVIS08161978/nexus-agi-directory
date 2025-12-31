"""
Meta-Agent Orchestrator - Coordinates multiple AI agents and reasoning strategies.

This is the central intelligence that:
- Orchestrates multiple reasoning strategies
- Coordinates autonomous coders
- Manages task distribution
- Synthesizes results from multiple approaches
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from .strategies import (
    ReasoningStrategy,
    ChainOfThoughtStrategy,
    TreeOfThoughtStrategy,
    ReflexionStrategy,
    EnsembleStrategy
)
from .autonomous_coder import AutonomousCoder, CodeGenerationTask
from .code_analyzer import CodeAnalyzer


@dataclass
class MetaAgentTask:
    """Task for meta-agent system."""
    task_id: str
    task_type: str  # 'code_generation', 'problem_solving', 'analysis'
    description: str
    context: Dict[str, Any]
    created_at: str


@dataclass
class MetaAgentResult:
    """Result from meta-agent processing."""
    task_id: str
    success: bool
    result: Any
    reasoning_strategies_used: List[str]
    execution_time_seconds: float
    confidence: float
    metadata: Dict[str, Any]


class MetaAgentOrchestrator:
    """
    Meta-Agent Orchestrator coordinating multiple AI approaches.

    This is a sophisticated system that combines:
    - Multiple reasoning strategies (CoT, ToT, Reflexion)
    - Autonomous code generation
    - Self-improvement capabilities
    - Parallel execution and synthesis
    """

    def __init__(self):
        """Initialize meta-agent orchestrator."""
        self.coder = AutonomousCoder(max_iterations=3)
        self.analyzer = CodeAnalyzer()

        # Initialize reasoning strategies
        self.strategies: Dict[str, ReasoningStrategy] = {
            'chain_of_thought': ChainOfThoughtStrategy(),
            'tree_of_thought': TreeOfThoughtStrategy(num_branches=3),
            'reflexion': ReflexionStrategy(max_iterations=3),
        }

        # Ensemble strategy combining all others
        self.ensemble_strategy = EnsembleStrategy(list(self.strategies.values()))

        self.task_history: List[MetaAgentResult] = []

    async def process_task(
        self,
        task: MetaAgentTask,
        use_ensemble: bool = True
    ) -> MetaAgentResult:
        """
        Process a task using meta-agent capabilities.

        Args:
            task: Task to process
            use_ensemble: Whether to use ensemble of all strategies

        Returns:
            MetaAgentResult
        """
        start_time = datetime.utcnow()

        if task.task_type == 'code_generation':
            result = await self._handle_code_generation(task, use_ensemble)
        elif task.task_type == 'problem_solving':
            result = await self._handle_problem_solving(task, use_ensemble)
        elif task.task_type == 'analysis':
            result = await self._handle_analysis(task, use_ensemble)
        else:
            result = MetaAgentResult(
                task_id=task.task_id,
                success=False,
                result=None,
                reasoning_strategies_used=[],
                execution_time_seconds=0.0,
                confidence=0.0,
                metadata={'error': f'Unknown task type: {task.task_type}'}
            )

        result.execution_time_seconds = (
            datetime.utcnow() - start_time
        ).total_seconds()

        self.task_history.append(result)
        return result

    async def _handle_code_generation(
        self,
        task: MetaAgentTask,
        use_ensemble: bool
    ) -> MetaAgentResult:
        """Handle code generation tasks."""
        strategies_used = []

        # First, use reasoning to plan the approach
        if use_ensemble:
            reasoning_result = await self.ensemble_strategy.reason(
                task.description,
                task.context
            )
            strategies_used = [self.ensemble_strategy.name]
        else:
            reasoning_result = await self.strategies['chain_of_thought'].reason(
                task.description,
                task.context
            )
            strategies_used = ['chain_of_thought']

        # Generate code using autonomous coder
        code_task = CodeGenerationTask(
            task_id=task.task_id,
            description=task.description,
            language=task.context.get('language', 'python'),
            constraints=task.context.get('constraints', []),
            created_at=task.created_at
        )

        code_result = await self.coder.generate_code(code_task)

        return MetaAgentResult(
            task_id=task.task_id,
            success=code_result.success,
            result={
                'code': code_result.code,
                'quality_score': code_result.quality_score,
                'iterations': code_result.iterations,
                'reasoning_trace': reasoning_result.steps,
                'code_reasoning': code_result.reasoning_trace,
                'improvements': code_result.improvements
            },
            reasoning_strategies_used=strategies_used,
            execution_time_seconds=0.0,  # Will be set by caller
            confidence=min(reasoning_result.confidence, code_result.quality_score),
            metadata={
                'reasoning_confidence': reasoning_result.confidence,
                'code_quality': code_result.quality_score,
                'num_reasoning_steps': len(reasoning_result.steps),
                'num_code_iterations': code_result.iterations
            }
        )

    async def _handle_problem_solving(
        self,
        task: MetaAgentTask,
        use_ensemble: bool
    ) -> MetaAgentResult:
        """Handle general problem-solving tasks."""
        strategies_used = []

        if use_ensemble:
            # Run all strategies in parallel
            result = await self.ensemble_strategy.reason(
                task.description,
                task.context
            )
            strategies_used = [self.ensemble_strategy.name]
        else:
            # Use best single strategy
            result = await self.strategies['reflexion'].reason(
                task.description,
                task.context
            )
            strategies_used = ['reflexion']

        return MetaAgentResult(
            task_id=task.task_id,
            success=True,
            result={
                'answer': result.final_answer,
                'reasoning_steps': [
                    {
                        'step': s.step_number,
                        'thought': s.thought,
                        'action': s.action,
                        'score': s.score
                    }
                    for s in result.steps
                ]
            },
            reasoning_strategies_used=strategies_used,
            execution_time_seconds=0.0,
            confidence=result.confidence,
            metadata=result.metadata
        )

    async def _handle_analysis(
        self,
        task: MetaAgentTask,
        use_ensemble: bool
    ) -> MetaAgentResult:
        """Handle code analysis tasks."""
        code = task.context.get('code', '')
        language = task.context.get('language', 'python')

        # Analyze the code
        analysis = self.analyzer.analyze(code, language)

        # Use reasoning to provide insights
        reasoning_result = await self.strategies['chain_of_thought'].reason(
            f"Analyze code quality and provide insights: {task.description}",
            {'analysis': analysis}
        )

        return MetaAgentResult(
            task_id=task.task_id,
            success=True,
            result={
                'quality_level': analysis.quality_level.value,
                'score': analysis.score,
                'issues': [
                    {
                        'severity': i.severity,
                        'line': i.line,
                        'message': i.message,
                        'suggestion': i.suggestion
                    }
                    for i in analysis.issues
                ],
                'metrics': analysis.metrics,
                'suggestions': analysis.suggestions,
                'reasoning': reasoning_result.final_answer
            },
            reasoning_strategies_used=['chain_of_thought'],
            execution_time_seconds=0.0,
            confidence=analysis.score,
            metadata={'num_issues': len(analysis.issues)}
        )

    async def run_parallel_tasks(
        self,
        tasks: List[MetaAgentTask]
    ) -> List[MetaAgentResult]:
        """
        Run multiple tasks in parallel.

        Args:
            tasks: List of tasks to process

        Returns:
            List of results
        """
        task_coroutines = [self.process_task(task) for task in tasks]
        results = await asyncio.gather(*task_coroutines, return_exceptions=True)

        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(MetaAgentResult(
                    task_id=tasks[i].task_id,
                    success=False,
                    result=None,
                    reasoning_strategies_used=[],
                    execution_time_seconds=0.0,
                    confidence=0.0,
                    metadata={'error': str(result)}
                ))
            else:
                processed_results.append(result)

        return processed_results

    def get_statistics(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        if not self.task_history:
            return {
                'total_tasks': 0,
                'success_rate': 0.0,
                'average_confidence': 0.0,
                'average_execution_time': 0.0
            }

        successful = [t for t in self.task_history if t.success]

        return {
            'total_tasks': len(self.task_history),
            'successful_tasks': len(successful),
            'success_rate': len(successful) / len(self.task_history),
            'average_confidence': sum(t.confidence for t in self.task_history) / len(self.task_history),
            'average_execution_time': sum(t.execution_time_seconds for t in self.task_history) / len(self.task_history),
            'strategies_used': list(set(
                s for t in self.task_history for s in t.reasoning_strategies_used
            )),
            'coder_statistics': self.coder.get_statistics()
        }

    async def self_improve(self) -> Dict[str, Any]:
        """
        Self-improvement cycle - analyze own performance and optimize.

        Returns:
            Improvement report
        """
        stats = self.get_statistics()

        improvements = []

        # Analyze success rate
        if stats['success_rate'] < 0.8:
            improvements.append("Consider increasing max iterations for better results")

        # Analyze confidence
        if stats['average_confidence'] < 0.7:
            improvements.append("Low confidence - consider using ensemble strategy more often")

        # Analyze execution time
        if stats['average_execution_time'] > 5.0:
            improvements.append("High execution time - consider optimizing parallel execution")

        # Analyze strategy effectiveness
        strategy_performance = {}
        for task in self.task_history:
            for strategy in task.reasoning_strategies_used:
                if strategy not in strategy_performance:
                    strategy_performance[strategy] = []
                strategy_performance[strategy].append(task.confidence)

        best_strategy = max(
            strategy_performance.items(),
            key=lambda x: sum(x[1]) / len(x[1]) if x[1] else 0,
            default=(None, [])
        )[0]

        if best_strategy:
            improvements.append(f"Best performing strategy: {best_strategy}")

        return {
            'current_stats': stats,
            'improvements_identified': improvements,
            'best_strategy': best_strategy,
            'recommendation': 'Continue using ensemble approach for complex tasks'
        }
