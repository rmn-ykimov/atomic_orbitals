#! /usr/bin/python3

import numpy as np  # NumPy нужен для всего
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from functions import pow_to_name, orb
from parser import parser


orb()

pow_to_name()

# а теперь распарсим аргументы
args, unknown = parser.parse_known_args()

# составляем вектора из степеней для каждой из трёх угловых функций из того,
# что ввёл юзер
n_pow1 = np.array([args.nx1, args.ny1, args.nz1], dtype=int)
n_pow2 = np.array([args.nx2, args.ny2, args.nz2], dtype=int)
n_pow3 = np.array([args.nx3, args.ny3, args.nz3], dtype=int)

# выбираем случайную стартовую точку в заданной юзером области пространства
# (кубике вокруг r=(0,0,0) со стороной 2*MaxBox)
current_r = np.random.uniform(low=-args.MaxBox, high=args.MaxBox, size=3)
# считаем значение орибитали в этой точке
current_orb_p = orb(r=current_r, n1=n_pow1, n2=n_pow2, n3=n_pow3,
                    coeff1=args.c1,
                    coeff2=args.c2, coeff3=args.c3, r0=args.R0)

# в этот файл мы будем сохранять саму траекторию
file_name = "orbital_%s%s%s.dat" % (
    pow_to_name(n_pow1, args.c1), pow_to_name(n_pow2, args.c2),
    pow_to_name(n_pow3, args.c3))
outf = open(file_name, "w")

acc_rate = 0  # Это количество принимаемых шагов в траектории, чтобы
# вычислить долю принятия (должна быть в диапазоне 20-60 %)

# начинаем итерации метода Метрополиса 
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
print(
    "Acc rate = %15.10f %%" % (100. * float(acc_rate) / float(args.NumSteps)))
outf.close()

# А теперь построим всю эту красоту, если юзер захотел
if args.plot:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    data = np.loadtxt(file_name)
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=data[:, 3],
               cmap='coolwarm', s=args.MaxSmallShift * 0.1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
