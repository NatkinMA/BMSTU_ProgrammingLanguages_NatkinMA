# -*- coding: utf-8 -*-
"""Лабораторная работа 08.1. Построение графиков функций.

Объектно-ориентированная версия программы.

Классы:
    Window   - главное окно программы (обёртка над Tk);
    Canvas   - полотно для рисования и пересчёт пользовательских
               координат в пикселы;
    Pen      - "перо": цвет, толщина и графические примитивы
               (линия, прямоугольник, текст, метка);
    Function - функция, заданная на отрезке [Xmin, Xmax];
               Sin2xDevx - y = sin(2x)/x через разложение в ряд Тейлора;
               Sin2xOnX  - y = sin(2x)/x + смещение, вычисленная напрямую.
"""

from tkinter import Tk, Label, Entry, Button, W, N, E, S, END
from tkinter.messagebox import askyesno, showwarning
from tkinter import Canvas as TkCanvas
from math import sin


class Window:
    """Главное окно приложения."""

    def __init__(self, title="Графика"):
        self._root = Tk()
        self._root.title(title)
        self._root.resizable(False, False)
        self._root.protocol("WM_DELETE_WINDOW", self.close_request)

    @property
    def tk(self):
        """Корневое окно Tk (нужно виджетам-обёрткам)."""
        return self._root

    def screen_width(self):
        return self._root.winfo_screenwidth()

    def screen_height(self):
        return self._root.winfo_screenheight()

    def label(self, text, row, column, width=10, fg="blue",
              font="Ubuntu 12", sticky="e"):
        lbl = Label(self._root, text=text, width=width, fg=fg, font=font)
        lbl.grid(row=row, column=column, sticky=sticky)
        return lbl

    def entry(self, row, column, value="", width=5,
              font="Ubuntu 12", sticky=None):
        ent = Entry(self._root, width=width, font=font)
        if sticky:
            ent.grid(row=row, column=column, sticky=sticky)
        else:
            ent.grid(row=row, column=column)
        ent.insert(0, value)
        return ent

    def button(self, text, row, column, command, width=20, bg="#ccc"):
        btn = Button(self._root, width=width, bg=bg, text=text)
        btn.grid(row=row, column=column)
        btn.bind("<Button-1>", command)
        return btn

    def close_request(self):
        """Завершаем работу по [X] или по кнопке "Выход"."""
        if askyesno("Выход", "Завершить работу?"):
            self._root.destroy()

    def mainloop(self):
        self._root.mainloop()


