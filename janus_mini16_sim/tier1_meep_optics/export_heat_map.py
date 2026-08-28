"""
ALGORITHM 1D: EXPORT_HEAT_MAP
=============================
Computes 3D volumetric optical absorption heat density:
    Q_opt(x,y,z) = 0.5 * omega_0 * eps_0 * Im(eps_r) * |E(x,y,z)|^2
Exports structured HDF5 (.h5) datasets for boundary heat source ingestion
by Tier 2 Elmer 3D Multi-Stratum Thermal FEM.
"""

import sys
import os
import numpy as np
import h5py

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


class HeatMapExporter:
    """Exports 3D optical heat absorption maps Q_opt(x,y,z) to HDF5 format."""

    def __init__(
        self, omega_0: float = cfg.omega_optical, eps_0: float = cfg.epsilon_0
    ):
        self.omega_0 = omega_0
        self.eps_0 = eps_0

    def compute_heat_density(
        self, E_field_3d: np.ndarray, eps_r_imag: float
    ) -> np.ndarray:
        """Calculates Q_opt(x,y,z) = 0.5 * omega_0 * eps_0 * Im(eps_r) * |E|^2 [W/m^3]."""
        E_sq = np.abs(E_field_3d) ** 2
        Q_opt = 0.5 * self.omega_0 * self.eps_0 * eps_r_imag * E_sq
        return Q_opt

    def export_hdf5(
        self, filepath: str, Q_opt: np.ndarray, coords: tuple, metadata: dict = None
    ) -> str:
        """Exports 3D array and spatial coordinate vectors to HDF5."""
        x_pts, y_pts, z_pts = coords
        assert Q_opt.size > 0, "Error: Heat map array is empty."
        assert Q_opt.shape == (
            len(x_pts),
            len(y_pts),
            len(z_pts),
        ), f"Shape mismatch: {Q_opt.shape} vs ({len(x_pts)}, {len(y_pts)}, {len(z_pts)})"

        with h5py.File(filepath, "w") as h5:
            dset_q = h5.create_dataset("Q_opt", data=Q_opt, compression="gzip")
            dset_q.attrs["units"] = "W/m^3"
            dset_q.attrs["description"] = "Volumetric optical absorption heat density"

            dset_x = h5.create_dataset("x_coords", data=x_pts)
            dset_x.attrs["units"] = "m"
            dset_y = h5.create_dataset("y_coords", data=y_pts)
            dset_y.attrs["units"] = "m"
            dset_z = h5.create_dataset("z_coords", data=z_pts)
            dset_z.attrs["units"] = "m"

            if metadata:
                for k, v in metadata.items():
                    h5.attrs[k] = v

        return filepath


if __name__ == "__main__":
    from tier1_meep_optics.sb2s3_switch_cell import Sb2S3SwitchCellFDTD

    solver = Sb2S3SwitchCellFDTD()
    res = solver.solve_state("crystalline")

    exporter = HeatMapExporter()
    eps_imag = res["n_complex"].imag * 2 * res["n_complex"].real
    Q_opt = exporter.compute_heat_density(res["E_field_3d"], eps_imag)

    out_h5 = os.path.join(os.path.dirname(__file__), "switch_cell_heat_crystal.h5")
    exporter.export_hdf5(
        out_h5,
        Q_opt,
        res["spatial_coords"],
        {"material": "Sb2S3", "state": "crystalline"},
    )

    print("=" * 70)
    print("JANUS MINI 16-TILE: OPTICAL ABSORPTION HEAT MAP EXPORTER (HDF5)")
    print("=" * 70)
    print(f"Exported HDF5 File  : {out_h5}")
    print(f"Heat Map Dimensions : {Q_opt.shape} ({Q_opt.size:,} voxels)")
    print(f"Peak Absorption (Q) : {np.max(Q_opt):.4e} W/m^3")
    print(f"Mean Absorption (Q) : {np.mean(Q_opt):.4e} W/m^3")
    print("-" * 70)
    print("[PASS] Optical heat map successfully exported for Elmer FEM ingestion.")
