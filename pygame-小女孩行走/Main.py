import pygame
import sys

class Game():
    fps = 0
    def __init__(self,title):
        pygame.init()  # 初始化pygame
        pygame.display.set_caption(title)
        self.size = width, height = 640, 640  # 设置窗口大小
        self.screen = pygame.display.set_mode(self.size)  # 显示窗口
        back = pygame.image.load('resource/background.png')
        
        backrect = back.get_rect()
        self.girl = Girl()
        print(backrect)
        clock=pygame.time.Clock()
        while True:  # 死循环确保窗口一直显示
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
                self.keyif(event)
            self.screen.blit(back, backrect)
            self.girl.grilMoving(self.fps); #调用小女孩移动刷新
            self.screen.blit(self.girl.girlimg, (self.girl.girlX, self.girl.girlY), (self.girl.girlWidth*self.girl.girlpicX,self.girl.girlHeight*self.girl.girlpicY , self.girl.girlWidth, self.girl.girlHeight))
            pygame.display.update()  # 把画好的画布显示在页面上
            self.fps+=1
            clock.tick(60)
        pygame.quit()

    def keyif(self,event):
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.girl.girlMove = True
                self.girl.girldirection = 'top'
                self.girl.girlpicY = 3
            if event.key == pygame.K_DOWN:
                self.girl.girlMove = True
                self.girl.girldirection = 'down'
                self.girl.girlpicY = 0
            if event.key == pygame.K_LEFT:
                self.girl.girlMove = True
                self.girl.girldirection = 'left'
                self.girl.girlpicY = 1
            if event.key == pygame.K_RIGHT:
                self.girl.girlMove = True
                self.girl.girldirection = 'right'
                self.girl.girlpicY = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if self.girl.girldirection == 'down':
                    self.girl.girlMove = False
            if event.key == pygame.K_LEFT:
                if self.girl.girldirection == 'left':
                    self.girl.girlMove = False
            if event.key == pygame.K_RIGHT:
                if self.girl.girldirection == 'right':
                    self.girl.girlMove = False
            if event.key == pygame.K_UP:
                if self.girl.girldirection == 'top':
                    self.girl.girlMove = False

class Girl():
    girlpicX = 0
    girlpicY = 0
    girlX = 100
    girlY =100
    girlMove = False
    girlSpeed = 3
    girldirection = 'left'
    girlWidth = 79
    girlHeight = 864 / 8
    def __init__(self):
        self.girlimg = pygame.image.load('resource/girl.png')
        print('成功')

    def grilMoving(self,fps): #移动函数，每帧都会调用
        if self.girlMove: #是否在移动状态
            if self.girldirection=='left': 
                self.girlX-=self.girlSpeed #依据速度和方向加减人物位置
            elif self.girldirection=='right':
                self.girlX+=self.girlSpeed 
            elif self.girldirection=='down':
                self.girlY+=self.girlSpeed 
            elif self.girldirection=='top':
                self.girlY-=self.girlSpeed 
            if(fps % 5 == 0):
                self.girlpicX+=1
                if(self.girlpicX>7):
                    self.girlpicX=0

if __name__ == "__main__":
    Game('flappy')
