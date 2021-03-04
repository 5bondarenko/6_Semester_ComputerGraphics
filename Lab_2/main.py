import matplotlib.pyplot as plt
from sympy import nan  # для проверки на NaN
from sympy import Piecewise  # кусочная функция
from sympy import Matrix  # матрицы из sympy
from numpy import linspace  # range для нецелых
from sympy.abc import t  # t в качестве символьной переменной (чтобы не использовать symbols() или var())


def plot_contour(points, ax, contour=True, **params):  # из первой лабы, но без 3D
    if params is None:
        params = {}
    x = [points[i][0] for i in range(0, len(points))]
    y = [points[i][1] for i in range(0, len(points))]
    if contour:
        ax.plot([*x, points[0][0]],
                [*y, points[0][1]],
                **params)
    else:
        ax.plot(x, y, **params)


def generateNodalVector(n, k):  # генерация узлового вектора (это 100% правильно, но перепроверь)
    return_list = []
    for i in range(n + k + 1):
        if i < k:
            return_list.append(0)
        elif i <= n:
            return_list.append(i - k + 1)
        else:
            return_list.append(n - k + 2)
    return return_list


def generateBasicFunctions(X, k):
    J = []
    if k == 1:
        for i in range(0, len(X) - 1):
            J.append(Piecewise((1, (X[i] <= t) & (t < X[i + 1])), (0, True)))
    else:
        J_previous = generateBasicFunctions(X, k - 1)
        for i in range(0, len(J_previous) - 1):
            # 1. (ОСНОВНОЙ ВАРИАНТ) Вариант не с Moodle - выдаёт правильную середину при k = 3
            J.append(J_previous[i] * (t - X[i]) / (X[i + k - 1] - X[i]) +
                     J_previous[i + 1] * (X[i + k] - t) / (X[i + k] - X[i + 1]))
            # 2. Вариант с Moodle - выдаёт zoo при k = 2
            # J.append(J_previous[i] * (t - X[i]) / X[i + k - 2] +
            #          J_previous[i + 1] * (X[i + k - 1] - t) / (X[i + k - 1] - X[i + 1]))
            # 3.1. Комбо - выдаёт zoo при k = 2
            # J.append(J_previous[i] * (t - X[i]) / (X[i + k - 2] - X[i]) +
            #          J_previous[i + 1] * (X[i + k - 1] - t) / (X[i + k - 1] - X[i + 1]))
            # 3.2. Комбо - выдаёт неправильную середину при k = 3
            # J.append(J_previous[i] * (t - X[i]) / X[i + k - 1] +
            #          J_previous[i + 1] * (X[i + k] - t) / (X[i + k] - X[i + 1]))
            if J[-1] == nan:
                J[-1] = 0
    return J


def drawBSpline(points, k: int, ax):
    N = len(points)  # количество точек
    n = N - 1  # n из материалов Moodle
    X = generateNodalVector(n, k)  # узловой вектор
    print("X = ", X)
    J = generateBasicFunctions(X, k)  # рекурсивное создание базисных функций (ПРОБЛЕМА ЗДЕСЬ)
    print("Элементы J:")
    for elem in J:
        print(elem)
    P = J[0] * points[0]
    for i in range(1, N):  # создание итоговой функции
        P = P + J[i] * points[i]
    x_func = P[0]
    y_func = P[1]
    spline_points = []
    t_values = linspace(0, n - k + 2, 100)
    for t_value in t_values[:-1]:
        print("Для t = ", t_value, " точка: ", [x_func.subs(t, t_value), y_func.subs(t, t_value)])
        spline_points.append([x_func.subs(t, t_value), y_func.subs(t, t_value)])
    plot_contour(spline_points, ax, contour=False)


def main():
    points = [Matrix([float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')])
              for i in range(1, int(input('Введите количество точек: ')) + 1)]
    k = int(input('Введите порядок B-сплайна (0 до N-1): '))
    # plotting
    plt.figure()
    ax = plt.axes()
    plot_contour(points, ax, contour=False)
    drawBSpline(points, k, ax)
    plt.show()


if __name__ == "__main__":
    main()
