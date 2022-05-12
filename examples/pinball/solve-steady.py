import firedrake as fd
from firedrake.petsc import PETSc
from firedrake import logging

import hydrogym as gym

Re = 100
flow = gym.flow.Pinball(Re=Re, mesh_name='fine')
flow.solve_steady(solver_parameters={'snes_monitor': None}, stabilization=None)

Re = 130
flow.Re.assign(Re)
flow.solve_steady(solver_parameters={'snes_monitor': None}, stabilization=None)
output_dir = f'{Re}_output'

CL, CD = flow.compute_forces()
gym.print([(L, D) for (L, D) in zip(CL, CD)])

flow.save_checkpoint(f"{output_dir}/steady.h5")

vort = flow.vorticity()
pvd = fd.File(f"{output_dir}/steady.pvd")
pvd.write(flow.u, flow.p, vort)