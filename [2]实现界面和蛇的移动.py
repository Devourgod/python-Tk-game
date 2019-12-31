# 引入TK窗口包
from tkinter import *

# 定义变量,画布的列和行
Column = 20
Row = 20
# 每个方块的大小
Size = 35
# 记录fps
fps = 0

# 蛇的身体坐标 最左边是头，最右边是尾
snake = [[2,1],[1,1],[0,1]]
#蛇的方向
direction = 'Down'

# TK()方法用于创建主窗口
root = Tk()
# 绘制canvas画布，第一个参数是父窗口,然后设置画布的宽度和高度和颜色  宽度为列*块大小  高度为行*高大小
cv = Canvas(root, bg='gray55',width=Column*Size+10, height=Row*Size+10)

# 画方块方法
def drawRect(x,y):
    """
    以指定x，y为坐标，画一个长块Size大小的方块
    :param x: 坐标
    :param y: 坐标
    """
    cv.create_rectangle(x*Size,y*Size,Size+x*Size,Size+y*Size,fill='blue')

def drawMap():
     # 循环行画出行
    for i in range(Row):
        # 坐标1为 x：0              y：i * 方块Size
        # 坐标2为 x：列数 * 方块size y：i * 方块Size
        cv.create_line(0, Size*i, Column*Size, Size*i,width = 2)
    # 循环列画出列
    for i in range(Column):
        cv.create_line(Size*i, 0, Size*i, Size*Row,width = 2)
    # 绘制一个大矩形作为边框
    cv.create_rectangle(0,0,Column*Size,Size*Row,width = 2)

# 刷新方法 每10毫米
def render():
    global fps
    # 当fps过去了50帧则调用一次move移动蛇
    if fps%50==0:
        move()
    fps+=1
    # 每间隔10毫秒执行一次渲染
    root.after(10,render)
def move():
    global snake,X,Y
    # 清空整个画布 参数为ALL
    cv.delete(ALL)
    # 调用渲染地图方法
    drawMap()
    # 缓存新的蛇身体
    cache = []
    if direction == 'Down':
        # 向下移动蛇的头部
        cache.append([snake[0][0],snake[0][1]+1])
    if direction == 'Left':
        cache.append([snake[0][0]-1,snake[0][1]])
    if direction == 'Right':
        cache.append([snake[0][0]+1,snake[0][1]])
    if direction == 'Up':
        cache.append([snake[0][0],snake[0][1]-1])
    # 重述肉身 去除数组的尾部 并放入新数组
    for k in range(len(snake)-1):
        cache.append(snake[k])
    snake = cache
    # 遍历蛇身体数组 重新以数组内的每一个坐标数组渲染贪吃蛇
    for v in snake:
        drawRect(v[0],v[1])

# 键盘监听事件回调
def handle_events(event):
    global direction
    if event.keysym == "Left" and direction!="Right":
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