#include <iostream>
#include "solver.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

// Create the pybind11 module
PYBIND11_MODULE(splinesolver, m) {
    m.doc() = "Solves cubic splines";
    
    m.def("solve_spline", &Solver::SolveSpline,
        pybind11::arg("x_list"), pybind11::arg("y_list")    
    );
}

int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}