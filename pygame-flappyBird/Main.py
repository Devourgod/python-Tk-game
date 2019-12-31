import json
import pygame
import sys
import random

class Game():
    fps = 0
    scores = 0
    isDie = False
    Width = 768
    height = 1024
    pipeList = []
    ScoreList = []
    def __init__(self, title):
        self.background = pygame.image.load('images/background.png')
        for i in range(0,9):
            self.ScoreList.append(pygame.image.load('images/'+str(i)+'.png'))

        print('-----图片资源加载完成')
        pygame.init()  # 初始化pygame
        pygame.display.set_caption(title)  # 设置标题
        self.size = width, height = 768, 1024  # 设置窗口大小
        self.screen = pygame.display.set_mode(self.size)  # 显示窗口
        self.backrect = self.background.get_rect()  # 获取背景图片尺寸的 rect
        self.bird = Bird(self.screen)
        self.earth = earth(self.screen) #地面对象
        self.font =  pygame.font.SysFont('microsoft Yahei',30)
        self.state() # 游戏运行
        

    def state(self):
        clock = pygame.time.Clock()
        while True:  # 死循环确保窗口一直显示
            #事件判断
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
                if not self.isDie:
                    if event.type == pygame.MOUSEBUTTONDOWN: # 如果鼠标单击，则飞行
                        self.bird.fly(self.fps)

            #更新 小鸟， 地面 ，管子的数据 并重新渲染
            self.screen.blit(self.background, self.backrect)
            self.earth.updata()
            self.earth.render()
            if not self.isDie:
                if self.fps % 70 == 0:
                    self.pipeList.append(Pipe(self.screen))
            self.bird.updata(self.fps)  # 小鸟位置数据更新
            #遍历管子列表，刷新管子的位置
            for obj in self.pipeList:
                if not self.isDie:
                    obj.updata()
                obj.render(self.fps)
                if self.isPengzhuang(self.bird,obj):
                    self.isDie = True
            #遍历管子列表，删除超出地图的管子，如果删除在上面的循环操作会发生渲染问题
            for obj in self.pipeList:
                if obj.isScore and obj.X+obj.Width<self.bird.X:
                    obj.isScore = False
                    self.scores+=1
                if obj.X < -260:
                        self.pipeList.remove(obj)
            if self.bird.Y<0 or self.bird.Y>self.height:
                self.isDie=True

            self.bird.render(self.fps)  # 小鸟重新渲染在画布
            
            self.showScores()
            self.fps += 1  # 增加一个fps
            surface = self.font.render(str(self.fps),False,(255,200,10)) #使用font和创建文字对象显示 当前已经过去时间的fps
            self.screen.blit(surface,(0,0)) #渲染文字到0,0坐标
            pygame.display.update()  # 把画好的画布显示在页面上
            clock.tick(60)  # 设置帧率，这个while循环会在一秒钟执行(帧率)次
        pygame.quit()

    def showScores(self):
        scoreStr = str(self.scores);
        for i in range(0,len(scoreStr)):
            char = scoreStr[i];
            if(len(scoreStr) % 2 == 1):
                self.screen.blit(self.ScoreList[int(char)], (self.Width / 2 - 16 * (len(scoreStr)) + 33 * i, 100), self.ScoreList[int(char)].get_rect());
            else:
                self.screen.blit(self.ScoreList[int(char)], (self.height / 2 - 32 * (len(scoreStr) / 2) + 33 * i, 100), self.ScoreList[int(char)].get_rect());

    # 矩形碰撞检测
    # 此函数将会获取a,b两个对象的坐标和宽高计算四边的坐标用于判断碰撞条件
    def isPengzhuang(self,a, b):
        t1 = a.Y;   #top 这个矩形的顶边
        l1 = a.X;   #left 这个矩形的左边
        r1 = a.X + a.Width;  #right 这个矩形的右边
        b1 = a.Y + a.Height; #bottom 这个矩形的底边

        #上面的柱子
        t2 = b.Y;
        l2 = b.X;
        r2 = b.X + b.Width;
        b2 = b.Y + b.Height;

        #下面的柱子
        # 间隔加上面柱子的高度才是自己的Y
        t3 = b.Y + b.Gap + b.Height;
        l3 = b.X;
        r3 = b.X + b.Width;
        b3 = t3 + b.Height;

        # 如果矩形1的底高于矩形2的顶说明不可能触碰
        # 如果矩形1的左大于矩形2的右则也不能
        # 诸如此例 top1>bottom2 和  right1<left2 也达成条件 
        # and左边是第一个柱子的判断，右边是第二根柱子的判断，两边都需要达成
        if ((b1<t2 or l1>r2 or t1>b2 or r1<l2 ) and (b1<t3 or l1>r3 or t1>b3 or r1<l3)): 
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

    def __init__(self, screen):
        self.screen = screen
        self.list.append(pygame.image.load('images/bird1_c1.png'))
        self.list.append(pygame.image.load('images/bird1_c2.png'))
        self.list.append(pygame.image.load('images/bird1_c3.png'))

    def fly(self, fps):
        self.isFly = True
        self.angle = 40
        self.flyf = fps
        self.Speed = 12

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
            if fps-self.flyf > 18:  # 开启飞行后的帧数大于35则关闭飞行状态
                self.isFly = False
                self.Speed = 0  # 恢复加速度
                self.step = 0  # 恢复图片为第一张
        # 非飞行状态
        else:
            self.Speed += 0.9
            self.Y += self.Speed
            self.angle -= 3

    def render(self, fps):
        # self.ratateImg = pygame.transform.scale(self.list[self.step],(46,32))
        self.ratateImg = pygame.transform.rotate(self.list[self.step], self.angle)
        self.screen.blit(self.ratateImg, (self.X, self.Y),self.ratateImg.get_rect())

class earth():
    X = 0
    Width = 37
    def __init__(self,screen):
        self.screen=screen
        self.ground = pygame.image.load('images/ground.png')
    def updata(self):
        self.X +=8
        if self.X >37:
            self.X =0
    def render(self):
        for i in range(0,26):
            self.screen.blit(self.ground, (i*37-self.X, 896), self.ground.get_rect())

class Pipe():
    X = 768+260
    Y = 0
    top = 20
    Speed = 8 #管子向左的速度
    Gap = 260 #管子间间隙有260像素
    Width = 138
    Height = 793
    isScore = True

    def __init__(self, screen):
        self.screen = screen
        self.pipeBottom = pygame.image.load('images/pipe.png')
        self.pipeTop = pygame.transform.flip(self.pipeBottom,False,True)
        self.Y = -793+random.randint(60,450) #随机一个管子间隙的高度

    def updata(self):
        self.X-=self.Speed
        
    def render(self, fps):
        self.screen.blit(self.pipeTop, (self.X, self.Y), self.pipeTop.get_rect())
        self.screen.blit(self.pipeBottom, (self.X, self.Y+self.Gap+793), self.pipeBottom.get_rect())


if __name__ == '__main__':
    Game('flappyBird')
