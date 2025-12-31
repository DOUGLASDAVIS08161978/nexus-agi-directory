"""
Meta-Agent System for Autonomous Code Generation and Improvement

This module provides a sophisticated multi-agent system that can:
- Write code autonomously using multiple reasoning strategies
- Test and validate generated code
- Iteratively improve code quality
- Orchestrate multiple AI models and approaches
"""

from .orchestrator import MetaAgentOrchestrator
from .autonomous_coder import AutonomousCoder
from .code_analyzer import CodeAnalyzer
from .strategies import (
    ReasoningStrategy,
    ChainOfThoughtStrategy,
    TreeOfThoughtStrategy,
    ReflexionStrategy,
    EnsembleStrategy
)

__all__ = [
    'MetaAgentOrchestrator',
    'AutonomousCoder',
    'CodeAnalyzer',
    'ReasoningStrategy',
    'ChainOfThoughtStrategy',
    'TreeOfThoughtStrategy',
    'ReflexionStrategy',
    'EnsembleStrategy',
]
