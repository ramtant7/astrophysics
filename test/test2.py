import rebound
import matplotlib

sim = rebound.Simulation()
sim.add(m=1)
sim.add(m=0.1, e=0.041, a=0.4, inc=0.2, f=0.43, Omega=0.82, omega=2.98)
sim.add(m=1e-3, e=0.24, a=1.0, pomega=2.14)
sim.add(m=1e-3, e=0.24, a=1.5, omega=1.14, l=2.1)
op = rebound.OrbitPlot(sim)



op1 = rebound.OrbitPlot(sim, particles=[1,3])
op2 = rebound.OrbitPlot(sim, particles=[2], ax=op1.ax, fig=op1.fig, lw=5, color="red")


for i in range(100):
    sim.integrate(sim.t+0.01)
    op1.update()
    op2.update()
    op1.fig.savefig("img/out_%02d.png"%i)


ops = rebound.OrbitPlotSet(sim)
ops.fig.savefig("orbit.png")


