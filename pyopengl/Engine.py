from math import radians, cos, sin

import numpy as np
import pyopencl as cl
import numpy


class Camera:
    def __init__(self):
        self.camX = 0
        self.camY = 0
        self.pos = [0, 0, 0]
        self.fov = 400

        self.speed = 2

    def get_sin_cos(self):
        return cos(self.camX), cos(self.camY), sin(self.camX), sin(self.camY)

    def go_up(self, dt):
        self.pos[1] -= self.speed * dt

    def go_down(self, dt):
        self.pos[1] += self.speed * dt

    def go_forward(self, dt):
        self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), self.speed * dt, -self.camY + radians(90))

    def go_backward(self, dt):
        self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), -self.speed * dt, -self.camY + radians(90))

    def go_left(self, dt):
        self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), self.speed * dt, -self.camY)

    def go_right(self, dt):
        self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), -self.speed * dt, -self.camY)


class Block:
    def __init__(self, coord, half_block):
        self.x = int(coord[0])
        self.y = int(coord[1])
        self.z = int(coord[2])

        self.half_block = half_block

        self.displayed_polygons = []

        point0 = (coord[0] + half_block, coord[1] + half_block, coord[2] - half_block)
        point1 = (coord[0] + half_block, coord[1] - half_block, coord[2] - half_block)
        point2 = (coord[0] - half_block, coord[1] - half_block, coord[2] - half_block)
        point3 = (coord[0] - half_block, coord[1] + half_block, coord[2] - half_block)
        point4 = (coord[0] + half_block, coord[1] + half_block, coord[2] + half_block)
        point5 = (coord[0] + half_block, coord[1] - half_block, coord[2] + half_block)
        point6 = (coord[0] - half_block, coord[1] - half_block, coord[2] + half_block)
        point7 = (coord[0] - half_block, coord[1] + half_block, coord[2] + half_block)

        self.top_polygon = Polygon(point1, point2, point6, point5)  # top
        self.bottom_polygon = Polygon(point7, point4, point0, point3)  # bottom
        self.left_polygon = Polygon(point7, point6, point2, point3)  # left
        self.right_polygon = Polygon(point1, point5, point4, point0)  # right
        self.back_polygon = Polygon(point7, point6, point5, point4)  # back
        self.front_polygon = Polygon(point1, point2, point3, point0)  # front

    def get_displayed_polygons(self, player_pos):
        self.displayed_polygons = []
        if self.y > player_pos[1]:
            self.displayed_polygons.append(self.top_polygon)
        else:
            self.displayed_polygons.append(self.bottom_polygon)

        if self.x > player_pos[0]:
            self.displayed_polygons.append(self.left_polygon)
        else:
            self.displayed_polygons.append(self.right_polygon)

        if self.z < player_pos[2]:
            self.displayed_polygons.append(self.back_polygon)
        else:
            self.displayed_polygons.append(self.front_polygon)
        return self.displayed_polygons

    def get_points(self):
        return self.top_polygon.points + self.bottom_polygon.points + self.left_polygon.points + self.right_polygon.points + self.front_polygon.points + self.back_polygon.points


class Polygon:
    def __init__(self, point1, point2, point3, point4):
        self.points = [
            Point(point1[0], point1[1], point1[2]),
            Point(point2[0], point2[1], point2[2]),
            Point(point3[0], point3[1], point3[2]),
            Point(point4[0], point4[1], point4[2])
        ]

    def get_points(self):
        return self.points

    def get_points_pos(self):
        return [self.points[0].get_coords(), self.points[1].get_coords(),
                self.points[2].get_coords(), self.points[3].get_coords()]


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.vs_point = None
        self.ps = None

        self.calculated = False

    def get_coords(self):
        return self.x, self.y, self.z

    def reset_ps(self):
        self.ps = None
        self.vs_point = None


class Engine:
    def __init__(self, screen_size):
        self.camera = Camera()

        self.half_screen_x = screen_size[0]/2
        self.half_screen_y = screen_size[1]/2

        self.camera_sensibility = 0.05 * 0.05
        self.RD85 = radians(85)
        self.NRD85 = -self.RD85

        self.points = []
        self.polygons = []
        self.blocks = []

        self.bool_switch = True

    def handle_mouse_movement(self, set_pos_function, mouse_pos_x, mouse_pos_y, dt):
        if mouse_pos_x != self.half_screen_x:
            self.camera.camY -= ((mouse_pos_x - self.half_screen_x) * (self.camera_sensibility / 2))
            set_pos_function(self.half_screen_x, mouse_pos_y)
        if mouse_pos_y != self.half_screen_y:
            move = mouse_pos_y - self.half_screen_y
            if (move > 0 and self.camera.camX <= self.RD85) or (move < 0 and self.camera.camX >= self.NRD85):
                self.camera.camX += (move * self.camera_sensibility)
            set_pos_function(mouse_pos_x, self.half_screen_y)

    def get_ps_vs_point(self):
        cos_x, cos_y, sin_x, sin_y = self.camera.get_sin_cos()

        self.bool_switch = not self.bool_switch

        self.polygons = []
        self.points = []
        pos_x, pos_y, pos_z = self.camera.pos
        for block in self.blocks:
            for polygon in block.get_displayed_polygons(self.camera.pos):
                self.polygons.append(polygon)
                for point in polygon.get_points():
                    if not point.calculated == self.bool_switch:
                        self.points.append(point)
                        p = (point.x - pos_x, point.y - pos_y, point.z - pos_z)
                        p_x, p_y, p_z = p
                        x, y, z = (p_x * cos_y + p_z * sin_y,
                                   p_x * (sin_x * sin_y) + p_y * cos_x - p_z * (sin_x * cos_y),
                                   p_y * sin_x + p_z * (cos_x * cos_y) - p_x * (cos_x * sin_y))
                        transformed_point = (x, y, z)
                        point.vs_point = transformed_point
                        if z > 0:
                            point.ps = [x * self.camera.fov / z + self.half_screen_x, y * self.camera.fov / z + self.half_screen_y]
                        else:
                            point.ps = None
                        point.calculated = self.bool_switch

    def create_block(self, coord, half_block):
        self.blocks.append(Block(coord, half_block))

    def optimise_points(self):
        all_points = []
        all_optimized_point = []
        for block in self.blocks:
            for polygon in [block.top_polygon, block.bottom_polygon, block.left_polygon, block.right_polygon, block.front_polygon, block.back_polygon]:
                for point in polygon.points:
                    if point.get_coords() not in all_points:
                        all_points.append(point.get_coords())
        for point in all_points:
            all_optimized_point.append(Point(point[0], point[1], point[2]))

        for block in self.blocks:
            for polygon in [block.top_polygon, block.bottom_polygon, block.left_polygon, block.right_polygon, block.front_polygon, block.back_polygon]:
                for point in all_optimized_point:
                    for pt in range(len(polygon.points)):
                        if polygon.points[pt].get_coords() == point.get_coords():
                            polygon.points[pt] = point



def clip3d(p1, p2, zcd, fov, screen_x, screen_y):
    step = ((zcd - p1[2]) / (p2[2] - p1[2]))
    return ((p1[0] + (p2[0] - p1[0]) * step) * fov / zcd + screen_x / 2,
            (p1[1] + (p2[1] - p1[1]) * step) * fov / zcd + screen_y / 2)


def calculate_new_xy(old_xy, speed, angle_in_radians):
    new_x = old_xy[0] + -(speed * cos(angle_in_radians))
    new_y = old_xy[1] + (speed * sin(angle_in_radians))
    return new_x, new_y
