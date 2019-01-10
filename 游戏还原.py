# 游戏还原即 将用户和系统初始的移动倒序执行一遍即可
# 当点击 解答游戏按钮时 将 系统初始步骤 和 用户自己修改的步骤 叠加起来
SOLVE_RECT.collidepoint(event.pos):
  sovleAnimation(mainBoard, solutionSeq , allMoves) # 
  allMoves = []
  
 # 解答游戏函数 
def sovleAnimation(board, squence, allMoves):
  revAllMoves = squence + allMoves # 将两个步骤数组合并
  revAllMoves.reverse() # 倒置

  for move in revAllMoves: #一次按倒序的内容执行
      if move == UP:
          oppositeMove = DOWN
      elif move == DOWN:
          oppositeMove = UP
      elif move == RIGHT:
          oppositeMove = LEFT
      elif move == LEFT:
          oppositeMove = RIGHT
      slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2)) # 添加滑动的效果
      makeMove(board, oppositeMove) #做滑动
