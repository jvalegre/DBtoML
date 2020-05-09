"""

* In this file, the paths to helper programs are collected.
* You mus t make sure that all the variables are correct before launching db_gen.py.

* OTHER functions USED THROUGHOUT THE PROGRAM ARE ALSO SET HERE.

"""
from DBGEN.confgen import *

possible_atoms = ["", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si",
				 "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
				 "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd",
				 "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm",
				 "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt",
				 "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu",
				 "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
				 "Rg", "Uub", "Uut", "Uuq", "Uup", "Uuh", "Uus", "Uuo"]
columns = ['Structure', 'E', 'ZPE', 'H', 'T.S', 'T.qh-S', 'G(T)', 'qh-G(T)']

"CLASS FOR LOGGING  "
class Logger:
    def __init__(self, filein, append):
        suffix = 'dat'
        self.log = open('{0}_{1}.{2}'.format(filein, append, suffix), 'w')

    def write(self, message):
        print(message, end='\n')
        self.log.write(message+ "\n")

    def fatal(self, message):
        print(message, end='\n')
        self.log.write(message + "\n")
        self.finalize()
        sys.exit(1)

    def finalize(self):
        self.log.close()

" SUBSTITUTION WITH I"
def substituted_mol(smi,args,log):
	mol = Chem.MolFromSmiles(smi)
	for atom in mol.GetAtoms():
		if atom.GetSymbol() in args.metal:
			args.metal_sym.append(atom.GetSymbol() )
			atom.SetAtomicNum(53)
			if len(atom.GetNeighbors()) == 2:
				atom.SetFormalCharge(-3)
			if len(atom.GetNeighbors()) == 3:
				atom.SetFormalCharge(-2)
			if len(atom.GetNeighbors()) == 4:
				atom.SetFormalCharge(-1)
			if len(atom.GetNeighbors()) == 5:
				atom.SetFormalCharge(0)
			if len(atom.GetNeighbors()) == 6:
				atom.SetFormalCharge(1)
			if len(atom.GetNeighbors()) == 7:
				atom.SetFormalCharge(2)
			if len(atom.GetNeighbors()) == 8:
				atom.SetFormalCharge(3)
			args.metal_idx.append(atom.GetIdx())
			args.complex_coord.append(len(atom.GetNeighbors()))
	return mol,args.metal_idx,args.complex_coord,args.metal_sym

"TEMPLATE GENERATION FOR SQUAREPLANAR AND SQUAREPYRIMIDAL "
def template_embed_sp(molecule,temp,name_input,args,log):
	mol_objects = [] # a list of mol objects that will be populated
	name_return = []
	coord_Map = []

	alg_Map = []
	mol_template = []

	for atom in molecule.GetAtoms():
		if atom.GetSymbol() == 'I'and (len(atom.GetBonds()) == 6 or len(atom.GetBonds()) == 5 or len(atom.GetBonds()) == 4 or len(atom.GetBonds()) == 3 or len(atom.GetBonds()) == 2):
			if len(atom.GetBonds()) == 5:
				atom.SetAtomicNum(53)
			if len(atom.GetBonds()) == 4:
				atom.SetAtomicNum(14)
			center_idx = atom.GetIdx()
			neighbours = atom.GetNeighbors()

	number_of_neighbours = len(neighbours)

	#log.write(number_of_neighbours)
	if number_of_neighbours == 4:
		#three cases for square planar
		for name in range(3):
			#assigning neighbours
			for atom in molecule.GetAtoms():
				if atom.GetIdx() == center_idx:
					neighbours = atom.GetNeighbors()
			#assugning order of replacement
			if name == 0:
				j = [1,2,3]
			elif name == 1:
				j = [2,3,1]
			elif name == 2:
				j = [3,1,2]
			#checking for same atom neighbours and assigning in the templates for all mols in suppl!
			for mol_1 in temp:
				for atom in mol_1.GetAtoms():
					#log.write(atom.GetSymbol()+'mol_1 atom')
					if atom.GetSymbol() == 'F':
						mol_1 = Chem.RWMol(mol_1)
						idx = atom.GetIdx()
						mol_1.RemoveAtom(idx)
						mol_1 = mol_1.GetMol()

				site_1,site_2,site_3,site_4,metal_site  = 0,0,0,0,0
				for atom in mol_1.GetAtoms():
					#log.write(atom.GetIdx(), atom.GetSymbol())
					#log.write(atom.GetSymbol()+'after remove F from mol_1')
					if atom.GetIdx() == 4 and metal_site == 0:
						atom.SetAtomicNum(14)
						center_temp = atom.GetIdx()
						metal_site = 1
					if atom.GetIdx() == 0 and site_1 == 0:
						atom.SetAtomicNum(neighbours[0].GetAtomicNum())
						site_1 = 1
					if atom.GetIdx() == 3 and site_2 == 0:
						atom.SetAtomicNum(neighbours[j[0]].GetAtomicNum())
						site_2 = 1
					if atom.GetIdx() == 2 and site_3 == 0:
						atom.SetAtomicNum(neighbours[j[1]].GetAtomicNum())
						site_3 = 1
					if atom.GetIdx() == 1 and site_4 == 0 :
						atom.SetAtomicNum(neighbours[j[2]].GetAtomicNum())
						site_4 = 1

				# #log.write to see if it is changed
				# for atom in mol_1.GetAtoms():
				# 	log.write(atom.GetSymbol()+'match')

				#embedding of the molecule onto the core
				molecule_new, coordMap, algMap = template_embed_optimize(molecule,mol_1,args,log)

				for atom in molecule_new.GetAtoms():
					if atom.GetIdx() == center_idx:
						atom.SetAtomicNum(53)
						atom.SetFormalCharge(-1)

				for atom in mol_1.GetAtoms():
					if atom.GetIdx() == center_temp:
						atom.SetAtomicNum(53)
						atom.SetFormalCharge(-1)

				#writing to mol_object file
				name_final = name_input + str(name)
				mol_objects.append(molecule_new)
				name_return.append(name_final)
				coord_Map.append(coordMap)
				alg_Map.append(algMap)
				mol_template.append(mol_1)

				# #writing to sdf file
				# sdwriter = Chem.SDWriter(str(name)+output)
				# sdwriter.write(molecule_new)
				#
				# sdwriter.close()

	if number_of_neighbours == 5:
		#fifteen cases for square pyrimidal
		for name_1 in range(5):
			for name_2 in range(3):
				#assigning neighbours
				for atom in molecule.GetAtoms():
					if atom.GetIdx() == center_idx:
						neighbours = atom.GetNeighbors()

				#assugning order of replacement for the top
				if name_1 == 0:
					k = 4
				elif name_1== 1:
					k = 3
				elif name_1 == 2:
					k = 2
				elif name_1== 3:
					k = 1
				elif name_1 == 4:
					k = 0

				#assigning order of replacement for the plane
				if name_2 == 0 and k == 4:
					j = [1,2,3]
				elif name_2 == 1 and k == 4:
					j = [2,3,1]
				elif name_2 == 2 and k == 4:
					j = [3,1,2]

				#assugning order of replacement for the plane
				if name_2 == 0 and k == 3:
					j = [1,2,4]
				elif name_2 == 1 and k == 3:
					j = [2,4,1]
				elif name_2 == 2 and k == 3:
					j = [4,1,2]

				#assugning order of replacement for the plane
				if name_2 == 0 and k == 2:
					j = [1,4,3]
				elif name_2 == 1 and k == 2:
					j = [4,3,1]
				elif name_2 == 2 and k == 2:
					j = [4,1,3]

				#assugning order of replacement for the plane
				if name_2 == 0 and k == 1:
					j = [4,2,3]
				elif name_2 == 1 and k == 1:
					j = [2,3,4]
				elif name_2 == 2 and k == 1:
					j = [3,4,2]

				#assugning order of replacement for the plane
				if name_2 == 0 and k == 0:
					j = [1,2,3]
				elif name_2 == 1 and k == 0:
					j = [2,3,1]
				elif name_2 == 2 and k == 0:
					j = [3,1,2]

				#checking for same atom neighbours and assigning in the templates for all mols in suppl!
				for mol_1 in temp:
					site_1,site_2,site_3,site_4,site_5,metal_site  = 0,0,0,0,0,0
					for atom in mol_1.GetAtoms():
						# log.write(atom.GetSymbol(), atom.GetIdx())
						#log.write(atom.GetSymbol()+'no remove F from mol_1')
						if atom.GetIdx()  == 5 and metal_site == 0:
							atom.SetAtomicNum(53)
							center_temp = atom.GetIdx()
							metal_site = 1
						if k!= 0:
							if atom.GetIdx()  == 1 and site_1 == 0:
								atom.SetAtomicNum(neighbours[0].GetAtomicNum())
								site_1 = 1
							elif atom.GetIdx()  == 2 and site_2 == 0:
								atom.SetAtomicNum(neighbours[j[0]].GetAtomicNum())
								site_2 = 1
							elif atom.GetIdx()  == 3 and site_3 == 0:
								atom.SetAtomicNum(neighbours[j[1]].GetAtomicNum())
								site_3 = 1
							elif atom.GetIdx()  == 4 and site_4 == 0:
								atom.SetAtomicNum(neighbours[j[2]].GetAtomicNum())
								site_4 = 1
							elif atom.GetIdx()  == 0 and site_5 == 0:
								atom.SetAtomicNum(neighbours[k].GetAtomicNum())
								site_5 = 1
						elif k == 0:
							if atom.GetIdx()  == 1 and site_1 == 0:
								atom.SetAtomicNum(neighbours[4].GetAtomicNum())
								site_1 = 1
							elif atom.GetIdx()  == 2 and site_2 == 0:
								atom.SetAtomicNum(neighbours[j[0]].GetAtomicNum())
								site_2 = 1
							elif atom.GetIdx()  == 3 and site_3 == 0:
								atom.SetAtomicNum(neighbours[j[1]].GetAtomicNum())
								site_3 = 1
							elif atom.GetIdx()  == 4 and site_4 == 0:
								atom.SetAtomicNum(neighbours[j[2]].GetAtomicNum())
								site_4 = 1
							elif atom.GetIdx() == 0 and site_5 == 0:
								atom.SetAtomicNum(neighbours[0].GetAtomicNum())
								site_5 = 1

					#assigning and embedding onto the core
					molecule_new, coordMap, algMap = template_embed_optimize(molecule,mol_1,args,log)

					for atom in molecule_new.GetAtoms():
						if atom.GetIdx() == center_idx:
							atom.SetAtomicNum(53)

					for atom in mol_1.GetAtoms():
						if atom.GetIdx() == center_temp:
							atom.SetAtomicNum(53)

					#writing to mol_object file
					name_final = name_input + str(name_1)+ str(name_2)
					mol_objects.append(molecule_new)
					name_return.append(name_final)
					coord_Map.append(coordMap)
					alg_Map.append(algMap)


					mol_template.append(mol_1)

					# #writing to sdf file
					# sdwriter = Chem.SDWriter(str(name_1)+str(name_2)+'.sdf')
					# sdwriter.write(molecule_new)
					# sdwriter.close()

	return mol_objects, name_return, coord_Map, alg_Map, mol_template

