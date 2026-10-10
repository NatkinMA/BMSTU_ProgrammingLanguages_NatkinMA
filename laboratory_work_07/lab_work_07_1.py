from math import sqrt
import turtle as tr


def function(x):
    y = 0.0
    if x < -5:
        y = 1
    elif -5 <= x < 0:
        y = -(3 / 5) * x - 2
    elif 0 <= x < 2:
        y = -sqrt(4 - x ** 2)
    elif 2 <= x < 4:
        y = x - 2
    elif 4 <= x < 8:
        y = 2 + sqrt(4 - (x - 6) ** 2)
    elif x >= 8:
        y = 2
    return y


def plot_axis(min_value, max_value, ax="X"):
    tr.up()
    if ax == "X":
        begin = (min_value, 0)
        end = (max_value, 0)
    else:
        begin = (0, min_value)
        end = (0, max_value)
    tr.goto(begin)
    tr.down()
    tr.goto(end)


def plot_mark(min_value, max_value, ax="X"):
    tr.up()
    for t in range(min_value, max_value):
        if ax == "X":
            point_begin = (t, 0)
            point_end = (t, 0.2)
            point_width = (t, -0.5)
        else:
            point_begin = (0, t)
            point_end = (0.2, t)
            point_width = (-0.5, t)
        tr.goto(point_begin)
        tr.down()
        tr.goto(point_end)
        tr.up()
        tr.goto(point_width)
        tr.write(str(t))


def plot_arrow(max_value, ax="X"):
    triangle = [(0.1, -0.1), (0, 0.3), (-0.1, -0.1)]
    tr.up()
    tr.goto(0, 0)
    tr.begin_poly()
    for couple in triangle:
        tr.goto(couple)
    tr.end_poly()
    arrow = tr.get_poly()
    tr.register_shape("myArrow", arrow)
    tr.resizemode("myArrow")
    tr.shapesize(1, 2, 1)
    if ax == "X":
        tr.tiltangle(0)
        tr.goto(max_value + 0.2, 0)
        point_width = (int(max_value), -1.0)
    else:
        tr.tiltangle(90)
        tr.goto(0, max_value + 0.2)
        point_width = (0.2, int(max_value))
    tr.stamp()
    tr.goto(point_width)
    tr.write(ax, font=("Arial", 14, "bold"))


def plot_function(min_value, max_value, n_max=1000):
    tr.color("green")
    tr.width(3)
    dx = (max_value - min_value) / n_max

    x = min_value
    y = function(x)
    if y is None:
        tr.up()
        tr.goto(x, y)
    else:
        tr.goto(x, y)
        tr.down()
    while x <= max_value:
        x = x + dx
        y = function(x)
        if y is None:
            tr.up()
            continue
        else:
            tr.goto(x, y)
            tr.down()


if __name__ == "__main__":
    aX = (-12, 12)
    aY = (-5, 5)

    Dx = 2000
    Dy = int(Dx / ((aX[1] - aX[0]) / (aY[1] - aY[0])))
    tr.setup(Dx, Dy)
    tr.reset()

    tr.setworldcoordinates(aX[0], aY[0], aX[1], aY[1])

    tr.title("lab_work_7_1")
    tr.width(2)
    tr.color("blue", "blue")

    tr.ht()
    tr.tracer(0, 0)

    plot_axis(aX[0], aX[1], "X")
    plot_mark(aX[0], aX[1], "X")
    plot_arrow(aX[1], "X")

    plot_axis(aY[0], aY[1], "Y")
    plot_mark(aY[0], aY[1], "Y")
    plot_arrow(aY[1], "Y")

    plot_function(aX[0], aX[1], 1000)

    tr.mainloop()
