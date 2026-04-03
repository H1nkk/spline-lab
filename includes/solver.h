#pragma once
#include <vector>
#include <tuple>

class Solver final
{
private:
    Solver() {}

public:
    static std::vector<std::tuple<double, double, double, double>> SolveSpline(std::vector<double> x_list, std::vector<double> y_list);

};