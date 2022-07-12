import pygame
import math


pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('PyBall')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

fps = 100
clock = pygame.time.Clock()



def vec_len(vec: list):
    summ = 0
    for coord in vec:
        summ+=coord**2
    return math.sqrt(summ)


def dist(a: list, b:list):
    vec = []
    for i in range(len(a)):
        vec.append(b[i] - a[i])
    return vec_len(vec)


def plus_vec(veca: list, vecb: list):
    return [vecb[i] + veca[i] for i in range(len(veca))]


def get_vec(a: list, b: list):
    return [b[i] - a[i] for i in range(len(a))]

def norm_vec(vec: list):
    length = vec_len(vec)
    return [vec[i]/length for i in range(len(vec))]


class Mouse:
    def __init__(self):
        self.prev_pos = pygame.mouse.get_pos()
        self.pos = list(pygame.mouse.get_pos())
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.speed = 0
        self.vec = [0, 0]

    def update(self):
        self.prev_pos = self.pos
        self.pos = pygame.mouse.get_pos()
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.vec = [self.x - self.prev_pos[0], self.y - self.prev_pos[1]]
        self.speed = vec_len(self.vec) * 0.1




class Ball:
    def __init__(self):
        self.x = screenWidth/2
        self.y = screenHeight/2
        self.pos = [self.x, self.y]
        self.dir = [0, 0]
        self.speed = 0
        self.color = BLACK
        self.width = 1
        self.radius = 20
        self.max_speed = 300



    def gravity(self):
        if self.y + self.radius < screenHeight:
            gravity_vec = [0, 0.3]
            #self.speed += 0.01
            self.dir = plus_vec(self.dir, gravity_vec)


    def move(self, mouse: Mouse):
        self.collide_walls()
        self.collide_mouse(mouse)
        # self.gravity()
        self.push(self.dir[0] * self.speed, self.dir[1] * self.speed)
        self.speed -= 0.007
        if self.speed < 0: self.speed = 0


    def push(self, x: float, y: float):
        self.x += x
        self.y += y
        if self.x + self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > screenWidth:
            self.x = screenWidth - self.radius
        if self.y + self.radius < 0:
            self.y = self.radius
        if self.y + self.radius > screenHeight:
            self.y = screenHeight - self.radius


        self.pos = [self.x, self.y]


    def collide_mouse(self, mouse: Mouse):
        if dist(mouse.pos, self.pos) <= self.radius:
            move_vec = plus_vec(get_vec(mouse.pos, self.pos), mouse.vec)
            self.dir = norm_vec(move_vec)
            self.speed += mouse.speed * 1

    def collide_walls(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= screenWidth:
            self.dir[0] *= -1
            self.speed -= 0.5
        if self.y - self.radius <= 0 or self.y + self.radius >= screenHeight:
            self.dir[1] *= -1
            self.speed -= 0.5



    def show(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius, self.width)
        try:
            img = pygame.image.load('ball.png')
            img = pygame.transform.scale(img, (2 * (self.radius+2), 2 * (self.radius+2)))
            screen.blit(img, [self.x - img.get_width()/2, self.y - img.get_height()/2])
        except: pass



class Game:
    def __init__(self):
        self.ball = Ball()
        self.mouse = Mouse()

    def tick(self):
        self.ball.show()
        self.mouse.update()
        self.ball.move(self.mouse)




    def start(self):
        running = True
        while running:
            clock.tick(fps)
            screen.fill(WHITE)



            self.tick()


            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False






if __name__ == '__main__':
    game = Game()
    game.start()








