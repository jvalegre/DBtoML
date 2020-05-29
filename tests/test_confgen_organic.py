#!/usr/bin/env python

######################################################.
# 		        Testing with pytest: 	             #
#     Conformer generation of organic molecules      #
######################################################.

import os
import pytest
from definitions_testing import conf_gen

# saves the working directory
path_organic = os.getcwd()
# decimal digits for comparing E
precision_organic = 5

# tests for individual organic molecules and metal complexes
@pytest.mark.parametrize("folder, smiles, params_file, n_confs, prefilter_confs_rdkit, filter_confs_rdkit, E_confs, charge, multiplicity, dihedral, xTB_ANI1",
[
    # tests for conformer generation with RDKit, xTB and ANI1
    ('Organic_molecules', 'pentane.smi', 'params_test1.yaml', 240, 236, 0, [-5.27175,-4.44184,-3.84858,-1.57172], 0, 1, False, False), # test sample = 'auto', auto_sample = 20
    ('Organic_molecules', 'pentane.smi', 'params_test2.yaml', 20, 17, 0, [-5.27175, -4.44184, -3.84858], 0, 1, False, False), # test sample = 20
    ('Organic_molecules', 'pentane.smi', 'params_test3.yaml', 20, 5, 11, [-5.27175, -4.44184, -4.44184, -3.84858], 0, 1, False, False), # test initial_energy_threshold = 1E-10
    ('Organic_molecules', 'pentane.smi', 'params_test4.yaml', 20, 11, 0, [-5.27175, -5.27175, -5.27175, -5.27175, -5.27175, -4.44184, -4.44184, -4.44184, -3.84858], 0, 1, False, False), # test energy_threshold = 1E-15
    ('Organic_molecules', 'pentane.smi', 'params_test5.yaml', 20, 11, 0, [-5.27175, -5.27175, -5.27175, -5.27175, -5.27175, -4.44184, -4.44184, -4.44184, -3.84858], 0, 1, False, False), # test rms_threshold = 1E-15
    ('Organic_molecules', 'pentane.smi', 'params_test6.yaml', 20, 5, 9, [-5.27175, -4.44184, -4.44184, -4.44184, -4.44184, -3.84858], 0, 1, False, False),
    ('Organic_molecules', 'pentane.smi', 'params_test7.yaml', 60, 56, 0, [-5.27175, -4.44184, -3.84858, -1.57172], 0, 1, False, False), # test sample = 'auto', auto_sample = 5
    ('Organic_molecules', 'pentane.smi', 'params_test8.yaml', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', False, False), # test max_torsions = 1
    ('Organic_molecules', 'pentane.smi', 'params_test9.yaml', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', False, False), # test max_MolWt = 1
    ('Organic_molecules', 'pentane.smi', 'params_test10.yaml', 20, 17, 0, [2.52059, 3.68961, 4.94318], 0, 1, False, False), # test ff = 'UFF'
    ('Organic_molecules', 'pentane.smi', 'params_test11.yaml', 20, 1, 12, [-5.27113, -4.44046, -4.43598, -4.06762, -3.90769, -3.81966, -2.53933], 0, 1, False, False), # test opt_steps_RDKit = 40
    ('Organic_molecules', 'pentane.smi', 'params_test12.yaml', 20, 16, 0, [-5.27175,-4.44184,-3.84858,-1.57172], 0, 1, False, True), # test xTB = True
    ('Organic_molecules', 'pentane.smi', 'params_test13.yaml', 20, 16, 0, [-5.27175,-4.44184,-3.84858,-1.57172], 0, 1, False, True), # test ANI1ccx = True
    ('Organic_molecules', 'pentane.smi', 'params_test14.yaml', 20, 17, 0, [-5.27175, -4.44184], 0, 1, False, False), # ewin = 1
    ('Organic_molecules', 'pentane.smi', 'params_test15.yaml', 27, 'nan', 4, [-5.27175,-4.44184,-3.84858,-1.57172], 0, 1, True, False), # test dihedral scan
    ('Organic_molecules', 'pentane.smi', 'params_test16.yaml', 20, 17, 0, [-5.27175, -4.44184, -3.84858], 0, 3, False, False), # test multiplicity = 3
])

def test_confgen_organic(folder, smiles, params_file, n_confs, prefilter_confs_rdkit, filter_confs_rdkit, E_confs, charge, multiplicity, dihedral, xTB_ANI1):
    # runs the program with the different tests
    cmd_organic = ['python', '-m', 'pyconfort', '--varfile', params_file]

    test_init_rdkit_confs,test_prefilter_rdkit_confs,test_filter_rdkit_confs,round_confs,test_round_confs,test_charge,test_unique_confs,count,charge_com,multiplicity_com = conf_gen(path_organic, precision_organic, cmd_organic, folder, smiles, E_confs, dihedral, xTB_ANI1, metal=False, template=False)

    # the assert statements are placed here, otherwise pytest doesn't explain the AssertionError
    # first, dicard tests 8 and 9 since they are designed to fail
    if n_confs != 'nan':
        # dihedral vs no dihedral scans
        if not dihedral:
            assert str(n_confs) == str(test_init_rdkit_confs[0])
            assert str(prefilter_confs_rdkit) == str(test_prefilter_rdkit_confs[0])
            assert str(filter_confs_rdkit) == str(test_filter_rdkit_confs[0])
        else:
            assert str(n_confs) == str(test_init_rdkit_confs[0])
            # I use the filter_confs_rdkit variable to assert for unique confs in dihedral scan
            assert str(filter_confs_rdkit) == str(test_unique_confs[0])

        assert str(round_confs) == str(test_round_confs)
        assert str(charge) == str(test_charge[0])

        # make sure the COM files have the right charge and multiplicity
        assert str(charge_com) == str(charge)
        assert str(multiplicity_com) == str(multiplicity)

    elif params_file == 'params_test8.yaml' or params_file == 'params_test9.yaml':
        assert str(test_filter_rdkit_confs) == 'nan'
        assert str(test_round_confs) == 'nan'

    else:
        assert 3 ==2
