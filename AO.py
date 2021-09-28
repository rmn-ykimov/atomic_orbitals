#! /usr/bin/python3

import numpy as np  # NumPy нужен для всего
import argparse     # Это модуль, для "общения" с юзером



# Эта функция даёт значение "орбитали" в некоторой точке пространства
# Орбиталь является суммой трёх угловых компонент с тремя коэффициентами, домноженной на единую радиальную компоненту.
# r  -- это трёхмерный вектор, расположение электрона в пространстве
# n1,n2,n3 -- это трёхмерный вектор степеней x,y,z компонент вектора в угловой части каждой из трёх компонент
# coeff1,coeff2,coeff3 -- это собственно коэффициенты перед угловыми компонентами
# r0 -- это "размер" радиальной части, даваемой выражением exp(-|r|/r0)
def orb(r, n1, n2=None, n3=None, coeff1=1., coeff2=1., coeff3=1., r0 = 1.0):

    # считаем значение угловой компоненты Ang
    Ang = coeff1 * np.prod(np.power(r,n1))
    if not n2 is None:
         Ang += coeff2 * np.prod(np.power(r,n2))
    if not n3 is None:
         Ang += coeff3 * np.prod(np.power(r,n3))

    Arg = np.sqrt(np.dot(r,r))/r0 # это аргумент для радиальной компоненты

    Rad = np.exp(-Arg)   # считаем значение радиальной компоненты орбитали
    
    return  Rad * Ang # ответ -- это произведение радиальной и угловой компонент
    
# данная функция нужна, чтобы сделать название орбитали
# нам нужны только степени угловой компоненты (n) и коэффициент перед ней
def PowToName(n, coeff=1.):
    FunctionName = ""

    # нет угловой компоненты -- нет и функции
    if n is None or coeff is None:
        return ""
        
    # смотрим на знак коэффициента для углового компонента    
    if not coeff is None:
        if coeff > 0:
            FunctionName += "+%.2f"  % coeff
        elif coeff <0:
            FunctionName += "%.2f" % coeff
        else:
            return "" # если коэффициент нулевой, эта компонента ничего и не даёт
    
    # Степень полинома угловой компоненты -- это тип функции (s/p/d/f...), его мы и проверяем
    if np.sum(n) == 0:
        FunctionName += "s"
    elif np.sum(n) == 1:
        FunctionName += "p"
    elif np.sum(n) == 2:
        FunctionName += "d"
    elif np.sum(n) == 3:
        FunctionName += "f"
    elif np.sum(n) == 4:
        FunctionName += "g"
    elif np.sum(n) == 5:
        FunctionName += "h"
    else:
        FunctionName += "X3" # можно пойти и дальше, но кому это нужно?
    
    
    # и показываем какая конкретно радиальная компонента у нас тут есть (естественно, нулевые степени мы не печатаем)
    if n[0]>0:
        FunctionName += "x"
        if n[0] > 1:
            FunctionName += "%i" %  (n[0])
    if n[1]>0:
        FunctionName += "y"
        if n[1] > 1:
            FunctionName += "%i" %  (n[1])
    if n[2]>0:
        FunctionName += "z"
        if n[2] > 1:
            FunctionName += "%i" %  (n[2])
               
    return FunctionName
   


# argument parser to get options from command line
parser = argparse.ArgumentParser(description='Давайте-ка нарисуем орбитальки при помощи метода Монте-Кало (МК)!') 


parser.add_argument('--c1', type=float, default=1.0, 
                    help="Коэффициент перед первой угловой функцией")  


parser.add_argument('--c2', type=float, default=0.0, 
                    help="Коэффициент перед второй угловой функцией")  


parser.add_argument('--c3', type=float, default=0.0, 
                    help="Коэффициент перед третьей угловой функцией")  

parser.add_argument('--nx1', type=int, default=0, 
                    help="Степень n в функции x**n для первой угловой функции") 

parser.add_argument('--nx2', type=int, default=0, 
                    help="Степень n в функции x**n для второй угловой функции") 

parser.add_argument('--nx3', type=int, default=0, 
                    help="Степень n в функции x**n для третьей угловой функции") 

parser.add_argument('--ny1', type=int, default=0, 
                    help="Степень n в функции y**n для первой угловой функции") 

parser.add_argument('--ny2', type=int, default=0, 
                    help="Степень n в функции y**n для второй угловой функции") 

parser.add_argument('--ny3', type=int, default=0, 
                    help="Степень n в функции y**n для третьей угловой функции") 

parser.add_argument('--nz1', type=int, default=0, 
                    help="Степень n в функции z**n для первой угловой функции") 

parser.add_argument('--nz2', type=int, default=0, 
                    help="Степень n в функции z**n для второй угловой функции") 

parser.add_argument('--nz3', type=int, default=0, 
                    help="Степень n в функции z**n для третьей угловой функции") 

