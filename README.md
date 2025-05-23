# FEniCS Lid-Driven Cavity Flow Simulation

This README file describes the FEniCS Python script for simulating the **lid-driven cavity flow** problem. The simulation is based on the **time-dependent Navier-Stokes equations** for an **incompressible, viscous fluid** within a **unit square domain** 

## Description

This script utilizes the **FEniCS** library to solve the time-dependent Navier-Stokes equations for the classic lid-driven cavity flow problem. The simulation models a fluid confined within a unit square where the **top boundary (the lid) moves at a constant horizontal velocity**, inducing flow within the cavity. 
The remaining **three boundaries are stationary walls** with a no-slip condition.

## Requirements

To execute this script, the following software must be installed on your system:

*   **FEniCS:** A free and open-source software library for automated solution of differential equations using the finite element method. Please refer FEniCS library for the installation 
*   **Python:** The programming language used to write the script.
*   **Paraview:** For Visualisation

## Problem Setup

The lid-driven cavity flow problem is set up in the script as follows:

*   **Mesh:** A **uniform mesh** of the unit square is created using `UnitSquareMesh(50, 50)`, resulting in **50 cells along each side**.
*   **Function Spaces:** Mixed finite element spaces are defined for the velocity and pressure fields:
    *   **Velocity (`P2`):** Defined using `VectorElement("P", mesh.ufl_cell(), 2)`, representing **second-order Lagrange vector elements**.
    *   **Pressure (`P1`):** Defined using `FiniteElement("P", mesh.ufl_cell(), 1)`, representing **first-order Lagrange scalar elements**.
    *   **Mixed Element (`TH`):** Combines the velocity and pressure elements using `MixedElement([P2, P1])`.
    *   **Mixed Function Space (`W`):** The function space over the mesh using the mixed element `TH`, defined by `FunctionSpace(mesh, TH)`.
*   **Boundary Conditions (`bcu`):** A list of Dirichlet boundary conditions applied to the velocity component (`W.sub(0)`) of the mixed function space:
    *   **Moving Lid:** On the boundary where `on_boundary` is true and `near(x[4], 1.0)` (the top boundary), the velocity is set to `inflow = Expression(("1.0", "0.0"), degree=2)`, meaning a **constant velocity of 1.0 in the x-direction and 0.0 in the y-direction**.
    *   **Stationary Walls:** On the boundary where `on_boundary` is true and `not near(x[4], 1.0)` (the other three walls) [1], the velocity is set to `Constant((0, 0))`, representing a **no-slip condition**.
*   **Physical Parameters:**
    *   **Kinematic Viscosity (`nu`):** Set to `0.01`.
    *   **Density (`rho`):** Set to `1.0`.

## Simulation Parameters

The time-stepping and solver parameters are configured as follows:

*   **Time Step (`dt`):** `0.01`.
*   **Total Simulation Time (`T`):** `2.0`.
*   **Current Time (`t`):** Initialized to `0.0`.
*   **Newton Solver Parameters (`prm`):** These parameters control the nonlinear Newton solver used to solve the discretized Navier-Stokes equations:
    *   **Absolute Tolerance:** `1e-12`.
    *   **Relative Tolerance:** `1e-14`.
    *   **Maximum Iterations:** `5`.
    *   **Linear Solver:** `'mumps'` is used as a robust direct linear solver.

## Results

Print the current time step to the console.
•
After the simulation completes, it will generate a set of velocity and pressure  and the corresponding saving step within the time loop as .pvd files which you can open in Paraview
◦
Velocity Field: A plot visualizing the velocity field within the unit square domain at the final time T.
◦
Pressure Field: A plot showing the pressure distribution within the unit square domain at the final time T.
