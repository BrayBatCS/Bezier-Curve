
from math import factorial, sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

start_point = (0, 0)

end_x = float(input("Enter ending point X coordinate: "))
end_y = float(input("Enter ending point Y coordinate: "))
end_point = (end_x, end_y)

num_points = int(input("Enter the number of control points: "))

random.seed()
control_points = []

control_points.append(start_point)

# Generate intermediate control points distributed naturally
if num_points > 2:
    # Calculate distance and direction from start to end
    dx = end_x - start_point[0]
    dy = end_y - start_point[1]
    distance = sqrt(dx**2 + dy**2)
    
    # Perpendicular vector (for natural offset)
    if distance > 0:
        perp_x = -dy / distance
        perp_y = dx / distance
    else:
        perp_x, perp_y = 1, 0
    
    # Max offset is proportional to distance
    max_offset = distance * 0.3
    
    for i in range(num_points - 2):
        # Position along the line from start to end
        t = (i + 1) / (num_points - 1)
        base_x = start_point[0] + t * dx
        base_y = start_point[1] + t * dy
        
        # Add natural perpendicular offset (bell curve distribution)
        offset_magnitude = random.uniform(-max_offset, max_offset) * (1 - (t - 0.5)**2 * 4)
        
        x = base_x + perp_x * offset_magnitude
        y = base_y + perp_y * offset_magnitude
        control_points.append((x, y))

# Last control point is the end point
control_points.append(end_point)

print(f"\nGenerated {num_points} control points:")
print(f"  Start point: ({start_point[0]:.2f}, {start_point[1]:.2f})")
for i, point in enumerate(control_points[1:-1], 1):
    print(f"  Middle point {i}: ({point[0]:.2f}, {point[1]:.2f})")
print(f"  End point: ({end_point[0]:.2f}, {end_point[1]:.2f})")

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

num_samples = 300  # Number of points on the curve
bezier_points = []

for i in range(num_samples + 1):
    t = i / num_samples
    bezier_points.append(bezier_curve(t, control_points))

# Extract all coordinates
bezier_x = [point[0] for point in bezier_points]
bezier_y = [point[1] for point in bezier_points]
control_x = [point[0] for point in control_points]
control_y = [point[1] for point in control_points]

# Create figure and axis for animation
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_title('Animated Bezier Curve Drawing', fontsize=14)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

# Set axis limits with some padding
all_x = control_x + bezier_x
all_y = control_y + bezier_y
margin = 1
ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

# Plot control points (static)
ax.plot(control_x, control_y, 'ro-', linewidth=1.5, markersize=8, label='Control Points')
ax.scatter(control_x, control_y, color='black', s=100, zorder=5)

# Add labels to control points
for i, (x, y) in enumerate(control_points):
    label = f'P{i}'
    ax.text(x, y+0.1, f'{label}', color='black')

# Line object for animation
line, = ax.plot([], [], 'b-', linewidth=2, label='Bezier Curve')
ax.legend(fontsize=10, loc='upper right')

def animate(frame):
    # Draw the curve up to the current frame
    line.set_data(bezier_x[:frame], bezier_y[:frame])
    return line,

num_frames = len(bezier_points)
interval = 1000 / num_frames  # Total animation time ~1 second
ani = FuncAnimation(fig, animate, frames=num_frames, interval=interval, blit=True, repeat=True)

plt.tight_layout()
plt.show()
