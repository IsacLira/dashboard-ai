"""Agents package for data analysis.

This package provides specialized agents for different tasks in the
data analysis pipeline.
"""

from .base import SimpleAgent
from .tools import DataTools
from .intent_evaluator import IntentEvaluator
from .analytics_agent import AnalyticsAgent

__all__ = [
    "SimpleAgent",
    "DataTools",
    "IntentEvaluator",
    "AnalyticsAgent",
]

__version__ = '1.0.0'
