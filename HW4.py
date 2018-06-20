import Tkinter as tk
import time 
from time import sleep
import math
import random 
from copy import deepcopy 
import threading
import json
gxbound=0
pos =  [[0 for i in range(3)]for i in range(3)]
map =  [[[] for i in range(3)]for i in range(3)]
remap = [[[] for i in range(3)]for i in range(3)]
tmap = [[[[] for i in range(3)]for i in range(3)]for i in range(4)]
tpos = [[[0 for i in range(3)]for i in range(3)]for i in range(4)]
appearmap = {}
step = 0
thstep=[0 for i in range(4)]
victor = [
  # X , Y
  [  0, -1 ], # L
  [  1,  0 ], # D
  [  0,  1 ], # R
  [ -1,  0 ]  # T
]

def dectcorrect(map):
  for i in range(3):
    for j in range(3):
      if(map[i][j]==3*i+j+1):pos[i][j] = 1
      else: pos[i][j] = 0

def thdectcorrect(map):
  for k in range(4):
    for i in range(3):
      for j in range(3):
        if(map[k][i][j]==3*i+j+1):tpos[k][i][j] = 1
        else: tpos[k][i][j] = 0

def createmap(map):
  global remap
  random.seed(time.time())
  i = random.randint(0,2)
  print i
  if(i==0):map=[[1,7,8],[5,[],2],[4,3,6]]
  elif(i==1):map=[[4,7,1],[3,[],5],[8,2,6]]
  elif(i==2):map=[[3,1,4],[5,[],6],[8,7,2]]
  remap = deepcopy(map)
  return map

def action(x, y, map):
  global remap,step
  samemap = deepcopy(map)
  if(not map[x][y]): return
  for i in range(4):
    tx = x + victor[i][0]
    ty = y + victor[i][1]
    if( 0 <= tx <= 2 and  0 <= ty <= 2 and not map[tx][ty] ):
      v = map[tx][ty]
      map[tx][ty] = map[x][y]
      map[x][y] = v
  if(samemap != map ): 
    step+=1
    remap = deepcopy(samemap)
  normalgraphic()
  endgame =[
    [1,2,3],
    [4,5,6],
    [7,8,[]]
  ]
  if(map == endgame): window.destroy()

def thaction(x, y, map):
  if(not map[x][y]): return
  for i in range(4):
    tx = x + victor[i][0]
    ty = y + victor[i][1]
    if( 0 <= tx <= 2 and  0 <= ty <= 2 and not map[tx][ty] ):
      v = map[tx][ty]
      map[tx][ty] = map[x][y]
      map[x][y] = v
  threadgraphic()
  endgame =[
    [1,2,3],
    [4,5,6],
    [7,8,[]]
  ]
  if(map == endgame): window.destroy()

def distance(a, b): return abs(a[0]- b[0]) + abs(a[1]- b[1])
#check not in correct position block count
def h_d(map):
  count = 0
  cp=[
    [0,0],[0,1],[0,2],
    [1,0],[1,1],[1,2],
    [2,0],[2,1]
  ]
  for i in range(3):
    for j in range(3):
      if(map[i][j]!=0): 
        target=cp[map[i][j]-1]
        count += distance([i, j],target)
  return count

ans = False
def aifun(map):
  global appearmap, ans
  print "ai s"
  dx = [-1, 1, 0, 0]
  dy = [0, 0, -1, 1]
  rev_dir = [1, 0, 3, 2]
  solution = [[]for i in range(200)]
  def onmap(pos): return 0<=pos[0]<3 and 0<=pos[1]<3 
  def swap(a, b, map):
    tem = map[a[0]][a[1]]
    map[a[0]][a[1]] = map[b[0]][b[1]]
    map[b[0]][b[1]] = tem
  def testhash(map):
    global appearmap
    astr = ''
    for i in range(9):
        if(map[i/3][i%3]): astr+= str(map[i/3][i%3])
        else: astr+= '0'
    try: 
      if(appearmap[astr]):  return True
    except KeyError: return False
  def hashfun(map):
    global appearmap
    astr = ''
    for i in range(9):
        if(map[i/3][i%3]): astr+= str(map[i/3][i%3])
        else: astr+= '0'
    try: 
      if(appearmap[astr]):  return
    except KeyError: 
      appearmap[astr] = True
  def IDAstar(x, y, gx, prev_dir, bound, map):
    global ans,gxbound
    hx = h_d(map)
    if (gx + hx > bound): return gx + hx
    if (hx == 0):
      ans = True
      return gx
    workdir=[-1 for i in range(4)]
    j=0
    for i in range(4):
      nx = x - dx[i]
      ny = y - dy[i]
      if (rev_dir[i] == prev_dir or (not onmap([nx, ny])) ): continue
      workdir[j] = i
      j+=1
    pmap=deepcopy(map)
    for i in range(len(workdir)):
      t = workdir[i]
      if(t!=-1):
        nx = x - dx[t]
        ny = y - dy[t]
        solution[gx] = t
        swap([nx, ny], [x, y], map)
        nbound = bound
        if(not testhash(map)):
          nbound = bound
          if(j==i+1):  hashfun(pmap)
          omap=deepcopy(map)
          bound = IDAstar(nx, ny, gx+1, t, nbound, omap)
          if(ans):return gx
        swap([x, y], [nx, ny], map)
        if(bound>=45 ): bound = nbound
    return bound
    
  # mainfun
  for i in range(9):
    if(map[i/3][i%3]==[]): map[i/3][i%3]=0
  for i in range(9):
    if(map[i/3][i%3]==0): 
      sx = i/3
      sy = i%3
  bound = 0 
  hashfun(map)
  while (not ans and bound <= 200):
    bound= IDAstar(sx, sy, 0, -1, bound, map)
  print "ai e"
  return solution

