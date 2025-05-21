import pyglet
import math
import physics

window = pyglet.window.Window(1200, 800)


@window.event
def on_draw():
    window.clear()
    windowbatch.draw()


def update(*args):
    global timer
    global timerticks
    if timer == 0:
        for obj in objlist:
            obj.update()
        timer = timerticks 
    else:
        timer -= 1


class ForceSum(physics.Force):
    def __init__(self, *args):
        super().__init__(*args)
        self.origin.forcelist.remove(self)


def gravityupdater(gravity):
    gravity.direction = math.atan2(400 - gravity.origin.y, 600 - gravity.origin.x)


def forcesumupdater(forcesum):
    x = 0
    y = 0
    for force in forcesum.origin.forcelist:
        x += force.magnitude * math.cos(force.direction)
        y += force.magnitude * math.sin(force.direction)
    forcesum.magnitude = math.sqrt(x ** 2 + y ** 2)
    forcesum.direction = math.atan2(y, x)


if __name__ == '__main__':
    windowbatch = pyglet.graphics.Batch()
    timer = 15
    timerticks = 15
    objlist = []
    circle = physics.PhysicObject(800, 400, 20, math.pi/2, 90, (255, 255, 255, 255), windowbatch, objlist)
    circle.momentum.mainline.color = (0, 0, 255, 255)
    circle.momentum.subline1.color = (0, 0, 255, 255)
    circle.momentum.subline2.color = (0, 0, 255, 255)
    gravity = physics.Force(circle, math.pi, 30, (255, 0, 0, 255), windowbatch, objlist, gravityupdater)
    sigmaforce = ForceSum(circle, 1, 1, (0, 255, 0, 255), windowbatch, objlist, forcesumupdater)
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()