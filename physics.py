import pyglet
import math


def momentumupdater(momentum):
    x = 0
    y = 0
    for force in momentum.origin.forcelist:
        x += force.magnitude * math.sin(force.direction)
        y += force.magnitude * math.cos(force.direction)
    momentum.direction = math.atan2(x, y)
    momentum.magnitude = math.sqrt(math.pow(x, 2) + math.pow(y, 2))


def followforce(origin, force):
    origin.x += force.magnitude * math.cos(force.direction)
    origin.y += force.magnitude * math.sin(force.direction)


class Arrow:
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int, int], batch: pyglet.graphics.Batch):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.mainline = pyglet.shapes.Line(x1, y1, x2,  y2, color=color, batch=batch)
        self.L = 10
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.subline1 = pyglet.shapes.Line(
            x2, y2,
            x2 - (self.L * (x2 - x1) / dist - self.L * (y2 - y1) / math.sqrt(2) / dist),
            y2 - (self.L * (y2 - y1) / dist + self.L * (x2 - x1) / math.sqrt(2) / dist),
            color=color, batch=batch
        )
        self.subline2 = pyglet.shapes.Line(
            x2, y2,
            x2 - (self.L * (x2 - x1) / dist + self.L * (y2 - y1) / math.sqrt(2) / dist),
            y2 - (self.L * (y2 - y1) / dist - self.L * (x2 - x1) / math.sqrt(2) / dist),
            color=color, batch=batch
        )

    def update(self, x1, y1, x2, y2):
        self.mainline.x = x1
        self.mainline.y = y1
        self.mainline.x2 = x2
        self.mainline.y2 = y2
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.subline1.x = x2
        self.subline1.y = y2
        self.subline1.x2 = x2 - (self.L * (x2 - x1) / dist - self.L * (y2 - y1) / math.sqrt(2) / dist)
        self.subline1.y2 = y2 - (self.L * (y2 - y1) / dist + self.L * (x2 - x1) / math.sqrt(2) / dist)
        self.subline2.x = x2
        self.subline2.y = y2
        self.subline2.x2 = x2 - (self.L * (x2 - x1) / dist + self.L * (y2 - y1) / math.sqrt(2) / dist)
        self.subline2.y2 = y2 - (self.L * (y2 - y1) / dist - self.L * (x2 - x1) / math.sqrt(2) / dist)


class PhysicObject(pyglet.shapes.Circle):
    def __init__(self, x, y, radius, direction, magnitude, color, batch, objlist):
        super().__init__(x, y, radius, color=color, batch=batch)
        self.forcelist = []
        objlist.append(self)
        self.momentum = Force(self, direction, magnitude, color, batch, objlist, momentumupdater)

    def update(self):
        for force in self.forcelist:
            followforce(self, force)


class Force(Arrow):
    def __init__(self, origin: PhysicObject, direction, magnitude, color, batch, objlist, updater):
        super().__init__(origin.x, origin.y, origin.x + magnitude * math.cos(direction), origin.y + magnitude * math.sin(direction), color, batch)
        self.origin = origin
        self.direction = direction
        self.magnitude = magnitude
        objlist.append(self)
        origin.forcelist.append(self)
        self.updater = updater

    def update(self):
        self.updater(self)
        super().update(self.origin.x, self.origin.y, self.origin.x + self.magnitude * math.cos(self.direction), self.origin.y + self.magnitude * math.sin(self.direction))