"TEMPLATE EMBED OPTIMIZE"
def template_embed_optimize(molecule_embed,mol_1,args,log):

	#assigning and embedding onto the core
	num_atom_match = molecule_embed.GetSubstructMatch(mol_1)
	# log.write(len(num_atom_match))
	# log.write('above match')

	#add H's to molecule
	molecule_embed = Chem.AddHs(molecule_embed)

	#definition of coordmap, the coreconfID(the firstone =-1)
	coordMap = {}
	coreConfId=-1
	randomseed=-1
	force_constant=10000

	# Choosing the type of force field
	for atom in molecule_embed.GetAtoms():
		if atom.GetAtomicNum() > 36: #upto Kr for MMFF, if not use UFF
			args.ff = "UFF"

	#making the ff definition general
	ff = args.ff

	# Force field parameters
	if ff == "MMFF":
		GetFF = lambda x,confId=-1:Chem.MMFFGetMoleculeForceField(x,Chem.MMFFGetMoleculeProperties(x),confId=confId)
	elif ff == "UFF":
		GetFF = lambda x,confId=-1:Chem.UFFGetMoleculeForceField(x)
	else: log.write('   Force field {} not supported!'.format(options.ff)); sys.exit()
	getForceField=GetFF


	# This part selects which atoms from molecule are the atoms of the core
	try:
		coreConf = mol_1.GetConformer(coreConfId)
	except:
		pass
	for k, idxI in enumerate(num_atom_match):
		core_mol_1 = coreConf.GetAtomPosition(k)
		coordMap[idxI] = core_mol_1
	# log.write(coordMap)

	# This is the original version, if it doesn't work without coordMap I'll come back to it late
	if len(num_atom_match) == 5:
		ci = Chem.EmbedMolecule(molecule_embed, coordMap=coordMap, randomSeed=randomseed)
	if len(num_atom_match) == 6:
		ci = Chem.EmbedMolecule(molecule_embed, coordMap=coordMap, randomSeed=randomseed,ignoreSmoothingFailures=True)
	if ci < 0:    log.write('Could not embed molecule.')

	#algin molecule to the core
	algMap = [(k, l) for l, k in enumerate(num_atom_match)]

	ff = getForceField(molecule_embed, confId=-1)
	for k, idxI in enumerate(num_atom_match):
		for l in range(k + 1, len(num_atom_match)):
			idxJ = num_atom_match[l]
			d = coordMap[idxI].Distance(coordMap[idxJ])
			ff.AddDistanceConstraint(idxI, idxJ, d, d, force_constant)
	ff.Initialize()
	#reassignned n from 4 to 10 for better embed and minimzation
	n = 10
	more = ff.Minimize()
	while more and n:
		more = ff.Minimize()
		n -= 1
	energy = ff.CalcEnergy()
	# rotate the embedded conformation onto the core_mol:
	rms = rdMolAlign.AlignMol(molecule_embed, mol_1, atomMap=algMap,reflect=True,maxIters=100)
	# else:
	# 	# rotate the embedded conformation onto the core_mol:
	# 	try:
	# 		rms = rdMolAlign.AlignMol(molecule_embed, mol_1, atomMap=algMap,reflect=True,maxIters=100)
	# 		ff = getForceField(molecule_embed, confId=-1)
	# 		conf_temp = mol_1.GetConformer()
	# 		for k in range(mol_1.GetNumAtoms()):
	# 			p = conf_temp.GetAtomPosition(k)
	# 			q = molecule_embed.GetConformer().GetAtomPosition(k)
	# 			pIdx = ff.AddExtraPoint(p.x, p.y, p.z, fixed=True) - 1
	# 			ff.AddDistanceConstraint(pIdx, num_atom_match[k], 0, 0, force_constant)
	# 		ff.Initialize()
	# 		n = 4
	# 		more = ff.Minimize(energyTol=1e-5, forceTol=1e-4)
	# 		while more and n:
	# 			more = ff.Minimize(energyTol=1e-5, forceTol=1e-4)
	# 			n -= 1
	# 		# realign
	# 		energy = ff.CalcEnergy()
	# 		rms = rdMolAlign.AlignMol(molecule_embed, mol_1, atomMap=algMap,reflect=True,maxIters=100)
	# 	except:
	# 		pass

	return molecule_embed, coordMap, algMap

" FUCNTION WORKING WITH MOL OBJECT TO CREATE CONFORMERS"

