import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg

# Estimates
g = -9.81
friction = 0.03
aerodrag = 0.5

# Input
mass = 79  # kg
height_inrun = 150
height_ramp = 100
length_ramp = 15
deg_inrun = 35
deg_slope = 32

# Calculations
distance_max = height_inrun * 2
angle_inrun = deg_inrun / 180 * math.pi
angle_slope = deg_slope / 180 * math.pi
distance_ramp = (height_inrun - height_ramp) / math.tan(angle_inrun)
length_slope = height_ramp / math.tan(angle_slope)
distance_slope = distance_ramp + length_ramp + length_slope
tan_inrun = math.tan(angle_inrun)
tan_slope = math.tan(angle_slope)
cos_inrun = math.cos(angle_inrun)
cos_slope = math.cos(angle_slope)
sin_inrun = math.sin(angle_inrun)
sin_slope = math.sin(angle_slope)

# Plotting
fig, ax = plt.subplots()
ax.set_xlim(0, distance_max)
ax.set_ylim(0, distance_max)
trajectory_x = []
trajectory_y = []
trajectory_line, = ax.plot([], [], '-', alpha=1)

img = mpimg.imread("image.png")
image = ax.imshow(img, extent=(0, 0, 0, 0), zorder=2)

def init():
    trajectory_line.set_data([], [])
    return trajectory_line, image

def draw_track():
    axis_x = np.array([0, distance_max])
    axis_y = np.array([0, distance_max])
    ax.plot(axis_x, axis_y, '.', zorder=1)

    track_x = []
    track_y = []

    track_x.append(0.0)
    track_y.append(height_inrun)
    track_x.append(distance_ramp)
    track_y.append(height_ramp)

    track_x.append(distance_ramp + length_ramp)
    track_y.append(height_ramp)

    track_x.append(distance_slope)
    track_y.append(0)

    ax.plot(track_x, track_y, '.-', zorder=1)

def ski_a_bit(posx, posy, vx, vy, timebit):
    # default
    gy = mass * g
    gx = 0

    # on the in-run
    if posx < distance_ramp:
        gx = mass * -g * sin_inrun * cos_inrun * (1 - friction)
        gy = mass * g * (1 - cos_inrun * cos_inrun) * (1 - friction)
    # on the ramp
    elif posx < distance_ramp + length_ramp:
        gx = 0
        gy = 0
        if vy != 0:
            vx = (vx ** 2 + vy ** 2) ** 0.5
            print('Speed at ramp: %.2fm/s' % vx)
        vy = 0
    # flying and landing
    elif posx < distance_slope:
        slope_height_posx = (distance_slope - posx) * tan_slope
        # flying
        if posy >= slope_height_posx - 3.0:
            gx = mass * g * aerodrag
            gy = mass * g * (1 - aerodrag)
        # landing
        else:
            # posy = slope_height_posx + 1.0
            gx = mass * -g * sin_slope * cos_slope * (1 - friction)
            gy = mass * g * (1 - cos_slope * cos_slope) * (1 - friction)
            angle_landing = math.atan(-vy / vx) - angle_slope
            jumped = ((posx - (distance_ramp + length_ramp)) ** 2 + (posy - height_ramp) ** 2) ** 0.5
            v_new = (vx ** 2 + vy ** 2) ** 0.5 * math.cos(angle_landing)
            vx = v_new * cos_slope
            vy = -v_new * sin_slope
            # filter false landing
            if angle_landing > 0.15:
                print('landing at angle %.2f, speed at %.2fm/s, jumped %.2fm' % (angle_landing, v_new, jumped))
    # on flat surface
    else:
        gx = 0

    if posy < 0:
        gy = 0
        vx = (vx ** 2 + vy ** 2) ** 0.5
        vy = 0

    # calculate new position for x and y
    vx += gx * timebit * 0.5
    posx += vx * timebit + 0.5 * gx * timebit ** 2
    vx += gx * timebit * 0.5

    vy += gy * timebit * 0.5
    posy += vy * timebit + 0.5 * gy * timebit ** 2
    vy += gy * timebit * 0.5

    return posx, posy, vx, vy

def animate(frame):
    global me_x, me_y, speed_x, speed_y

    if me_x < distance_max:
        (me_x, me_y, speed_x, speed_y) = ski_a_bit(me_x, me_y, speed_x, speed_y, timebit)
        trajectory_x.append(me_x)  # Add current position to trajectory
        trajectory_y.append(me_y)
        trajectory_line.set_data(trajectory_x, trajectory_y)
        # ax.clear()
        image.set_extent((me_x - 10, me_x + 10, me_y - 10, me_y + 10))
        draw_track()

    return trajectory_line, image

def ski():
    global me_x, me_y, speed_x, speed_y, timebit

    me_x = 0
    me_y = height_inrun
    speed_x = 0
    speed_y = 0
    timebit = 0.02

    draw_track()
    ani = FuncAnimation(fig, animate, frames=1001, interval=20, init_func=init)
    ax.set_aspect('auto')
    plt.show()

ski()