class Canvas:
    """Полотно рисования с пересчётом координат пользователя в пикселы."""

    def __init__(self, window, width, height, bg="white",
                 row=0, column=0, columnspan=9):
        self.width = width
        self.height = height
        self._cv = TkCanvas(window.tk, width=width, height=height, bg=bg)
        self._cv.grid(row=row, column=column, columnspan=columnspan)
        # Границы области построения в пользовательских координатах
        self.x_min = -10.0
        self.x_max = 10.0
        self.y_min = -5.0
        self.y_max = 5.0
        self.update_scale()

    def update_scale(self):
        """Пересчитать масштабные множители Kx и Ky."""
        self.kx = self.width / abs(self.x_max - self.x_min)
        self.ky = self.height / abs(self.y_max - self.y_min)

    def bind(self, event, handler):
        self._cv.bind(event, handler)

    def clear(self):
        self._cv.delete("all")

    def delete(self, *ids):
        self._cv.delete(*ids)

    def to_pixels(self, x, y):
        """Пользовательские координаты -> пикселы полотна."""
        px = self.kx * (x - self.x_min)
        py = self.height - self.ky * (y - self.y_min)
        return px, py

    def from_pixels(self, px, py):
        """Пикселы полотна -> пользовательские координаты."""
        x = self.x_min + px / self.kx
        y = self.y_min + (self.height - py) / self.ky
        return x, y

    def line(self, points, fill="black", width=1, dash=None):
        args = []
        for point in points:
            args.extend(point)
        if dash is None:
            return self._cv.create_line(*args, fill=fill, width=width)
        return self._cv.create_line(*args, fill=fill, width=width, dash=dash)

    def rectangle(self, x1, y1, x2, y2, fill="white", outline="black", width=1):
        return self._cv.create_rectangle(x1, y1, x2, y2,
                                         fill=fill, outline=outline, width=width)

    def text(self, x, y, s, anchor=N):
        return self._cv.create_text(x, y, text=s, anchor=anchor)

    def draw_axes(self, d_x, d_y):
        """Рисуем координатные линейки (рамка, метки, подписи)."""
        pen = Pen(self)
        pen.rectangle(5, 5, self.width - 5, self.height - 5,
                      fill="white", outline="green", width=2)
        # Метки по оси Y: слева и справа
        y = self.y_min
        y_pix = self.height
        flag = False
        while y < self.y_max:
            text_y = str(round(y, 2))
            pen.mark(0, y_pix)                     # слева
            pen.mark(self.width - 10, y_pix)       # справа
            if flag:
                pen.text(15, y_pix, text_y, anchor=W)
                pen.text(self.width - 15, y_pix, text_y, anchor=E)
            y += d_y
            y_pix -= d_y * self.ky
            flag = not flag
        # Метки по оси X: внизу и вверху
        x = self.x_min
        x_pix = 0
        flag = False
        while x < self.x_max:
            text_x = str(round(x, 2))
            pen.mark(x_pix, 0, horizontal=False)   # внизу
            pen.mark(x_pix, self.height, horizontal=False)  # вверху
            if flag:
                pen.text(x_pix, 15, text_x, anchor=N)
                pen.text(x_pix, self.height - 15, text_x, anchor=S)
            x += d_x
            x_pix += d_x * self.kx
            flag = not flag

    def plot(self, function, pen=None):
        """Получение значений функции, преобразование в пикселы, рисование."""
        if pen is None:
            pen = Pen(self, color=function.color)
        pixels = []
        for x, y in function.points():
            if y is None:            # точки вне области определения пропускаем
                continue
            pixels.append(self.to_pixels(x, y))
        pen.line(pixels, color=function.color, width=2)


class Pen:
    """Перо: цвет, толщина и примитивы рисования на полотне."""

    def __init__(self, canvas, color="black", width=1):
        self.canvas = canvas
        self.color = color
        self.width = width

    def line(self, points, color=None, width=None, dash=None):
        return self.canvas.line(points, fill=color or self.color,
                                width=width or self.width, dash=dash)

    def rectangle(self, x1, y1, x2, y2, fill="white",
                  outline=None, width=None):
        return self.canvas.rectangle(x1, y1, x2, y2, fill=fill,
                                     outline=outline or self.color,
                                     width=width or self.width)

    def text(self, x, y, s, anchor=N):
        return self.canvas.text(x, y, s, anchor=anchor)

    def mark(self, x, y, horizontal=True):
        """Нанесение метки на линейке: слева/справа (horizontal=True)
        или внизу/вверху (horizontal=False)."""
        if horizontal:
            points = [(x, y), (x + 10, y)]
        else:
            points = [(x, y), (x, y - 10)]
        return self.line(points, color="black", width=2)


class Function:
    """Функция на отрезке [x_min, x_max] с шагом step (в единицах x)."""

    def __init__(self, x_min, x_max, step, color="blue", shift=0.0):
        self.x_min = x_min
        self.x_max = x_max
        self.step = step
        self.color = color
        self.shift = shift

    def value(self, x):
        """Значение функции в точке x (переопределяется в наследниках)."""
        raise NotImplementedError

    def points(self):
        """Список точек (x, y) по всему отрезку построения."""
        pts = []
        x = self.x_min
        while x <= self.x_max:
            pts.append((x, self.value(x)))
            x += self.step
        return pts


class Sin2xDevx(Function):
    """y = sin(2x)/x через разложение в ряд Тейлора с точностью eps."""

    EPS = 0.0001

    def value(self, x):
        an = 1.0
        total = an
        n = 1
        while abs(an) > self.EPS:
            an *= -(2 ** 2) * (x ** 2) / ((2 * n) * (2 * n + 1))
            total += an
            n += 1
        return 2 * total + self.shift


class Sin2xOnX(Function):
    """y = sin(2x)/x + смещение, вычисленное напрямую.

    В точке x = 0 доопределяем пределом, равным 2.
    """

    def value(self, x):
        if x != 0:
            return sin(2 * x) / x + self.shift
        return 2.0 + self.shift


