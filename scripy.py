import fipy as fp

m = fp.Grid2D(nx=10, ny=10)

v = fp.CellVariable(mesh=m, value=m.x * m.y)