def solactionfun(thi, solution):
  global tmap, thstep
  dx = [-1, 1, 0, 0]
  dy = [0, 0, -1, 1]
  ans = [ [1,2,3],[4,5,6],[7,8,[]] ]
  def swap(a, b, tmap):
    tem = tmap[thi][a[0]][a[1]]
    tmap[thi][a[0]][a[1]] = tmap[thi][b[0]][b[1]]
    tmap[thi][b[0]][b[1]] = tem
  for j in range(9):
    if(not tmap[thi][j/3][j%3]):
      x = j/3
      y = j%3
  for i in solution:
    if(i!=[]):
      thstep[thi]+=1
      nx = x - dx[i]
      ny = y - dy[i]
      swap([nx, ny], [x, y], tmap)
      x = nx
      y = ny
      sleep(0.5)
      threadgraphic()
    else: break

def testact( solution):
  global map, step
  dx = [-1, 1, 0, 0]
  dy = [0, 0, -1, 1]
  ans = [ [1,2,3],[4,5,6],[7,8,[]] ]
  def swap(a, b, map):
    tem = map[a[0]][a[1]]
    map[a[0]][a[1]] = map[b[0]][b[1]]
    map[b[0]][b[1]] = tem
  for j in range(9):
    if(not map[j/3][j%3]):
      x = j/3
      y = j%3
  for i in solution:
    if(i!=[]):
      step+=1
      nx = x - dx[i]
      ny = y - dy[i]
      swap([nx, ny], [x, y], map)
      x = nx
      y = ny
      sleep(0.5)
      normalgraphic()
    else: break

def play():
  global map
  map = createmap(map)
  normalgraphic()
  aa=raw_input()
  solution = [[]for i in range(200)]
  solution= aifun(map)
  map = deepcopy(remap)
  testact(solution)

def re():
  global map, step
  if(map!=remap):
    step-=1
    map = deepcopy(remap)
  normalgraphic()

def th():
  global tmap, map
  map =  [[[] for i in range(3)]for i in range(3)]
  map = createmap(map)
  for i in range(4): tmap[i] = deepcopy(map)
  threadgraphic()

def ai():
  global tmap, map, thstep
  solution = [[]for i in range(200)]
  solution= aifun(map)
  thread0 = threading.Thread(target = solactionfun, args=(0, solution))
  thread1 = threading.Thread(target = solactionfun, args=(1, solution))
  thread2 = threading.Thread(target = solactionfun, args=(2, solution))
  thread3 = threading.Thread(target = solactionfun, args=(3, solution))
  thread0.start()
  thread1.start()
  thread2.start()
  thread3.start()
  print 'end'
  threadgraphic()

  

