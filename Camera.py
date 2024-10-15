#3d object camera parser
import math

##Dot product
def dot(x1, y1, z1, x2, y2, z2):
    return x1 * x2 + y1 * y2 + z1 * z2

## Retuns Cartiesian x given a polar coordinate
def cx(r, t, p):
    return r*math.cos(t)*math.cos(p)

## Retuns Cartiesian y given a polar coordinate
def cy(r, t, p):
    return r*math.sin(t)*math.cos(p)

## Retuns Cartiesian z given a polar coordinate
def cz(r, t, p):
    return r*math.sin(p)

class camera:
    def __init__(self):
        self.r = 1
        self.t = 0
        self.p = 0
        self.xp = [0,1,0]
        self.yp = [0,0,1]

    def updR(self,r):
        self.r = r

    def updTheta(self,t):
        self.t = t
        self.xp[0] = -math.sin(self.t)
        self.xp[1] = math.cos(self.t)
        self.xp[2] = 0
        self.yp[0] = -1*math.cos(self.t)*math.sin(self.p)
        self.yp[1] = -1*math.sin(self.t)*math.sin(self.p)
        self.yp[2] = math.cos(self.p)

    def updPhi(self,p):
        self.p = p
        self.xp[0] = -math.sin(self.t)
        self.xp[1] = math.cos(self.t)
        self.xp[2] = 0
        self.yp[0] = -1*math.cos(self.t)*math.sin(self.p)
        self.yp[1] = -1*math.sin(self.t)*math.sin(self.p)
        self.yp[2] = math.cos(self.p)

    def addR(self,r):
        self.r += r

    def addTheta(self,t):
        self.t += t
        self.xp[0] = -math.sin(self.t)
        self.xp[1] = math.cos(self.t)
        self.xp[2] = 0
        self.yp[0] = -1*math.cos(self.t)*math.sin(self.p)
        self.yp[1] = -1*math.sin(self.t)*math.sin(self.p)
        self.yp[2] = math.cos(self.p)

    def addPhi(self,p):
        self.p += p
        self.xp[0] = -math.sin(self.t)
        self.xp[1] = math.cos(self.t)
        self.xp[2] = 0
        self.yp[0] = -1*math.cos(self.t)*math.sin(self.p)
        self.yp[1] = -1*math.sin(self.t)*math.sin(self.p)
        self.yp[2] = math.cos(self.p)

    def screenx(self, x, y, z):
        return dot(self.xp[0],self.xp[1],self.xp[2],x,y,z)
    
    def screeny(self, x, y, z):
        return dot(self.yp[0],self.yp[1],self.yp[2],x,y,z)
    
    def displayPosition(self, x, y, z):
        #gets the position relitive to the camera position
        pp = [x-cx(self.r,self.t, self.p),y-cy(self.r,self.t, self.p),z-cz(self.r,self.t, self.p)]
        #returns the screen position of point
        return [self.screenx(pp[0],pp[1],pp[2]),self.screeny(pp[0],pp[1],pp[2])]
    
    def getTheta(self):
        return self.t
    
    def getPhi(self):
        return self.p
    
    def getXprime(self):
        return self.xp
    
    def getYprime(self):
        return self.yp