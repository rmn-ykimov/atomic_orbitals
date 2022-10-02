import numpy as np


def orb(r, n1, n2=None, n3=None, coeff1=1., coeff2=1., coeff3=1., r0=1.0):
    """This function gives the value of the "orbital" at some point in
    space. An orbital is the sum of three angular components with three
    coefficients multiplied by a single radial component.

    r is a three-dimensional vector, the location of an electron in space.

    n1, n2, n3 is a 3D vector of x, y, z powers.

    The vector component in the angular part of each of the three components

    coeff1, coeff2, coeff3 are the coefficients in front of the corner
    components.

    r0 is the "size" of the radial part given by exp(-|r|/r0)."""
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


# Данная функция нужна, чтобы создать название орбитали. Требуются только
# степени угловой компоненты (n) и коэффициент перед ней.
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


def metropolis():
    """We start iterations using the Metropolis algorithm"""
    for nstep in range(0, args.NumSteps):
        # генерируем новую точку, приписывая случайное смещение к нынешнему
        # положению в пространстве
        trial_r = current_r + np.random.uniform(low=-args.MaxStep,
                                                high=args.MaxStep,
                                                size=3)
        # считаем значение орбитали в этой точке
        trial_orb_p = orb(r=trial_r, n1=n_pow1, n2=n_pow2, n3=n_pow3,
                          coeff1=args.c1,
                          coeff2=args.c2, coeff3=args.c3, r0=args.R0)
        # выбрасываем вероятность принятия новой точки
        p_trial = np.random.uniform(low=0, high=1)

        # а здесь мы сохраним значение того, примем ли мы новую точку, или нет
        do_we_accept = False

        # сначала просто проверим, что новая вероятность (квадрат орбитали)
        # выше, чем была, и если да, то принимаем точку
        if trial_orb_p ** 2 > current_orb_p ** 2:
            do_we_accept = True
        else:
            # если вероятность новой точки ниже, сравниваем вероятность перехода
            # в эту точку с вероятностью принятия
            if trial_orb_p ** 2 / current_orb_p ** 2 > p_trial:
                do_we_accept = True

        # если новую точку принимаем, то она становится новым значенем точки в
        # траектории, а ещё увеличиваем число принятых точек
        if do_we_accept:
            current_r = trial_r
            current_orb_p = trial_orb_p
            acc_rate += 1
            shift = np.zeros(
                current_r.shape)  # в этом случае сдвиг никакой нам не нужен
        else:
            # если точку не приняли, чтобы было не очень уныло, сохраним
            # значение старой точки с некоторым малым случайным сдвигом
            shift = np.random.uniform(low=-args.MaxSmallShift,
                                      high=args.MaxSmallShift, size=3)

        # и если часть игнорирования траектории закончилась, то сохраняем новое
        # значение
        if nstep > int(args.NumSteps * args.PartToIgnore):
            outf.write(" %15.10f %15.10f %15.10f " % tuple(current_r + shift))
            outf.write("  %15.5e   %10i\n" % (current_orb_p, nstep))
            outf.flush()

    # в конце выдаём процент принятых точек в траекторию (хотелось бы, чтобы оно
    # было в районе 20-60 %)
    outf.close()
    return print(
        "Acc rate = %15.10f %%" % (
                100. * float(acc_rate) / float(args.NumSteps)))
    outf.close()
