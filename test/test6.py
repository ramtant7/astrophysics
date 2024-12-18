import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from plotly.graph_objects import Scatter3d, Figure, Frame

# Задаем время начала (эпоху)
epoch = Time("2024-01-01")

# Эллиптическая орбита
orbit_elliptic = Orbit.from_classical(
    attractor=Sun,
    a=1 * u.au,           # Большая полуось
    ecc=0.5 * u.one,      # Эксцентриситет (добавлено)
    inc=7.25 * u.deg,     # Наклонение
    raan=0 * u.deg,       # Долгота восходящего узла
    argp=102.9373 * u.deg,# Аргумент перицентра
    nu=0 * u.deg          # Истинная аномалия
)

# Параболическая орбита (эксцентриситет = 1)
# Нужно задать параметр p, который является фокусным параметром орбиты
orbit_parabolic = Orbit.parabolic(
    attractor=Sun,
    p=1 * u.au,  # Параметр орбиты (расстояние от Солнца до перицентра)
    inc=7.25 * u.deg,        # Наклонение
    raan=0 * u.deg,          # Долгота восходящего узла
    argp=102.9373 * u.deg,   # Аргумент перицентра
    nu=0 * u.deg,            # Истинная аномалия
)

# Гиперболическая орбита (эксцентриситет > 1)
orbit_hyperbolic = Orbit.from_classical(
    attractor=Sun,
    a=-1 * u.au,           # Большая полуось
    ecc=1.5 * u.one,      # Эксцентриситет (больше 1 для гиперболической орбиты)
    inc=7.25 * u.deg,     # Наклонение
    raan=0 * u.deg,       # Долгота восходящего узла
    argp=102.9373 * u.deg,# Аргумент перицентра
    nu=0 * u.deg          # Истинная аномалия
)

# Функция для генерации точек орбиты
def generate_orbit_points(orbit, n_points=500):
    times = epoch + np.linspace(-365*2, 365, n_points) * u.day  # 1 год с шагом в n_points
    positions = [orbit.propagate(time).rv()[0] for time in times]
    x = [pos[0].to_value(u.au) for pos in positions]
    y = [pos[1].to_value(u.au) for pos in positions]
    z = [pos[2].to_value(u.au) for pos in positions]
    return x, y, z

# Генерация точек для орбит
x_elliptic, y_elliptic, z_elliptic = generate_orbit_points(orbit_elliptic)
x_parabolic, y_parabolic, z_parabolic = generate_orbit_points(orbit_parabolic)
x_hyperbolic, y_hyperbolic, z_hyperbolic = generate_orbit_points(orbit_hyperbolic)

# Определяем границы для пропорционального масштабирования отдельно для каждой орбиты
def get_max_range(x, y, z):
    return max(max(np.abs(x)), max(np.abs(y)), max(np.abs(z)))

max_range_elliptic = get_max_range(x_elliptic, y_elliptic, z_elliptic)
max_range_parabolic = get_max_range(x_parabolic, y_parabolic, z_parabolic)
max_range_hyperbolic = get_max_range(x_hyperbolic, y_hyperbolic, z_hyperbolic)

sun_size = 10
object_size = 5

# Функция для создания кадров анимации
def create_frames(x, y, z, n_points):
    frames = [
        Frame(data=[
            # Центральное тело (Солнце)
            Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
            # Орбита
            Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
            # Объект на орбите (позиций k)
            Scatter3d(
                x=[x[k]], y=[y[k]], z=[z[k]],
                mode="markers", marker=dict(size=object_size, color="red"), name="Объект"
            )
        ])
        for k in range(n_points)
    ]
    return frames

# Создание кадров для анимации орбит
frames_elliptic = create_frames(x_elliptic, y_elliptic, z_elliptic, len(x_elliptic))
frames_parabolic = create_frames(x_parabolic, y_parabolic, z_parabolic, len(x_parabolic))
frames_hyperbolic = create_frames(x_hyperbolic, y_hyperbolic, z_hyperbolic, len(x_hyperbolic))

# Создание графика для эллиптической орбиты
fig_elliptic = Figure(
    data=[
        # Траектория орбиты
        Scatter3d(x=x_elliptic, y=y_elliptic, z=z_elliptic, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
        # Центральное тело (Солнце)
        Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
        # Объект на орбите (начальная точка)
        Scatter3d(x=[x_elliptic[0]], y=[y_elliptic[0]], z=[z_elliptic[0]], mode="markers", marker=dict(size=object_size, color="red"), name="Объект"),
    ],
    frames=frames_elliptic
)

# Создание графика для параболической орбиты
fig_parabolic = Figure(
    data=[
        # Траектория орбиты
        Scatter3d(x=x_parabolic, y=y_parabolic, z=z_parabolic, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
        # Центральное тело (Солнце)
        Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
        # Объект на орбите (начальная точка)
        Scatter3d(x=[x_parabolic[0]], y=[y_parabolic[0]], z=[z_parabolic[0]], mode="markers", marker=dict(size=object_size, color="red"), name="Объект"),
    ],
    frames=frames_parabolic
)

# Создание графика для гиперболической орбиты
fig_hyperbolic = Figure(
    data=[
        # Траектория орбиты
        Scatter3d(x=x_hyperbolic, y=y_hyperbolic, z=z_hyperbolic, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
        # Центральное тело (Солнце)
        Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
        # Объект на орбите (начальная точка)
        Scatter3d(x=[x_hyperbolic[0]], y=[y_hyperbolic[0]], z=[z_hyperbolic[0]], mode="markers", marker=dict(size=object_size, color="red"), name="Объект"),
    ],
    frames=frames_hyperbolic
)

# Настройка осей и анимации для каждого графика
def update_layout(fig, max_range):
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_range, max_range], title="X (AU)", visible=True),
            yaxis=dict(range=[-max_range, max_range], title="Y (AU)", visible=True),
            zaxis=dict(range=[-max_range, max_range], title="Z (AU)", visible=True),
            aspectmode="cube",  # Гарантирует одинаковый масштаб для всех осей
        ),
        title="Динамическая 3D модель орбиты",
        updatemenus=[
            {
                "buttons": [
                    {"args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
                     "label": "\u25B6", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                     "label": "\u275A\u275A", "method": "animate"},
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0.1,
                "yanchor": "top"
            }
        ]
    )

# Обновляем графики с соответствующими пределами
update_layout(fig_elliptic, max_range_elliptic)
update_layout(fig_parabolic, max_range_parabolic)
update_layout(fig_hyperbolic, max_range_hyperbolic)

# Сохранение в HTML для всех орбит
fig_elliptic.write_html("html/elliptic_orbit.html", auto_open=True)
fig_parabolic.write_html("html/parabolic_orbit.html", auto_open=True)
fig_hyperbolic.write_html("html/hyperbolic_orbit.html", auto_open=True)
