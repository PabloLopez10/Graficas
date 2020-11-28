#Pablo Lopez
#Graficas por computadora
#14509
#Proyecto2

import intersect
from utils import *
from math import *


class Material(object):
  def __init__(self, diffuse=(0,0,0), albedo=(1, 0,1), spec=0, deg=None):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec
    self.deg = deg


class Sphere(object):
  def __init__(self, center, radius, material, colour=(0,0,0)):
    self.center = center
    self.radius = radius
    self.colour = colour
    self.material = material

  def ray_intersect(self, orig, direction):
    L = sub(self.center, orig)
    tca = dot(L, direction)
    l = length(L)
    d2 = l**2 - tca**2
    if d2 > self.radius**2:
      return None
    thc = (self.radius**2 - d2)**1/2
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    hit = sum(orig, mul(direction, t0))
    
    normal = norm(sub(hit, self.center))
    
    return intersect.Intersect(
      distance=t0,
      point=hit,
      normal = normal
    )

class Cube(object):
  def __init__(self, lengths, material, rotation='y', rotation_normal=1):
    self.x = min(lengths[0])
    self.x2 = max(lengths[0])
    self.y = min(lengths[1])
    self.y2 = max(lengths[1])
    self.z = min(lengths[2])
    self.z2 = max(lengths[2])
    self.material = material

  def ray_intersect(self, orig, direction):
    try:
        invdir = V3(1 / direction.x, 1/direction.y, 1/direction.z)
    except:
        return None
    if invdir.x >= 0:
        tmin = (self.x - orig.x) * invdir.x
        tmax = (self.x2 - orig.x) * invdir.x
    else:
        tmin = (self.x2 - orig.x) * invdir.x
        tmax = (self.x - orig.x) * invdir.x
    if invdir.y >= 0:
        tymin = (self.y - orig.y) * invdir.y
        tymax = (self.y2 - orig.y) * invdir.y
    else:
        tymin = (self.y2 - orig.y) * invdir.y
        tymax = (self.y - orig.y) * invdir.y

    if ((tmin > tymax) or (tymin > tmax)):
        return None
    if (tymin > tmin):
        tmin = tymin
    if (tymax < tmax):
        tmax = tymax
    
    if invdir.z >=0:
        tzmin = (self.z - orig.z) * invdir.z
        tzmax = (self.z2 - orig.z) * invdir.z
    else: 
        tzmin = (self.z2 - orig.z) * invdir.z
        tzmax = (self.z - orig.z) * invdir.z

    if (tmin > tzmax) or (tzmin > tmax):
        return None
    if (tzmin > tmin):
        tmin = tzmin
    if (tzmax < tmax):
        tmax = tzmax
    
    t = tmin

    if t<0:
        t=tmax
    if t<0:
        return None
    

    xmid = (self.x + self.x2) /2
    ymid = (self.y + self.y2) /2
    zmid = (self.z + self.z2) /2
    center = V3(xmid, ymid, zmid)
    hit = sum(orig, mul(direction, t))
    normal = norm(sub(hit, center))
    return intersect.Intersect(
      distance=t,
      point=hit,
      normal = normal
    )