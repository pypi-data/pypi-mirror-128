#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function
from openmm.app import *
from openmm import *
from simtk.unit import *
from sys import stdout
import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', "--steps", type=int, help="", default=100)#0)
    parser.add_argument('-n', "--nsim", type=int, help="", default=30000)#00)
    parser.add_argument('-r', "--run", help="", default='_')
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("file", help="", default="") # nargs='+')
    parser.add_argument("--no-min",
                        action="store_true", help="be verbose")
    parser.add_argument("--pymol",
                        action="store_true", help="be verbose")
    parser.add_argument("--solv-padding",
                        action="store_true", help="be verbose")

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if list != type(args.file):
        args.file = [args.file]

    for f in args.file:
        print(f, '...')
        out = f.replace('.pdb','') + '_MD.pdb'
        pdb = PDBFile(f)
        log = f.replace('.pdb','') + '_log.csv'
        modeller = Modeller(pdb.topology, pdb.positions)
        ff = 'ff14SB.xml' #amber14sb.xml' # 'amber14-all.xml'
        ff = 'amberfb15.xml'#amber14-all.xml'
        forcefield = ForceField(ff, 'tip3p.xml') #'amber14/tip3pfb.xml')

        modeller.addHydrogens(forcefield)
        #modeller.addSolvent(forcefield, ionicStrength=0.1*molar)
        # modeller.addSolvent(forcefield, model='tip5p')

        if args.solv_padding:
            modeller.addSolvent(forcefield, padding=0.5*nanometers)
        else:
            #print('boxSize=Vec3(5.0, 3.5, 3.5)*nanometers')
            #x = 5.0, 3.5, 3.5
            #x = 1, 1, 1
            modeller.addSolvent(forcefield, boxSize=Vec3(5.0, 3.5, 3.5)*nanometers)
        
        system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, #nonbondedMethod=PME,
                nonbondedCutoff=1*nanometer, constraints=HBonds)
        integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
        simulation = Simulation(modeller.topology, system, integrator)
        simulation.context.setPositions(modeller.positions)
        if not args.no_min:
            simulation.minimizeEnergy()
        nstep = args.steps
        simulation.reporters.append(PDBReporter(out, nstep))
        simulation.reporters.append(StateDataReporter(stdout, nstep, step=True,
                potentialEnergy=True, temperature=True, progress=True, totalSteps=args.nsim, remainingTime=True, totalEnergy=True))
        simulation.reporters.append(StateDataReporter(log, nstep, step=True,
                potentialEnergy=True, temperature=True, progress=True, totalSteps=args.nsim, remainingTime=True, totalEnergy=True))
        simulation.step(args.nsim)
        print('saved ', out)
        if args.pymol:
            os.system('open %s' % out)
