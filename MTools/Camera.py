# A quick camera class to store the values needed to represent a
# camera in this pipeline.
from MTools.Vector import Vector
from MTools.Ray import Ray
import math


class Camera(object):
    def __init__(self, width=800, height=600):
        self.e = Vector(0, 0, 0)
        self.g = Vector(0, 0, -1)
        self.t = Vector(0, 100, 0)
        self.n = 2
        self.f = 10
        self.angle = 90
        self.width = width
        self.height = height
        self.calc()

    def calc(self):
        self.w = -1 * self.g
        self.u = self.t.cross(self.w).normalize()
        self.v = self.w.cross(self.u)
        self.top = abs(self.n) * math.tan(math.radians(self.angle / 2))
        self.bot = -self.top
        self.rit = self.top * self.width / self.height
        self.lef = -self.rit

    def eSet(self, x, y, z):
        self.e = Vector(x, y, z)
        self.calc()

    def gSet(self, x, y, z):
        self.g = Vector(x, y, z)
        self.g.normalize()
        self.calc()

    def tSet(self, x, y, z):
        self.t = Vector(x, y, z)
        self.t.normalize()
        self.calc()

    def nSet(self, val):
        self.n = val
        self.calc()

    def fSet(self, val):
        self.f = val
        self.calc()

    def angleSet(self, val):
        self.angle = val
        self.calc()

    def nudgePos(self, *list):
        vect = Vector(*list)
        self.eSet(*(self.e + vect))

    def nudgeGaz(self, *list):
        vect = Vector(*list)
        self.gSet(*(self.g + vect))

    def nudgeT(self, *list):
        vect = Vector(*list)
        self.tSet(*(self.t + vect))

    def xPosSet(self, val):
        self.eSet(val, self.e.y, self.e.z)

    def yPosSet(self, val):
        self.eSet(self.e.x, val, self.e.z)

    def zPosSet(self, val):
        self.eSet(self.e.x, self.e.y, val)

    # The following is for raytracing:
    def ray(self, xPixel, yPixel):
        xCam = self.lef + ((self.rit - self.lef) * (xPixel + 0.5) / self.width)
        yCam = self.bot + ((self.top - self.bot) * (yPixel + 0.5) / self.height)
        result = (self.w * -self.n) + (self.u * xCam) + (self.v * yCam)
        result.normalize()
        return Ray(self.e, result)

    def lookAt(self, x, y, z):
        point = Vector(x, y, z)
        direction = point - self.e
        self.gSet(direction.x, direction.y, direction.z)



if __name__ == '__main__':
    c = Camera()
    print(c.e)
    c.xPosSet(-2)
    print(c.e)
    c.nudgePos(-1, 4, 4)
    print(c.e)
    c.gSet(1, 1, 1)
    print(c.g)