def conformer_generation(mol,name,start_time,args,log,dup_data,dup_data_idx,coord_Map=None,alg_Map=None,mol_template=None):
	valid_structure = filters(mol, args,log)
	if valid_structure:
		if args.verbose: log.write("\n   ----- {} -----".format(name))

		try:
			# the conformational search
			gen = summ_search(mol, name,args,log,dup_data,dup_data_idx,coord_Map,alg_Map,mol_template)
			if gen != -1:
				if args.nodihedrals == True:
					if args.ANI1ccx != False: conformers, energies = mult_min(name+'_'+'rdkit', args, 'ani',log,dup_data,dup_data_idx)
					if args.xtb != False: conformers, energies = mult_min(name+'_'+'rdkit', args, 'xtb',log,dup_data,dup_data_idx)
				else:
					if args.ANI1ccx != False: conformers, energies = mult_min(name+'_'+'rdkit'+'_'+'rotated', args, 'ani',log,dup_data,dup_data_idx)
					if args.xtb != False: conformers, energies = mult_min(name+'_'+'rdkit'+'_'+'rotated', args, 'xtb',log,dup_data,dup_data_idx)
			else: pass
		except (KeyboardInterrupt, SystemExit):
			raise
		except Exception as e: print(traceback.print_exc())
	else: log.write("ERROR: The structure is not valid")

	# removing temporary files
	temp_files = ['gfn2.out', 'xTB_opt.traj', 'ANI1_opt.traj', 'wbo', 'xtbrestart']
	for file in temp_files:
		if os.path.exists(file): os.remove(file)

	if args.time:
		log.write("\n Execution time: %s seconds" % (round(time.time() - start_time,2)))
		dup_data.at[dup_data_idx, 'time (seconds)'] = round(time.time() - start_time,2)

" RULES TO GET EXPERIMENTAL CONFORMERS"
def exp_rules_output(mol, args,log):
	passing = True
	ligand_links = []
	atom_indexes = []
	for atom in mol.GetAtoms():
		# Finds the Ir atom and gets the atom types and indexes of all its neighbours
		for el in elementspt:
			if el.symbol == args.metal:
				atomic_number = el.number
		if atom.GetAtomicNum() == atomic_number:
			metal_idx = atom.GetIdx()
			for x in atom.GetNeighbors():
				ligand_links.append(x.GetSymbol())
				atom_indexes.append(x.GetIdx())
	# I need to get the only 3D conformer generated in that mol object for rdMolTransforms
	mol_conf = mol.GetConformer(0)
	# This part will identify the pairs of C and N atoms that are part of the same Ph_Py ligand.
	# The shape of the atom pairs is '[[C1_ATOM_NUMBER, N1_ATOM_NUMBER],[C2, N2],...]'.
	# This information is required for the subsequent filtering process based on angles
	if len(atom_indexes) == args.complex_coord:
		ligand_atoms = []
		for i in range(len(atom_indexes)):
			# This is a filter that excludes molecules that fell apart during DFT geometry
			# optimization (i.e. a N atom from one of the ligands separated from Ir). The
			# max distance allowed can be tuned in length_filter
			bond_length = rdMolTransforms.GetBondLength(mol_conf,metal_idx,atom_indexes[i])
			length_filter = 2.25
			if bond_length > length_filter:
				passing = False
				break
			for j in range(len(atom_indexes)):
				# Avoid combinations of the same atom with itself
				if atom_indexes[i] != atom_indexes[j]:
					# We know that the ligands never have 2 carbon atoms bonding the Ir atom. We
					# only use atom_indexes[i] for C atoms, and atom_indexes[j] for the potential
					# N atoms that are part of the same Ph_Py ligand
					if ligand_links[i] == 'C' and atom_indexes[j] != 'C':
						# This part detects the Ir-C bond and breaks it, breaking the Ph_Py ring
						bond = mol.GetBondBetweenAtoms(atom_indexes[i], metal_idx)
						new_mol = Chem.FragmentOnBonds(mol, [bond.GetIdx()],addDummies=True, dummyLabels=[(atom_indexes[i], metal_idx)])
						# Now, identify whether or not the initial 5-membered ring formed between
						# [-Ir-C-C-C-N-] is broken when we break the Ir-C bond. This works
						# because Ph_Py units bind Ir in the same way always, through 1 C and 1 N
						# that are in the same position, forming a 5-membered ring.
						# If this ring is broken, atom_indexes[j] will not be part of a
						# 5-membered ring (atom.IsInRingSize(5) == False) which means that
						# this atom was initially inside the same ligand as the
						# parent C of atom_indexes[i])
						if new_mol.GetAtomWithIdx(atom_indexes[j]).IsInRingSize(5) == False:
							# This will append pairs of atoms indexes in the form:
							# '[idx for C, idx for N]', where the couples are C and N atoms that
							# are part of the same Ph_Py ligand
							ligand_atoms.append([atom_indexes[i],atom_indexes[j]])
							break
						else:
							# An additional filter just in case the N is part of a 5-membered
							# ring besides the 5-membered ring that forms with Ir
							bond_2 = mol.GetBondBetweenAtoms(atom_indexes[j], metal_idx)
							new_mol_2 = Chem.FragmentOnBonds(mol, [bond_2.GetIdx()],addDummies=True, dummyLabels=[(atom_indexes[j], metal_idx)])
							if new_mol_2.GetAtomWithIdx(atom_indexes[i]).IsInRingSize(5) == False:
								ligand_atoms.append([atom_indexes[i],atom_indexes[j]])
								break
		if passing == True:
			# This stop variable and the breaks inside the inner loops will make that if there
			# is one angle that does not meet the criteria for valid conformers, the outter (i)
			# and inner (j) loops will stop simultaneously (saves time since the molecule is
			# already an invalid geometry, it does not make sense to keep iterating)
			stop = False
			# For complexes with 3 Ph_Py ligands:
			if len(ligand_atoms) == 3:
				for i in range(len(ligand_atoms)):
					if stop != True:
						for j in range(len(ligand_atoms)):
							# the i<=j part avoids repeating atoms, the i != j part avoid angles
							# containing the same number twice (i.e. 4-16-4, this angle will fail)
							if i <= j and i != j:
								# Calculate the angle between 2 N atoms from different Ph_Py ligands.
								# When there are 3 Ph_Py ligands, no 2 N atoms must be in 180 degrees
								angle = rdMolTransforms.GetAngleDeg(mol_conf,ligand_atoms[i][1],metal_idx,ligand_atoms[j][1])
								if (180 - args.angle_off) <= angle <= (180 + args.angle_off):
									passing = False
									break
			# For complexes with 2 Ph_Py ligands + 1 ligand that is not Ph_Py
			if len(ligand_atoms) == 2:
				# Since there are only 2 N atoms, we do not need to include a nested loop
					angle = rdMolTransforms.GetAngleDeg(mol_conf,ligand_atoms[0][1],metal_idx,ligand_atoms[1][1])
					# Calculate the angle between 2 N atoms from different Ph_Py ligands.
					# When there are 2 Ph_Py ligands, the 2 N atoms from the 2 Ph_Py ligands
					# must be in 180 degrees
					if (180 - args.angle_off) <= angle <= (180 + args.angle_off):
						pass
					else:
						passing = False
	# This is a second filter that excludes molecules that fell apart during DFT geometry
	# optimization (i.e. a N atom from one of the ligands separated from Ir). In this case,
	# it filters off molecules that the SDF only detects 5 Ir neighbours
	else:
		passing = False
	return passing

