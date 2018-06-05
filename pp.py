def puzzle():
  ans = False
  bound = 0
  while (not ans and bound <= 200):
    bound = IDAstar(sx, sy, 0, -1, bound, ans)

  if (not ans):
    cout << "200步內無法解得答案"
    return

  for i in range(1, bound):
    cout << command[solution[i]] << ' '
