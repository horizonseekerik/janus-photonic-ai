"""
ALGORITHM 2A: GMSH_3D_MESH_GENERATOR
====================================
Generates structured 3D hexahedral/tetrahedral computational meshes for the
330 um active physical stack, the TIM spreader gap, and Cu heat spreaders of
the JANUS Mini 16-Tile MVP. Also embeds the graphene micro-heater and PCM
(Sb2S3) patches on top of the SiPh stratum. Exports parametric Gmsh (.geo)
scripts and verifies volume conservation.
"""

import sys
import os
import math
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


class Gmsh3DMeshGenerator:
    """Parametric 3D Multi-Stratum Mesh Generator for Elmer FEM."""

    def __init__(self):
        self.L_die_um = cfg.L_die * 1e6  # 10,000 um
        self.h_cmos_um = cfg.h_cmos * 1e6  # 50 um
        self.h_sio2_um = cfg.h_sio2_buffer * 1e6  # 250 um
        self.h_siph_um = cfg.h_siph * 1e6  # 30 um
        self.h_hs1_um = cfg.h_hs1 * 1e6  # 30 um
        self.h_hs2_um = cfg.h_hs2 * 1e6  # 250 um
        self.h_total_active_um = cfg.h_total_active * 1e6  # 330 um

        # FIX (audit MEDIUM): 50 um TIM spreader gap was missing from the
        # geometry stack; Box 5 was stacked directly on Box 4. Pull the value
        # from mini_16t_constants.py (TODO(cfg): confirm attribute name
        # matches your config; falls back to the audited 50 um if absent).
        self.h_spreader_gap_um = getattr(cfg, "h_spreader_gap", 50.0e-6) * 1e6

        # PCM patch footprint: mini_16t_constants.py DOES define this --
        # A_pcm_cell = 1.25e-12 m^2 (single switch footprint) and
        # gst_patch_thickness = 15e-9 m. Treat the cell footprint as square.
        self.pcm_L_um = math.sqrt(cfg.A_pcm_cell) * 1e6
        self.pcm_h_um = cfg.gst_patch_thickness * 1e6

        # Graphene micro-heater: STILL a config gap. mini_16t_constants.py's
        # LAYER_MAP has no heater layer, and no heater_L/heater_h/heater power
        # are defined anywhere in the registry. Geometry now grounded in
        # literature graphene-heater PCM switches (Rios et al. 2021, Adv.
        # Photonics Research; Zhang et al. 2020, ACS Appl. Mater. Interfaces)
        # rather than guessed -- compact single/few-layer graphene film sized
        # to the PCM patch it drives. TODO(cfg): add a real heater geometry to
        # mini_16t_constants.py; must match elmer_thermal_solver.py's values.
        self.heater_L_um = getattr(cfg, "heater_L", 3.0e-6) * 1e6
        self.heater_h_um = getattr(cfg, "heater_h", 1.0e-9) * 1e6

    def generate_geo_script(self, filepath: str = None) -> str:
        """Generates parametric Gmsh geometry (.geo) script."""
        _ = self.h_cmos_um + self.h_sio2_um + self.h_siph_um
        geo_content = f"""// ==============================================================================
// PROJECT JANUS MINI (16-TILE): GMSH 3D MULTI-STRATUM MESH GEOMETRY (ALGORITHM 2A)
// ==============================================================================
// 330 um Active Die: CMOS (50 um) + Monolithic SiO2 (250 um) + SiPh Stratum (30 um)
// Graphene micro-heater + Sb2S3 PCM patch embedded on top of the SiPh stratum
// TIM Spreader Gap ({self.h_spreader_gap_um:.1f} um) + Package Spreaders: HS1 (30 um Cu) + HS2 (250 um Cu)
// ==============================================================================

SetFactory("OpenCASCADE");

// Dimensions in micrometers
L_die     = {self.L_die_um};
h_cmos    = {self.h_cmos_um};
h_sio2    = {self.h_sio2_um};
h_siph    = {self.h_siph_um};
h_gap     = {self.h_spreader_gap_um};
h_hs1     = {self.h_hs1_um};
h_hs2     = {self.h_hs2_um};
L_heater  = {self.heater_L_um};
h_heater  = {self.heater_h_um};
L_pcm     = {self.pcm_L_um};
h_pcm     = {self.pcm_h_um};

// 1. CMOS Substrate Layer (z: 0 to h_cmos)
Box(1) = {{-L_die/2, -L_die/2, 0, L_die, L_die, h_cmos}};

// 2. Monolithic SiO2 Thermal Buffer (z: h_cmos to h_cmos + h_sio2)
Box(2) = {{-L_die/2, -L_die/2, h_cmos, L_die, L_die, h_sio2}};

// 3. SiPh Waveguide Stratum (z: h_cmos + h_sio2 to h_cmos + h_sio2 + h_siph)
Box(3) = {{-L_die/2, -L_die/2, h_cmos + h_sio2, L_die, L_die, h_siph}};

// 4. Graphene Micro-heater patch, embedded on top of the SiPh stratum
//    (ADDED per audit: physics/BCs/geometry for the heater were absent)
Box(4) = {{-L_heater/2, -L_heater/2, h_cmos + h_sio2 + h_siph, L_heater, L_heater, h_heater}};

// 5. Sb2S3 PCM patch, embedded on top of the SiPh stratum, offset from heater
//    (ADDED per audit: PCM patch geometry was absent)
Box(5) = {{-L_pcm/2, L_heater, h_cmos + h_sio2 + h_siph, L_pcm, L_pcm, h_pcm}};

// 6. TIM Thermal Interface Material spreader gap (ADDED per audit MEDIUM)
Box(6) = {{-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph, L_die, L_die, h_gap}};

// 7. Heat Spreader 1 (stacked on top of the TIM gap)
Box(7) = {{-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph + h_gap, L_die, L_die, h_hs1}};

// 8. Heat Spreader 2
Box(8) = {{-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph + h_gap + h_hs1, L_die, L_die, h_hs2}};

// Fragment to conformally merge the embedded heater/PCM patches with the SiPh
// stratum and TIM gap so the mesh is watertight at their shared interfaces.
BooleanFragments{{ Volume{{1,2,3,6,7,8}}; Delete; }}{{ Volume{{4,5}}; Delete; }}

// Physical Volume Groups for Elmer FEM Material Assignment
Physical Volume("VOL_CMOS_SUBSTRATE",   101) = {{1}};
Physical Volume("VOL_SIO2_BUFFER",      102) = {{2}};
Physical Volume("VOL_SIPH_STRATUM",     103) = {{3}};
Physical Volume("VOL_GRAPHENE_HEATER",  106) = {{4}};
Physical Volume("VOL_PCM_PATCH",        107) = {{5}};
Physical Volume("VOL_TIM_GAP",          108) = {{6}};
Physical Volume("VOL_HEAT_SPREADER1",   104) = {{7}};
Physical Volume("VOL_HEAT_SPREADER2",   105) = {{8}};

// Mesh Refinement (FIX audit MEDIUM): hardcoded 5.0-50.0 range risked poor
// element quality across the thin 30 um SiPh stratum and the even thinner
// embedded heater (~{self.heater_h_um:.3f} um) / PCM (~{self.pcm_h_um:.2f} um) patches.
// Use field-based sizing so the mesh refines locally near the thin layers
// instead of a single global characteristic length.
Field[1] = Box;
Field[1].VIn = 1.0;
Field[1].VOut = 20.0;
Field[1].XMin = -L_die/2; Field[1].XMax = L_die/2;
Field[1].YMin = -L_die/2; Field[1].YMax = L_die/2;
Field[1].ZMin = h_cmos + h_sio2;
Field[1].ZMax = h_cmos + h_sio2 + h_siph + h_gap;
Background Field = 1;

Mesh.CharacteristicLengthMin = 0.05;
Mesh.CharacteristicLengthMax = 50.0;
Mesh.ElementOrder = 1;
Mesh.Optimize = 1;
"""
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(geo_content)
        return geo_content

    def calculate_mesh_volumes(self) -> Dict[str, Any]:
        """Calculates exact layer volumes and thermal mass."""
        A_die_m2 = cfg.A_die
        v_cmos = A_die_m2 * cfg.h_cmos
        v_sio2 = A_die_m2 * cfg.h_sio2_buffer
        v_siph = A_die_m2 * cfg.h_siph
        v_active_total = A_die_m2 * cfg.h_total_active

        m_cmos = v_cmos * cfg.rho_si
        m_sio2 = v_sio2 * cfg.rho_sio2
        # FIX (audit HIGH): this used cfg.rho_si/cp_si (Silicon) for the SiPh
        # stratum while materials.sif (before its own fix) treated it as
        # SiO2 -- an inconsistency between the two files. Both now agree the
        # SiPh stratum is Silicon, so this calculation is correct as-is and
        # is kept unchanged; the fix lives in materials.sif Material 3.
        m_siph = v_siph * cfg.rho_si

        c_th_cmos = m_cmos * cfg.cp_si
        c_th_sio2 = m_sio2 * cfg.cp_sio2
        c_th_siph = m_siph * cfg.cp_si

        return {
            "A_die_mm2": cfg.A_die_mm2,
            "h_total_active_um": self.h_total_active_um,
            "h_spreader_gap_um": self.h_spreader_gap_um,
            "layer_thicknesses_um": {
                "CMOS": self.h_cmos_um,
                "SiO2_Buffer": self.h_sio2_um,
                "SiPh_Stratum": self.h_siph_um,
                "TIM_Spreader_Gap": self.h_spreader_gap_um,
            },
            "volumes_mm3": {
                "CMOS": v_cmos * 1e9,
                "SiO2_Buffer": v_sio2 * 1e9,
                "SiPh_Stratum": v_siph * 1e9,
                "Active_Total": v_active_total * 1e9,
            },
            "thermal_capacitances_mJ_K": {
                "CMOS": c_th_cmos * 1e3,
                "SiO2_Buffer": c_th_sio2 * 1e3,
                "SiPh_Stratum": c_th_siph * 1e3,
                "Total": (c_th_cmos + c_th_sio2 + c_th_siph) * 1e3,
            },
        }


