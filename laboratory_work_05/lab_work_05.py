from random import *

def create_array(n, m):
    array = []
    for i in range(n):
        array.append([])
        for j in range(m):
            array[i].append(uniform(-10, 10))
    return array

def average(array):
    sum = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            sum += array[i][j]
    return sum / n**2

def

n = int(input("Введите размер матрицы N: "))

array = create_array(n, n)

print(array)
print(average(array))