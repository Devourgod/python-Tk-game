import json
import sys
import random
# pillow 图像处理库 用于图片的旋转、读取和镜像
# 安装指令：pip install pillow
import PIL
from PIL import ImageTk
from tkinter import *

# 游戏主程序
class Game():
    fps = 0
    scores = 0
    isDie = False
    Width = 768
    height = 1024
    pipeList = []
    ScoreList = []

    def __init__(self, title):
        self.root = Tk()
        self.canvas = Canvas(self.root, bg='gray55',width=768, height=1024)
        self.canvas.pack()
        self.background = ImageTk.PhotoImage(file='images/background.png')
        for i in range(0, 9):
            self.ScoreList.append(ImageTk.PhotoImage(
                file='images/'+str(i)+'.png'))
        print('-----图片资源加载完成')

        self.bird = Bird(self.canvas)
        self.earth = earth(self.canvas)  # 地面对象

        self.updata()  # 游戏运行
        # self.root.bind("<Key>", handle_events)
        self.root.bind("<Button-1>", self.mouse_event)
        self.root.mainloop()

    def updata(self):
        #更新 小鸟， 地面 ，管子的数据 并重新渲染
        self.canvas.delete(ALL)
        self.canvas.create_image(0, 0, anchor=NW,image=self.background)
        
        if not self.isDie:
            if self.fps % 120 == 0:
                self.pipeList.append(Pipe(self.canvas))
        self.bird.updata(self.fps)  # 小鸟位置数据更新
        # 遍历管子列表，刷新管子的位置
        for obj in self.pipeList:
            if not self.isDie:
                obj.updata()
            obj.render(self.fps)
            if self.isPengzhuang(self.bird, obj):
                self.isDie = True
        # 遍历管子列表，删除超出地图的管子，如果删除在上面的循环操作会发生渲染问题
        for obj in self.pipeList:
            if obj.isScore and obj.X+obj.Width < self.bird.X:
                obj.isScore = False
                self.scores += 1
            if obj.X < -260:
                self.pipeList.remove(obj)
        # if self.bird.Y < 0 or self.bird.Y > self.height:
        #     self.isDie = True

        self.bird.render(self.fps)  # 小鸟重新渲染在画布
        self.earth.updata()
        self.earth.render()
        self.showScores()
        self.fps += 1  # 增加一个fps
        self.canvas.create_text(0, 0,anchor=NW, text=str(self.fps))  # 渲染fps到0,0坐标
        self.root.after(16, self.updata)
   
    def mouse_event(self,event):
        if not self.isDie:
            self.bird.fly(self.fps)

    # 显示得分
    def showScores(self):
        scoreStr = str(self.scores)
        for i in range(0, len(scoreStr)):
            char = scoreStr[i]
            # 有bug
            if(len(scoreStr) % 2 == 1):
                self.canvas.create_image(
                    self.Width / 2 - 16 * (len(scoreStr)) + 33 * i, 100,anchor=NW, image=self.ScoreList[int(char)])
            else:
                self.canvas.create_image(
                    self.height / 2 - 32 * (len(scoreStr) / 2) + 33 * i, 100,anchor=NW, image=self.ScoreList[int(char)])

    # 矩形碰撞检测
    # 此函数将会获取a,b两个对象的坐标和宽高计算四边的坐标用于判断碰撞条件
    def isPengzhuang(self, a, b):
        t1 = a.Y  # top 这个矩形的顶边
        l1 = a.X  # left 这个矩形的左边
        r1 = a.X + a.Width  # right 这个矩形的右边
        b1 = a.Y + a.Height  # bottom 这个矩形的底边

        # 上面的柱子
        t2 = b.Y
        l2 = b.X
        r2 = b.X + b.Width
        b2 = b.Y + b.Height

        # 下面的柱子
        # 间隔加上面柱子的高度才是自己的Y
        t3 = b.Y + b.Gap + b.Height
        l3 = b.X
        r3 = b.X + b.Width
        b3 = t3 + b.Height

        # 如果矩形1的底高于矩形2的顶说明不可能触碰
        # 如果矩形1的左大于矩形2的右则也不能
        # 诸如此例 top1>bottom2 和  right1<left2 也达成条件
        # and左边是第一个柱子的判断，右边是第二根柱子的判断，两边都需要达成
        if ((b1 < t2 or l1 > r2 or t1 > b2 or r1 < l2) and (b1 < t3 or l1 > r3 or t1 > b3 or r1 < l3)):
            return False
        else:
            return True


class Bird():
    angle = 90
    picX = 0
    X = 100
    Y = 100
    Move = False
    Speed = 0
    isFly = False
    Width = 92
    Height = 64
    step = 0
    list = []

    def __init__(self, canvas):
        self.canvas = canvas
        self.list.append(PIL.Image.open('images/bird1_c1.png'))
        self.list.append(PIL.Image.open('images/bird1_c2.png'))
        self.list.append(PIL.Image.open('images/bird1_c3.png'))

    def fly(self, fps):
        self.isFly = True
        self.angle = 40
        self.flyf = fps
        self.Speed = 8

    def updata(self, fps):
        # 飞行状态
        if self.isFly:
            self.Speed -= 0.3
            self.Y -= self.Speed
            self.angle -= 0.5
            if fps % 3 == 0:
                self.step += 1
                if self.step >= 3:
                    self.step = 1
            if fps-self.flyf > 60:  # 开启飞行后的帧数大于35则关闭飞行状态
                self.isFly = False
                self.Speed = 0  # 恢复加速度
                self.step = 0  # 恢复图片为第一张
        # 非飞行状态
        else:
            self.Speed += 0.5
            self.Y += self.Speed
            self.angle -= 3

    def render(self, fps):
        
        self.ratateImg = ImageTk.PhotoImage(self.list[self.step].rotate(self.angle,expand=True))
        self.canvas.create_image(self.X, self.Y, anchor=NW,image=self.ratateImg)


class earth():
    X = 0
    Width = 37

    def __init__(self, canvas):
        self.canvas = canvas
        self.ground = ImageTk.PhotoImage(file='images/ground.png')
    def updata(self):
        self.X += 4
        if self.X > 37:
            self.X = 0
    def render(self):
        for i in range(0, 26):
            self.canvas.create_image(i*37-self.X, 896, anchor=NW,image=self.ground)


class Pipe():
    X = 768+260
    Y = 0
    top = 20
    Speed = 4  # 管子向左的速度
    Gap = 260  # 管子间间隙有260像素
    Width = 138
    Height = 793
    isScore = True

    def __init__(self, canvas):
        self.canvas = canvas
        self.pipeImage = PIL.Image.open('images/pipe.png')
        self.pipeBottom = ImageTk.PhotoImage(self.pipeImage)
        self.pipeTop = ImageTk.PhotoImage(
            self.pipeImage.transpose(PIL.Image.FLIP_TOP_BOTTOM))
        self.Y = -793 + random.randint(60, 450)  # 随机一个管子间隙的高度

    def updata(self):
        self.X -= self.Speed

    def render(self, fps):
        guanzi1 = self.canvas.create_image(self.X, self.Y, anchor=NW,image=self.pipeTop)
        guanzi2 = self.canvas.create_image(
            self.X, self.Y+self.Gap+793, anchor=NW,image=self.pipeBottom)


if __name__ == '__main__':
    Game('flappyBird')
