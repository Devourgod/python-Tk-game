# 引入TK窗口包
from tkinter import *

# 定义变量,画布的列和行
Column = 20
Row = 20
# 每个方块的大小
Size = 35


# 画方块方法
def drawRect(x,y):
    """
    以指定x，y为坐标，画一个长块Size大小的方块
    :param x: 坐标
    :param y: 坐标
    """
    # 以坐标乘于方块大小得出真实坐标
    # 真实坐标加上一个方格高度和宽度得到第二个坐标
    x1 = x*Size
    y1 = y*Size
    x2 = x*Size+Size
    y2 = y*Size+Size
    cv.create_rectangle(x1,y2,x2,y2,fill='blue')


# 绘制出地图
def drawMap():
    # 绘制一个大矩形作为边框
    cv.create_rectangle(0, 0, Column*Size, Size*Row, width=2)
    # 循环行画出行
    for i in range(Row):
        # 坐标1为 x：0              y：i * 方块Size
        # 坐标2为 x：列数 * 方块size y：i * 方块Size
        cv.create_line(0, Size*i, Column*Size, Size*i,width = 2)
    # 循环列画出列
    for i in range(Column):
        cv.create_line(Size*i, 0, Size*i, Size*Row,width = 2)
# TK()方法用于创建主窗口
root = Tk()
# 绘制canvas画布，第一个参数是父窗口,然后设置画布的宽度和高度和颜色
# 它用于绘制图片和其他复杂的布局，如图形、文本和小部件。
cv = Canvas(root, bg='gray55',width=Column*Size+10, height=Row*Size+10)
# 调用绘制地图方法
drawMap()
#调用绘制方块方法在1,1位置绘制方块
drawRect(1,1)
drawRect(2,3)
# 初始化canvas
cv.pack()
# 运行tk窗口
root.mainloop()
