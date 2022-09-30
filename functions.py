import numpy as np


# Эта функция даёт значение "орбитали" в некоторой точке пространства
# Орбиталь является суммой трёх угловых компонент с тремя коэффициентами,
# домноженной на единую радиальную компоненту. r  -- это трёхмерный вектор,
# расположение электрона в пространстве n1,n2,n3 -- это трёхмерный вектор
# степеней x,y,z компонент вектора в угловой части каждой из трёх компонент
# coeff1,coeff2,coeff3 -- это собственно коэффициенты перед угловыми
# компонентами r0 -- это "размер" радиальной части, даваемой выражением exp(
# -|r|/r0)
def orb(r, n1, n2=None, n3=None, coeff1=1., coeff2=1., coeff3=1., r0=1.0):
    # считаем значение угловой компоненты Ang
    ang = coeff1 * np.prod(np.power(r, n1))
    if not n2 is None:
        ang += coeff2 * np.prod(np.power(r, n2))
    if not n3 is None:
        ang += coeff3 * np.prod(np.power(r, n3))

    arg = np.sqrt(np.dot(r, r)) / r0  # это аргумент для радиальной компоненты

    rad = np.exp(-arg)  # считаем значение радиальной компоненты орбитали

    return rad * ang  # ответ -- это произведение радиальной и угловой
    # компонент


# данная функция нужна, чтобы сделать название орбитали
# нам нужны только степени угловой компоненты (n) и коэффициент перед ней
def pow_to_name(n, coeff=1.):
    function_name = ""

    # нет угловой компоненты -- нет и функции
    if n is None or coeff is None:
        return ""

    # смотрим на знак коэффициента для углового компонента
    if not coeff is None:
        if coeff > 0:
            function_name += "+%.2f" % coeff
        elif coeff < 0:
            function_name += "%.2f" % coeff
        else:
            return ""  # если коэффициент нулевой, эта компонента ничего и
            # не даёт

    # Степень полинома угловой компоненты - это тип функции (s/p/d/f...),
    # его мы и проверяем
    if np.sum(n) == 0:
        function_name += "s"
    elif np.sum(n) == 1:
        function_name += "p"
    elif np.sum(n) == 2:
        function_name += "d"
    elif np.sum(n) == 3:
        function_name += "f"
    elif np.sum(n) == 4:
        function_name += "g"
    elif np.sum(n) == 5:
        function_name += "h"
    else:
        function_name += "X3"  # можно пойти и дальше, но кому это нужно?

    # и показываем какая конкретно радиальная компонента у нас тут есть (
    # естественно, нулевые степени мы не печатаем)
    if n[0] > 0:
        function_name += "x"
        if n[0] > 1:
            function_name += "%i" % (n[0])
    if n[1] > 0:
        function_name += "y"
        if n[1] > 1:
            function_name += "%i" % (n[1])
    if n[2] > 0:
        function_name += "z"
        if n[2] > 1:
            function_name += "%i" % (n[2])

    return function_name
