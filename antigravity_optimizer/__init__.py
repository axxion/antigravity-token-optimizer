"""
Antigravity Token Optimizer: The Next-Gen Context & Output Optimization Engine for Google Antigravity.
"""

from antigravity_optimizer.core.auditor import AuditReport, ProjectAuditor, WasteFinding
from antigravity_optimizer.core.compressor import CompressionReport, ContextCompressor
from antigravity_optimizer.core.config import (
    DEFAULT_FEATURES,
    OptimizationFeature,
    OptimizerConfig,
    ProfileType,
)
from antigravity_optimizer.generators.rules_gen import RulesGenerator
from antigravity_optimizer.generators.skills_gen import SkillsGenerator
from antigravity_optimizer.parsers.ast_skeleton import ASTSkeletonExtractor, SkeletonResult

__version__ = "1.0.0"

__all__ = [
    "OptimizerConfig",
    "ProfileType",
    "OptimizationFeature",
    "DEFAULT_FEATURES",
    "ContextCompressor",
    "CompressionReport",
    "ProjectAuditor",
    "AuditReport",
    "WasteFinding",
    "RulesGenerator",
    "SkillsGenerator",
    "ASTSkeletonExtractor",
    "SkeletonResult",
]