parser.add_argument('--NumSteps', type=int, default=50000, 
                    help="Число шагов в МК симуляции") 

parser.add_argument('--R0', type=float, default=1.0, 
                    help="Размер орбитали R0") 

parser.add_argument('--PartToIgnore', type=float, default=0.1, 
                    help="Доля МК траектории в начале, которая игнорируется в расчётах, как стадия уравновешивания") 


parser.add_argument('--MaxBox', type=float, default=0.1, 
                    help="Размер стартовой области, из которой случайно выбирается стартовая точка МК-траектории") 


parser.add_argument('--MaxStep', type=float, default=2.0, 
                    help="Максимальная длина шага в МК-траектории") 


parser.add_argument('--MaxSmallShift', type=float, default=0.1, 
                    help="Маленькая добавочка к значениям траектории, когда мы остаёмся в той же точке (для красоты)") 


parser.add_argument('--plot',action='store_true', 
                    help="Флаг, чтобы нарисовать орбитальку при помощи matplotlib") 



# а теперь распарсим аргументы
args,unknown = parser.parse_known_args()


# составляем вектора из степеней для каждой из трёх угловых функций из того, что ввёл юзер
NPow1 = np.array([args.nx1,args.ny1,args.nz1] ,dtype=int)
NPow2 = np.array([args.nx2,args.ny2,args.nz2] ,dtype=int)
NPow3 = np.array([args.nx3,args.ny3,args.nz3] ,dtype=int)    
        

# выбираем случайную стартовую точку в заданной юзером области пространства (кубике вокруг r=(0,0,0) со стороной 2*MaxBox)
currentR = np.random.uniform(low=-args.MaxBox, high=args.MaxBox, size=3) 
# считаем значение орибитали в этой точке
currentOrbP = orb(r=currentR, n1=NPow1, n2=NPow2, n3=NPow3, coeff1=args.c1, coeff2=args.c2, coeff3=args.c3, r0 = args.R0)

# в этот файл мы будем сохранять саму траекторию
FileName="orbital_%s%s%s.dat" % (PowToName(NPow1, args.c1),PowToName(NPow2, args.c2),PowToName(NPow3, args.c3))
outf = open(FileName, "w")

AccRate = 0 # Это количество принимаемых шагов в траектории, чтобы вычислить долю принятия (должна быть в диапазоне 20-60 %)

# начинаем итерации метода Метрополиса 
for nstep in range(0,args.NumSteps):
    # генерируем новую точку, приписывая случайное смещение к нынешнему положению в пространстве
    trialR = currentR + np.random.uniform(low=-args.MaxStep, high=args.MaxStep, size=3) 
    # считаем значение орбитали в этой точке
    trialOrbP = orb(r=trialR, n1=NPow1, n2=NPow2, n3=NPow3, coeff1=args.c1, coeff2=args.c2, coeff3=args.c3, r0 = args.R0)        
    # выбрасываем вероятность принятия новой точки
    Ptrial = np.random.uniform(low=0, high=1)
    
    # а здесь мы сохраним значение того, примем ли мы новую точку, или нет
    DoWeAccept = False
    
    # сначала просто проверим, что новая вероятность (квадрат орбитали) выше, чем была, и если да, то принимаем точку
    if (trialOrbP**2 > currentOrbP**2):
        DoWeAccept = True
    else:
        # если вероятность новой точки ниже, сравниваем вероятность перехода в эту точку с вероятностью принятия
        if trialOrbP**2/currentOrbP**2 > Ptrial:
            DoWeAccept = True
    
    # если новую точку принимаем, то она становится новым значенем точки в траектории, а ещё увеличиваем число принятых точек
    if DoWeAccept:
        currentR = trialR
        currentOrbP = trialOrbP
        AccRate += 1
        shift = np.zeros(currentR.shape) # в этом случае сдвиг никакой нам не нужен
    else:
        # если точку не приняли, чтобы было не очень уныло, сохраним значение старой точки с некоторым малым случайным сдвигом
        shift = np.random.uniform(low=-args.MaxSmallShift, high=args.MaxSmallShift, size=3)
    
    # и если часть игнорирования траектории закончилась, то сохраняем новое значение    
    if nstep > int(args.NumSteps * args.PartToIgnore):
        outf.write(" %15.10f %15.10f %15.10f " % tuple(currentR + shift))
        outf.write("  %15.5e   %10i\n" % (currentOrbP, nstep))    
        outf.flush()
    
    
# в конце выдаём процент принятых точек в траекторию (хотелось бы, чтобы оно было в районе 20-60 %)
print("Acc rate = %15.10f %%" % (100.*float(AccRate)/float(args.NumSteps)) )
outf.close()    


############## А теперь построим всю эту красоту, если юзер захотел
if args.plot:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    data = np.loadtxt(FileName)
    ax.scatter(data[:,0], data[:,1], data[:,2], c=data[:,3],cmap = 'coolwarm',s=args.MaxSmallShift*0.1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()