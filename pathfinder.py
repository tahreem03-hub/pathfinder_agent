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
def main():
    r=int(input("Rows (5-20): "))
    c=int(input("Cols (5-25): "))
    d=float(input("Density (0-1): "))
    a=input("Algo? (1=A*,2=G): ")
    a="a" if a=="1" else "g"
    hh=input("Heur? (1=Man,2=Euc): ")
    hh="m" if hh=="1" else "e"
    
    g=Grid(r,c)
    for row in g.data:
        for cell in row:
            if cell!=g.start and cell!=g.goal and random.random()<d:
                cell.wall=True
    
    dyn=False; path=None; nodes=0; cost=0; t=0; run=True
    while run:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: run=False
            elif e.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                cx,cy=x//40,y//40
                cell=g.get(cy,cx)
                if cell and cell!=g.start and cell!=g.goal:
                    if e.button==1: cell.wall=True; path=None
                    elif e.button==3: cell.wall=False; path=None
            elif e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r:
                    for row in g.data:
                        for cell in row:
                            if cell!=g.start and cell!=g.goal:
                                cell.wall=random.random()<d
                    path=None
                elif e.key==pygame.K_c:
                    for row in g.data:
                        for cell in row:
                            if cell!=g.start and cell!=g.goal: cell.wall=False
                    path=None
                elif e.key==pygame.K_SPACE:
                    path,nodes,cost,t=search(g,a,hh)
                elif e.key==pygame.K_d: dyn=not dyn
        
        if dyn and random.random()<0.005:
            rr,cc=random.randint(0,r-1),random.randint(0,c-1)
            cell=g.get(rr,cc)
            if cell and cell!=g.start and cell!=g.goal:
                cell.wall=True
                if path:
                    for p in path:
                        if p.wall: path,nodes,cost,t=search(g,a,hh); break
        
        screen.fill(W)
        for row in g.data:
            for cell in row:
                if cell.wall: pygame.draw.rect(screen,B,(cell.x,cell.y,38,38))
                else: pygame.draw.rect(screen,cell.color,(cell.x,cell.y,38,38))
                pygame.draw.rect(screen,(200,200,200),(cell.x,cell.y,38,38),1)
        
        y=10
        algo_name="A*" if a=="a" else "Greedy"
        heur_name="Man" if hh=="m" else "Euc"
        for txt in [f"Algo:{algo_name}",f"Heur:{heur_name}",f"Den:{d}",f"Dyn:{dyn}",
                    f"Nodes:{nodes}",f"Cost:{cost}",f"Time:{t:.0f}ms",
                    "","L:add","R:remove","R:rand","C:clear","Space:run","D:dyn"]:
            screen.blit(font.render(txt,True,B),(620,y)); y+=20
        pygame.display.flip()
    
    pygame.quit()

if __name__=="__main__":
    main()