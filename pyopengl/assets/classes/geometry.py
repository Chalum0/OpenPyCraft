from math import dist


class Block:
    def __init__(self, coord, half_block, display, points):
        self.x = int(coord[0])
        self.y = int(coord[1])
        self.z = int(coord[2])

        self.display = display

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

        self.top_polygon = Polygon(point1, point2, point6, point5, points, "top")  # top
        self.bottom_polygon = Polygon(point7, point4, point0, point3, points, "bottom")  # bottom
        self.left_polygon = Polygon(point7, point6, point2, point3, points, "left")  # left
        self.right_polygon = Polygon(point1, point5, point4, point0, points, "right")  # right
        self.back_polygon = Polygon(point7, point6, point5, point4, points, "back")  # back
        self.front_polygon = Polygon(point1, point2, point3, point0, points, "front")  # front

    def get_displayed_polygons(self, player_pos):
        self.displayed_polygons = []
        if self.y > player_pos[1]:
            if self.display["top"]:
                self.displayed_polygons.append(self.top_polygon)
        else:
            if self.display["bottom"]:
                self.displayed_polygons.append(self.bottom_polygon)


        if self.display["left"]:
            self.displayed_polygons.append(self.left_polygon)
        if self.display["right"]:
            self.displayed_polygons.append(self.right_polygon)
        if self.display["back"]:
            self.displayed_polygons.append(self.back_polygon)
        if self.display["front"]:
            self.displayed_polygons.append(self.front_polygon)

        return self.displayed_polygons

    def get_points(self):
        return self.top_polygon.points + self.bottom_polygon.points + self.left_polygon.points + self.right_polygon.points + self.front_polygon.points + self.back_polygon.points


class Polygon:
    def __init__(self, point1, point2, point3, point4, points, name):

        self.points = []
        self.name = name

        point_pos = f"({point1[0]}, {point1[1]}, {point1[2]}"
        if point_pos not in points:
            point = Point(point1[0], point1[1], point1[2])
            points[point_pos] = point
            self.points.append(point)

        else:
            self.points.append(points[point_pos])

        point_pos = f"({point2[0]}, {point2[1]}, {point2[2]}"
        if point_pos not in points:
            point = Point(point2[0], point2[1], point2[2])
            points[point_pos] = point
            self.points.append(point)

        else:
            self.points.append(points[point_pos])

        point_pos = f"({point3[0]}, {point3[1]}, {point3[2]}"
        if point_pos not in points:
            point = Point(point3[0], point3[1], point3[2])
            points[point_pos] = point
            self.points.append(point)

        else:
            self.points.append(points[point_pos])

        point_pos = f"({point4[0]}, {point4[1]}, {point4[2]}"
        if point_pos not in points:
            point = Point(point4[0], point4[1], point4[2])
            points[point_pos] = point
            self.points.append(point)

        else:
            self.points.append(points[point_pos])

        sum_x = sum(point.x for point in self.points)
        sum_y = sum(point.y for point in self.points)
        sum_z = sum(point.z for point in self.points)
        self.center = (sum_x / len(self.points), sum_y / len(self.points), sum_z / len(self.points))

    def get_points(self):
        return self.points

    def get_points_pos(self):
        return [self.points[0].get_coords(), self.points[1].get_coords(),
                self.points[2].get_coords(), self.points[3].get_coords()]

    def get_distance(self, position, render_dist):
        return dist(position, self.center)


class UnoptimisedPolygon:
    def __init__(self, point1, point2, point3, point4, name):
        self.points = []
        self.name = name

        point = UnFixedPoint(point1[0], point1[1], point1[2])
        self.points.append(point)

        point = UnFixedPoint(point2[0], point2[1], point2[2])
        self.points.append(point)

        point = UnFixedPoint(point3[0], point3[1], point3[2])
        self.points.append(point)

        point = UnFixedPoint(point4[0], point4[1], point4[2])
        self.points.append(point)

        sum_x = sum(point.x for point in self.points)
        sum_y = sum(point.y for point in self.points)
        sum_z = sum(point.z for point in self.points)
        self.center = (sum_x / len(self.points), sum_y / len(self.points), sum_z / len(self.points))

    def get_points(self):
        return self.points

    def get_points_pos(self):
        return [self.points[0].get_coords(), self.points[1].get_coords(),
                self.points[2].get_coords(), self.points[3].get_coords()]

    def get_distance(self, position, render_dist):
        return dist(position, self.center)

    def set_pos(self, point1, point2, point3, point4):
        self.points[0].set_pos((point1[0], point1[1], point1[2]))
        self.points[1].set_pos((point2[0], point2[1], point2[2]))
        self.points[2].set_pos((point3[0], point3[1], point3[2]))
        self.points[3].set_pos((point4[0], point4[1], point4[2]))

        sum_x = sum(point.x for point in self.points)
        sum_y = sum(point.y for point in self.points)
        sum_z = sum(point.z for point in self.points)
        self.center = (sum_x / len(self.points), sum_y / len(self.points), sum_z / len(self.points))


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


