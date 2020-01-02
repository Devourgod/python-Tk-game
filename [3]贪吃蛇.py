# 引入TK窗口包
from tkinter import *
# 引入随机数生成包
import random

# 定义变量,画布的列和行
Column = 20
Row = 20
# 每个方块的大小
Size = 35


#蛇身体颜色
Color = 'blue'
# 蛇的身体坐标 最左边是头，最右边是尾
snake = [[2,1],[1,1],[0,1]]
# 蛇的行走方向
direction = 'Down'

# 苹果位置
apple = [5,5]
# 游戏状态
gameState = True
# 记录fps
fps = 0


# 绘制一个设定大小的方块
def drawRect(x,y,color):
    """
    以指定x，y为坐标，画一个长块Size大小的方块
    :param x: 坐标
    :param y: 坐标
    """
    cv.create_rectangle(x*Size,y*Size,Size+x*Size,Size+y*Size,fill=color)

# 绘制地图函数
def drawMap():
    # 循环行画出行
    for i in range(Row):
        # 坐标1为 x：0              y：i * 方块Size
        # 坐标2为 x：列数 * 方块size y：i * 方块Size
        cv.create_line(0, Size*i, Column*Size, Size*i,width = 2)
    # 循环行画出列
    for i in range(Column):
        cv.create_line(Size*i, 0, Size*i, Size*Row,width = 2)
    # 绘制一个大矩形作为边框
    cv.create_rectangle(0,0,Column*Size,Size*Row,width = 2)

def render():
    global fps
    # 当fps过去了50帧则调用一次move移动蛇
    if fps%50==0:
        move()
    fps+=1
    # 如果游戏结束了则退出
    if not gameState:
        return None
    # 每间隔10毫秒执行一次渲染
    root.after(10,render)

def move():
    global snake,X,Y,apple,gameState,Color,direction
    # 清空整个画布 参数为ALL
    cv.delete(ALL)
    # 调用渲染地图方法
    drawMap()
    # 缓存新的蛇身体
    cache = []
    #默认在当前移动过程中没有吃到苹果
    iseat = 1
    if direction == 'Down':
        # 向下移动蛇的头部
        cache.append([snake[0][0],snake[0][1]+1])
    elif direction == 'Left':
        cache.append([snake[0][0]-1,snake[0][1]])
    elif direction == 'Right':
        cache.append([snake[0][0]+1,snake[0][1]])
    elif direction == 'Up':
        cache.append([snake[0][0],snake[0][1]-1])
    # 如果蛇的头部位置等于当前苹果的位置 则表示吃到了苹果
    if cache[0]==apple:
        # 设置成功吃到了苹果
        iseat = 0
        # 随机一个新的苹果坐标
        apple=[random.randint(0,Row-1),random.randint(0,Column-1)]
    if cache[0][0] > Row-1 or cache[0][0]<0 or cache[0][1]>Column-1 or cache[0][1]<0:
        print('撞到了')
        # 改变蛇身体为红色
        Color = 'red'
        # 删除头部缓存
        cache.pop(0)
        # 游戏状态改为结束
        gameState = False
        # 调用判断 如果头部移动的位置有蛇的身体，则游戏结束
    elif arrIsHas(snake,cache[0]):
        Color = 'red'
        cache.pop(0)
        gameState = False
    # 重述肉身 去除数组的尾部 并放入新数组 如果吃到了苹果则不删除尾部
    for k in range(len(snake)-iseat):
        cache.append(snake[k])
    # 把新蛇给snake变量
    snake = cache
    # 绘制苹果
    drawRect(*apple,'red')
    # 绘制蛇的头部
    drawRect(snake[0][0],snake[0][1],'yellow')
    # 遍历蛇身体数组 重新以数组内的坐标渲染蛇的身体
    for k in range(1,len(snake)):
        # 从数组的第1项开始遍历 省略头部
        drawRect(snake[k][0],snake[k][1],Color)

def handle_events(event):
    # event.keysym为按下按键的名称
    global direction,gameState,snake,apple,directio,Color
    if gameState:
        # 如果按下的键为左键 并且 当前方法不为右
        if event.keysym == "Left" and direction!="Right":
            # 设置方向为左并调用move方法移动一次
            direction="Left"
            move()
        elif event.keysym == "Right" and direction!="Left":
            direction="Right"
            move()
        elif event.keysym == "Down" and direction!="Up":
            direction="Down"
            move()
        elif event.keysym == "Up" and direction!="Down":
            direction="Up"
            move()
    # 如果为空格则重新开始
    if event.keysym == "space":
        # 如果当前游戏为暂停状态则执行
        if not gameState:
            # 重新生成蛇
            snake=[[2,1],[1,1],[0,1]]
            # 重新生成一个苹果
            apple=[random.randint(0,Row-1),random.randint(0,Column-1)]
            # 设置游戏开始
            gameState=True
            # 设置方向为下
            direction = 'Down'
            # 设置蛇颜色为blue
            Color = 'blue'
            # 调用刷新函数开始游戏
            render()

# 判断数组内是否包含另一个数组
def arrIsHas(arr1,arr2):
    for v in arr1:
        if v==arr2:
            return True

# 创建Tk窗口
root = Tk()
# 绘制canvas画布，第一个参数是父窗口,然后设置画布的宽度和高度和颜色  宽度为列*块大小  高度为行*高大小
cv = Canvas(root, bg='gray55',width=Column*Size+10, height=Row*Size+10)
# 调用绘制地图方法
drawMap()
# 初始化canvas
cv.pack()
# 调用渲染方法，方法会重新渲染方块的位置和地图 方法每隔100毫秒会自动执行一次
render()
# 绑定监听，如果监听到键盘按下会执行handle_events函数并传入此次事件
root.bind("<Key>", handle_events)
# 运行tk窗口
root.mainloop()
