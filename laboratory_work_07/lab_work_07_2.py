import turtle
from random import uniform

def function(x, y):
    if (x < -1) or (x > 4):
        flag = 0   #False
    if ((x>=-1) and (x<1) and (y>=2*x+2)
            and (y<=x**3-4*x**2+x+6) or (x>=1)
            and (x<=4) and (y>=x**3-4*x**2+x+6)
            and (y<=2*x+2)):
        flag = 1
    else:
        flag = 0
    return flag

def plot_axis(min_value, max_value, ax="X"):
    turtle.up()
    if ax == "X":
        begin = (min_value, 0)
        end = (max_value, 0)
    else:
        begin = (0, min_value)
        end = (0, max_value)
    turtle.goto(begin)
    turtle.down()
    turtle.goto(end)


def plot_mark(min_value, max_value, ax="X"):
    turtle.up()
    for t in range(min_value, max_value):
        if ax == "X":
            point_begin = (t, 0)
            point_end = (t, 0.2)
            point_width = (t, -0.5)
        else:
            point_begin = (0, t)
            point_end = (0.2, t)
            point_width = (-0.5, t)
        turtle.goto(point_begin)
        turtle.down()
        turtle.goto(point_end)
        turtle.up()
        turtle.goto(point_width)
        turtle.write(str(t))


def plot_arrow(max_value, ax="X"):
    triangle = [(0.1, -0.1), (0, 0.3), (-0.1, -0.1)]
    turtle.up()
    turtle.goto(0, 0)
    turtle.begin_poly()
    for couple in triangle:
        turtle.goto(couple)
    turtle.end_poly()
    arrow = turtle.get_poly()
    turtle.register_shape("myArrow", arrow)
    turtle.resizemode("myArrow")
    turtle.shapesize(1, 2, 1)
    if ax == "X":
        turtle.tiltangle(0)
        turtle.goto(max_value + 0.2, 0)
        point_width = (int(max_value), -1.0)
    else:
        turtle.tiltangle(90)
        turtle.goto(0, max_value + 0.2)
        point_width = (0.2, int(max_value))
    turtle.stamp()
    turtle.goto(point_width)
    turtle.write(ax, font=("Arial", 14, "bold"))


def plot_function(min_value, max_value, n_max=1000):
    turtle.color("green")
    turtle.width(3)
    dx = (max_value - min_value) / n_max

    x = min_value
    y = function(x)
    if y is None:
        turtle.up()
        turtle.goto(x, y)
    else:
        turtle.goto(x, y)
        turtle.down()
    while x <= max_value:
        x = x + dx
        y = function(x)
        if y is None:
            turtle.up()
            continue
        else:
            turtle.goto(x, y)
            turtle.down()

if __name__ == "__main__":
    aX = [-2, 5] # левая и правая
    aY = [-2, 11] # нижняя и верхняя
    Dx = 1000
    Dy = Dx/((aX[1] - aX[0])/(aY[1] - aY[0]))
    turtle.setup(Dx, Dy, 200, 200)
    turtle.reset()
    Nmax = 10000
    turtle.setworldcoordinates(aX[0], aY[0], aX[1], aY[1])
    turtle.title("Laboratory work 7 task 2")

    turtle.width(5)
    turtle.color("blue")
    turtle.tracer(0, 0)

    turtle.up()
    mfun = 0
    for n in range(Nmax):
        x = uniform(aX[0], aX[1])
        y = uniform(aY[0], aY[1])
        turtle.goto(x, y)
        if function(x, y) != 0:
            turtle.dot(10, "green")
            mfun += 1
        else:
            turtle.dot(10, "cyan")

    plot_axis(aX[0], aX[1], "X")
    plot_mark(aX[0], aX[1], "X")
    plot_arrow(aX[1], "X")

    plot_axis(aY[0], aY[1], "Y")
    plot_mark(aY[0], aY[1], "Y")
    plot_arrow(aY[1], "Y")

    turtle.mainloop()