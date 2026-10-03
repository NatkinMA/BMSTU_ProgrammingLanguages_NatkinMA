from math import *
from lab_work_01_02 import function_1, function_2

#def function_1(x, a):
#    return tan(x**2/2-1)**2+(2*cos(x-pi/6))/(1/2+sin(a)**2)

#def function_2(x):
#    return pow(2, log(3-cos(pi/4+2*x), 3+sin(x))/(1+tan(2*x/pi)**2))

if __name__ == "__main__":
    file = open("input.txt", "r")
    file_output = open("output.txt", "w")

    print(__name__)

    for line in file:
        if line == "\n":
            continue
        a, b = line.split()
        file_output.write(f"{a} {b} {function_1(float(a), float(b))} {function_2(float(a))}\n")

