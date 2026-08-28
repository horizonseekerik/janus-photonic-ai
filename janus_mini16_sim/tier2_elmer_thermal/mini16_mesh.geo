// ==============================================================================
// PROJECT JANUS MINI (16-TILE): GMSH 3D MULTI-STRATUM MESH GEOMETRY (ALGORITHM 2A)
// ==============================================================================
SetFactory("OpenCASCADE");

L_die = 10000.0;
h_cmos = 50.0;
h_sio2 = 250.0;
h_siph = 30.0;
h_hs1  = 30.0;
h_hs2  = 250.0;

Box(1) = {-L_die/2, -L_die/2, 0, L_die, L_die, h_cmos};
Box(2) = {-L_die/2, -L_die/2, h_cmos, L_die, L_die, h_sio2};
Box(3) = {-L_die/2, -L_die/2, h_cmos + h_sio2, L_die, L_die, h_siph};
Box(4) = {-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph, L_die, L_die, h_hs1};
Box(5) = {-L_die/2, -L_die/2, h_cmos + h_sio2 + h_siph + h_hs1, L_die, L_die, h_hs2};

Physical Volume("VOL_CMOS_SUBSTRATE", 101) = {1};
Physical Volume("VOL_SIO2_BUFFER",    102) = {2};
Physical Volume("VOL_SIPH_STRATUM",   103) = {3};
Physical Volume("VOL_HEAT_SPREADER1", 104) = {4};
Physical Volume("VOL_HEAT_SPREADER2", 105) = {5};

Mesh.CharacteristicLengthMin = 5.0;
Mesh.CharacteristicLengthMax = 50.0;
Mesh.ElementOrder = 1;
Mesh.Optimize = 1;
