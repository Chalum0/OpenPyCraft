from math import radians, cos, sin, dist
import numpy as np
import pyopencl as cl
import time
import threading

from assets.classes.geometry import *


class Player:
    def __init__(self):
        self.pos = [0, -11, 0]
        self.light_color = (255, 150, 255)
        self.light_distance = 4
        self.entity = None

    def set_entity_pos(self):
        self.entity.set_pos(self.pos)


class Camera:
    def __init__(self, fixed):
        self.fixed = fixed

        if self.fixed:
            self.camX = 1.01
            self.camY = 51.34
            self.pos = [64, -90, -22]
            self.fov = 1000
        else:
            self.camX = 0
            self.camY = 0
            self.pos = [0, 0, 0]
            self.fov = 1000

        self.player = Player()

        self.speed = 2

    def get_sin_cos(self):
        return cos(self.camX), cos(self.camY), sin(self.camX), sin(self.camY)

    def go_up(self, dt):
        if not self.fixed:
            self.pos[1] -= self.speed * dt

    def go_down(self, dt):
        if not self.fixed:
            self.pos[1] += self.speed * dt

    def go_forward(self, dt):
        if self.fixed:
            self.pos[2] += self.speed * dt
            self.player.pos[2] += self.speed * dt
            self._move_player_entity()
        else:
            self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), self.speed * dt, -self.camY + radians(90))

    def go_backward(self, dt):
        if self.fixed:
            self.pos[2] -= self.speed * dt
            self.player.pos[2] -= self.speed * dt
            self._move_player_entity()
        else:
            self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), -self.speed * dt, -self.camY + radians(90))

    def go_left(self, dt):
        if self.fixed:
            self.pos[0] -= self.speed * dt
            self.player.pos[0] -= self.speed * dt
            self._move_player_entity()
        else:
            self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), self.speed * dt, -self.camY)

    def go_right(self, dt):
        if self.fixed:
            self.pos[0] += self.speed * dt
            self.player.pos[0] += self.speed * dt
            self._move_player_entity()
        else:
            self.pos[0], self.pos[2] = calculate_new_xy((self.pos[0], self.pos[2]), -self.speed * dt, -self.camY)

    def _move_player_entity(self):
        self.player.set_entity_pos()


