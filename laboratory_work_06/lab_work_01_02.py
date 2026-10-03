from math import *

def function_1(x, a):
    return pow(2, tan(x**2/2-1)**2+(2*cos(x-pi/6))/(1/2+sin(a)**2))

def function_2(x):
    return pow(2, log(3-cos(pi/4+2*x), 3+sin(x))/(1+tan(2*x/pi)**2))

a = float(input('Введите параметр а: '))
x = float(input('Введите значение x: '))

y = function_1(x, a)
print("{0:.2f} {1:.2f} {2:.4f}".format(a, x, y))

y = function_2(x)
print("{0:.2f} {1:.4f}".format(x, y))
