import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from plotly.graph_objects import Scatter3d, Figure, Frame

def NewtonsMethod(e,M):

    E = np.radians(M) if e < 0.8 else np.pi

    for i in range(100):
        f = E - e *np.sin(E) - M
        f_deriv = 1 - e * np.sin(E)
        E_new = E - f /f_deriv
        if abs(E_new - E) < 10**(-6):
            break
        E = E_new
    nu = 2 * np.arctan( np.sqrt( ( 1 + e ) / ( 1 - e ) ) * np.tan( E / 2 ))
    return np.degrees(nu)



def calculate3d(sentMessage):
    # Задаем время начала (эпоху)
    epoch = Time("2024-01-01")

    nu = NewtonsMethod(np.float64(sentMessage['E']),np.float64(sentMessage['M']))

    # Параметры эллиптической орбиты
    orbit_elliptic = Orbit.from_classical(
        attractor=Sun,
        a = np.float64(sentMessage['A']) * u.au,           # Большая полуось
        ecc = np.float64(sentMessage['E']) * u.one,      # Эксцентриситет
        inc = np.float64(sentMessage['I']) * u.deg,        # Наклонение
        raan = np.float64(sentMessage['Omega']) * u.deg,      # Долгота восходящего узла
        argp = np.float64(sentMessage['omega']) * u.deg,      # Аргумент перицентра
        nu = nu * u.deg          # Истинная аномалия
    )


    # Функция для генерации точек орбиты
    def generate_orbit_points(orbit, n_points=500):
        times = epoch + np.linspace(-365, 365, n_points) * u.day  # 1 год с шагом n_points
        positions = [orbit.propagate(time).rv()[0] for time in times]
        x = [pos[0].to_value(u.au) for pos in positions]
        y = [pos[1].to_value(u.au) for pos in positions]
        z = [pos[2].to_value(u.au) for pos in positions]
        return x, y, z

    # Генерация точек
    x_elliptic, y_elliptic, z_elliptic = generate_orbit_points(orbit_elliptic)

    # Определение границ
    max_range = max(max(np.abs(x_elliptic)), max(np.abs(y_elliptic)), max(np.abs(z_elliptic)))

    sun_size = 10
    object_size = 5

    # Создание кадров анимации
    def create_frames(x, y, z, n_points):
        frames = [
            Frame(data=[
                Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
                Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
                Scatter3d(
                    x=[x[k]], y=[y[k]], z=[z[k]],
                    mode="markers", marker=dict(size=object_size, color="red"), name="Объект"
                )
            ])
            for k in range(n_points)
        ]
        return frames

    frames_elliptic = create_frames(x_elliptic, y_elliptic, z_elliptic, len(x_elliptic))

    # Создание графика
    fig_elliptic = Figure(
        data=[
            Scatter3d(x=x_elliptic, y=y_elliptic, z=z_elliptic, mode="lines", line=dict(color="blue", width=3), name="Орбита"),
            Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=sun_size, color="yellow"), name="Солнце"),
            Scatter3d(x=[x_elliptic[0]], y=[y_elliptic[0]], z=[z_elliptic[0]], mode="markers", marker=dict(size=object_size, color="red"), name="Объект"),
        ],
        frames=frames_elliptic
    )

    # Настройка осей и анимации
    fig_elliptic.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_range, max_range], title="X (AU)", visible=True),
            yaxis=dict(range=[-max_range, max_range], title="Y (AU)", visible=True),
            zaxis=dict(range=[-max_range, max_range], title="Z (AU)", visible=True),
            aspectmode="cube",
        ),
        title="Эллиптическая орбита",
        updatemenus=[
            {
                "buttons": [
                    {"args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
                     "label": "▶", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                     "label": "⏸", "method": "animate"},
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

    # Сохранение в HTML
    output_filename = "orbit/elliptic_orbit.html"
    fig_elliptic.write_html("../static/" + output_filename, auto_open=False)

    return output_filename