class UnFixedPoint:
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

    def set_pos(self, pos):
        self.x, self.y, self.z = pos


class Entity:
    def __init__(self, pos, half_block, type):

        self.type = type
        self.half_block = half_block
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.z = int(pos[2])

        self.half_block = half_block

        self.displayed_polygons = []

        point0 = (pos[0] + half_block, pos[1] + half_block, pos[2] - half_block)
        point1 = (pos[0] + half_block, pos[1] - half_block, pos[2] - half_block)
        point2 = (pos[0] - half_block, pos[1] - half_block, pos[2] - half_block)
        point3 = (pos[0] - half_block, pos[1] + half_block, pos[2] - half_block)
        point4 = (pos[0] + half_block, pos[1] + half_block, pos[2] + half_block)
        point5 = (pos[0] + half_block, pos[1] - half_block, pos[2] + half_block)
        point6 = (pos[0] - half_block, pos[1] - half_block, pos[2] + half_block)
        point7 = (pos[0] - half_block, pos[1] + half_block, pos[2] + half_block)

        self.top_polygon = UnoptimisedPolygon(point1, point2, point6, point5, "top")  # top
        self.bottom_polygon = UnoptimisedPolygon(point7, point4, point0, point3, "bottom")  # bottom
        self.left_polygon = UnoptimisedPolygon(point7, point6, point2, point3, "left")  # left
        self.right_polygon = UnoptimisedPolygon(point1, point5, point4, point0, "right")  # right
        self.back_polygon = UnoptimisedPolygon(point7, point6, point5, point4, "back")  # back
        self.front_polygon = UnoptimisedPolygon(point1, point2, point3, point0, "front")  # front

    def set_pos(self, pos):
        point0 = (pos[0] + self.half_block, pos[1] + self.half_block, pos[2] - self.half_block)
        point1 = (pos[0] + self.half_block, pos[1] - self.half_block, pos[2] - self.half_block)
        point2 = (pos[0] - self.half_block, pos[1] - self.half_block, pos[2] - self.half_block)
        point3 = (pos[0] - self.half_block, pos[1] + self.half_block, pos[2] - self.half_block)
        point4 = (pos[0] + self.half_block, pos[1] + self.half_block, pos[2] + self.half_block)
        point5 = (pos[0] + self.half_block, pos[1] - self.half_block, pos[2] + self.half_block)
        point6 = (pos[0] - self.half_block, pos[1] - self.half_block, pos[2] + self.half_block)
        point7 = (pos[0] - self.half_block, pos[1] + self.half_block, pos[2] + self.half_block)

        self.top_polygon.set_pos(point1, point2, point6, point5)  # top
        self.bottom_polygon.set_pos(point7, point4, point0, point3)  # bottom
        self.left_polygon.set_pos(point7, point6, point2, point3)  # left
        self.right_polygon.set_pos(point1, point5, point4, point0)  # right
        self.back_polygon.set_pos(point7, point6, point5, point4)  # back
        self.front_polygon.set_pos(point1, point2, point3, point0)  # front

    def get_displayed_polygons(self, p):
        self.displayed_polygons = []
        self.displayed_polygons.append(self.top_polygon)
        self.displayed_polygons.append(self.bottom_polygon)
        self.displayed_polygons.append(self.left_polygon)
        self.displayed_polygons.append(self.right_polygon)
        self.displayed_polygons.append(self.back_polygon)
        self.displayed_polygons.append(self.front_polygon)

        return self.displayed_polygons

    def get_points(self):
        return self.top_polygon.points + self.bottom_polygon.points + self.left_polygon.points + self.right_polygon.points + self.front_polygon.points + self.back_polygon.points
