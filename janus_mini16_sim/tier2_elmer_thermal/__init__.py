"""
PROJECT JANUS MINI (16-TILE): TIER 2 THERMAL FEM PACKAGE
========================================================
Provides 3D multi-stratum mesh generation, transient heat diffusion solvers,
and reduced-order thermal impedance ROM extraction:
- Algorithm 2A: Gmsh 3D Multi-Stratum Mesh Generator (gmsh_mesh_generator.py)
- Algorithm 2B & 2C: Elmer 3D Transient Thermal Diffusion Solver (elmer_thermal_solver.py)
- Algorithm 2D: 5-Pole Foster RC Thermal Impedance Extractor (extract_thermal_rom.py)
"""

from .gmsh_mesh_generator import Gmsh3DMeshGenerator
from .elmer_thermal_solver import ElmerTransientThermalSolver
from .extract_thermal_rom import ThermalROMExtractor

__all__ = ["Gmsh3DMeshGenerator", "ElmerTransientThermalSolver", "ThermalROMExtractor"]

__version__ = "1.0.0"
__tier__ = "Tier 2: 3D Multi-Stratum Thermal FEM"
