# 在 main() 里边 循环监听事件
for event in pygame.event.get(): # 事件处理循环
            if event.type == MOUSEBUTTONUP: # 事件为鼠标点击事件
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                  '''
                getSpotClicked 通过循环遍历border 判断点击的坐标是否在border内 
                            在
                            -> 返回在border 二维数组里边的坐标
                            不在
                            -> 返回 (None, None)
                '''
          
                if (spotx, spoty) == (None, None):
                    # 检查用户是否点击了 按钮 若点击的
                    if RESET_RECT.collidepoint(event.pos): # 点击重置按钮
                        resetAnimation(mainBoard, allMoves) # 调用重置的方法
                        allMoves = [] # 存储的是用户自己的移动  重置时应置为空
                    elif NEW_RECT.collidepoint(event.pos): # 点击重新开始
                        mainBoard, solutionSeq = generateNewPuzzle(80) #重新调用初始移动的函数
                        allMoves = [] # 置为空
                    elif SOLVE_RECT.collidepoint(event.pos):
                        sovleAnimation(mainBoard, solutionSeq , allMoves) # clicked on Solve button
                        allMoves = []
                else:
                    # 检查点击的滑块是否在空缺的旁边
                    # 如果在孔雀旁边 则记录滑动方向 slideTo
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP: # 事件为键盘事件
                # 检查用户是否通过按键滑动滑块
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo: 
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # 
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # 记录移动步骤
        pygame.display.update() # 刷新
        FPSCLOCK.tick(FPS) #动画每秒的桢数 控制帧速率

def makeMove(board, move):
    # 做具体的滑动
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]



def isValidMove(board, move): # 判断是否是非法移动
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)




def slideAnimation(board, direction, message, animationSpeed):
    # Note: 此函数不检查移动是否有效，在执行此函数之前就已经判断过移动是否有效

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # 准备一个模板 用来覆盖原版制作动画效果
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # 在模板上的移动滑块并绘制空白区域.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
    
    # 通过不断循环覆盖来制作移动效果
    for i in range(0, TILESIZE, animationSpeed):
        # 动画平铺滑动
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getSpotClicked(board, x, y):
    # 从X和Y像素坐标中，获取X和Y在列表中的坐标
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            print(tileRect.collidepoint(x, y))
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

