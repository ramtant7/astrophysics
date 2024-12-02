# import numpy as np
# import matplotlib.pyplot as plt
# from sbpy.data import Orbit
# from astropy import units as u
# from astropy.time import Time
#
#
#
# # Параметры орбиты (Кеплеровы элементы)
# a = 1.0 * u.au  # большая полуось (в астрономических единицах)
# e = 0.1  # эксцентриситет
# i = 10 * u.deg  # наклонение (в градусах)
# Omega = 100 * u.deg  # долгота восходящего узла (в градусах)
# omega = 50 * u.deg  # аргумент перицентра (в градусах)
# M0 = 0 * u.deg  # начальная средняя аномалия (в градусах)
#
# # Время, на которое нужно рассчитать орбиту
# t0 = Time("2024-01-01 00:00:00", scale='utc')  # начальное время
# t = Time("2024-11-27 00:00:00", scale='utc')  # момент времени для вычислений
#
# # Создаем объект орбиты с использованием sbpy
# orbit = Orbit(a=a, e=e, i=i, Omega=Omega, omega=omega, M=M0)
#
# # Переводим время в годы для вычислений
# dt = (t - t0).to(u.day)  # время между t и t0 в днях
# dt_years = dt.to(u.year)  # преобразуем в годы
#
# # Рассчитаем положение тела на орбите на момент времени t
# orbit.compute(t)
#
# # Получаем координаты тела в 3D
# x, y, z = orbit.position.au  # координаты в астрономических единицах
#
# print(f"Координаты тела на орбите: x = {x:.2f} AU, y = {y:.2f} AU, z = {z:.2f} AU")
#
# # Визуализация орбиты
#
# # Параметры для визуализации эллиптической орбиты
# theta = np.linspace(0, 2 * np.pi, 100)
# r_orbit = a * (1 - e**2) / (1 + e * np.cos(theta))
#
# # Координаты для эллипса в плоскости орбиты
# x_orbit_ellipse = r_orbit * np.cos(theta)
# y_orbit_ellipse = r_orbit * np.sin(theta)
# z_orbit_ellipse = np.zeros_like(x_orbit_ellipse)
#
# # Преобразуем координаты эллипса в 3D
# orbit_points = np.array([x_orbit_ellipse, y_orbit_ellipse, z_orbit_ellipse])
#
# # Визуализируем орбиту
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
#
# # Отображаем орбиту
# ax.plot(orbit_points[0], orbit_points[1], orbit_points[2], label='Орбита', color='b')
#
# # Отображаем положение тела
# ax.scatter(x, y, z, color='r', label='Тело на орбите')
#
# # Настройки графика
# ax.set_xlabel('X (AU)')
# ax.set_ylabel('Y (AU)')
# ax.set_zlabel('Z (AU)')
# ax.set_title('Эллиптическая орбита тела в 3D')
# ax.legend()
#
# plt.show()
from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from sbpy.data import Ephem, Orbit

def plot_orbit(ax, orb, **plot_kwargs):
    """Orthographic projection onto the xy plane.

    2-body propagation of orbital elements, neglecting non-grav forces.

    """
    #epochs = orb['datetime_jd'] + np.linspace(-1, 1, 1000) * orb['P'] / 2
    eph = Ephem.from_oo(orb, epochs=1, dynmodel='2')
    ax.plot(eph['x'].value, eph['y'].value, **plot_kwargs)


def plot_object(ax, orb, epochs, **plot_kwargs):
    """Same as plot_orbit, but for single points."""
    eph = Ephem.from_oo(orb, epochs=epochs, dynmodel='2')
    ax.scatter(eph['x'].value, eph['y'].value, **plot_kwargs)


orbit = {
    'e':0,
    'q': 0.335950 * u.au,
    'i': 11.78142 * u.deg,
    'datetime_jd': 2458462.5
}

body1 = Orbit.from_dict(orbit)




fig = plt.figure(1, (8, 8))
fig.clear()
ax = fig.gca()

# H and G required for openorb's propagation
body1['H'] = 0
body1['G'] = 0.15

# orbits
plot_orbit(ax,body1,label = 'body1')

# Tp08 = Time(comet[0]['Tp_jd'], format='jd', scale='tt')
# Tp19 = Time(comet[1]['Tp_jd'], format='jd', scale='tt')
#
# # comet in 2008 (approximated with 2019 elements)
# TmTp = obs_dates['spitzer'] - Tp08
# epochs = (TmTp + Tp19).jd  # Julian Dates as a work around Issue #206
# plot_object(ax, comet[1], epochs, label='Spitzer epochs', zorder=99)
#
# # comet in 2019
# plot_object(ax, comet[1], obs_dates['bass'], label='BASS epoch', zorder=99)

plt.setp(ax, xlabel='X (au)', ylabel='Y (au)')
plt.legend()
plt.show()