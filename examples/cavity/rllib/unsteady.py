import firedrake as fd
from ufl import sqrt

import hydrogym as gym

Re = 5000
output_dir = "./output"
pvd_out = f"{output_dir}/solution.pvd"
checkpoint = f"{output_dir}/checkpoint.h5"

flow = gym.flow.Cavity(Re=Re, mesh="coarse")

# Time step
Tf = 500
dt = 2.5e-4

h = fd.CellSize(flow.mesh)


def log_postprocess(flow):
    KE = 0.5 * fd.assemble(fd.inner(flow.u, flow.u) * fd.dx)
    CFL = (
        fd.project(
            dt * sqrt(flow.u.sub(0) ** 2 + flow.u.sub(1) ** 2) / h, flow.pressure_space
        )
        .vector()
        .max()
    )
    (m,) = flow.get_observations()
    return [CFL, KE, m]


print_fmt = "t: {0:0.3f}\t\tCFL: {1:0.3f}\t\t KE: {2:0.12e}\t\t m: {3:0.6e}"
callbacks = [
    gym.io.CheckpointCallback(interval=100, filename=checkpoint),
    gym.io.LogCallback(
        postprocess=log_postprocess,
        nvals=3,
        interval=10,
        filename=f"{output_dir}/stats.dat",
        print_fmt=print_fmt,
    ),
]

gym.integrate(flow, t_span=(0, Tf), dt=dt, callbacks=callbacks, method="IPCS")