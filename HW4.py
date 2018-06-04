import Tkinter as tk
import time as sleep
import math
import random 
from copy import deepcopy 
import threading

pos =  [[0 for i in range(3)]for i in range(3)]
map =  [[[] for i in range(3)]for i in range(3)]
remap = [[[] for i in range(3)]for i in range(3)]
tmap = [[[[] for i in range(3)]for i in range(3)]for i in range(4)]
tpos = [[[0 for i in range(3)]for i in range(3)]for i in range(4)]
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
  ran = random.sample(xrange(1,9), 8)
  k=0
  for i in range(3):
    for j in range(3):
      map[i][j]=ran[k]
      k+=1
      if(k==8): 
        break
        break
  remap = deepcopy(map) 
  return 

def action(x, y, map):
  global remap
  samemap = deepcopy(map)
  if(not map[x][y]): return
  for i in range(4):
    tx = x + victor[i][0]
    ty = y + victor[i][1]
    if( 0 <= tx <= 2 and  0 <= ty <= 2 and not map[tx][ty] ):
      v = map[tx][ty]
      map[tx][ty] = map[x][y]
      map[x][y] = v
  if(samemap != map ): remap = deepcopy(samemap)
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

def play():
  global map
  createmap(map)
  normalgraphic()

def re():
  global map
  map = deepcopy(remap)
  normalgraphic()

def th():
  global tmap
  for i in range(4):  createmap(tmap[i])
  threadgraphic()

def ai():
  global tmap
  createmap(map)
  normalgraphic()

def normalgraphic():
  global map
  dectcorrect(map)
  back = ['#f9f7f7', '#60efb8']
  B1 = tk.Button(window, text ="Play", command = play)
  B2 = tk.Button(window, text ="Return", command = re)
  B3 = tk.Button(window, text ="4-thread", command = th)
  B4 = tk.Button(window, text ="AI", command = ai)
  B1.grid(column=0, row=0)
  B2.grid(column=1, row=0)
  B3.grid(column=2, row=0)
  B4.grid(column=3, row=0)
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
  global tmap
  thdectcorrect(tmap)
  back = ['#f9f7f7', '#60efb8']
  B1 = tk.Button(window, text ="Play", command = play)
  B2 = tk.Button(window, text ="Return", command = re)
  B3 = tk.Button(window, text ="4-thread", command = th)
  B4 = tk.Button(window, text ="AI", command = ai)
  B1.grid(column=0, row=0)
  B2.grid(column=1, row=0)
  B3.grid(column=2, row=0)
  B4.grid(column=3, row=0)
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