" FILTER TO BE APPLIED FOR SMILES"
def filters(mol,args,log):
	valid_structure = True
	# First filter: number of rotatable bonds-bonds
	if Lipinski.NumRotatableBonds(mol) < args.num_rot_bonds:
		# Second filter: molecular weight
		if Descriptors.MolWt(mol) < args.max_MolWt:
			# Third filter: this filters salts off (2 separated components)
			#if len(Chem.MolToSmiles(mol).split('.')) == 1:
			for atom in mol.GetAtoms():
				#Fourth filter: atoms outside the scope chosen in 'possible_atoms'
				if atom.GetSymbol() not in possible_atoms:
					valid_structure = False
					if args.verbose == True: log.write(" Exiting as atom isn't in atoms in the periodic table")
			#else: valid_structure = False
		else:
			valid_structure = False
			if args.verbose == True: log.write(" Exiting as total molar mass > 1000")
	else:
		valid_structure = False
		if args.verbose == True: log.write(" Exiting as number of rotatable bonds > 10")
	return valid_structure

"PARSES THE ENERGIES FROM SDF FILES"
def read_energies(file,log): # parses the energies from sdf files - then used to filter conformers
	energies = []
	f = open(file,"r")
	readlines = f.readlines()
	for i in range(len(readlines)):
		if readlines[i].find('>  <Energy>') > -1:
			energies.append(float(readlines[i+1].split()[0]))
	f.close()
	return energies

