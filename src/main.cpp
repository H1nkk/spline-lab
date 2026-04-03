#include <iostream>
#include "solver.h"
#include "pybind11/pybind11.h"
#include <pybind11/stl.h>

namespace py = pybind11;

// Create the pybind11 module
PYBIND11_MODULE(splinesolver, m) {
    m.doc() = "Solves cubic splines";
    
    // Wrap the return_0 function
    m.def("solve_spline", &Solver::SolveSpline, "A function that solves a cubic spline and returns splie coefficients");
}