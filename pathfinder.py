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
def h(cell,goal,t):
    d=abs(cell.r-goal.r)+abs(cell.c-goal.c)
    return d if t=="m" else math.sqrt((cell.r-goal.r)**2+(cell.c-goal.c)**2)

def search(g,algo,heur):
    start=time.time()
    nodes=0
    for row in g.data:
        for c in row:
            if c!=g.start and c!=g.goal and not c.wall: c.color=W
            c.g=999999; c.f=999999; c.parent=None
    g.start.g=0
    g.start.f=g.start.g+h(g.start,g.goal,heur) if algo=="a" else h(g.start,g.goal,heur)
    pq=PriorityQueue()
    cid=0
    pq.put((g.start.f,cid,g.start))
    in_pq={g.start}
    while not pq.empty():
        cur=pq.get()[2]
        in_pq.remove(cur)
        if cur!=g.start and cur!=g.goal: cur.color=R
        nodes+=1
        if cur==g.goal:
            path=[]
            while cur: path.append(cur); cur=cur.parent
            path.reverse()
            for c in path:
                if c!=g.start and c!=g.goal: c.color=G
            return path,nodes,g.goal.g,(time.time()-start)*1000
        for n in g.neigh(cur):
            ng=cur.g+1
            if ng<n.g:
                n.parent=cur; n.g=ng
                n.f=n.g+h(n,g.goal,heur) if algo=="a" else h(n,g.goal,heur)
                if n not in in_pq:
                    cid+=1; pq.put((n.f,cid,n)); in_pq.add(n)
                    if n!=g.goal: n.color=Y
    return None,nodes,0,(time.time()-start)*1000