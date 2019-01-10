#游戏可视化设计，
#1、包括创建图形4*4网格规划设计、
#2、滑块大小、形状、颜色、数字等设计(李晓宁)
import pygame, sys, random
from pygame.locals import *
#创建一个图形优化的常量以便后期使用
#列数，行数，框占比，游戏整个长，宽，图形刷新的帧数,是否有空白
BOARDWIDTH = 4
BOARDHEIGHT = 4          #游戏的行列
TILESIZE   = 80         #格子的大小
WINDOWWIDTH = 640       #整个游戏的宽
WINDOWHEIGHT = 480      #整个游戏的高
FPS=30                  #刷新常数
BLANK=None              #空白
#颜色常量的定义
BLACK =         (  0,   0,   0)#黑
WHITE =         (255, 255, 255)#白
BRIGHTBLUE =    (  0,  50, 255)#亮蓝色
DARKTURQUOISE = (  3,  54,  73)#暗绿色
GREEN =         (  0, 204,   0)#绿
red =         (255,   0,   0)#红
#组件颜色的定义
BGCOLOR = DARKTURQUOISE #背景颜色暗绿色
TILECOLOR = GREEN       #格子和文字背景颜色#绿
TEXTCOLOR = WHITE       #文字颜色
BORDERCOLOR = BRIGHTBLUE#边界颜色亮蓝色
BASICFONTSIZE = 20      #初始字体大小
MESSAGECOLOR = WHITE    #提示消息的颜色
#整个游戏内部操作图形位置的计算
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
#按钮上下左右的定义
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
#主函数
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
     #全局变量基本字体
    pygame.init()
     #初始化pygame
    FPSCLOCK = pygame.time.Clock()
     #创建一个对象来帮助跟踪时间
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
     #生成主屏幕screen；第一个参数是屏幕大小，第二个0表示不使用特性
    pygame.display.set_caption('Slide Puzzle')
     #左上角题目
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
     #干净浑厚的英文粗体字体

     #主界面的按钮布局
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
     #重置游戏
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
     #重新开始
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
     #解答游戏

     #生成新品图部分
    mainBoard, solutionSeq = generateNewPuzzle(80)
     #获得启动板块状态
    SOLVEDBOARD = getStartingBoard()
     #存储坐标的列表
    while True: # 主游戏循环
        #slideTo = None # 方向如果有的话画片移动
        msg = '单击“平铺”或按箭头键滑动.' # 包含要在左上角显示的消息。
        #if mainBoard == SOLVEDBOARD:
            #msg = 'Solved!'
        drawBoard(mainBoard, msg)#画板函数
        checkForQuit()#退出检测函数
       
        #if slideTo:
            #slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
            #makeMove(mainBoard, slideTo)
            #allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)
#退出游戏和系统
def terminate():
    pygame.quit()
    sys.exit()
#退出检测函数
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present  
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
#按钮位置制作专用函数
'''
@param text  文本名
@param color 颜色
@param bgcolor 背景颜色
@param top 顶端距离
@param left 左端距离
@return 文本状态和矩形
'''
def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)#文字字体,是否开启抗锯齿（就是是否平滑）,颜色,别境颜色
    textRect = textSurf.get_rect()#返回一个矩形外框
    textRect.topleft = (top, left)#定义高和宽
    return (textSurf, textRect)
'''
@return 返回启动版内部的二维列表信息类似[[1，4，7]，[2，5，8]，[3，6，空白]]
'''
def getStartingBoard():
    #返回画板的数据结构，其中画板处于完成状态。.
    # 例如，如果BoardWidth和BoardHeight均为3，则此函数
    # 返回[[1，4，7]，[2，5，8]，[3，6，空白]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board
'''
画滑片
@param tilex   画片的位置
@param tiley   画片的位置
@param number
@param adjx  滑片的相对位置
@param adjy  滑片的相对位置
'''
def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)
'''
@param  tileX
@param  tileY
return  left,top

'''
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top  =  YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)
'''
画板的创建
'''
def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left -5, top -5, width + 11, height + 11),4)
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
'''
生成拼图
'''
def generateNewPuzzle(numSlides):
    sequence=[]
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    return (board, sequence)
