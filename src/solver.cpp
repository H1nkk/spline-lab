#include "solver.h"
#include <stdexcept>

std::vector<std::tuple<double, double, double, double>> Solver::SolveSpline(std::vector<double> x_list, std::vector<double> y_list) {
    // число точек для интерполяции
    size_t n = x_list.size() - 1;
    if (n + 1 < 2) {
        throw std::invalid_argument("too few points (required > 1)");
    }

    // шаг сетки (равномерный случай)
    double h = x_list[1] - x_list[0];

    // граничные условия
    double mu_1 = 0, mu_2 = 12;

    // Spline coefficients: размеры+1 для удобства
    std::vector<double> a_list(n + 1);
    std::vector<double> b_list(n + 1);
    std::vector<double> c_list(n + 2);
    std::vector<double> d_list(n + 1);

    // a_i = f_i
    for (int i = 1; i <= n; i++) {
        a_list[i] = y_list[i];
    }

    // вспомогательные параметры метода прогонки (на самом деле их n-1, размеры равны n для удобства нумерации)
    std::vector<double> alpha_list(n + 1);
    std::vector<double> beta_list(n + 1);
    double kappa_1 = 0.0, kappa_2 = 0.0;

    // коэффициенты при неизвестных в СЛАУ (тут тоже на 1 больше размер для удобства)
    std::vector<double> A_list(n + 1);
    std::vector<double> B_list(n + 1);
    std::vector<double> C_list(n + 1);

    // столбец значений в СЛАУ
    std::vector<double> phi_list(n);

    // заполняем матрицу коэффициентов и вектор, задающие СЛАУ
    for (int i = 1; i <= n; i++) {
        A_list[i] = h;
        C_list[i] = -2.0 * (h + h);
        B_list[i] = h;

        if (i <= n - 1)
            phi_list[i] = -6.0 * ((y_list[i + 1] - y_list[i]) / h - (y_list[i] - y_list[i - 1]) / h);
    }

    // прямой ход прогонки
    alpha_list[1] = kappa_1;
    beta_list[1] = mu_1;
    for (int i = 1; i < n; i++) {
        alpha_list[i + 1] = B_list[i] / (C_list[i] - alpha_list[i] * A_list[i]);
        beta_list[i + 1] = (phi_list[i] + A_list[i] * beta_list[i]) / (C_list[i] - alpha_list[i] * A_list[i]);
    }

    // обратный ход прогонки в случае, когда kappa_2 = 0
    c_list[n] = mu_2;
    for (int i = n - 1; i >= 1; i--) {
        c_list[i] = alpha_list[i + 1] * c_list[i + 1] + beta_list[i + 1];
    }
    c_list[0] = mu_1;

    // заполняем b и d
    for (int i = 1; i <= n; i++) {
        b_list[i] = (y_list[i] - y_list[i - 1]) / h + c_list[i] * h / 3.0 + c_list[i - 1] * h / 6.0;
        d_list[i] = (c_list[i] - c_list[i - 1]) / h;
    }

    // создаем и заполняем ответ
    std::vector<std::tuple<double, double, double, double>> result(n);
    for (int i = 0; i < n; i++) {
        result[i] = std::make_tuple(
            a_list[i + 1],
            b_list[i + 1],
            c_list[i + 1],
            d_list[i + 1]
        );
    }

    return result;
}
