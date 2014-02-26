
"""
Usage: fipy_timing.py [<jsonfile>]

"""

from docopt import docopt
import json
import timeit
import numpy as np
import fipy as fp
import os

arguments = docopt(__doc__, version='Run FiPy timing')
jsonfile = arguments['<jsonfile>']

if jsonfile:
    with open(jsonfile, 'rb') as ff:
        params = json.load(ff)
else:
    params = dict()
    
N = params.get('N', 10)
iterations = params.get('iterations', 100)
suite = params.get('suite', 'trilinos')
sumatra_label = params.get('sumatra_label', '')

attempts = 3

setup_str = '''
import fipy as fp
import numpy as np
np.random.seed(1)
L = 1.
N = {N:d}
m = fp.GmshGrid3D(nx=N, ny=N, nz=N, dx=L / N, dy=L / N, dz=L / N)
v0 = np.random.random(m.numberOfCells)
v = fp.CellVariable(mesh=m)
v0 = np.resize(v0, len(v)) ## Gmsh doesn't always give us the correct sized grid!
eqn = fp.TransientTerm(1e-3) == fp.DiffusionTerm()
v[:] = v0.copy()

import fipy.solvers.{suite} as solvers
solver = solvers.linearPCGSolver.LinearPCGSolver(precon=None, iterations={iterations}, tolerance=1e-100)

eqn.solve(v, dt=1., solver=solver)
v[:] = v0.copy()
'''

timeit_str = '''
eqn.solve(v, dt=1., solver=solver)
fp.parallelComm.Barrier()
'''

timer = timeit.Timer(timeit_str, setup=setup_str.format(N=N, suite=suite, iterations=iterations))
times = timer.repeat(attempts, 1)

if fp.parallelComm.procID == 0:
    filepath = os.path.join('Data', sumatra_label)
    filename = 'data.txt'
    np.savetxt(os.path.join(filepath, filename), times)