
from math import factorial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

control_points = []
num_points_target = 0
fig = None
ax = None
cid = None

def on_click(event):
    """handle mouse click events to add points"""
    global control_points, num_points_target, fig, ax
    
    if event.inaxes != ax or num_points_target == 0:
        return
    
    if len(control_points) < num_points_target:
        # add point to list
        control_points.append((event.xdata, event.ydata))
        
        # plot point
        ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
        
        # Add label
        label = f'P{len(control_points)-1}'
        ax.text(event.xdata, event.ydata + 0.5, label, fontsize=10, ha='center')
        
        # lines between points
        if len(control_points) > 1:
            prev_point = control_points[-2]
            ax.plot([prev_point[0], event.xdata], [prev_point[1], event.ydata], 
                   'r--', linewidth=1, alpha=0.5)
        
        fig.canvas.draw()
        
        if len(control_points) == num_points_target:
            generate_and_animate_curve()

def generate_and_animate_curve():
    """Generate the Bezier curve and display the animation"""
    global control_points, fig, ax, cid
    
    # Disconnect the click event
    fig.canvas.mpl_disconnect(cid)
    
    def bezier_curve(t, control_points):
        n = len(control_points) - 1
        x = 0
        y = 0
        for i in range(n + 1):
            binomial_coeff = factorial(n) / (factorial(i) * factorial(n - i))
            bernstein_poly = binomial_coeff * (t ** i) * ((1 - t) ** (n - i))
            x += bernstein_poly * control_points[i][0]
            y += bernstein_poly * control_points[i][1]
        return (x, y)
    
    # generate curve points
    num_samples = 300
    bezier_points = []
    for i in range(num_samples + 1):
        t = i / num_samples
        bezier_points.append(bezier_curve(t, control_points))
    
    bezier_x = [point[0] for point in bezier_points]
    bezier_y = [point[1] for point in bezier_points]
    
    ax.set_title('Bezier Curves', fontsize=14)
    
    # Line object for animation
    line, = ax.plot([], [], 'b-', linewidth=2, label='Bezier Curve')
    
    def animate(frame):
        line.set_data(bezier_x[:frame], bezier_y[:frame])
        return line,
    
    num_frames = len(bezier_points)
    interval = 1000 / num_frames
    ani = FuncAnimation(fig, animate, frames=num_frames, interval=interval, blit=True, repeat=True)
    fig.canvas.draw()

num_points_target = int(input("Enter the number of control points: "))

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_title(f'Click to add {num_points_target} control points', fontsize=14)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')
ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)

# run function on click
cid = fig.canvas.mpl_connect('button_press_event', on_click)

plt.tight_layout()
plt.show()