class GraphApp:
    """Приложение: окно, полотно, элементы управления и графики."""

    def __init__(self):
        self.window = Window("Графика")
        k_p = 0.7
        self.max_x = int(self.window.screen_width() * k_p)
        self.max_y = int(self.window.screen_height() * k_p)

        self.canvas = Canvas(self.window, self.max_x, self.max_y)
        self.canvas.bind("<Button-1>", self.show_xy)

        self.dash_pen = Pen(self.canvas)          # перо для визирных линий
        self.cross_v = None
        self.cross_h = None
        self.shift = 1.0                          # смещение функции
        self.step = 1.0                           # шаг меток

        self._build_ui()

    def _build_ui(self):
        win = self.window
        # Текущие координаты курсора
        win.label("X:", 1, 0)
        self.ent_x = win.entry(1, 1, "0", sticky="w")
        win.label("Y:", 2, 0)
        self.ent_y = win.entry(2, 1, "0", sticky="w")
        # Границы области построения
        win.label("Xmin:", 1, 2)
        self.ent_xmin = win.entry(1, 3, self.canvas.x_min)
        win.label("Xmax:", 1, 4)
        self.ent_xmax = win.entry(1, 5, self.canvas.x_max)
        win.label("Ymin:", 2, 2)
        self.ent_ymin = win.entry(2, 3, self.canvas.y_min)
        win.label("Ymax:", 2, 4)
        self.ent_ymax = win.entry(2, 5, self.canvas.y_max)
        # Шаг меток и смещение
        win.label("Шаг меток:", 1, 6)
        self.ent_step = win.entry(1, 7, self.step)
        win.label("Смещение:", 2, 6)
        self.ent_shift = win.entry(2, 7, self.shift)
        # Кнопки
        win.button("Рисовать", 1, 8, self.on_draw)
        win.button("Выход", 2, 8, self.on_exit)

    def read_bounds(self):
        """Получить данные из полей ввода и пересчитать масштаб."""
        try:
            x_max = float(self.ent_xmax.get())
            x_min = float(self.ent_xmin.get())
            y_max = float(self.ent_ymax.get())
            y_min = float(self.ent_ymin.get())
            step = float(self.ent_step.get())
            shift = float(self.ent_shift.get())
        except ValueError:
            showwarning(title="Ошибка ввода",
                        message="Все параметры должны быть числами")
            return False
        if (x_min >= x_max) or (y_min >= y_max) or (step <= 0):
            showwarning(title="Ошибка задания границ",
                        message="Должны выполняться неравенства:\n"
                                "Xmax > Xmin;\n"
                                "Ymax > Ymin;\n"
                                "Шаг меток > 0")
            return False
        self.canvas.x_min = x_min
        self.canvas.x_max = x_max
        self.canvas.y_min = y_min
        self.canvas.y_max = y_max
        self.canvas.update_scale()
        self.step = step
        self.shift = shift
        return True

    def on_draw(self, event):
        """Подготовка полотна и рисование графиков."""
        if not self.read_bounds():
            return
        self.canvas.clear()
        self.canvas.draw_axes(self.step, self.step)
        h = 1.0 / self.canvas.kx    # один шаг = один пиксел по X
        self.canvas.plot(Sin2xDevx(self.canvas.x_min, self.canvas.x_max, h,
                                   color="blue"))
        self.canvas.plot(Sin2xOnX(self.canvas.x_min, self.canvas.x_max, h,
                                  color="red", shift=self.shift))
        print("Рисуем")   # тестовое сообщение

    def on_exit(self, event):
        self.window.close_request()

    def show_xy(self, event):
        """Показать координаты курсора и нарисовать визирные линии."""
        x, y = self.canvas.from_pixels(event.x, event.y)
        self.ent_x.delete(0, END)
        self.ent_x.insert(0, str(round(x, 2)))
        self.ent_y.delete(0, END)
        self.ent_y.insert(0, str(round(y, 2)))
        self.canvas.delete(self.cross_v, self.cross_h)
        self.cross_v = self.dash_pen.line(
            [(event.x, 0), (event.x, self.max_y)], dash=(3, 5))
        self.cross_h = self.dash_pen.line(
            [(0, event.y), (self.max_x, event.y)], dash=(3, 5))

    def run(self):
        self.window.mainloop()


def main():
    GraphApp().run()


if __name__ == "__main__":
    main()
