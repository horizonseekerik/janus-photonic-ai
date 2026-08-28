"""
PROJECT JANUS MINI (16-TILE): TIER 0 & TIER 1 OPTICS PACKAGE
============================================================
Provides 3D FDTD Maxwell solvers, GDS pre-processing, and physical exporters:
- Tier 0: GDS II Layout Discretization & Refractive Index Mapping (gds_layout_processor.py)
- Algorithm 1A: 3D FDTD Sb2S3 Phase-Change Switch Cell (sb2s3_switch_cell.py)
- Algorithm 1B: Parabolic MMI Waveguide Crossing Solver (waveguide_crossing.py)
- Algorithm 1C: Thin-Film LiTaO3 Electro-Optic Pockels Modulator (litao3_pockels_router.py)
- Algorithm 1D: Touchstone .s4p S-Parameter Exporter (export_touchstone.py)
- Algorithm 1D: Q_opt(x,y,z) Optical Absorption Heat Map Exporter (export_heat_map.py)
"""

from .gds_layout_processor import GDSLayoutProcessor
from .sb2s3_switch_cell import Sb2S3SwitchCellFDTD
from .waveguide_crossing import WaveguideCrossingFDTD
from .litao3_pockels_router import LiTaO3PockelsModulator
from .export_touchstone import TouchstoneExporter
from .export_heat_map import HeatMapExporter

__all__ = [
    "GDSLayoutProcessor",
    "Sb2S3SwitchCellFDTD",
    "WaveguideCrossingFDTD",
    "LiTaO3PockelsModulator",
    "TouchstoneExporter",
    "HeatMapExporter",
]

__version__ = "1.0.0"
__tier__ = "Tier 0: GDS II Pre-Processor & Tier 1: MEEP 3D FDTD Optics"
