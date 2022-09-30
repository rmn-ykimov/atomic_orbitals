# argument parser to get options from command line
import argparse

parser = argparse.ArgumentParser(
    description='We display the image of the orbitals using the Monte Carlo '
                'method.')

parser.add_argument('--c1', type=float, default=1.0,
                    help="Coefficient before the first angle function")

parser.add_argument('--c2', type=float, default=0.0,
                    help="Coefficient before the second angle function.")

parser.add_argument('--c3', type=float, default=0.0,
                    help="Coefficient before the third angle function.")

parser.add_argument('--nx1', type=int, default=0,
                    help="The power of n in the x**n function for the first "
                         "angle function.")

parser.add_argument('--nx2', type=int, default=0,
                    help="The power of n in the x**n function for the second "
                         "angle function.")

parser.add_argument('--nx3', type=int, default=0,
                    help="The power of n in the x**n function for the third "
                         "angle function.")

parser.add_argument('--ny1', type=int, default=0,
                    help="The power of n in the y**n function for the first "
                         "angle function.")

parser.add_argument('--ny2', type=int, default=0,
                    help="The power of n in the y**n function for the second "
                         "angle function.")

parser.add_argument('--ny3', type=int, default=0,
                    help="The power of n in the y**n function for the third "
                         "angle function.")

parser.add_argument('--nz1', type=int, default=0,
                    help="The power of n in the z**n function for the first "
                         "angle function.")

parser.add_argument('--nz2', type=int, default=0,
                    help="The power of n in the z**n function for the second "
                         "angle function.")

parser.add_argument('--nz3', type=int, default=0,
                    help="The power of n in the z**n function for the third "
                         "angle function.")

parser.add_argument('--NumSteps', type=int, default=50000,
                    help="The number of steps in the Monte Carlo simulation.")

parser.add_argument('--R0', type=float, default=1.0,
                    help="R0 orbital size")

parser.add_argument('--PartToIgnore', type=float, default=0.1,
                    help="The portion of the Monte Carlo trajectory at the "
                         "beginning that is ignored in the calculations as a "
                         "balancing stage.")

parser.add_argument('--MaxBox', type=float, default=0.1,
                    help="The size of the starting area from which the "
                         "starting point of the Monte Carlo trajectory is "
                         "randomly selected.")

parser.add_argument('--MaxStep', type=float, default=2.0,
                    help="Maximum step length in the Monte Carlo trajectory.")

parser.add_argument('--MaxSmallShift', type=float, default=0.1,
                    help="A small addition to the trajectory values when we "
                         "stay at the same point (for beauty).")

parser.add_argument('--plot', action='store_true',
                    help="Flag to plot orbitals using matplotlib")
