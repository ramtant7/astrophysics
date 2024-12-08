import numpy as np
import matplotlib.pyplot as plt
import imageio
from joblib import Parallel, delayed


def calculate(sentMessage):
    # Шесть Кеплеровских элементов орбиты
    a = np.float64(sentMessage['A'])  # Большая полуось (в астрономических единицах)
    e = np.float64(sentMessage['E'])  # Эксцентриситет
    i = np.float64(sentMessage['I'])  # Наклонение (в градусах)
    Omega = np.float64(sentMessage['Omega'])  # Долгота восходящего узла (в градусах)
    omega = np.float64(sentMessage['omega'])  # Аргумент перицентра (в градусах)
    M = np.float64(sentMessage['M'])  # Средняя аномалия (в градусах)

    # Преобразование углов из градусов в радианы
    i_rad = np.radians(i)
    Omega_rad = np.radians(Omega)
    omega_rad = np.radians(omega)
    M_rad = np.radians(M)

    # Количество кадров для анимации
    frames = 360


    # Функция для вычисления позиции на орбите
    def compute_orbital_position(M_deg):
        M_rad = np.radians(M_deg)

        # Вычисление истинной аномалии E через уравнение Кеплера
        E = M_rad + e * np.sin(M_rad) * (1.0 + e * np.cos(M_rad))
        nu = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))

        # Положение объекта на орбите в полярных координатах
        r = a * (1 - e ** 2) / (1 + e * np.cos(nu))
        x_polar = r * np.cos(nu)
        y_polar = r * np.sin(nu)

        # Поворот системы координат по аргументу перицентра
        x_prime = x_polar * np.cos(omega_rad) - y_polar * np.sin(omega_rad)
        y_prime = x_polar * np.sin(omega_rad) + y_polar * np.cos(omega_rad)

        # Поворот системы координат по наклонению и долготе восходящего узла
        x = x_prime
        y = y_prime * np.cos(i_rad)
        z = y_prime * np.sin(i_rad)

        return x, y, z


    # Генерация данных для орбиты
    orbital_data = []
    for frame in range(frames):
        orbital_data.append(compute_orbital_position(frame))

    # Разделение данных на компоненты X, Y, Z
    x_data, y_data, z_data = zip(*orbital_data)

    # Инициализация списков для хранения изображений
    xy_images = []
    yz_images = []
    xz_images = []

    # Параметры для визуализации
    axis_limits = [-1.5, 1.5]
    line_color = "blue"
    point_color = "red"
    sun_color = "yellow"


    # Функция для генерации одного кадра
    def generate_frame(frame):
        # Создание фигур и осей
        xy_fig, xy_ax = plt.subplots(figsize=(8, 8))
        yz_fig, yz_ax = plt.subplots(figsize=(8, 8))
        xz_fig, xz_ax = plt.subplots(figsize=(8, 8))

        # XY-плоскость
        xy_ax.scatter([0], [0], color=sun_color, s=100)  # Солнце
        xy_ax.plot(x_data[:frame + 1], y_data[:frame + 1], line_color)
        xy_ax.scatter(x_data[frame], y_data[frame], color=point_color, s=50)
        xy_ax.set_xlim(axis_limits)
        xy_ax.set_ylim(axis_limits)
        xy_ax.set_xlabel('X')
        xy_ax.set_ylabel('Y')

        # YZ-плоскость
        yz_ax.scatter([0], [0], color=sun_color, s=100)  # Солнце
        yz_ax.plot(y_data[:frame + 1], z_data[:frame + 1], line_color)
        yz_ax.scatter(y_data[frame], z_data[frame], color=point_color, s=50)
        yz_ax.set_xlim(axis_limits)
        yz_ax.set_ylim(axis_limits)
        yz_ax.set_xlabel('Y')
        yz_ax.set_ylabel('Z')

        # XZ-плоскость
        xz_ax.scatter([0], [0], color=sun_color, s=100)  # Солнце
        xz_ax.plot(x_data[:frame + 1], z_data[:frame + 1], line_color)
        xz_ax.scatter(x_data[frame], z_data[frame], color=point_color, s=50)
        xz_ax.set_xlim(axis_limits)
        xz_ax.set_ylim(axis_limits)
        xz_ax.set_xlabel('X')
        xz_ax.set_ylabel('Z')

        # Получение изображений кадров
        xy_fig.canvas.draw()
        xy_img = np.frombuffer(xy_fig.canvas.tostring_rgb(), dtype=np.uint8)
        xy_img = xy_img.reshape(xy_fig.canvas.get_width_height()[::-1] + (3,))

        yz_fig.canvas.draw()
        yz_img = np.frombuffer(yz_fig.canvas.tostring_rgb(), dtype=np.uint8)
        yz_img = yz_img.reshape(yz_fig.canvas.get_width_height()[::-1] + (3,))

        xz_fig.canvas.draw()
        xz_img = np.frombuffer(xz_fig.canvas.tostring_rgb(), dtype=np.uint8)
        xz_img = xz_img.reshape(xz_fig.canvas.get_width_height()[::-1] + (3,))

        # Закрытие фигур
        plt.close(xy_fig)
        plt.close(yz_fig)
        plt.close(xz_fig)

        return xy_img, yz_img, xz_img


    # Распараллеленная генерация кадров
    results = Parallel(n_jobs=-1)(delayed(generate_frame)(frame) for frame in range(frames))

    # Сбор результатов
    for result in results:
        xy_images.append(result[0])
        yz_images.append(result[1])
        xz_images.append(result[2])

    files = [
        ('../static/orbit/xy_orbit_animation.gif', xy_images),
        ('../static/orbit/yz_orbit_animation.gif', yz_images),
        ('../static/orbit/xz_orbit_animation.gif', xz_images)
    ]

    results = Parallel(n_jobs=-1)(delayed(imageio.mimsave)(f1, f2, fps=24, loop=0) for f1, f2 in files)

    # # Создание GIF-анимаций
    # imageio.mimsave('xy_orbit_animation.gif', xy_images, fps=24, loop=0)
    # imageio.mimsave('yz_orbit_animation.gif', yz_images, fps=24, loop=0)
    # imageio.mimsave('xz_orbit_animation.gif', xz_images, fps=24, loop=0)
    #
    # print("Анимации созданыны! Проверь файлы xy_orbit_animation.gif, yz_orbit_animation.gif и xz_orbit_animation.gif.")