#include <iostream>
#include "solver.h"
#include "pybind11/pybind11.h"

int return_0()
{
    return 0;
}

// Create the pybind11 module
PYBIND11_MODULE(splinesolver, m) {
    m.doc() = "Solves cubic splines";
    
    // Wrap the return_0 function
    m.def("return_0", &return_0, "A function that returns 0");
}

int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}