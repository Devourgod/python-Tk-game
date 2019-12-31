# 引入TK窗口包
from tkinter import *
# 引入随机数生成包
import random

# 定义变量,画布的列和行
Column = 10
Row = 25
# 每个方块的大小
Size = 35

# TK()方法用于创建主窗口
root = Tk()

# 方块模板 可以依据模板渲染出方块
fangKuai = [
        [
            [0, 1, 0],
            [1, 1, 1],
            [1, 1, 1]
        ],
        [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],

        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
    ]


# 储存当前的方块
nowFangkuai = fangKuai[random.randint(0,len(fangKuai)-1)]
# 储存正在移动的方块坐标
nowX = 0
nowY = 0
# 是否处于碰撞状态
isStop = False


# 创建地图数组
map = []
# 建立地图
# 循环Row行次
for i in range(Row):
    # 推入一个空列表
    map.append([])
    # 循环Column列次
    for x in range(Column):
        # 推入代表 此处没有方块的标识 ‘0’
        map[i].append(0)

# 绘制一个设定大小的方块
def drawRect(x, y):
    """
    以指定x，y为坐标，画一个长块Size大小的方块
    :param x: 坐标
    :param y: 坐标
    """
    cv.create_rectangle(x*Size, y*Size, Size+x*Size, Size+y*Size, fill='blue')

# 绘制地图函数
def drawMap():
    # 绘制一个大矩形作为边框
    cv.create_rectangle(0, 0, Column*Size, Size*Row, width=2)
    # 循环行画出线条
    for i in range(Row):
        # 坐标1为 x：0              y：i * 方块Size
        # 坐标2为 x：列数 * 方块size y：i * 方块Size
        cv.create_line(0, Size*i, Column*Size, Size*i, width=2)
    for i in range(Column):
        cv.create_line(Size*i, 0, Size*i, Size*Row, width=2)
    # 遍历地图，如果遍历到的坐标有方块则绘制方块
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 1:
                # 绘制当前坐标方块
                drawRect(x, y)

# 重新渲染函数
def render():
    global nowX, nowY, nowFangkuai, map,isStop
    # 清空整个画布 参数为ALL
    cv.delete(ALL)
    # 调用渲染地图方法
    drawMap()
    # 遍历方块的每个坐标绘出方块
    for y in range(len(nowFangkuai)):
        for x in range(len(nowFangkuai[y])):
            # 如果方块的坐标有方块 则渲染这个坐标的方块
            if nowFangkuai[y][x] == 1:
                # 绘制一个方块
                drawRect(x+nowX, y+nowY)
                # 检测是否为碰撞状态
                if isStop:
                    # 如果到底了，则绘制这个坐标到地图上 地图就会存在当前位置的方块
                    map[y + nowY][x + nowX] = 1
    # 如果到底了则重新生成方块并重置坐标
    if isStop:
        # 重置坐标
        nowX = 0
        nowY = 0
        # 重新随机一个方块模板
        nowFangkuai = fangKuai[random.randint(0,len(fangKuai)-1)]
        # 执行消除判断
        xiaochu()
    # 停止标识设回False
    isStop = False
    # 每隔100毫秒重新渲染一次方块和地图

# 移动方块整体向下一格函数
def moveDown():
    global nowX, nowY, nowFangkuai, map,isStop
    # 检测是否可能会碰撞
    isStop = isPengzhuang(0, +1,nowFangkuai)
    # 如果没有碰撞则向下移动
    if not isStop:
        nowY += 1
    # 调用后立即渲染
    render()
    # 每隔500毫秒调用一次自己
    root.after(500, moveDown)

# 碰撞检测函数
def isPengzhuang(addx, addy, arr):
    """
    依据增量模拟位移方块，判断是否碰撞，碰撞则return True
    :param addx: x轴增量
    :param addy: y轴增量
    """
    # 遍历模板的每个方块
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            # 如果模板当前坐标有方块则进行判断
            if arr[y][x] == 1:
                # 判断此方块移动位置是否可能超出地图
                if y + nowY+addy >= Row or y + nowY+addy < 0 or x+nowX+addx >= Column or x+nowX+addx < 0:
                    return True
                # 判断此方块移动位置是否已经有方块
                elif map[y+nowY+addy][x+nowX+addx] == 1:
                    return True
    # 如果没有碰撞到就返回False
    return False

# 消除完成的行函数
def xiaochu():
    global map
    # 遍历地图每一行
    for y in range(len(map)):
        # 设置默认状态为成功消除这一行
        succeed = True
        # 遍历行中的每一项
        for x in range(len(map[y])):
            # 如果这一项为0则不成功消除
            if map[y][x]==0:
                # 设为未成功消除
                succeed = False
        # 如果这一行都是方块而没有空则执行删除
        if succeed:
            # 创建一个新地图列表
            newMap = []
            # 创建一个空行 
            noneRow = []
            for k in range(Column):
                noneRow.append(0)
            # 推入一个空行在新地图顶部
            newMap.append(noneRow)
            # 遍历老地图 把老地图里没有消除的行推入新地图
            for i in range(len(map)):
                # 如果不是老地图要被消除的那一行就推入新数组
                if i!=y:
                    newMap.append(map[i])
            map = newMap
            print('得分！！！')

# 键盘监听事件回调
def handle_events(event):
    global nowX,nowY,nowFangkuai
    # event.keysym为按下按键的名称
    if event.keysym == "Left":
        # 如果是左键，则调用是否碰撞方法 传入位移的值和需要检测的方块
        if not isPengzhuang(-1, 0,nowFangkuai):
            # 如果没有碰撞则移动方块
            nowX -= 1
    elif event.keysym == "Right":
        if not isPengzhuang(1, 0,nowFangkuai):
            nowX += 1
    elif event.keysym == "Down":
        if not isPengzhuang(0, 1,nowFangkuai):
            nowY += 1
    elif event.keysym == "Up":
        # 如果按下了上键则旋转方块
        arr = []
        # 循环遍历第一行的长度
        for x in range(len(nowFangkuai[0])):
            # 缓存一行列表
            cache = []
            # 遍历 i 长度为方块数组的长度
            for i in range(len(nowFangkuai)):
                # 插入 第i行的第x个到新列表的头部
                cache.insert(0,nowFangkuai[i][x])
            # 把这一行加入新列表中
            arr.append(cache)
        # 检测新的方块是否和地图有碰撞
        if not isPengzhuang(0, 0,arr):
            # 没有碰撞则改变现状的方块为新方块
            nowFangkuai = arr
    render()

# 创建canvas对象
cv = Canvas(root, bg='gray55', width=Column*Size+50, height=Row*Size+50)
# 初始化canvas
cv.pack()
# 调用渲染方法，方法会重新渲染方块的位置和地图 方法每隔100毫秒会自动执行一次
render()
# 调用方块下移方法，方法会下移方块一格，执行后会每隔500毫秒自动执行一次
moveDown()
# 绑定监听，如果监听到键盘按下会执行handle_events函数并传入此次事件
root.bind("<Key>", handle_events)
# 运行tk窗口
root.mainloop()