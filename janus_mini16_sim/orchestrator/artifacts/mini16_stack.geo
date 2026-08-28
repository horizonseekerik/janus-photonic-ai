// ==============================================================================
// PROJECT JANUS MINI (16-TILE): GMSH 3D MULTI-STRATUM MESH GEOMETRY (ALGORITHM 2A)
// ==============================================================================
// 330 um Active Die: CMOS (50 um) + Monolithic SiO2 (250 um) + SiPh Stratum (30 um)
// Graphene micro-heater + Sb2S3 PCM patch embedded on top of the SiPh stratum
// TIM Spreader Gap (50.0 um) + Package Spreaders: HS1 (30 um Cu) + HS2 (250 um Cu)
// ==============================================================================

SetFactory("OpenCASCADE");

// Dimensions in micrometers
L_die     = 10000.0;
h_cmos    = 50.0;
h_sio2    = 250.0;
h_siph    = 30.0;
h_gap     = 50.0;
h_hs1     = 30.0;
h_hs2     = 250.0;
L_heater  = 3.0;
h_heater  = 0.001;
L_pcm     = 1.1180339887498947;
h_pcm     = 0.015;

// 1. CMOS Substrate Layer (z: 0 to h_cmos)
Box(1) = {-L_die/2, -L_die/2, 0, L_die, L_die, h_cmos};

// 2. Monolithic SiO2 Thermal Buffer (z: h_cmos to h_cmos + h_sio2)
Box(2) = {-L_die/2, -L_die/2, h_cmos, L_die, L_die, h_sio2};

// 3. SiPh Waveguide Stratum (z: h_cmos + h_sio2 to h_cmos + h_sio2 + h_siph)
Box(3) = {-L_die/2, -L_die/2, h_cmos + h_sio2, L_die, L_die, h_siph};

// 4. Graphene Micro-heater patch, embedded on top of the SiPh stratum
//    (ADDED per audit: physics/BCs/geometry for the heater were absent)
Box(4) = {-L_heater/2, -L_heater/2, h_cmos + h_sio2 + h_siph, L_heater, L_heater, h_heater};

// 5. Sb2S3 PCM patch, embedded on top of the SiPh stratum, offset from heater
//    (ADDED per audit: PCM patch geometry was absent)
Box(5) = {-L_pcm/2, L_heater, h_cmos + h_sio2 + h_siph, L_pcm, L_pcm, h_pcm};

// 6. TIM Thermal Interface Material spreader gap (ADDED per audit MEDIUM)
Box(6) = {-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph, L_die, L_die, h_gap};

// 7. Heat Spreader 1 (stacked on top of the TIM gap)
Box(7) = {-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph + h_gap, L_die, L_die, h_hs1};

// 8. Heat Spreader 2
Box(8) = {-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph + h_gap + h_hs1, L_die, L_die, h_hs2};

// Fragment to conformally merge the embedded heater/PCM patches with the SiPh
// stratum and TIM gap so the mesh is watertight at their shared interfaces.
BooleanFragments{ Volume{1,2,3,6,7,8}; Delete; }{ Volume{4,5}; Delete; }

// Physical Volume Groups for Elmer FEM Material Assignment
Physical Volume("VOL_CMOS_SUBSTRATE",   101) = {1};
Physical Volume("VOL_SIO2_BUFFER",      102) = {2};
Physical Volume("VOL_SIPH_STRATUM",     103) = {3};
Physical Volume("VOL_GRAPHENE_HEATER",  106) = {4};
Physical Volume("VOL_PCM_PATCH",        107) = {5};
Physical Volume("VOL_TIM_GAP",          108) = {6};
Physical Volume("VOL_HEAT_SPREADER1",   104) = {7};
Physical Volume("VOL_HEAT_SPREADER2",   105) = {8};

// Mesh Refinement (FIX audit MEDIUM): hardcoded 5.0-50.0 range risked poor
// element quality across the thin 30 um SiPh stratum and the even thinner
// embedded heater (~0.001 um) / PCM (~0.01 um) patches.
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