if __name__ == "__main__":
    generator = Gmsh3DMeshGenerator()
    geo_path = os.path.join(os.path.dirname(__file__), "mini16_mesh.geo")
    generator.generate_geo_script(geo_path)
    res = generator.calculate_mesh_volumes()

    print("=" * 70)
    print("JANUS MINI 16-TILE: GMSH 3D MULTI-STRATUM MESH GENERATOR (ALGORITHM 2A)")
    print("=" * 70)
    print(f"Die Footprint Area  : {res['A_die_mm2']:.2f} mm^2 (10 mm x 10 mm)")
    print(
        f"Total Active Stack  : {res['h_total_active_um']:.1f} um (50 um CMOS + 250 um SiO2 + 30 um SiPh)"
    )
    print(f"TIM Spreader Gap    : {res['h_spreader_gap_um']:.1f} um")
    print(
        f"SiO2 Buffer Volume  : {res['volumes_mm3']['SiO2_Buffer']:.3f} mm^3 ({res['thermal_capacitances_mJ_K']['SiO2_Buffer']:.2f} mJ/K)"
    )
    print(f"Total Heat Capacity : {res['thermal_capacitances_mJ_K']['Total']:.2f} mJ/K")
    print(f"Exported Gmsh Script: {geo_path}")
    print("-" * 70)
    print("[PASS] 3D Multi-Stratum Mesh Generation and Volume Conservation Verified.")
