import pyglet
import math

window = pyglet.window.Window(1200, 800)


@window.event
def on_draw():
    window.clear()
    windowbatch.draw()


class Arrow:
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int, int], batch: pyglet.graphics.Batch):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.mainline = pyglet.shapes.Line(x1, y1, x2,  y2, color=color, batch=batch)
        self.L = 10
        self.subline1 = pyglet.shapes.Line(x2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) + (y2 - y1)), y2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) - (y2 - y1)), x2, y2, color=color, batch=batch)
        self.subline2 = pyglet.shapes.Line(x2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) - (y2 - y1)), y2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) + (y2 - y1)), x2, y2, color=color, batch=batch)

    def update(self, x1, y1, x2, y2):
        self.mainline.x = x1
        self.mainline.y = y1
        self.mainline.x2 = x2
        self.mainline.y2 = y2
        self.subline1.x = x2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) + (y2 - y1))
        self.subline1.y = y2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) - (y2 - y1))
        self.subline1.x2 = x2
        self.subline1.y2 = y2
        self.subline2.x = x2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) - (y2 - y1))
        self.subline2.y = y2 - self.L / (math.sqrt(2) * math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))) * ((x2 - x1) + (y2 - y1))
        self.subline2.x2 = x2
        self.subline2.y2 = y2


class PhysicObject(pyglet.shapes.Circle):
    def __init__(self, x, y, radius, direction, magnitude, color, batch):
        super().__init__(x, y, radius, color=color, batch=batch)
        self.momentum = Force(self, direction, magnitude, color, batch)
        self.forcelist = []

    def update(self):
        for force in self.forcelist:
            followforce(self, force)
        followforce(self, self.momentum)


class Force(Arrow):
    def __init__(self, origin: PhysicObject, direction, magnitude, color, batch):
        super().__init__(origin.x, origin.y, origin.x + magnitude * math.cos(direction), origin.y + magnitude * math.sin(direction), color, batch)
        self.origin = origin
        self.direction = direction
        self.magnitude = magnitude
        origin.forcelist.append(self)

    def update(self):
        super().update(self.origin.x, self.origin.y, self.origin.x + self.magnitude * math.cos(self.direction), self.origin.y + self.magnitude * math.sin(self.direction))


def followforce(origin, force):
    origin.x += force.magnitude * math.cos(force.direction)
    origin.y += force.magnitude * math.sin(force.direction)


def update(*args):
    pass
    #for obj in objlist:
    #    obj.update()


if __name__ == '__main__':
    windowbatch = pyglet.graphics.Batch()
    objlist =[]
    arrow1 = Arrow(30, 30, 70, 70, (255, 255, 255, 255), windowbatch)
    circle = pyglet.shapes.Circle(500, 500, 20, color=(255, 255, 255, 255))
    objlist.append(arrow1)
    objlist.append(circle)
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()