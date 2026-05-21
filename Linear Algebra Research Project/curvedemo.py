
from math import factorial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox

control_points = []
num_points_target = 2
fig = None
ax = None
cid = None
ani = None
status_text = None
num_points_box = None
restart_button = None


def update_status():
    """Update the plot title and status text."""
    remaining = max(0, num_points_target - len(control_points))
    ax.set_title(f'Click to add {num_points_target} control points ({remaining} left)', fontsize=14)
    status_text.set_text(f'Points: {len(control_points)}/{num_points_target}')
    fig.canvas.draw_idle()


def reset_plot():
    """Clear the plot and reset click state."""
    global control_points, cid
    control_points = []
    ax.clear()
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(-5, 15)
    ax.set_ylim(-5, 15)
    ax.plot([], [])
    ax.text(0.02, 0.95, 'Click on the plot to add control points.', transform=ax.transAxes,
            fontsize=10, va='top')
    update_status()
    if cid is not None:
        fig.canvas.mpl_disconnect(cid)
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.draw_idle()


def on_click(event):
    """Handle mouse click events to add control points."""
    global control_points
    if event.inaxes != ax or num_points_target == 0:
        return

    if len(control_points) < num_points_target:
        control_points.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
        label = f'P{len(control_points) - 1}'
        ax.text(event.xdata, event.ydata + 0.5, label, fontsize=10, ha='center')
        if len(control_points) > 1:
            prev_point = control_points[-2]
            ax.plot([prev_point[0], event.xdata], [prev_point[1], event.ydata],
                    'r--', linewidth=1, alpha=0.5)
        update_status()
        if len(control_points) == num_points_target:
            generate_and_animate_curve()


def generate_and_animate_curve():
    """Generate the Bezier curve and animate it."""
    global cid, ani
    if cid is not None:
        fig.canvas.mpl_disconnect(cid)
        cid = None

    def bezier_curve(t, points):
        n = len(points) - 1
        x = 0
        y = 0
        for i in range(n + 1):
            binomial_coeff = factorial(n) / (factorial(i) * factorial(n - i))
            bernstein_poly = binomial_coeff * (t ** i) * ((1 - t) ** (n - i))
            x += bernstein_poly * points[i][0]
            y += bernstein_poly * points[i][1]
        return x, y

    num_samples = 200
    bezier_points = [bezier_curve(i / num_samples, control_points) for i in range(num_samples + 1)]
    bezier_x = [p[0] for p in bezier_points]
    bezier_y = [p[1] for p in bezier_points]

    line, = ax.plot([], [], 'b-', linewidth=2, label='Bezier Curve')
    ax.legend(loc='upper right')
    update_status()

    def animate(frame):
        line.set_data(bezier_x[:frame + 1], bezier_y[:frame + 1])
        return line,

    num_frames = len(bezier_points)
    interval = 300 / num_frames
    ani = FuncAnimation(fig, animate, frames=num_frames, interval=interval, blit=False, repeat=False)
    fig.canvas.draw_idle()


def submit_num_points(text):
    """Handle text box submission for number of points."""
    global num_points_target, control_points
    try:
        value = int(text)
        if value < 2:
            raise ValueError
    except ValueError:
        num_points_box.set_val(str(num_points_target))
        return
    num_points_target = value
    reset_plot()


def on_restart(event):
    """Restart point selection and clear the plot."""
    reset_plot()


fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.18)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')
ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)
ax.text(0.02, 0.95, 'Click on the plot to add control points.', transform=ax.transAxes, fontsize=10, va='top')

status_text = fig.text(0.02, 0.90, '', transform=fig.transFigure, fontsize=10, va='top')
num_points_box_ax = fig.add_axes([0.05, 0.05, 0.18, 0.05])
num_points_box = TextBox(num_points_box_ax, 'Points', initial=str(num_points_target))
num_points_box.on_submit(submit_num_points)
restart_button_ax = fig.add_axes([0.28, 0.05, 0.12, 0.05])
restart_button = Button(restart_button_ax, 'Restart')
restart_button.on_clicked(on_restart)

update_status()
cid = fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
 