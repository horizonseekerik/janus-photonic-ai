"""
PROJECT JANUS MINI (16-TILE): GLOBAL CONFIGURATION REGISTRY
===========================================================
Exports all immutable simulation constants across Sections 2.1 through 2.28
and Tier 0 GDS variables.
"""

from . import mini_16t_constants
from .mini_16t_constants import export_specs_json

__all__ = ["mini_16t_constants", "export_specs_json"]
