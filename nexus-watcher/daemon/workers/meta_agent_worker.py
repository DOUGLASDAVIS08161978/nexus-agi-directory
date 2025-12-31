"""Meta-Agent Worker for Nexus Watcher Daemon."""

import asyncio
from typing import List, Dict, Any
from datetime import datetime

from .base_worker import BaseWorker
from ..meta_agent import MetaAgentOrchestrator
from ..meta_agent.orchestrator import MetaAgentTask


class MetaAgentWorker(BaseWorker):
    """
    Worker that runs autonomous meta-agent tasks.

    This worker continuously:
    - Analyzes the codebase for improvement opportunities
    - Generates code enhancements autonomously
    - Self-improves based on performance metrics
    - Demonstrates advanced AI reasoning capabilities
    """

    def __init__(self, *args, **kwargs):
        super().__init__("meta_agent", *args, **kwargs)
        self.orchestrator = MetaAgentOrchestrator()
        self._task_queue: List[MetaAgentTask] = []
        self._iteration_count = 0

    async def run_iteration(self):
        """Execute one meta-agent iteration."""
        self._iteration_count += 1

        self.logger.info(
            f"Meta-Agent Iteration {self._iteration_count} starting..."
        )

        # Generate autonomous improvement tasks
        tasks = await self._generate_autonomous_tasks()

        if not tasks:
            self.logger.info("No autonomous tasks generated this iteration")
            return

        # Process tasks
        results = await self.orchestrator.run_parallel_tasks(tasks)

        # Log results
        successful = [r for r in results if r.success]
        self.logger.info(
            f"Processed {len(results)} meta-agent tasks: "
            f"{len(successful)} successful, "
            f"avg confidence: {sum(r.confidence for r in results) / len(results):.2%}"
        )

        # Log interesting results
        for result in results[:3]:  # Show first 3
            self.logger.info(
                f"Task {result.task_id}: "
                f"Success={result.success}, "
                f"Confidence={result.confidence:.2%}, "
                f"Time={result.execution_time_seconds:.3f}s"
            )

        # Self-improvement check
        if self._iteration_count % 5 == 0:  # Every 5 iterations
            self.logger.info("Running self-improvement analysis...")
            improvement_report = await self.orchestrator.self_improve()

            stats = improvement_report['current_stats']
            self.logger.info(
                f"Self-Improvement Report: "
                f"Success Rate: {stats['success_rate']:.2%}, "
                f"Avg Confidence: {stats['average_confidence']:.2%}"
            )

            if improvement_report['improvements_identified']:
                self.logger.info(
                    f"Improvements identified: "
                    f"{len(improvement_report['improvements_identified'])}"
                )
                for improvement in improvement_report['improvements_identified'][:2]:
                    self.logger.info(f"  → {improvement}")

        # Save statistics to database
        stats = self.orchestrator.get_statistics()
        await self.db.set_state('meta_agent_stats', stats)
        await self.db.set_state('meta_agent_last_run', datetime.utcnow().isoformat())

    async def _generate_autonomous_tasks(self) -> List[MetaAgentTask]:
        """Generate autonomous improvement tasks."""
        tasks = []

        # Task types rotate based on iteration
        task_types = [
            ('code_generation', 'Create a helper function for data validation'),
            ('code_generation', 'Generate a utility for configuration management'),
            ('problem_solving', 'How to optimize API response times?'),
            ('code_generation', 'Create a caching mechanism for API calls'),
            ('problem_solving', 'Best practices for error handling in async code'),
        ]

        # Generate 2-3 tasks per iteration
        num_tasks = min(3, self._iteration_count % 4 + 1)

        for i in range(num_tasks):
            task_idx = (self._iteration_count + i) % len(task_types)
            task_type, description = task_types[task_idx]

            task = MetaAgentTask(
                task_id=f"auto_task_{self._iteration_count}_{i}",
                task_type=task_type,
                description=description,
                context={
                    'language': 'python',
                    'iteration': self._iteration_count,
                    'autonomous': True
                },
                created_at=datetime.utcnow().isoformat()
            )
            tasks.append(task)

        return tasks

    def get_interval(self) -> int:
        """Get worker interval from config."""
        return self.config.get('meta_agent.run_interval', 3600)  # 1 hour default

    def get_status(self) -> dict:
        """Get worker status including meta-agent statistics."""
        base_status = super().get_status()

        # Add meta-agent specific stats
        stats = self.orchestrator.get_statistics()
        base_status['meta_agent'] = {
            'iterations': self._iteration_count,
            'total_tasks': stats.get('total_tasks', 0),
            'success_rate': stats.get('success_rate', 0.0),
            'average_confidence': stats.get('average_confidence', 0.0),
        }

        return base_status