" MAIN FUNCTION TO CREATE GAUSSIAN JOBS"
def write_gaussian_input_file(file, name,lot, bs, bs_gcp, energies, args,log,charge_data):

	#find location of molecule and respective scharges
	name_list = name.split('_')
	if 'xtb' or 'ani' in name_list:
		name_molecule = name[:-4]
	if 'rdkit' in name_list:
		name_molecule = name[:-6]
	if 'rdkit_rotated' in name_list:
		name_molecule = name[:-14]

	for i in range(len(charge_data)):
		if charge_data.loc[i,'Molecule'] == name_molecule:
			charge_com = charge_data.loc[i,'Overall charge']

	#definition of input lines
	if args.frequencies == True:
		if args.dispersion_correction == True:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0}) freq=noraman empiricaldispersion={1}'.format(args.max_cycle_opt,args.empirical_dispersion)
				input_sp = 'nmr=giao empiricaldispersion={0}'.format(args.empirical_dispersion)  #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) freq=noraman scrf=({1},solvent={2}) empiricaldispersion={3}'.format(args.max_cycle_opt, args.solvent_model, args.solvent_name,args.empirical_dispersion ) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao empiricaldispersion={2}'.format(args.solvent_model, args.solvent_name, args.empirical_dispersion)  ##add solvent if needed
		else:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0}) freq=noraman'.format(args.max_cycle_opt)
				input_sp = 'nmr=giao ' #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) freq=noraman scrf=({1},solvent={2})'.format(args.max_cycle_opt,args.solvent_model, args.solvent_name) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao'.format(args.solvent_model, args.solvent_name)  ##add solvent if needed
	else:
		if args.dispersion_correction == True:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0}) empiricaldispersion={1}'.format(args.max_cycle_opt,args.empirical_dispersion)
				input_sp = 'nmr=giao empiricaldispersion={0}'.format(args.empirical_dispersion)  #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) scrf=({1},solvent={2}) empiricaldispersion={3}'.format(args.max_cycle_opt,args.solvent_model, args.solvent_name,args.empirical_dispersion ) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao empiricaldispersion={2}'.format(args.solvent_model, args.solvent_name, args.empirical_dispersion)  ##add solvent if needed
		else:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0})'.format(args.max_cycle_opt)
				input_sp = 'nmr=giao ' #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) scrf=({1},solvent={2})'.format(args.max_cycle_opt,args.solvent_model, args.solvent_name) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao'.format(args.solvent_model, args.solvent_name)  ##add solvent if needed

	#defining genecp
	genecp = 'None'

	try:
		#reading the sdf to check for I atom_symbol
		suppl = Chem.SDMolSupplier(file)
		for atom in suppl[0].GetAtoms():
			if atom.GetSymbol() in args.genecp_atoms:
				genecp = 'genecp'
				break
			elif atom.GetSymbol() in args.gen_atoms:
				genecp = 'gen'
				break
	except:
		read_lines = open(file,"r").readlines()
		for line in range(len(read_lines)):
			for atom in args.genecp_atoms:
				if read_lines[line].find(atom)>-1:
					genecp = 'genecp'
					break
			for atom in args.gen_atoms:
				if read_lines[line].find(atom)>-1:
					genecp = 'gen'
					break

	if args.single_point == True:
		#pathto change to
		path_write_gjf_files = 'generated_sp_files/' + str(lot) + '-' + str(bs)
		#log.write(path_write_gjf_files)
		os.chdir(path_write_gjf_files)
	else:
		#pathto change to
		path_write_gjf_files = 'generated_gaussian_files/' + str(lot) + '-' + str(bs)
		#log.write(path_write_gjf_files)
		os.chdir(path_write_gjf_files)

	path_for_file = '../../'

	com = '{0}_.com'.format(name)
	com_low = '{0}_low.com'.format(name)

	com_sdf = '{0}_.sdf'.format(name)
	com_low_sdf = '{0}_low.sdf'.format(name)

	if genecp =='genecp' or genecp == 'gen':
		#chk option
		if args.chk == True:
			if args.single_point == True:
				header = [
					'%chk={}.chk'.format(name),
					'%mem={}'.format(args.mem),
					'%nprocshared={}'.format(args.nprocs),
					'# {0}'.format(lot)+ '/'+ genecp + ' '+ input_sp ]
			else:
				header = [
						'%chk={}.chk'.format(name),
						'%mem={}'.format(args.mem),
						'%nprocshared={}'.format(args.nprocs),
						'# {0}'.format(lot)+ '/'+ genecp + ' '+ input ]

		else:
			if args.single_point == True:
				header = [
					'%mem={}'.format(args.mem),
					'%nprocshared={}'.format(args.nprocs),
					'# {0}'.format(lot)+ '/'+ genecp + ' '+ input_sp ]
			else:
				header = [
					'%mem={}'.format(args.mem),
					'%nprocshared={}'.format(args.nprocs),
					'# {0}'.format(lot)+ '/'+ genecp + ' '+ input ]

		if args.lowest_only == True:
			subprocess.run(
				  ['obabel', '-isdf', path_for_file+file, '-ocom', '-O'+com_low,'-l' , '1', '-xk', '\n'.join(header)]) #takes the lowest conformer which is the first in the file
		elif args.lowest_n == True:
			no_to_write = 0
			if len(energies) != 1:
				for i in range(len(energies)):
					energy_diff = energies[i] - energies[0]
					if energy_diff < args.energy_threshold_for_gaussian: # thershold is in kcal/mol and energies are in kcal/mol as well
						no_to_write +=1
				subprocess.run(
					 ['obabel', '-isdf', path_for_file+file, '-f', '1', '-l' , str(no_to_write), '-osdf', '-Otemp.sdf'])
				subprocess.run(
					  ['obabel', '-isdf', 'temp.sdf', '-ocom', '-O'+com,'-m', '-xk', '\n'.join(header)])
			else:
				subprocess.run(
					  ['obabel', '-isdf', path_for_file+file, '-ocom', '-O'+com,'-m', '-xk', '\n'.join(header)])
		else:
			subprocess.run(
				  ['obabel', '-isdf', path_for_file+file, '-ocom', '-O'+com,'-m', '-xk', '\n'.join(header)])

		#adding the basis set at the end of the FILES
		#grab all the com FILES
		com_files = glob.glob('{0}_*.com'.format(name))

		for file in com_files:
			ecp_list,ecp_genecp_atoms,ecp_gen_atoms = [],False,False
			read_lines = open(file,"r").readlines()

			#chaanging the name of the files to the way they are in xTB Sdfs
			#getting the title line
			for i in range(0,len(read_lines)):
				if len(read_lines[i].strip()) == 0:
					title_line = read_lines[i+1]
					title_line = title_line.lstrip()
					rename_file_name = title_line.replace(" ", "_")
					break

			rename_file_name = rename_file_name.strip()+'.com'

			#change charge and multiplicity for Octahydrasl
			if args.metal_complex == True:
				for i in range(0,len(read_lines)):
					if len(read_lines[i].strip()) == 0:
						read_lines[i+3] = str(charge_com)+' '+ str(args.complex_spin)+'\n'
						break
				out = open(file, 'w')
				out.writelines(read_lines)
				out.close()
				read_lines = open(file,"r").readlines()

			fileout = open(file, "a")
			# Detect if there are I atoms to use genecp or not (to use gen)
			for i in range(4,len(read_lines)):
				if read_lines[i].split(' ')[0] not in ecp_list and read_lines[i].split(' ')[0] in possible_atoms:
					ecp_list.append(read_lines[i].split(' ')[0])
				if read_lines[i].split(' ')[0] in args.genecp_atoms:
				   ecp_genecp_atoms = True
				if read_lines[i].split(' ')[0] in args.gen_atoms:
				   ecp_gen_atoms = True

			#error if both genecp and gen are
			if ecp_genecp_atoms == True and ecp_gen_atoms == True:
				sys.exit("ERROR: Can't use Gen and GenECP at the same time")

			for i in range(len(ecp_list)):
				if ecp_list[i] not in (args.genecp_atoms or args.gen_atoms):
					fileout.write(ecp_list[i]+' ')
			fileout.write('0\n')
			fileout.write(bs+'\n')
			fileout.write('****\n')
			if ecp_genecp_atoms == False and ecp_gen_atoms == False :
				fileout.write('\n')
			else:
				if len(bs_gcp.split('.')) > 1:
					if bs_gcp.split('.')[1] == 'txt':
						os.chdir(path_for_file)
						read_lines = open(bs_gcp,"r").readlines()
						os.chdir(path_write_gjf_files)
						#chaanging the name of the files to the way they are in xTB Sdfs
						#getting the title line
						for line in read_lines:
							fileout.write(line)
						fileout.write('\n\n')
				else:
					for i in range(len(ecp_list)):
						if ecp_list[i] in args.genecp_atoms :
							fileout.write(ecp_list[i]+' ')
						elif ecp_list[i] in args.gen_atoms :
							fileout.write(ecp_list[i]+' ')
					fileout.write('0\n')
					fileout.write(bs_gcp+'\n')
					fileout.write('****\n\n')
					if ecp_genecp_atoms == True:
						for i in range(len(ecp_list)):
							if ecp_list[i] in args.genecp_atoms:
								fileout.write(ecp_list[i]+' ')
					fileout.write('0\n')
					fileout.write(bs_gcp+'\n\n')
			fileout.close()

			#change file by moving to new file
			os.rename(file,rename_file_name)

			#submitting the gaussian file on summit
			if args.qsub == True:
				os.system(args.submission_command + rename_file_name)

		os.chdir(path_for_file)

	else:
		#chk option
		if args.chk == True:
			if args.single_point == True:
				header = [
					'%chk={}.chk'.format(name),
					'%mem={}'.format(args.mem),
					'%nprocshared={}'.format(args.nprocs),
					'# {0}'.format(lot)+ '/'+ bs + ' '+ input_sp ]
			else:
				header = [
						'%chk={}.chk'.format(name),
						'%mem={}'.format(args.mem),
						'%nprocshared={}'.format(args.nprocs),
						'# {0}'.format(lot)+ '/'+ bs + ' '+ input ]

		else:
			if args.single_point == True:
				header = [
					'%mem={}'.format(args.mem),
					'%nprocshared={}'.format(args.nprocs),
					'# {0}'.format(lot)+ '/'+ bs + ' '+ input_sp ]
			else:
				header = [
					'%mem={}'.format(args.mem),
					'%nprocshared={}'.format(args.nprocs),
					'# {0}'.format(lot)+ '/'+ bs + ' '+ input ]

		if args.lowest_only == True:
			subprocess.run(
				  ['obabel', '-isdf', path_for_file+file, '-ocom', '-O'+com_low,'-l' , '1', '-xk', '\n'.join(header)]) #takes the lowest conformer which is the first in the file
			# except:
			# 	subprocess.run(
			# 	  ['obabel', '-isdf', path_for_file+file, '-osdf', '-O'+com_low_sdf,'-l' , '1']) #takes the lowest conformer which is the first in the file
			# 	temp_sdf_files = glob.glob(name+'_low_*.sdf')
			# 	for file in temp_sdf_files:
			# 		generate_com_not_obabel(file, header)
		elif args.lowest_n == True:
			no_to_write = 0
			if len(energies) != 1:
				for i in range(len(energies)):
					energy_diff = energies[i] - energies[0]
					if energy_diff < args.energy_threshold_for_gaussian: # thershold is in kcal/mol and energies are in kcal/mol as well
						no_to_write +=1
				subprocess.run(
					 ['obabel', '-isdf', path_for_file+file, '-f', '1', '-l' , str(no_to_write), '-osdf', '-Otemp.sdf'])
				subprocess.run(
					  ['obabel', '-isdf', 'temp.sdf', '-ocom', '-O'+com,'-m', '-xk', '\n'.join(header)])
				# except:
				# 	subprocess.run(
				# 		 ['obabel', '-isdf', path_for_file+file, '-f', '1', '-l' , str(no_to_write), '-osdf', '-Otemp.sdf'])
				# 	subprocess.run(
				# 		  ['obabel', '-isdf', 'temp.sdf', '-osdf', '-O'+com_sdf,'-m'])
				# 	temp_sdf_files = glob.glob(name+'_*.sdf')
				# 	for file in temp_sdf_files:
				# 		generate_com_not_obabel(file, header)
			else:
				subprocess.run(
					  ['obabel', '-isdf', path_for_file+file, '-ocom', '-O'+com,'-m', '-xk', '\n'.join(header)])
				# except:
				# 	subprocess.run(
				# 	  ['obabel', '-isdf', path_for_file+file, '-osdf', '-O'+com_sdf,'-m']) #takes the lowest conformer which is the first in the file
				# 	temp_sdf_files = glob.glob(name+'_*.sdf')
				# 	for file in temp_sdf_files:
				# 		generate_com_not_obabel(file, header)
		else:
			subprocess.run(
				  ['obabel', '-isdf', path_for_file+file, '-ocom', '-O'+com,'-m', '-xk', '\n'.join(header)])
			# except:
			# 	subprocess.run(
			# 	  ['obabel', '-isdf', path_for_file+file, '-osdf', '-O'+com_sdf,'-m']) #takes the lowest conformer which is the first in the file
			# 	temp_sdf_files = glob.glob(name+'_*.sdf')
			# 	for file in temp_sdf_files:
			# 		generate_com_not_obabel(file, header)

		com_files = glob.glob('{0}_*.com'.format(name))

		for file in com_files:
			read_lines = open(file,"r").readlines()

			#chaanging the name of the files to the way they are in xTB Sdfs
			#getting the title line
			for i in range(0,len(read_lines)):
				if len(read_lines[i].strip()) == 0:
					title_line = read_lines[i+1]
					title_line = title_line.lstrip()
					rename_file_name = title_line.replace(" ", "_")
					break

			rename_file_name = rename_file_name.strip()+'.com'

			#change charge and multiplicity for Octahydrasl
			if args.metal_complex == True:
				for i in range(0,len(read_lines)):
					if len(read_lines[i].strip()) == 0:
						read_lines[i+3] = str(charge_com)+' '+ str(args.complex_spin)+'\n'
						break
				out = open(file, 'w')
				out.writelines(read_lines)
				out.close()

			#change file by moving to new file
			os.rename(file,rename_file_name)

			#submitting the gaussian file on summit
			if args.qsub == True:
				os.system(args.submission_command + rename_file_name)

		os.chdir(path_for_file)

