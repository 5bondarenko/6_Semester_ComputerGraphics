import matplotlib.pyplot as plt  # библиотека для визуализации
from sympy import Piecewise  # кусочная функция
from sympy import Matrix  # матрицы из sympy
from numpy import linspace  # генератор промежуточных точек
from sympy.abc import t  # t в качестве символьной переменной (чтобы не использовать symbols() или var())


def plot_contour(points, ax, contour=True, **params):  # из первой лабораторной работы, но в 2D
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
        
        
def generateNodalVector(n, k):  # генерация узлового вектора
    return_list = []
    for i in range(n + k + 1):
        if i < k:
            return_list.append(0)
        elif i <= n:
            return_list.append(i - k + 1)
        else:
            return_list.append(n - k + 2)
    return return_list
  
  
def generateBasicFunctions(X, k):  # построение вектора базисных функций
    J = []
    if k == 1:
        for i in range(0, len(X) - 1):
            J.append(Piecewise((1, (X[i] <= t) & (t < X[i + 1])), (0, True)))
    else:
        J_previous = generateBasicFunctions(X, k - 1)
        for i in range(0, len(J_previous) - 1):
            if X[i + k - 1] - X[i] == 0:  # проверка деления на 0
                first_operand = 0
            else:
                first_operand = J_previous[i] * (t - X[i]) / (X[i + k - 1] - X[i])
            if X[i + k] - X[i + 1] == 0:  # проверка деления на 0
                second_operand = 0
            else:
                second_operand = J_previous[i + 1] * (X[i + k] - t) / (X[i + k] - X[i + 1])
            J.append(first_operand + second_operand)
    return J
  
  
def drawBSpline(points, k: int, ax):  # отрисовка B-сплайна
    N = len(points)  # количество точек
    n = N - 1  # n из материалов Moodle
    X = generateNodalVector(n, k)  # узловой вектор
    J = generateBasicFunctions(X, k)  # рекурсивное создание базисных функций
    P = J[0] * points[0]  # создание итоговой функции
    for i in range(1, N):
        P = P + J[i] * points[i]
    x_func = P[0]  # выделение функций для каждой из координат
    y_func = P[1]
    spline_points = []
    t_values = linspace(0, n - k + 2, 100)  # значения параметра для построения
    for t_value in t_values[:-1]:
        spline_points.append([x_func.subs(t, t_value), y_func.subs(t, t_value)])  # вычисление точек для отрисовки
    plot_contour(spline_points, ax, contour=False)

    
def main():
    points = [Matrix([float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')])
              for i in range(1, int(input('Введите количество точек: ')) + 1)]
    if (len(points)) <= 1:
        print('B-сплайн не имеет смысла для данного количества точек')
        return 0
    k = 0  # порядок B-сплайна
    while k < 1 or k > len(points) + 1:
        k = int(input('Введите порядок B-сплайна (от 1 до N+1): '))
    # построение
    plt.figure()
    ax = plt.axes()
    plot_contour(points, ax, contour=False)
    drawBSpline([points[0], *points, points[-1]], k, ax)  # поправка на крайние нулевые базисные функции
    plt.title(f'Построение B-сплайна {k}-ого порядка')
    plt.legend(['Исходные точки', f'B-сплайн {k}-ого порядка'])
    plt.show()
    while True:
        point_for_change = int(input('Введите 0 для выхода или номер точки для изменения её координат: '))
        if point_for_change == 0:
            break
        else:
            points[point_for_change - 1] = Matrix([float(elem)
                                                   for elem in
                                                   input(f'Введите точку фигуры {point_for_change}: ').split(',')])
            plt.figure()
            ax = plt.axes()
            plot_contour(points, ax, contour=False)
            drawBSpline([points[0], *points, points[-1]], k, ax)
            plt.title(f'Построение B-сплайна {k}-ого порядка')
            plt.legend(['Исходные точки', f'B-сплайн {k}-ого порядка'])
            plt.show()

    
if __name__ == "__main__":
    main()
