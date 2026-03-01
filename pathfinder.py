import pygame, random, math, time
from queue import PriorityQueue

pygame.init()
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.Font(None, 24)

# Colors
W = (255,255,255)
B = (0,0,0)
R = (255,0,0)
G = (0,255,0)
BL = (0,0,255)
Y = (255,255,0)
P = (128,0,128)

class Cell:
    def __init__(self,r,c):
        self.r=r; self.c=c
        self.x=c*40; self.y=r*40
        self.wall=False; self.color=W
        self.g=999999; self.f=999999
        self.parent=None
class Grid:
    def __init__(self,r,c):
        self.r=r; self.c=c
        self.data=[[Cell(i,j) for j in range(c)] for i in range(r)]
        self.start=self.data[0][0]; self.start.color=BL
        self.goal=self.data[r-1][c-1]; self.goal.color=P
    
    def get(self,r,c):
        if 0<=r<self.r and 0<=c<self.c: return self.data[r][c]
    def neigh(self,cell):
        out=[]
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            n=self.get(cell.r+dr,cell.c+dc)
            if n and not n.wall: out.append(n)
        return out