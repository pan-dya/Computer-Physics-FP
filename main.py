import matplotlib.pyplot as pl
import numpy as np
import math
import time

g = -9.81
mass = 75 # kg

# Estimates
friction = 0.03
aerodrag = 0.5

height_inrun = 150
height_ramp = 100
length_ramp = 15
distance_max = height_inrun * 2

angle_inrun = 35/180 * math.pi
angle_slope = 32/180 * math.pi

distance_ramp = (height_inrun - height_ramp) / math.tan(angle_inrun)
length_slope = height_ramp / math.tan(angle_slope)
distance_slope = distance_ramp + length_ramp + length_slope
tan_inrun = math.tan(angle_inrun)
tan_slope = math.tan(angle_slope)
cos_inrun = math.cos(angle_inrun)
cos_slope = math.cos(angle_slope)
sin_inrun = math.sin(angle_inrun)
sin_slope = math.sin(angle_slope)

def draw_track ():
    axis_x = np.array([0, distance_max])
    axis_y = np.array([0, distance_max])
    pl.plot(axis_x, axis_y, '.')

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

    pl.plot(track_x,track_y,'.-')
    pl.show()

def ski_a_bit(posx, posy, vx, vy, timebit):

    gy = mass * g
    gx = 0

    if posx < distance_ramp:
        gx = -g * sin_inrun * cos_inrun * (1-friction)
        gy = g * (1-cos_inrun*cos_inrun) * (1 - friction)
    elif posx < distance_ramp + length_ramp:
        gx = 0
        gy = 0
        if vy != 0:
            vx = (vx**2 + vy**2)**0.5
            print ('Speed at ramp: %.2fm/s' % vx)  
        vy = 0
    elif posx < distance_slope:
        slope_height_posx = (distance_slope - posx) * tan_slope
        if posy >= slope_height_posx - 1.0:
            gx = g * aerodrag
            gy = g * (1- aerodrag)
        else:
            posy = slope_height_posx + 1
            gx = mass * -g * sin_slope * cos_slope * (1-friction)
            gy = mass * g * (1-cos_slope * cos_slope) * (1-friction)
            angle_landing = math.atan(-vy/vx) - angle_slope
            jumped = ((posx - (distance_ramp + length_ramp))**2 + (posy - height_ramp)**2)**0.5
            v_new = (vx**2 + vy**2)**0.5 * math.cos(angle_landing)
            vx = v_new * cos_slope
            vy = -v_new * sin_slope
            if angle_landing > 0.15:
                print('landing at angle %.2f, speed at %.2fm/s, jumped %.2fm' % (angle_landing, v_new, jumped))
    else:
        gx = 0

    if posy < 0:
        gy = 0
        vx = (vx**2 + vy**2)**0.5
        vy = 0

    vx += gx * timebit * 0.5
    posx += vx * timebit + 0.5 * gx * timebit ** 2
    vx += gx * timebit * 0.5
    
    vy += gy * timebit * 0.5
    posy += vy * timebit + 0.5 * gy * timebit ** 2
    vy += gy * timebit * 0.5

    return posx, posy, vx, vy

def ski():
    me_x = 0
    me_y = height_inrun
    speed_x = 0
    speed_y = 0
    timebit = 0.02
    counter = 0

    while me_x < distance_max:
        (me_x, me_y, speed_x, speed_y) = ski_a_bit(me_x, me_y, speed_x, speed_y, timebit)
        counter += 1
        if counter % 10 == 0:
            draw_track()
            pl.plot([me_x],[me_y], 'o')
            pl.show()

ski()