class Engine:
    def __init__(self, screen_size, map_matrix, block_size=10, render_dist=10, fixed_camera=False):
        self.camera = Camera(fixed_camera)

        self.half_screen_x = screen_size[0]/2
        self.half_screen_y = screen_size[1]/2

        self.camera_sensibility = 0.05 * 0.05
        self.RD85 = radians(85)
        self.NRD85 = -self.RD85

        # self.points = []
        self.polygons = []
        self.entity_polygons = []
        self.blocks = []
        self.entities = []
        self.entity_ids = {}
        self.camera.player.entity = Entity(self.camera.player.pos, 5, "player")
        # self.entities.append(self.camera.player.entity)

        self.bool_switch = True
        self.map = map_matrix
        self.block_size = block_size
        self.transparent_block_ids = [0]
        self.render_distance = render_dist * block_size
        self.create_map()

        self.done = False

    def create_map(self):
        points = {}
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                for z in range(len(self.map[y][x])):
                    if self.map[y][x][z] not in self.transparent_block_ids:
                        display = {"front": False, "back": False, "left": False, "right": False, "top": False, "bottom": False}
                        if y == 0:
                            display["bottom"] = True
                        if y == len(self.map)-1:
                            display["top"] = True
                        if not y == 0 and not y == len(self.map)-1:
                            if self.map[y+1][x][z] in self.transparent_block_ids:
                                display["top"] = True

                            if self.map[y-1][x][z] in self.transparent_block_ids:
                                display["bottom"] = True

                        if x == 0:
                            display["left"] = True
                        if x == len(self.map[y])-1:
                            display["right"] = True
                        if not x == 0 and not x == len(self.map[y])-1:
                            if self.map[y][x+1][z] in self.transparent_block_ids:
                                display["right"] = True
                            if self.map[y][x-1][z] in self.transparent_block_ids:
                                display["left"] = True

                        if z == 0:
                            display["front"] = True
                        if z == len(self.map[y][x])-1:
                            display["back"] = True
                        if not z == 0 and not z == len(self.map[y][x])-1:
                            if self.map[y][x][z+1] in self.transparent_block_ids:
                                display["back"] = True
                            if self.map[y][x][z-1] in self.transparent_block_ids:
                                display["front"] = True

                        self.create_block((x*self.block_size, y*-self.block_size, z*self.block_size), self.block_size/2, display, points)
        print("done")

    def handle_mouse_movement(self, set_pos_function, mouse_pos_x, mouse_pos_y, dt):
        if not self.camera.fixed:
            if mouse_pos_x != self.half_screen_x:
                self.camera.camY -= ((mouse_pos_x - self.half_screen_x) * (self.camera_sensibility / 2)) * 0.1 * 20
                set_pos_function(self.half_screen_x, mouse_pos_y)
            if mouse_pos_y != self.half_screen_y:
                move = mouse_pos_y - self.half_screen_y
                if (move > 0 and self.camera.camX <= self.RD85) or (move < 0 and self.camera.camX >= self.NRD85):
                    self.camera.camX += (move * self.camera_sensibility) * 0.1 * 20
                set_pos_function(mouse_pos_x, self.half_screen_y)

    def get_entity_polygons(self):
        self.entity_polygons = []

        for entity in self.entities:
            for polygon in entity.get_displayed_polygons(self.camera.pos):
                if self.camera.fixed:
                    if not (self.camera.pos[0] - 21 * self.block_size < polygon.center[0] < self.camera.pos[
                        0] + 4 * self.block_size and self.camera.pos[2] - 7 * self.block_size < polygon.center[2] <
                            self.camera.pos[2] + 21 * self.block_size) or polygon.name == "bottom" or dist(
                            self.camera.player.pos, polygon.center) > self.render_distance:
                        continue
                else:
                    if polygon.get_distance(self.camera.pos, self.render_distance) >= self.render_distance * 10:
                        continue
                self.entity_polygons.append(polygon)

    def get_polygons(self):
        thread = threading.Thread(target=self._get_polygons)
        thread.start()

    def _get_polygons(self):
        self.polygons = []
        self.points = []

        for block in self.blocks:
            for polygon in block.get_displayed_polygons(self.camera.pos):
                if self.camera.fixed:
                    if not (self.camera.pos[0] - 21 * self.block_size < polygon.center[0] < self.camera.pos[0] + 4 * self.block_size and self.camera.pos[2] - 7 * self.block_size < polygon.center[2] < self.camera.pos[2] + 21 * self.block_size) or polygon.name == "bottom" or dist(self.camera.player.pos, polygon.center) > self.render_distance:
                        continue
                else:
                    if polygon.get_distance(self.camera.pos, self.render_distance) >= self.render_distance*10:
                        continue
                self.polygons.append(polygon)

        # self.polygons = sorted(self.polygons, key=self.distance_to_camera)
        # self.polygons.reverse()

    def get_ps_vs_point(self):
        if not self.camera.fixed:
            print(self.camera.pos, self.camera.camX, self.camera.camY)
        self.get_polygons()
        thread = threading.Thread(target=self._get_ps_vs_point)
        thread.start()

    def _get_ps_vs_point(self):
        cos_x, cos_y, sin_x, sin_y = self.camera.get_sin_cos()

        self.bool_switch = not self.bool_switch
        pos_x, pos_y, pos_z = self.camera.pos

        for polygon in self.polygons + self.entity_polygons:
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

    def distance_to_camera(self, polygon):
        return dist(self.camera.pos, polygon.center)

    def create_block(self, coord, half_block, display, points):
        self.blocks.append(Block(coord, half_block, display, points))

    def display_polygons(self, renderer, image):
        self.get_entity_polygons()
        self.get_ps_vs_point()

        polygons = []
        filters = []

        # print(self.entity_polygons)

        self.get_entity_polygons()
        all_polygons = self.polygons + self.entity_polygons
        all_polygons = sorted(all_polygons, key=self.distance_to_camera)
        all_polygons.reverse()

        if len(self.points) >= 2:
            for k in all_polygons:
                i = k.get_points()
                not_false_point = []
                len_points = 0
                points = []
                pts = []
                for y in range(len(i)):
                    point = i[y]
                    ps_point = point.ps
                    points.append(ps_point)
                    len_points += 1
                    pts.append(point.vs_point)
                    if ps_point is not None:
                        not_false_point.append(ps_point)
                if len(not_false_point) >= 1:
                    if None in points:
                        pass
                    else:
                        r, g, b = self.camera.player.light_color
                        distance = self.camera.player.light_distance
                        filters.append((r / (dist(k.center, self.camera.player.pos) / self.block_size) * distance,
                                        g / (dist(k.center, self.camera.player.pos) / self.block_size) * distance,
                                        b / (dist(k.center, self.camera.player.pos) / self.block_size) * distance))
                        polygons.append([points[0], points[1], points[2], points[3]])
        renderer.draw_polygons(image, polygons, filters)

    def kill_all_entities(self):
        for entity in self.entities:
            if entity.type != 'player':
                self.entities.remove(entity)

    def get_entities(self):
        entities = [self.camera.player.entity]
        for entity in self.entity_ids.values():
            entities.append(entity)
        self.entities = entities



def clip3d(p1, p2, zcd, fov, screen_x, screen_y):
    step = ((zcd - p1[2]) / (p2[2] - p1[2]))
    return ((p1[0] + (p2[0] - p1[0]) * step) * fov / zcd + screen_x / 2,
            (p1[1] + (p2[1] - p1[1]) * step) * fov / zcd + screen_y / 2)


def calculate_new_xy(old_xy, speed, angle_in_radians):
    new_x = old_xy[0] + -(speed * cos(angle_in_radians))
    new_y = old_xy[1] + (speed * sin(angle_in_radians))
    return new_x, new_y
