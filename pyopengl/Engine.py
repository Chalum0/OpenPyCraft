from math import cos, sin

class Camera:
    def __init__(self):
        self.camX = 0
        self.camY = 0
        self.pos = [0, 0, 0]
        self.fov = 400


def calculate_new_xy(old_xy, speed, angle_in_radians):
    new_x = old_xy[0] + -(speed * cos(angle_in_radians))
    new_y = old_xy[1] + (speed * sin(angle_in_radians))
    return new_x, new_y
