#!/usr/bin/env python

#####################################################.
#      This file contains the argument parser 		#
#####################################################.

import argparse

def parser_args():
	parser = argparse.ArgumentParser(description="Generate conformers depending on type of optimization (change parameters in the params yaml file).")

	#necessary input details
	parser.add_argument("--varfile", dest="varfile", default=None, help="Parameters in YAML format")
	parser.add_argument("-i", "--input", help="File containing molecular structure(s)",dest="input", default=" ")
	parser.add_argument("--output_name",action="store", default="output", help="Change output filename to pyCONFORT-\"output\".dat", type=str)

	parser.add_argument("--path", help="Path for analysis/boltzmann factor/combining files where the gaussian folder created is present",dest="path", default="")
	parser.add_argument("-v","--verbose",action="store_true",default=False, help="verbose output")
	parser.add_argument("--output", dest="output", default=".sdf", metavar="output", help="The extension of the SDF files written")

	#work the script has to do
	parser.add_argument("--CSEARCH", action="store", default=None, help="Perform conformational analysis with or without dihedrals",choices=['rdkit','summ','fullmonte'])
	parser.add_argument("--CMIN", action="store", default=None, help="Perform minimization after conformational analysis",choices=['xtb','ani'])
	parser.add_argument("--QPREP", action="store", default=None, help="Create input files for QM calculations", choices=['gaussian'])
	parser.add_argument("--QCORR", action="store", default=None, help="Fix the output files from QM calculations",choices=['gaussian'])
	parser.add_argument("--QSTAT", action="store", default=None, help="Generate parameters for different conformers",choices=['graph','descp'])
	parser.add_argument("--QPRED", action="store", default=None, help="Perform predictions for different conformers", choices=['nmr','energy'])

	#arguments for TMBUILD
	parser.add_argument("--metal_complex", action="store_true", default=False, help="Request metal complex with coord. no. 4, 5 or 6")
	parser.add_argument("--metal",  help="Specify metallic element", default=[], dest="metal", type=str)
	parser.add_argument("--mult",  help="Multiplicity of metal complex or organic complexes", default="1", dest="mult", type=int)
	parser.add_argument("--complex_coord", help="Coord. no. of metal complex (automatically updates)", default=[], dest="complex_coord", type=int)
	parser.add_argument("--complex_type",  help="Force geometry of the metal complex (options: linear, trigonalplanar, squareplanar, squarepyramidal)", default="", dest="complex_type", type=str)
	parser.add_argument("--m_oxi",  help="Metal oxidation state", default=[], dest="m_oxi", type=int)
	parser.add_argument("--metal_idx",  help="Metal index (automatically updates)", default=[], dest="metal_idx", type=int)
	parser.add_argument("--charge",  help="Charge of metal complex (automatically updates)", default=[], dest="charge", type=int)
	parser.add_argument("--charge_default",  help="Charge default to be considered", default='auto', dest="charge_default")
	parser.add_argument("--metal_sym",  help="Symbols of metals to be considered from list (automatically updates)", default=[], dest="metal_sym", type=str)

	#argumets for CSEARCH and CMIN
	parser.add_argument("--ewin_cmin", action="store",default=5.0, help="energy window to print conformers for minimization using xTB or ANI (kcal/mol)", type=float)
	parser.add_argument("--ewin_csearch", action="store",default=5.0, help="energy window to print conformers for RDKit (kcal/mol)", type=float)
	parser.add_argument("--opt_fmax", action="store",default=0.05, help="fmax value used in xTB and AN1 optimizations", type=float)
	parser.add_argument("--opt_steps", action="store",default=1000, help="max cycles used in xTB and AN1 optimizations", type=int)
	parser.add_argument("--opt_steps_RDKit", action="store",default=1000, help="max cycles used in RDKit optimizations", type=int)
	parser.add_argument("--time","-t",action='store_true', default=True, help="request program runtime")
	parser.add_argument("--heavyonly", help="only consider torsion angles involving heavy (non H) elements (default=True)", default=True, metavar="heavyonly")
	parser.add_argument("-d","--degree", type=float, help="Amount, in degrees, to enumerate torsions by (default 120.0)",default=120.0)
	parser.add_argument("--max_torsions",type=int,help="Skip any molecules with more than this many torsions (default 20)",default=20)
	parser.add_argument("--sample", help="number of conformers to sample to get non-torsional differences (default 100)", default='auto', metavar="sample")
	parser.add_argument("--auto_sample", help="final factor to multiply in the auto mode for the sample option (default 20)", default=20, type=int, metavar="auto_sample")
	parser.add_argument("--ff", help="force field (MMFF or UFF)", default="MMFF", metavar="ff")
	parser.add_argument("--seed", help="random seed (default 062609)", default="062609", type=int, metavar="s")
	parser.add_argument("--rms_threshold", help="cutoff for considering sampled conformers the same (default 0.25)", default=0.25, type=float, metavar="R")
	parser.add_argument("--max_matches_RMSD", help="iteration cutoff for considering  matches in sampled conformers the same (default 1000)", default=1000 , type=int, metavar="max_matches_RMSD")
	parser.add_argument("--energy_threshold", dest="energy_threshold",action="store",default=0.25, help="energy difference between unique conformers (default 0.25)")
	parser.add_argument("--initial_energy_threshold", dest="initial_energy_threshold",action="store",default=0.0001, help="energy difference between unique conformers for the first filter of only E (default 0.0001)")
	parser.add_argument("--max_MolWt", help="Max. molecular weight of molecule", default=10000, type=int, metavar="max_MolWt")
	parser.add_argument("--ani_method", help="Specify ANI method used (i.e. ANI1x, ANI1ccx, ANI2x)", default='ANI2x', dest="ani_method", type=str)
	parser.add_argument("--STACKSIZE", help="STACKSIZE for optimization of large systems", default="1G")
	parser.add_argument("--xtb_method", help="Specify xTB method used", default='GFN2-xTB', dest="xtb_method", type=str)
	parser.add_argument("--xtb_solvent", help="Specify GBSA solvent used", default='none', dest="xtb_solvent", type=str)
	parser.add_argument("--xtb_accuracy", help="Numerical accuracy of the xTB calculation", action="store", default=1.0, dest="xtb_accuracy")
	parser.add_argument("--xtb_electronic_temperature", help="Electronic temperature for TB methods", action="store", default=300.0, dest="xtb_electronic_temperature")
	parser.add_argument("--xtb_max_iterations", help="Numerical accuracy of the xTB calculation", action="store", default=250, dest="xtb_max_iterations")

	#argument for FULLMONTE
	parser.add_argument("--ewin_sample_fullmonte", action="store",default=2.0, help="energy window to consider conformers for sampling in FULLMONTE (default 2 kcal/mol)", type=float)
	parser.add_argument("--ewin_fullmonte", action="store",default=5.0, help="energy window to consider conformers for FULLMONTE (default 5 kcal/mol)", type=float)
	parser.add_argument("--nsteps_fullmonte", action="store",default=100, help="Number of step to consider for FULLMONTE (default 100)", type=int)
	parser.add_argument("--nrot_fullmonte", action="store",default=3, help="Number of diherals to rotate for FULLMONTE (default 3) ", type=int)
	parser.add_argument("--ang_fullmonte", action="store",default=30, help="Angle to rotate each diheral of for FULLMONTE (default 30)", type=float)

	#arguments for QPREP
	parser.add_argument("-l", "--level_of_theory",help="Level of Theory", default=['wb97xd'], dest="level_of_theory", type=str, nargs='*')
	parser.add_argument("--basis_set",  help="Basis Set", default=['6-31g*'], dest="basis_set", type=str, nargs='*')
	parser.add_argument("--basis_set_genecp_atoms",default=[''], help="Basis Set genecp/gen: Can specify only one as basis_set", dest="basis_set_genecp_atoms", type=str, nargs='?')
	parser.add_argument("--input_for_gauss",  help="Input line for DFT optimization ", default="None", dest="input_for_gauss")
	parser.add_argument("--genecp_atoms",  help="genecp atoms",default=[], dest="genecp_atoms",type=str, nargs='*')
	parser.add_argument("--gen_atoms",  help="gen atoms",default=[], dest="gen_atoms",type=str, nargs='*')
	parser.add_argument("--max_cycle_opt", help="Number of cycles for DFT optimization", default="100", type=int, dest="max_cycle_opt")
	parser.add_argument("--frequencies",action="store_true", default=True, help="Request only optimization without any frequency calculation")
	parser.add_argument("--single_point",action="store_true", default=False, help="Request only single point calculation")
	parser.add_argument("--calcfc",action="store_true", default=False, help="Request calcfc in the optimization")
	parser.add_argument("--lowest_only", action="store_true", default=False, help="Lowest conformer to write for gaussian")
	parser.add_argument("--lowest_n", action="store_true", default=False, help="Lowest Number of conformers to write for gaussian")
	parser.add_argument("--energy_threshold_for_gaussian", help="cutoff for considering sampled conformers for gaussian input", default="100.0", type=float, dest="energy_threshold_for_gaussian")
	parser.add_argument("--empirical_dispersion",  help="Type of Dispersion ", default="None", dest="empirical_dispersion", type=str)
	parser.add_argument("--solvent_model",  help="Type of solvent model", default="gas_phase", dest="solvent_model", type=str)
	parser.add_argument("--solvent_name",  help="Name of Solvent", default="Acetonitrile", dest="solvent_name", type=str)
	parser.add_argument("--nprocs", help="Number of Processors", default=24, type=int, dest="nprocs")
	parser.add_argument("--mem", help="Memory", default="96GB", type=str, dest="mem")
	parser.add_argument("--chk", action="store_true", default=False, help="Create .chk files for Gaussian")
	parser.add_argument("--last_line_for_input",  help="Last input line for DFT optimization ", default="None", dest="last_line_for_input", type=str)

	#other options for QPREP
	parser.add_argument("--com_from_xyz", action="store_true", default=False, help="Create input files for Gaussian from an xyz file")

	#arguments for QCORR including the ones from QPREP
	#analysis of files
	parser.add_argument("--dup",action="store_true",default=False, help="Remove Duplicates after DFT optimization")
	#sorting of files
	parser.add_argument("--amplitude_ifreq", action="store",default=0.2, help="amplitude use to displace the imaginary frequencies to fix during analysis", type=float)
	parser.add_argument("--ifreq_cutoff", action="store",default=0.0, help="Cut off for imaginary frequencies during analysis", type=float)
	#writing single point files
	parser.add_argument("--sp", action="store_true", default=False, help="Resubmit Gaussian single point input files")
	parser.add_argument("--level_of_theory_sp",help="Level of Theory for single point after optimization", default=['wb97xd'], dest="level_of_theory_sp", type=str, nargs='*')
	parser.add_argument("--basis_set_sp",  help="Basis Set for single point after optimization", default=['6-31g*'], dest="basis_set_sp", type=str, nargs='*')
	parser.add_argument("--genecp_atoms_sp",  help="genecp atoms for single-point calculations",default=[], dest="genecp_atoms_sp",type=str, nargs='*')
	parser.add_argument("--gen_atoms_sp",  help="gen atoms for single-point calculations",default=[], dest="gen_atoms_sp",type=str, nargs='*')
	parser.add_argument("--basis_set_genecp_atoms_sp",default=['LANL2DZ'], help="Basis Set genecp/gen: Can specify only one for single point after optimization", dest="basis_set_genecp_atoms_sp", type=str, nargs='?')
	parser.add_argument("--empirical_dispersion_sp",  help="Type of Dispersion for single point after optimization", default="None", dest="empirical_dispersion_sp", type=str)
	parser.add_argument("--solvent_model_sp",  help="Type of solvent model for single point after optimization", default="gas_phase", dest="solvent_model_sp", type=str)
	parser.add_argument("--solvent_name_sp",  help="Name of Solvent for single point after optimization", default="Acetonitrile", dest="solvent_name_sp", type=str)
	parser.add_argument("--input_for_sp",  help="Input line for Single point after DFT optimization ", default="", dest="input_for_sp", type=str)
	parser.add_argument("--last_line_for_sp",  help="Last input line for Single point after DFT optimization ", default="", dest="last_line_for_sp", type=str)
	parser.add_argument("--charge_sp", help="The charge for single point calculation", default="None", metavar="charge_sp")
	parser.add_argument("--mult_sp", help="The multiplicity for single point calculation", default="None", metavar="mult_sp")
	parser.add_argument("--suffix_sp", help="The suffix for single point calculation", default="None", type=str, metavar="suffix_sp")

	#argumets for QSTAT
	parser.add_argument("--rot_dihedral", action="store_true", default=False, help="Turn on for tracking the geometric parameters for the rotatable dihedrals (Need not specify anything in the dihedral list)")
	parser.add_argument("--dihedral", help="Specify the atom indexes to track dihedrals for different conformes only for specific dihedrals (For all rotatable dihedrals turn rot_dihedral to True)", default=[], dest="dihedral", type=str, nargs=4,action='append')
	parser.add_argument("--bond", help="Specify the atom indexes to track bond lengths for different conformers", default=[], dest="bond", type=str, nargs=2,action='append')
	parser.add_argument("--angle", help="Specify the atom indexes to track angles for different conformers", default=[], dest="angle", type=str, nargs=3,action='append')
	parser.add_argument("--geom_par_name",action="store",dest="geom_par_name", default="descp", help="Change the prefix for the descriptors obtained")

	#arguments for nmr
	parser.add_argument("--nmr_exp", default='fromsdf', help="From where the ecperimental NMR details will be obtained",choices=['fromsdf','exp_file'])
	parser.add_argument("--nmr_exp_file", dest="nmr_exp_file", action="store", help="Specify the NMR experimental file", default="No file passed")
	parser.add_argument("--nmr_online", action="store_true", default=False, help="Turn to true for checking NMR scaling factors from ChesHire Database")
	parser.add_argument("--nmr_aos", help="Specify the type of atomic basis used for nmr calculation (default = giao) ", default='giao', type=str)
	parser.add_argument("--nmr_nucleus",help="Specify the nucleus for nmr analysis default (['C','H'])", default=['C','H'], dest="nmr_nucleus", type=str, nargs='*')
	parser.add_argument("--nmr_slope",help="Specify the slope for each nucleus for nmr analysis default([1.0673,1.0759])", default=[1.0673,1.0759], dest="nmr_slope", type=float, nargs='*')
	parser.add_argument("--nmr_intercept",help="Specify the intercept for each nucleus for nmr analysis default([-15.191,-2.2094])", default=[-15.191,-2.2094], dest="nmr_intercept", type=float, nargs='*')
	parser.add_argument("--nmr_tms_ref",help="Specify the reference for TMS for each nucleus for nmr analysis default([189.504625,31.56496667])", default=[189.504625,31.56496667], dest="nmr_tms_ref", type=float, nargs='*')

	# parser.add_argument("--nmr_nucleus",help="Specify the nucleus for nmr analysis default (['1H'])", default=['1H'], dest="nmr_nucleus", type=str, nargs='*')
	# parser.add_argument("--nmr_slope",help="Specify the slope for each nucleus for nmr analysis default([1.0759])", default=[1.0759], dest="nmr_slope", type=float, nargs='*')
	# parser.add_argument("--nmr_intercept",help="Specify the intercept for each nucleus for nmr analysis default([-2.2094])", default=[-2.2094], dest="nmr_intercept", type=float, nargs='*')
	# parser.add_argument("--nmr_tms_ref",help="Specify the reference for TMS for each nucleus for nmr analysis default([31.56496667])", default=[31.56496667], dest="nmr_tms_ref", type=float, nargs='*')

	# submission of Gaussion files
	parser.add_argument("--qsub", action="store_true", default=False, help="Submit Gaussian files when they are created")
	parser.add_argument("--qsub_ana", action="store_true", default=False, help="Submit Gaussian files after analysis")
	parser.add_argument("--submission_command",  help="Queueing system that the submission is done on", default="qsub_summit", metavar="submission_command", type=str)

	#apply exp rules
	parser.add_argument("--exp_rules", dest="exp_rules", default=False, help="Discarding rules applied to filter-off conformers (based on experimental observation for example). Format: ['ATOM1-ATOM2-ATOM3, ANGLE'] (i.e. ['C-Pd-C, 180'])")
	parser.add_argument("--angle_off", type=float, help="Deviation to discard in exp_rules (i.e. 180 +- 30 degrees)",default=30)

	##### further additions #####
	#NCI complex
	parser.add_argument("--nci_complex", action="store_true", default=False, help="Request NCI complexes")
	parser.add_argument("--prefix", help="Prefix for naming files", default="None", metavar="prefix",type=str)

	args = parser.parse_args()
	return args

def possible_atoms():
	possible_atoms = ["", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si",
					 "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
					 "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd",
					 "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm",
					 "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt",
					 "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu",
					 "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
					 "Rg", "Uub", "Uut", "Uuq", "Uup", "Uuh", "Uus", "Uuo"]
	return possible_atoms
