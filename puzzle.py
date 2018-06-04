import Tkinter as tk
import time as sleep
import math
import random 
from copy import deepcopy 
import threading

pos = [[0 for i in range(3)]for i in range(3)]
map = [[[] for i in range(3)]for i in range(3)]
remap = [[[] for i in range(3)]for i in range(3)]

victor = [
  # X , Y
  [  0, -1 ], # L
  [  1,  0 ], # D
  [  0,  1 ], # R
  [ -1,  0 ]  # T
]

def dectcorrect():
  global map
  for i in range(3):
    for j in range(3):
      if(map[i][j]==3*i+j+1):pos[i][j] = 1
      else: pos[i][j] = 0

def createmap():
  global map
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

def action(x, y):
  global map
  samemap = deepcopy(map)
  # print map
  # print str(x) +'-'+str(y)
  # print map[x][y]
  if(not map[x][y]): return
  for i in range(4):
    tx = x + victor[i][0]
    ty = y + victor[i][1]
    if( 0 <= tx <= 2 and  0 <= ty <= 2 and not map[tx][ty] ):
      v = map[tx][ty]
      map[tx][ty] = map[x][y]
      map[x][y] = v
  if(samemap != map ): remap = deepcopy(map)
  graphic()

def play():
  global map
  createmap()
  print map
  graphic()

def re():
  global map
  print map
  print remap
  map = deepcopy(remap)
  graphic()

def th():
  global map
  createmap()
  print map
  graphic()

def ai():
  global map
  createmap()
  print map
  graphic()

def graphic():
  global map
  dectcorrect()
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
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(0, 0)
  ).grid(column=0, row=1, padx=1, pady=1)
  tk.Button(window, text = map[0][1], bg = back[pos[0][1]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(0, 1)
  ).grid(column=1, row=1, padx=1, pady=1)
  tk.Button(window, text = map[0][2], bg = back[pos[0][2]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(0, 2)
  ).grid(column=2, row=1, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = map[1][0], bg = back[pos[1][0]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(1, 0)
  ).grid(column=0, row=2, padx=1, pady=1)
  tk.Button(window, text = map[1][1], bg = back[pos[1][1]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(1, 1)
  ).grid(column=1, row=2, padx=1, pady=1)
  tk.Button(window, text = map[1][2], bg = back[pos[1][2]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(1, 2)
  ).grid(column=2, row=2, padx=1, pady=1)
  #===========================================
  tk.Button(window, text = map[2][0], bg = back[pos[2][0]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(2, 0)
  ).grid(column=0, row=3, padx=1, pady=1)
  tk.Button(window, text = map[2][1], bg = back[pos[2][1]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(2, 1)
  ).grid(column=1, row=3, padx=1, pady=1)
  tk.Button(window, text = map[2][2], bg = back[pos[2][2]],
    font=('Arial', 28), width = 3, height = 2, command = lambda: action(2, 2)
  ).grid(column=2, row=3, padx=1, pady=1)
  window.update_idletasks()









if __name__ == '__main__':
  window = tk.Tk()
  window.title('puzzle')
  window.geometry('350x350')
  graphic()

  window.mainloop()