"CHECKS THE FOLDER OF FINAL LOG FILES"
def check_for_final_folder(w_dir,log):
	dir_found = False
	while dir_found == False:
		temp_dir = w_dir+'New_Gaussian_Input_Files/'
		if os.path.isdir(temp_dir):
			w_dir = temp_dir
		else:
			dir_found =True
	return w_dir

" DEFINTION OF OUTPUT ANALYSER and NMR FILES CREATOR"
def output_analyzer(log_files, w_dir, lot, bs,bs_gcp, args, w_dir_fin,log):

	#log.write(w_dir)

	#definition of input lines
	if args.frequencies == True:
		if args.dispersion_correction == True:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0}) freq=noraman empiricaldispersion={1}'.format(args.max_cycle_opt,args.empirical_dispersion)
				input_sp = 'nmr=giao empiricaldispersion={0}'.format(args.empirical_dispersion)  #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) freq=noraman scrf=({1},solvent={2}) empiricaldispersion={3}'.format(args.max_cycle_opt, args.solvent_model, args.solvent_name,args.empirical_dispersion ) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao empiricaldispersion={2}'.format(args.solvent_model, args.solvent_name, args.empirical_dispersion)  ##add solvent if needed
		else:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0}) freq=noraman'.format(args.max_cycle_opt)
				input_sp = 'nmr=giao ' #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) freq=noraman scrf=({1},solvent={2})'.format(args.max_cycle_opt,args.solvent_model, args.solvent_name) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao'.format(args.solvent_model, args.solvent_name)  ##add solvent if needed
	else:
		if args.dispersion_correction == True:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0}) empiricaldispersion={1}'.format(args.max_cycle_opt,args.empirical_dispersion)
				input_sp = 'nmr=giao empiricaldispersion={0}'.format(args.empirical_dispersion)  #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) scrf=({1},solvent={2}) empiricaldispersion={3}'.format(args.max_cycle_opt,args.solvent_model, args.solvent_name,args.empirical_dispersion ) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao empiricaldispersion={2}'.format(args.solvent_model, args.solvent_name, args.empirical_dispersion)  ##add solvent if needed
		else:
			if args.solvent_model == 'gas_phase':
				input = 'opt=(maxcycles={0})'.format(args.max_cycle_opt)
				input_sp = 'nmr=giao ' #input for single point nmr
			else :
				input = 'opt=(maxcycles={0}) scrf=({1},solvent={2})'.format(args.max_cycle_opt,args.solvent_model, args.solvent_name) #add solvent if needed
				input_sp = 'scrf=({0},solvent={1}) nmr=giao'.format(args.solvent_model, args.solvent_name)  ##add solvent if needed

	for file in log_files:

		#made it global for all functions
		rms = 10000
		#defined the variable stop_rms, standor
		stop_rms = 0
		standor = 0
		NATOMS = 0

		outfile = open(file,"r")
		outlines = outfile.readlines()
		ATOMTYPES, CARTESIANS = [],[]
		FREQS, REDMASS, FORCECONST, NORMALMODE = [],[],[],[]; IM_FREQS = 0
		freqs_so_far = 0
		TERMINATION = "unfinished"
		ERRORTYPE = 'unknown'
		stop=0
		#Change to reverse
		for i in reversed(range(0,len(outlines))):
			if stop == 3: break
			# Get the name of the compound (specified in the title)
			if outlines[i].find('Symbolic Z-matrix:') > -1:
				name = outlines[i-2]
				stop=stop+1
			# Determine the kind of job termination
			if outlines[i].find("Normal termination") > -1:
				TERMINATION = "normal"
				stop=stop+1
			elif outlines[i].find("Error termination") > -1:
				TERMINATION = "error"
				if outlines[i-1].find("Atomic number out of range") > -1:
					ERRORTYPE = "atomicbasiserror"
				if outlines[i-3].find("SCF Error SCF Error SCF Error SCF Error SCF Error SCF Error SCF Error SCF Error") > -1:
					ERRORTYPE = "SCFerror"
				stop=stop+1
			# Determine charge and multiplicity
			if outlines[i].find("Charge = ") > -1:
				CHARGE = int(outlines[i].split()[2])
				MULT = int(outlines[i].split()[5].rstrip("\n"))
				stop=stop+1
		#log.write(TERMINATION)

		###reverse
		stop_get_details_stand_or = 0
		stop_get_details_dis_rot = 0
		stop_get_details_freq = 0
		for i in reversed(range(0,len(outlines))):
			if TERMINATION == "normal":
				if stop_get_details_stand_or == 1 and stop_get_details_dis_rot == 1 and stop_get_details_freq == 1:
					break
				# Sets where the final coordinates are inside the file
				###if outlines[i].find("Input orientation") > -1: standor = i
				if outlines[i].find("Standard orientation") > -1 and stop_get_details_stand_or !=1 :
					standor = i
					NATOMS = disrotor-i-6
					#log.write(NATOMS)
					stop_get_details_stand_or += 1
				if stop_get_details_dis_rot !=1 and (outlines[i].find("Distance matrix") > -1 or outlines[i].find("Rotational constants") >-1) :
					if outlines[i-1].find("-------") > -1:
						disrotor = i
						stop_get_details_dis_rot += 1
				# Get the frequencies and identifies negative frequencies
				if outlines[i].find(" Frequencies -- ") > -1 and stop_get_details_freq != 1:
					nfreqs = len(outlines[i].split())
					for j in range(2, nfreqs):
						FREQS.append(float(outlines[i].split()[j]))
						NORMALMODE.append([])
						if float(outlines[i].split()[j]) < 0.0: IM_FREQS += 1
					for j in range(3, nfreqs+1): REDMASS.append(float(outlines[i+1].split()[j]))
					for j in range(3, nfreqs+1): FORCECONST.append(float(outlines[i+2].split()[j]))
					for j in range(0,NATOMS):
						for k in range(0, nfreqs-2):
							NORMALMODE[(freqs_so_far + k)].append([float(outlines[i+5+j].split()[3*k+2]), float(outlines[i+5+j].split()[3*k+3]), float(outlines[i+5+j].split()[3*k+4])])
					freqs_so_far = freqs_so_far + nfreqs - 2
					stop_get_details_freq += 1
			if TERMINATION != "normal":
				if outlines[i].find('Cartesian Forces:  Max') > -1:
					if float(outlines[i].split()[5]) < rms:
						rms = float(outlines[i].split()[5])
						stop_rms = i

		if TERMINATION == "normal":
			# Get the coordinates for jobs that finished well with and without imag. freqs
			try: standor
			except NameError: pass
			else:
				for i in range(standor+5,standor+5+NATOMS):
					massno = int(outlines[i].split()[1])
					if massno < len(possible_atoms):
						atom_symbol = possible_atoms[massno]
					else: atom_symbol = "XX"
					ATOMTYPES.append(atom_symbol)
					CARTESIANS.append([float(outlines[i].split()[3]), float(outlines[i].split()[4]), float(outlines[i].split()[5])])


		if TERMINATION != "normal":
			# Get he coordinates for jobs that did not finished or finished with an error
			if stop_rms == 0:
				last_line = len(outlines)
				log.write('lastline')
			else:
				last_line = stop_rms
				log.write('stoprms')
			stop_get_details_stand_or = 0
			stop_get_details_dis_rot = 0
			for i in reversed(range(0,last_line)):
				if stop_get_details_stand_or == 1 and stop_get_details_dis_rot == 1 and stop_get_details_freq == 1:
					break
				# Sets where the final coordinates are inside the file
				if outlines[i].find("Standard orientation") > -1 and stop_get_details_stand_or != 1:
					standor = i
					NATOMS = disrotor-i-6
					stop_get_details_stand_or += 1
				if stop_get_details_stand_or != 1 and (outlines[i].find("Distance matrix") > -1 or outlines[i].find("Rotational constants") >-1):
					if outlines[i-1].find("-------") > -1:
						#log.write(i)
						disrotor = i
						stop_get_details_dis_rot += 1
			###no change after this
			for i in range (standor+5,standor+5+NATOMS):
				massno = int(outlines[i].split()[1])
				if massno < len(possible_atoms):
					atom_symbol = possible_atoms[massno]
				else: atom_symbol = "XX"
				ATOMTYPES.append(atom_symbol)
				CARTESIANS.append([float(outlines[i].split()[3]), float(outlines[i].split()[4]), float(outlines[i].split()[5])])

		# This part fixes jobs with imaginary freqs
		if IM_FREQS > 0:
			# Multiplies the imaginary normal mode vector by this amount (from -1 to 1).
			amplitude = 0.2 # default in pyQRC
			shift = []

			# Save the original Cartesian coordinates before they are altered
			orig_carts = []
			for atom in range(0,NATOMS):
				orig_carts.append([CARTESIANS[atom][0], CARTESIANS[atom][1], CARTESIANS[atom][2]])

			# could get rid of atomic units here, if zpe_rat definition is changed
			for mode, wn in enumerate(FREQS):
				# Either moves along any and all imaginary freqs, or a specific mode requested by the user
				if FREQS[mode] < 0.0:
					shift.append(amplitude)
				else: shift.append(0.0)

			# The starting geometry is displaced along the each normal mode according to the random shift
				for atom in range(0,NATOMS):
					for coord in range(0,3):
						CARTESIANS[atom][coord] = CARTESIANS[atom][coord] + NORMALMODE[mode][atom][coord] * shift[mode]
		outfile.close()

		# This part places the calculations in different folders depending on the type of
		# termination and number of imag. freqs
		source = w_dir+file

		if IM_FREQS == 0 and TERMINATION == "normal":

			#only if normally terminated move to the finished folder of first run.
			# destination = finished_folder(w_dir)
			destination = w_dir_fin

			try:
				os.makedirs(destination)
				shutil.move(source, destination)
			except OSError:
				if  os.path.isdir(destination) and not os.path.exists(destination+file):
					shutil.move(source, destination)
				else:
					raise

		if IM_FREQS > 0:
			destination = w_dir+'imaginary_frequencies/'
			try:
				os.makedirs(destination)
				shutil.move(source, destination)
			except OSError:
				if  os.path.isdir(destination) and not os.path.exists(destination+file):
					shutil.move(source, destination)
				else:
					raise

		if IM_FREQS == 0 and TERMINATION == "error":
			if stop_rms == 0 and ERRORTYPE == "atomicbasiserror":
				destination = w_dir+'failed_Error/atomic_basis_error'
			elif stop_rms == 0 and ERRORTYPE == "SCFerror":
				destination = w_dir+'failed_error/SCF_error'
			else:
				destination = w_dir+'failed_error/unknown_error'
			try:
				os.makedirs(destination)
				shutil.move(source, destination)
			except OSError:
				if  os.path.isdir(destination) and not os.path.exists(destination+file):
					shutil.move(source, destination)
				else:
					raise

		if IM_FREQS == 0 and TERMINATION == "unfinished":
			destination = w_dir+'failed_unfinished/'
			try:
				os.makedirs(destination)
				shutil.move(source, destination)
			except OSError:
				if  os.path.isdir(destination) and not os.path.exists(destination+file):
					shutil.move(source, destination)
				else:
					raise


		if IM_FREQS > 0 or TERMINATION != "normal" and not os.path.exists(w_dir+'failed_error/unknown_error/'+file) and not os.path.exists(w_dir+'failed_error/atomic_basis_error/'+file):

			# creating new folder with new input gaussian files
			new_gaussian_input_files = w_dir+'new_gaussian_input_files'

			try:
				os.makedirs(new_gaussian_input_files)
			except OSError:
				if  os.path.isdir(new_gaussian_input_files):
					os.chdir(new_gaussian_input_files)
				else:
					raise

			os.chdir(new_gaussian_input_files)

			log.write('-> Creating new gaussian input files for {0}/{1} file {2}'.format(lot,bs,name))

			# Options for genecp
			ecp_list,ecp_genecp_atoms = [],False

			for i in range(len(ATOMTYPES)):
				if ATOMTYPES[i] not in ecp_list and ATOMTYPES[i] in possible_atoms:
					ecp_list.append(ATOMTYPES[i])
				if ATOMTYPES[i] in args.genecp_atoms:
				   ecp_genecp_atoms = True
			if ecp_genecp_atoms == False:
				genecp = 'gen'
			if ecp_genecp_atoms == True:
				genecp = 'genecp'

			if genecp == 'genecp':
				if ERRORTYPE == 'SCFerror':
					if args.single_point == True:
						keywords_opt = lot +'/'+ genecp+' '+ input_sp + 'SCF=QC'
					else:
						keywords_opt = lot +'/'+ genecp+' '+ input + 'SCF=QC'
				else:
					if args.single_point == True:
						keywords_opt = lot +'/'+ genecp+' '+ input_sp
					else:
						keywords_opt = lot +'/'+ genecp+' '+ input

				fileout = open(file.split(".")[0]+'.com', "w")
				fileout.write("%mem="+str(args.mem)+"\n")
				fileout.write("%nprocshared="+str(args.nprocs)+"\n")
				fileout.write("# "+keywords_opt+"\n")
				fileout.write("\n")
				fileout.write(name+"\n")
				fileout.write(str(CHARGE)+' '+str(MULT)+'\n')
				for atom in range(0,NATOMS):
					fileout.write('{0:>2} {1:12.8f} {2:12.8f} {3:12.8f}'.format(ATOMTYPES[atom], CARTESIANS[atom][0],  CARTESIANS[atom][1],  CARTESIANS[atom][2]))
					fileout.write("\n")
				fileout.write("\n")
				for i in range(len(ecp_list)):
					if ecp_list[i] not in args.genecp_atoms:
						fileout.write(ecp_list[i]+' ')
				fileout.write('0\n')
				fileout.write(bs+'\n')
				fileout.write('****\n')
				if ecp_genecp_atoms == False:
					fileout.write('\n')
				else:
					for i in range(len(ecp_list)):
						if ecp_list[i] in args.genecp_atoms:
							fileout.write(ecp_list[i]+' ')
					fileout.write('0\n')
					fileout.write(bs_gcp+'\n')
					fileout.write('****\n\n')
					for i in range(len(ecp_list)):
						if ecp_list[i] in args.genecp_atoms:
							fileout.write(ecp_list[i]+' ')
					fileout.write('0\n')
					fileout.write(bs_gcp+'\n\n')
				fileout.close()
			else:
				if ERRORTYPE == 'SCFerror':
					if args.single_point == True:
						keywords_opt = lot +'/'+ genecp+' '+ input_sp + 'SCF=QC'
					else:
						keywords_opt = lot +'/'+ genecp+' '+ input + 'SCF=QC'
				else:
					if args.single_point == True:
						keywords_opt = lot +'/'+ bs +' '+ input_sp
					else:
						keywords_opt = lot +'/'+ bs +' '+ input

				fileout = open(file.split(".")[0]+'.com', "w")
				fileout.write("%mem="+str(args.mem)+"\n")
				fileout.write("%nprocshared="+str(args.nprocs)+"\n")
				fileout.write("# "+keywords_opt+"\n")
				fileout.write("\n")
				fileout.write(name+"\n")
				fileout.write(str(CHARGE)+' '+str(MULT)+'\n')
				for atom in range(0,NATOMS):
					fileout.write('{0:>2} {1:12.8f} {2:12.8f} {3:12.8f}'.format(ATOMTYPES[atom], CARTESIANS[atom][0],  CARTESIANS[atom][1],  CARTESIANS[atom][2]))
					fileout.write("\n")
				fileout.write("\n")
				fileout.close()

		#changing directory back to where all files are from new files created.
		os.chdir(w_dir)

		#adding in the NMR componenet only to the finished files after reading from normally finished log files
		if args.sp == True and TERMINATION == "normal":

			# creating new folder with new input gaussian files
			single_point_input_files = w_dir+'/single_point_input_files'

			try:
				os.makedirs(single_point_input_files)
			except OSError:
				if  os.path.isdir(single_point_input_files):
					os.chdir(single_point_input_files)
				else:
					raise

			os.chdir(single_point_input_files)
			log.write('Creating new single point files files for {0}/{1} file {2}'.format(lot,bs,name))

			# Options for genecp
			ecp_list,ecp_genecp_atoms = [],False

			for i in range(len(ATOMTYPES)):
				if ATOMTYPES[i] not in ecp_list and ATOMTYPES[i] in possible_atoms:
					ecp_list.append(ATOMTYPES[i])
				if ATOMTYPES[i] in args.genecp_atoms:
				   ecp_genecp_atoms = True
			if ecp_genecp_atoms == False:
				genecp = 'gen'
			if ecp_genecp_atoms == True:
				genecp = 'genecp'

			if genecp =='genecp':
				keywords_opt = lot +'/'+ genecp+' '+ input_sp

				fileout = open(file.split(".")[0]+'.com', "w")
				fileout.write("%mem="+str(args.mem)+"\n")
				fileout.write("%nprocshared="+str(args.nprocs)+"\n")
				fileout.write("# "+keywords_opt+"\n")
				fileout.write("\n")
				fileout.write(name+"\n")
				fileout.write(str(CHARGE)+' '+str(MULT)+'\n')
				for atom in range(0,NATOMS):
					fileout.write('{0:>2} {1:12.8f} {2:12.8f} {3:12.8f}'.format(ATOMTYPES[atom], CARTESIANS[atom][0],  CARTESIANS[atom][1],  CARTESIANS[atom][2]))
					fileout.write("\n")
				fileout.write("\n")
				for i in range(len(ecp_list)):
					if ecp_list[i] not in args.genecp_atoms:
						fileout.write(ecp_list[i]+' ')
				fileout.write('0\n')
				fileout.write(bs+'\n')
				fileout.write('****\n')
				if ecp_genecp_atoms == False:
					fileout.write('\n')
				else:
					for i in range(len(ecp_list)):
						if ecp_list[i] in args.genecp_atoms:
							fileout.write(ecp_list[i]+' ')
					fileout.write('0\n')
					fileout.write(bs_gcp+'\n')
					fileout.write('****\n\n')
					for i in range(len(ecp_list)):
						if ecp_list[i] in args.genecp_atoms:
							fileout.write(ecp_list[i]+' ')
					fileout.write('0\n')
					fileout.write(bs_gcp+'\n\n')
				fileout.close()
			else:
				keywords_opt = lot +'/'+ bs +' '+ input_sp

				fileout = open(file.split(".")[0]+'.com', "w")
				fileout.write("%mem="+str(args.mem)+"\n")
				fileout.write("%nprocshared="+str(args.nprocs)+"\n")
				fileout.write("# "+keywords_opt+"\n")
				fileout.write("\n")
				fileout.write(name+"\n")
				fileout.write("\n")
				fileout.write(str(CHARGE)+' '+str(MULT)+'\n')
				for atom in range(0,NATOMS):
					fileout.write('{0:>2} {1:12.8f} {2:12.8f} {3:12.8f}'.format(ATOMTYPES[atom], CARTESIANS[atom][0],  CARTESIANS[atom][1],  CARTESIANS[atom][2]))
					fileout.write("\n")
				fileout.write("\n")

		#changing directory back to where all files are from new files created.
		os.chdir(w_dir)

