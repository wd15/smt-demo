
import json
import timeit
import numpy as np
import fipy as fp

with open('params.json', 'rb') as fp:
    params = json.load(fp)
    
N = params['N']
iterations = params['iterations']
suite = params['suite']

print N
print type(iterations)
attempts = 3

setup_str = '''
import fipy as fp
import numpy as np
np.random.seed(1)
L = 1.
N = {N:d}
m = fp.GmshGrid3D(nx=N, ny=N, nz=N, dx=L / N, dy=L / N, dz=L / N)
v0 = np.random(m.numberOfCells)
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
    print min(times)