#!/usr/bin/env python3
"""
Meta-Agent System Demonstration

This demonstrates the advanced autonomous coding and reasoning capabilities.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add daemon to path
sys.path.insert(0, str(Path(__file__).parent))

from daemon.meta_agent import MetaAgentOrchestrator
from daemon.meta_agent.orchestrator import MetaAgentTask


async def demonstrate_code_generation():
    """Demonstrate autonomous code generation."""
    print("=" * 80)
    print("🤖 META-AGENT SYSTEM DEMONSTRATION")
    print("=" * 80)
    print()

    orchestrator = MetaAgentOrchestrator()

    # Task 1: Generate Fibonacci function
    print("📝 TASK 1: Generate Fibonacci Function")
    print("-" * 80)

    task1 = MetaAgentTask(
        task_id="task_001",
        task_type="code_generation",
        description="Create a function to calculate Fibonacci numbers",
        context={
            'language': 'python',
            'constraints': ['Should be efficient', 'Include docstrings']
        },
        created_at=datetime.utcnow().isoformat()
    )

    result1 = await orchestrator.process_task(task1, use_ensemble=True)

    print(f"\n✅ Success: {result1.success}")
    print(f"⚡ Confidence: {result1.confidence:.2%}")
    print(f"⏱️  Execution Time: {result1.execution_time_seconds:.3f}s")
    print(f"🧠 Strategies Used: {', '.join(result1.reasoning_strategies_used)}")
    print(f"\n📊 Metadata:")
    for key, value in result1.metadata.items():
        print(f"   • {key}: {value}")

    print(f"\n💻 Generated Code:")
    print("-" * 80)
    print(result1.result['code'])
    print("-" * 80)

    print(f"\n🔄 Improvements Made ({len(result1.result['improvements'])} iterations):")
    for improvement in result1.result['improvements']:
        print(f"   • {improvement}")

    print(f"\n🧪 Code Quality Score: {result1.result['quality_score']:.2%}")
    print()

    # Task 2: Generate sorting algorithm
    print("\n" + "=" * 80)
    print("📝 TASK 2: Generate Sorting Algorithm")
    print("-" * 80)

    task2 = MetaAgentTask(
        task_id="task_002",
        task_type="code_generation",
        description="Create a quicksort implementation",
        context={
            'language': 'python',
            'constraints': ['Should handle edge cases', 'Add type hints']
        },
        created_at=datetime.utcnow().isoformat()
    )

    result2 = await orchestrator.process_task(task2, use_ensemble=True)

    print(f"\n✅ Success: {result2.success}")
    print(f"⚡ Confidence: {result2.confidence:.2%}")
    print(f"\n💻 Generated Code:")
    print("-" * 80)
    print(result2.result['code'])
    print("-" * 80)
    print()

    # Task 3: Problem solving
    print("\n" + "=" * 80)
    print("📝 TASK 3: Problem Solving with Multiple Strategies")
    print("-" * 80)

    task3 = MetaAgentTask(
        task_id="task_003",
        task_type="problem_solving",
        description="How to optimize a slow database query?",
        context={
            'domain': 'database optimization',
            'constraints': ['Production environment', 'Cannot change schema']
        },
        created_at=datetime.utcnow().isoformat()
    )

    result3 = await orchestrator.process_task(task3, use_ensemble=True)

    print(f"\n✅ Success: {result3.success}")
    print(f"⚡ Confidence: {result3.confidence:.2%}")
    print(f"\n🧠 Answer: {result3.result['answer']}")
    print(f"\n🔍 Reasoning Steps ({len(result3.result['reasoning_steps'])} steps):")
    for step in result3.result['reasoning_steps']:
        print(f"   Step {step['step']}: {step['thought'][:70]}...")
        if step['action']:
            print(f"      → Action: {step['action']}")
        print(f"      → Score: {step['score']:.2f}")
    print()

    # Parallel execution demonstration
    print("\n" + "=" * 80)
    print("⚡ PARALLEL EXECUTION: Processing Multiple Tasks Simultaneously")
    print("-" * 80)

    parallel_tasks = [
        MetaAgentTask(
            task_id=f"parallel_task_{i}",
            task_type="code_generation",
            description=desc,
            context={'language': 'python'},
            created_at=datetime.utcnow().isoformat()
        )
        for i, desc in enumerate([
            "Create a prime number checker",
            "Create a calculator class",
            "Create a binary search function"
        ], 1)
    ]

    print(f"\n🚀 Launching {len(parallel_tasks)} tasks in parallel...")
    start_time = datetime.utcnow()

    parallel_results = await orchestrator.run_parallel_tasks(parallel_tasks)

    total_time = (datetime.utcnow() - start_time).total_seconds()

    print(f"\n✅ Completed {len(parallel_results)} tasks in {total_time:.3f}s")
    for i, result in enumerate(parallel_results, 1):
        print(f"\n   Task {i}: {parallel_tasks[i-1].description}")
        print(f"   • Success: {result.success}")
        print(f"   • Confidence: {result.confidence:.2%}")
        print(f"   • Quality: {result.result['quality_score']:.2%}")
        print(f"   • Iterations: {result.result['iterations']}")

    # Self-improvement analysis
    print("\n" + "=" * 80)
    print("🔄 SELF-IMPROVEMENT ANALYSIS")
    print("-" * 80)

    improvement_report = await orchestrator.self_improve()

    print(f"\n📊 Current Performance:")
    stats = improvement_report['current_stats']
    print(f"   • Total Tasks: {stats['total_tasks']}")
    print(f"   • Success Rate: {stats['success_rate']:.2%}")
    print(f"   • Average Confidence: {stats['average_confidence']:.2%}")
    print(f"   • Average Execution Time: {stats['average_execution_time']:.3f}s")

    print(f"\n🎯 Coder Statistics:")
    coder_stats = stats['coder_statistics']
    print(f"   • Code Generation Tasks: {coder_stats['total_tasks']}")
    print(f"   • Success Rate: {coder_stats['success_rate']:.2%}")
    print(f"   • Average Quality: {coder_stats['average_quality']:.2%}")
    print(f"   • Average Iterations: {coder_stats['average_iterations']:.1f}")

    print(f"\n💡 Improvements Identified:")
    for improvement in improvement_report['improvements_identified']:
        print(f"   • {improvement}")

    print(f"\n🏆 Best Strategy: {improvement_report['best_strategy']}")
    print(f"📌 Recommendation: {improvement_report['recommendation']}")

    # Final statistics
    print("\n" + "=" * 80)
    print("📈 FINAL STATISTICS")
    print("=" * 80)

    final_stats = orchestrator.get_statistics()
    print(f"\n🎯 Overall Performance:")
    print(f"   • Total Tasks Processed: {final_stats['total_tasks']}")
    print(f"   • Successful: {final_stats['successful_tasks']}")
    print(f"   • Success Rate: {final_stats['success_rate']:.2%}")
    print(f"   • Average Confidence: {final_stats['average_confidence']:.2%}")
    print(f"   • Average Execution Time: {final_stats['average_execution_time']:.3f}s")
    print(f"   • Strategies Used: {', '.join(final_stats['strategies_used'])}")

    print("\n" + "=" * 80)
    print("✨ DEMONSTRATION COMPLETE!")
    print("=" * 80)
    print()
    print("🚀 This meta-agent system demonstrates:")
    print("   ✓ Autonomous code generation with iterative improvement")
    print("   ✓ Multiple reasoning strategies (CoT, ToT, Reflexion, Ensemble)")
    print("   ✓ Self-analysis and quality assessment")
    print("   ✓ Parallel task execution")
    print("   ✓ Self-improvement capabilities")
    print("   ✓ Advanced orchestration and synthesis")
    print()


if __name__ == '__main__':
    asyncio.run(demonstrate_code_generation())
