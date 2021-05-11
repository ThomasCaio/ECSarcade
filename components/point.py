from components.render import Renderable


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 1
        self.width = 1

    @property
    def position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y


def check_collision(p1: [Point, Renderable], p2: [Point, Renderable]):
    if isinstance(p1, Point):
        w1, h1 = p1.width, p1.height
        x1, y1 = p1.x, p1.y
    else:
        w1 = p1.width
        h1 = p1.height
        x1, y1 = p1.position[0] - p1.width // 2, p1.position[1] - p1.height // 2
    if isinstance(p2, Point):
        w2, h2 = p2.width, p2.height
        x2, y2 = p2.x, p2.y
    else:
        w2 = p2.width
        h2 = p2.height
        x2, y2 = p2.position[0] - p2.width // 2, p2.position[1] - p2.height // 2
    if x1 < x2 + w2 and\
            x1 + w1 > x2 and\
            y1 < y2 + h2 and\
            y1 + h1 > y2:
        return True
