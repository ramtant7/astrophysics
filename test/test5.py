import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from plotly.graph_objects import Scatter3d, Figure, Frame

# Задаем орбиту
epoch = Time("2024-01-01")
orbit = Orbit.parabolic(
    attractor=Sun,
    a=1 * u.au,           	# Большая полуось (астрономическая единица)
    ecc=0.5 * u.one,   	# Эксцентриситет
    inc=7.25 * u.deg,     	# Наклонение
    raan=0 * u.deg,       	# Долгота восходящего узла
    argp=102.9373 * u.deg,	# Аргумент перицентра
    nu=0 * u.deg,         	# Истинная аномалия
    #epoch=epoch,
    #p = 1 * u.au
)

# Генерация точек для орбиты
n_points = 500  # Увеличено количество точек для плавности траектории
times = epoch + np.linspace(-365*2, 365, n_points) * u.day  # 1 год с шагом в n_points
positions = [orbit.propagate(time).rv()[0] for time in times]

# Получение координат орбиты
x = [pos[0].to_value(u.au) for pos in positions]
y = [pos[1].to_value(u.au) for pos in positions]
z = [pos[2].to_value(u.au) for pos in positions]

# Определяем границы для пропорционального масштабирования
max_range = max(max(np.abs(x)), max(np.abs(y)), max(np.abs(z)))

sun_size = 10
object_size = 5

# Создание кадров для анимации
frames = [
    Frame(data=[
        # Центральное тело (Солнце)
        Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
        Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
        Scatter3d(
            x=[x[k]], y=[y[k]], z=[z[k]],
            mode="markers", marker=dict(size=object_size, color="red"), name="Объект"
        )
    ])
    for k in range(n_points)
]

# Создание графика
fig = Figure(
    data=[
        # Траектория орбиты (статичный элемент)
        Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
        # Центральное тело (Солнце)
        Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
        # Объект на орбите (начальная точка)
        Scatter3d(x=[x[0]], y=[y[0]], z=[z[0]], mode="markers", marker=dict(size=object_size, color="red"), name="Объект"),
    ],
    frames=frames
)

# Настройка осей и анимации
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-max_range, max_range], title="X (AU)", visible=True),
        yaxis=dict(range=[-max_range, max_range], title="Y (AU)", visible=True),
        zaxis=dict(range=[-max_range, max_range], title="Z (AU)", visible=True),
        aspectmode="cube",  # Гарантирует одинаковый масштаб для всех осей
    ),
    title="Динамическая 3D модель движения по орбите",
    updatemenus=[
        {
            "buttons": [
                {"args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
                 "label": "▶",
                 "method": "animate"},
                {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                 "label": "❚❚",
                 "method": "animate"},
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ],
)

# Сохранение в HTML
output_filename = "dynamic_orbit.html"
fig.write_html(output_filename, auto_open=True)
