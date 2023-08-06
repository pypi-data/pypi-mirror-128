import argparse, inspect, os, importlib, random
import cantera_adaptive_testing.utilities as utilities
import cantera_adaptive_testing.mechanisms as mechanisms
from mpi4py import MPI
import cantera as ct
import numpy as np


def MPIRunAll(*args, **kwargs):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        parser, args = parserSetup()
        data = vars(args)
        mechs = inspect.getmembers(mechanisms, inspect.isclass)
        mechs = [mech for mname, mech in mechs]
        random.shuffle(mechs)
        mechs = np.array_split(mechs, comm.Get_size())
    else:
        mechs = None
        data = None
    data = comm.bcast(data, root=0)
    rankMech = comm.scatter(mechs, root=0)
    for rm in rankMech:
        currMech = rm(**data)
        currMech()


def parserSetup():
    """This function is the main call for the commandline interface for
    testing the additions to Cantera."""
    parser = argparse.ArgumentParser(description="""adaptive-testing:
    This entry was created to measure and analyze performance of the
    newly implemented reactor and preconditioning features into cantera.
    This interface works by specifying a mechanism and flags to tune the
    simulation.""")
    parser.add_argument("mechanism", type=str, help="Specify the mechanism you would like to run. List all mechanisms by using \"list\" as the positional argument.")
    # Configurable options
    parser.add_argument('-w', '--write', action='store_true', help="If this flag is added and the study has an associated data output, it will be generated.")
    parser.add_argument('-L', '--log', action='store_true', help="Flag to log the simulation if possible in \"log.yaml\". Specify -n to override the log file name.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose simulation.")
    parser.add_argument('-S', '--solver', type=str, default="DENSE + NOJAC", help="Enable use of different solvers")
    parser.add_argument('-P', '--precon_on', action='store_true', default=False, help="Enable the use of preconditioner.")
    parser.add_argument('-T', '--threshold', type=float, default=1e-8, help="Set a threshold value used for the preconditioned simulation.")
    parser.add_argument('-M', '--moles', action='store_true', default=False, help="Use mole based reactors.")
    args = parser.parse_args()
    return parser, args


def commandLineMain():
    parser, args = parserSetup()
    # Handle mechanisms
    mechs = inspect.getmembers(mechanisms, inspect.isclass)
    mechs = {element[0]: element[1] for element in mechs}
    del mechs['MechanismBase'] # delete mechanism because it is not a valid option
    if args.mechanism not in mechs:
        # print mechanisms
        print("Available mechanisms include:")
        for mech in mechs:
            print("\t"+mech)
    else:
        selected = mechs[args.mechanism](**vars(args))
        selected()
