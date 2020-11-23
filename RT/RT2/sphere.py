#Pablo Lopez   
#Graficas
#14509
#RT2

from utils import sub, dot, length, sum, mul, norm, Intersect


class Sphere(object):
  def __init__(self, center, radius, material):
    self.center = center
    self.radius = radius
    self.material = material

  def rayIntersect(self, origin, direction):
    L = sub(self.center, origin)
    tca = dot(L, direction)
    l = length(L)
    d2 = l ** 2 - tca ** 2
    if d2 > self.radius ** 2:
        return None
    thc = (self.radius ** 2 - d2) ** 0.5
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
        t0 = t1
    if t0 < 0:
        return None
    hit = sum(origin, mul(direction, t0))
    normal = norm(sub(hit, self.center))
    return Intersect(
        distance=t0,
        point=hit,
        normal=normal
    )
