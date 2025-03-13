from dolfin import *
import matplotlib.pyplot as plt

# Define mesh and function space
mesh = UnitSquareMesh(50, 50)
P2 = VectorElement("P", mesh.ufl_cell(), 2)  # Velocity element
P1 = FiniteElement("P", mesh.ufl_cell(), 1)  # Pressure element
TH = MixedElement([P2, P1])
W = FunctionSpace(mesh, TH)                  #Mixed function space

# Define boundary conditions
inflow = Expression(("1.0", "0.0"), degree=2) # Inflow velocity

def lid(x, on_boundary):
    return on_boundary and near(x[1], 1.0)

def walls(x, on_boundary):
    return on_boundary and not near(x[1], 1.0)

bcu = [DirichletBC(W.sub(0), inflow, lid),
       DirichletBC(W.sub(0), Constant((0, 0)), walls)]

# Time parameters
dt = 0.01
T = 2.0
t = 0.0 # Time step

# Functions
w = Function(W)
w_prev = Function(W)
u, p = split(w)
u_prev, p_prev = split(w_prev)
v, q = TestFunctions(W)

# Physical parameters
nu = 0.01
rho = 1.0

# Variational formulation
F = (rho * inner((u - u_prev)/dt, v) * dx
     + rho * inner(dot(u_prev, nabla_grad(u)), v) * dx
     + nu * inner(grad(u), grad(v)) * dx
     - p * div(v) * dx
     + div(u) * q * dx)

# Critical fix: Compute Jacobian and don't redefine problem
J = derivative(F, w, TrialFunction(W))
problem = NonlinearVariationalProblem(F, w, bcu, J=J) 
solver = NonlinearVariationalSolver(problem)
print(solver.parameters)
# Add solver parameters
prm = solver.parameters
prm['newton_solver']['absolute_tolerance'] = 1e-12
prm['newton_solver']['relative_tolerance'] = 1e-14
prm['newton_solver']['maximum_iterations'] = 5
prm['newton_solver']['linear_solver'] = 'mumps' 

# Create output files for velocity and pressure
u_file = File("velocity.pvd")
p_file = File("pressure.pvd")

# Time-stepping
while t < T:
    w_prev.assign(w)
    solver.solve()
    t += dt
    print(f"Time step t = {t:.3f}")

    # Save velocity and pressure to files for visualization in ParaView
    u, p = w.split()
    u_file << (u, t)
    p_file << (p, t)