" CALCULATION OF BOLTZMANN FACTORS "
def boltz_calculation(val,i,log):
	#need to have good vibes
	cmd = 'python' +  ' -m' + ' goodvibes' + ' --csv' + ' --boltz ' +'--output ' + str(i) + ' ' + val
	os.system(cmd)

" CHECKING FOR DUPLICATES"
def dup_calculation(val,w_dir, agrs,log):
	#need to have good vibes
	cmd = 'python' +  ' -m' + ' goodvibes' + ' --dup ' + ' ' + val + '>' + ' ' + 'duplicate_files_checked.txt'
	os.system(cmd)

	#reading the txt files to get the DUPLICATES
	dup_file_list = []
	dupfile = open('duplicate_files_checked.txt',"r")
	duplines = dupfile.readlines()

	for i in range(0,len(duplines)):
		if duplines[i].find('duplicate') > -1:
			dup_file_list.append(duplines[i].split(' ')[1])

	#move the files to specific directory
	destination = w_dir+'Duplicates/'
	for source in dup_file_list:
		try:
			os.makedirs(destination)
			shutil.move(source, destination)
		except OSError:
			if  os.path.isdir(destination) and not os.path.exists(destination+file):
				shutil.move(source, destination)
			else:
				raise

"COMBINING FILES FOR DIFFERENT MOLECULES"
def combine_files(csv_files, lot, bs, args,log):
	#final dataframe with only the boltzmann averaged values
	final_file_avg_thermo_data = pd.DataFrame(columns=columns)
	compare_G = pd.DataFrame(columns=['Structure_of_min_conf','min_qh-G(T)','boltz_avg_qh-G(T)'])

	files = []
	#combine all the csv_files

	for f in csv_files:

		log.write(f)

		df = pd.read_csv(f, skiprows = 16)
		# df['Structure']= df['Structure'].astype(str)
		df = df.rename(columns={"   Structure": "Structure"})

		#dropping the ************* line
		df = df.drop(df.index[0])
		df.iloc[-1] = np.nan

		for col in columns:
			if col == 'Structure':
				#identifyin the minmum energy if the conformers
				min_G = df['qh-G(T)'].min()
				#getting the name of the structure of the min G
				idx_name_of_min_conf = df['qh-G(T)'].idxmin() - 1
				name_of_min_conf = df.iloc[idx_name_of_min_conf]['Structure']
				#df.at[df.index[-1], col] = name_of_min_conf
			elif col != 'Structure':
				boltz_avg = np.sum(df[col] * df['Boltz'])
				df.at[df.index[-1], col] = boltz_avg
				if col == 'qh-G(T)':
					compare_G = compare_G.append({'Structure_of_min_conf': name_of_min_conf,'min_qh-G(T)': min_G,'boltz_avg_qh-G(T)': boltz_avg}, ignore_index=True)

		final_file_avg_thermo_data = final_file_avg_thermo_data.append({'Structure':name_of_min_conf , 'E': df.iloc[-1]['E'] , 'ZPE': df.iloc[-1]['ZPE'], 'H':df.iloc[-1]['H'] , 'T.S':df.iloc[-1]['T.S'] , 'T.qh-S':df.iloc[-1]['T.qh-S'] , 'G(T)': df.iloc[-1]['G(T)'], 'qh-G(T)':df.iloc[-1]['qh-G(T)'] },ignore_index=True)

		files.append(df)

	final_file_all_data = pd.concat(files, axis=0, ignore_index=True)

	#combined_csv = pd.concat([pd.read_csv(f, skiprows = 14, skipfooter = 1) for f in csv_files ])
	#change directory to write all files in one place
	destination = args.path+'All csv files/'+ str(lot)+ '-'+ str(bs)
	try:
		os.makedirs(destination)
	except OSError:
		if  os.path.isdir(destination):
			pass
		else:
			raise
	os.chdir(destination)

	#export to csv
	final_file_all_data.to_csv( str(lot) + '-' + str(bs) + '_all_molecules_all data.csv', index=False, encoding='utf-8-sig')
	final_file_avg_thermo_data.to_csv( str(lot) + '-' + str(bs) + '_all_molecules_avg_thermo_data.csv', index=False, encoding='utf-8-sig')
	compare_G.to_csv( str(lot) + '-' + str(bs) + '_all_molecules_compare_G(T).csv', index=False, encoding='utf-8-sig')