def normalgraphic():
  global map, step
  dectcorrect(map)
  back = ['#f9f7f7', '#60efb8']
  B1 = tk.Button(window, text ="Play", command = play)
  B2 = tk.Button(window, text ="Return", command = re)
  B3 = tk.Button(window, text ="4-thread", command = th)
  B4 = tk.Button(window, text ="AI", command = ai)
  L5 = tk.Label(window, text=step, font=('Arial', 14))
  B1.grid(column=0, row=0)
  B2.grid(column=1, row=0)
  B3.grid(column=2, row=0)
  B4.grid(column=3, row=0)
  L5.grid(column=3, row=1)
  #===========================================
  tk.Button(window, text = map[0][0], bg = back[pos[0][0]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(0, 0, map)
  ).grid(column=0, row=1, padx=1, pady=1)
  tk.Button(window, text = map[0][1], bg = back[pos[0][1]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(0, 1, map)
  ).grid(column=1, row=1, padx=1, pady=1)
  tk.Button(window, text = map[0][2], bg = back[pos[0][2]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(0, 2, map)
  ).grid(column=2, row=1, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = map[1][0], bg = back[pos[1][0]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(1, 0, map)
  ).grid(column=0, row=2, padx=1, pady=1)
  tk.Button(window, text = map[1][1], bg = back[pos[1][1]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(1, 1, map)
  ).grid(column=1, row=2, padx=1, pady=1)
  tk.Button(window, text = map[1][2], bg = back[pos[1][2]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(1, 2, map)
  ).grid(column=2, row=2, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = map[2][0], bg = back[pos[2][0]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(2, 0, map)
  ).grid(column=0, row=3, padx=1, pady=1)
  tk.Button(window, text = map[2][1], bg = back[pos[2][1]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(2, 1, map)
  ).grid(column=1, row=3, padx=1, pady=1)
  tk.Button(window, text = map[2][2], bg = back[pos[2][2]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(2, 2, map)
  ).grid(column=2, row=3, padx=1, pady=1)
  window.update_idletasks()

def threadgraphic():
  window.geometry('400x400')
  global tmap, thstep
  print thstep
  thdectcorrect(tmap)
  back = ['#f9f7f7', '#60efb8']
  B1 = tk.Button(window, text ="Play", command = play)
  B2 = tk.Button(window, text ="Return", command = re)
  B3 = tk.Button(window, text ="4-thread", command = th)
  B4 = tk.Button(window, text ="AI", command = ai)
  L0 = tk.Label(window, text=thstep[0], font=('Arial', 14))
  L1 = tk.Label(window, text=thstep[1], font=('Arial', 14))
  L2 = tk.Label(window, text=thstep[2], font=('Arial', 14))
  L3 = tk.Label(window, text=thstep[3], font=('Arial', 14))
  B1.grid(column=0, row=0)
  B2.grid(column=1, row=0)
  B3.grid(column=2, row=0)
  B4.grid(column=3, row=0)
  L0.grid(column=0, row=7)
  L1.grid(column=1, row=7)
  L2.grid(column=2, row=7)
  L3.grid(column=3, row=7)
  #----------------------------------------------------------------
  #-----G0-----
  tk.Button(window, text = tmap[0][0][0], bg = back[tpos[0][0][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 0, tmap[0])
  ).grid(column=0, row=1, padx=1, pady=1)
  tk.Button(window, text = tmap[0][0][1], bg = back[tpos[0][0][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 1, tmap[0])
  ).grid(column=1, row=1, padx=1, pady=1)
  tk.Button(window, text = tmap[0][0][2], bg = back[tpos[0][0][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 2, tmap[0])
  ).grid(column=2, row=1, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[0][1][0], bg = back[tpos[0][1][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 0, tmap[0])
  ).grid(column=0, row=2, padx=1, pady=1)
  tk.Button(window, text = tmap[0][1][1], bg = back[tpos[0][1][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 1, tmap[0])
  ).grid(column=1, row=2, padx=1, pady=1)
  tk.Button(window, text = tmap[0][1][2], bg = back[tpos[0][1][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 2, tmap[0])
  ).grid(column=2, row=2, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[0][2][0], bg = back[tpos[0][2][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 0, tmap[0])
  ).grid(column=0, row=3, padx=1, pady=1)
  tk.Button(window, text = tmap[0][2][1], bg = back[tpos[0][2][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 1, tmap[0])
  ).grid(column=1, row=3, padx=1, pady=1)
  tk.Button(window, text = tmap[0][2][2], bg = back[tpos[0][2][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 2, tmap[0])
  ).grid(column=2, row=3, padx=1, pady=1)
  #----------------------------------------------------------------
  #-----G1-----
  tk.Button(window, text = tmap[1][0][0], bg = back[tpos[1][0][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 0, tmap[1])
  ).grid(column=3, row=1, padx=1, pady=1)
  tk.Button(window, text = tmap[1][0][1], bg = back[tpos[1][0][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 1, tmap[1])
  ).grid(column=4, row=1, padx=1, pady=1)
  tk.Button(window, text = tmap[1][0][2], bg = back[tpos[1][0][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 2, tmap[1])
  ).grid(column=5, row=1, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[1][1][0], bg = back[tpos[1][1][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 0, tmap[1])
  ).grid(column=3, row=2, padx=1, pady=1)
  tk.Button(window, text = tmap[1][1][1], bg = back[tpos[1][1][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 1, tmap[1])
  ).grid(column=4, row=2, padx=1, pady=1)
  tk.Button(window, text = tmap[1][1][2], bg = back[tpos[1][1][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 2, tmap[1])
  ).grid(column=5, row=2, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[1][2][0], bg = back[tpos[1][2][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 0, tmap[1])
  ).grid(column=3, row=3, padx=1, pady=1)
  tk.Button(window, text = tmap[1][2][1], bg = back[tpos[1][2][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 1, tmap[1])
  ).grid(column=4, row=3, padx=1, pady=1)
  tk.Button(window, text = tmap[1][2][2], bg = back[tpos[1][2][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 2, tmap[1])
  ).grid(column=5, row=3, padx=1, pady=1)
  #----------------------------------------------------------------
  #-----G2-----
  tk.Button(window, text = tmap[2][0][0], bg = back[tpos[2][0][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 0, tmap[2])
  ).grid(column=0, row=4, padx=1, pady=1)
  tk.Button(window, text = tmap[2][0][1], bg = back[tpos[2][0][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 1, tmap[2])
  ).grid(column=1, row=4, padx=1, pady=1)
  tk.Button(window, text = tmap[2][0][2], bg = back[tpos[2][0][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 2, tmap[2])
  ).grid(column=2, row=4, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[2][1][0], bg = back[tpos[2][1][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 0, tmap[2])
  ).grid(column=0, row=5, padx=1, pady=1)
  tk.Button(window, text = tmap[2][1][1], bg = back[tpos[2][1][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 1, tmap[2])
  ).grid(column=1, row=5, padx=1, pady=1)
  tk.Button(window, text = tmap[2][1][2], bg = back[tpos[2][1][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 2, tmap[2])
  ).grid(column=2, row=5, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[2][2][0], bg = back[tpos[2][2][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 0, tmap[2])
  ).grid(column=0, row=6, padx=1, pady=1)
  tk.Button(window, text = tmap[2][2][1], bg = back[tpos[2][2][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 1, tmap[2])
  ).grid(column=1, row=6, padx=1, pady=1)
  tk.Button(window, text = tmap[2][2][2], bg = back[tpos[2][2][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 2, tmap[2])
  ).grid(column=2, row=6, padx=1, pady=1)
  #----------------------------------------------------------------
  #-----G3-----
  tk.Button(window, text = tmap[3][0][0], bg = back[tpos[3][0][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 0, tmap[3])
  ).grid(column=3, row=4, padx=1, pady=1)
  tk.Button(window, text = tmap[3][0][1], bg = back[tpos[3][0][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 1, tmap[3])
  ).grid(column=4, row=4, padx=1, pady=1)
  tk.Button(window, text = tmap[3][0][2], bg = back[tpos[3][0][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(0, 2, tmap[3])
  ).grid(column=5, row=4, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[3][1][0], bg = back[tpos[3][1][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 0, tmap[3])
  ).grid(column=3, row=5, padx=1, pady=1)
  tk.Button(window, text = tmap[3][1][1], bg = back[tpos[3][1][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 1, tmap[3])
  ).grid(column=4, row=5, padx=1, pady=1)
  tk.Button(window, text = tmap[3][1][2], bg = back[tpos[3][1][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(1, 2, tmap[3])
  ).grid(column=5, row=5, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = tmap[3][2][0], bg = back[tpos[3][2][0]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 0, tmap[3])
  ).grid(column=3, row=6, padx=1, pady=1)
  tk.Button(window, text = tmap[3][2][1], bg = back[tpos[3][2][1]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 1, tmap[3])
  ).grid(column=4, row=6, padx=1, pady=1)
  tk.Button(window, text = tmap[3][2][2], bg = back[tpos[3][2][2]],
    font=('Arial', 14), width = 3, height = 2, command = lambda: thaction(2, 2, tmap[3])
  ).grid(column=5, row=6, padx=1, pady=1)
  window.update_idletasks()

def initwindow():
  back = ['#f9f7f7', '#60efb8']
  B1 = tk.Button(window, text ="Play", command = play)
  B2 = tk.Button(window, text ="Return", command = re)
  B3 = tk.Button(window, text ="4-thread", command = th)
  B4 = tk.Button(window, text ="AI", command = ai)
  B1.grid(column=0, row=0)
  B2.grid(column=1, row=0)
  B3.grid(column=2, row=0)
  B4.grid(column=3, row=0)
  window.update_idletasks()

if __name__ == '__main__':
  window = tk.Tk()
  window.title('puzzle')
  window.geometry('350x350')
  initwindow()
  window.mainloop()