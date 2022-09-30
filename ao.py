#! /usr/bin/python3

import numpy as np  # NumPy нужен для всего
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from functions import pow_to_name, orb, metropolis
from parser import parser


orb()

pow_to_name()

# Распарсим аргументы
args, unknown = parser.parse_known_args()

# составляем вектора из степеней для каждой из трёх угловых функций из того,
# что ввёл пользователь
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

metropolis()

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
