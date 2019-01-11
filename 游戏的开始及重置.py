 # 音乐播放代码
pygame.mixer.init() 
track1=pygame.mixer.music.load("a.mp3")  
pygame.mixer.music.play()
#游戏成功的判断
if mainBoard == SOLVEDBOARD:
            msg = '成功!'

'''
@获得新拼图状态
@param numSlides 随机改变滑片的次数
@return (board, sequence) 随机后的坐标列表
'''
def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlFAnd
    # animate these moves).
    sequence = []
    board = getStartingBoard()#获得初始化滑板
    drawBoard(board, '')#画滑板
    pygame.display.update()#刷新界面
    pygame.time.wait(500) # 暂停500ms以达到滑动效果
    lastMove = None         #定义变量记录最后一次移动
    for i in range(numSlides):#循环随机次数
        move = getRandomMove(board, lastMove)#随机移动函数
        slideAnimation(board, move, '拼图生成中。。。。', animationSpeed=int(TILESIZE / 3))#动画设置
        makeMove(board, move)#移动函数
        sequence.append(move)#添加到列表,变成二维列表
        lastMove = move     
    return (board, sequence)   #返回滑板，和二维列表

'''
@重置函数，将滑块初始到人员操作前的状态
@param board 记录类似[[1, 5, 9, 13], [6, 11, 15, 10], [2, 7, 8, 12], [3, 4, None, 14]]
@param allMoves 记录的是初始到人员操作时的记录列表步骤
'''
def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # 列表的复制
    revAllMoves.reverse()#反转列表

    for move in revAllMoves:#返现操作回到最初
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))#滑动的动画效果
        makeMove(board, oppositeMove)#做具体的移动
