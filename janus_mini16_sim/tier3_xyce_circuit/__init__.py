"""
PROJECT JANUS MINI (16-TILE): TIER 3 CIRCUIT & SIGNAL INTEGRITY PACKAGE
=======================================================================
Provides S-parameter vector fitting, SAC2M APD models, StrongARM latches,
and 100 GHz eye diagram / BER analysis:
- Algorithm 3A: S-Parameter Vector Fitting & SPICE Exporter (vector_fit_s_params.py)
- Algorithm 3B: SAC2M Ge/Si APD Receiver Model (apd_receiver_model.py)
- Algorithm 3C: 100 GHz StrongARM Regenerative Decision Latch (strongarm_latch.py)
- Algorithm 3D & 3E: 100 GHz Eye Diagram & BER <= 10^-18 Engine (eye_diagram_ber.py)
"""

from .vector_fit_s_params import VectorFitSParams
from .apd_receiver_model import SAC2MAPDReceiver
from .strongarm_latch import StrongARMLatch
from .eye_diagram_ber import EyeDiagramAndBERSolver
from .ilo_comb_lock import ILOFrequencyCombLock

__all__ = [
    "VectorFitSParams",
    "SAC2MAPDReceiver",
    "StrongARMLatch",
    "EyeDiagramAndBERSolver",
    "ILOFrequencyCombLock",
]

__version__ = "1.0.0"
__tier__ = "Tier 3: Xyce Circuit & Signal Integrity"
