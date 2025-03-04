import pygame
import sys
import random
from bg_from import new_bg

# 全局定义
SCREEN_X = 800
SCREEN_Y = 600
# 蛇类
class Snake(object):
    def __init__(self):
        self.target_direction = pygame.K_RIGHT
        self.direction = pygame.K_RIGHT
        self.speed = 4
        self.body = []
        for x in range(10):
            self.addnode()

    def addnode(self):
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 20, 20)
        if self.direction == pygame.K_LEFT:
            node.left -= self.speed
        elif self.direction == pygame.K_RIGHT:
            node.left += self.speed
        elif self.direction == pygame.K_UP:
            node.top -= self.speed
        elif self.direction == pygame.K_DOWN:
            node.top += self.speed
        self.body.insert(0, node)

    def delnode(self):
        self.body.pop()

    def isdead(self):
        # 撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False
    def show_po(self):
        return self.body[0].left , self.body[0].top

    def move(self):
        self.addnode()
        self.delnode()

    def check_turn(self):
        head = self.body[0]
        if head.top%20 == 0 and head.left%20 == 0:
            self.direction = self.target_direction

    def change_direction(self, new_direction):
        if new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.target_direction = pygame.K_LEFT
        elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.target_direction = pygame.K_RIGHT
        elif new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.target_direction = pygame.K_UP
        elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.target_direction = pygame.K_DOWN
# 食物类
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-20, 0, 20, 20)
        self.allposx = []
        self.allposy = []
        for pos in range(20, SCREEN_X - 20, 20):
            self.allposx.append(pos)
        for pos in range(20, SCREEN_Y - 20, 20):
            self.allposy.append(pos)

    def remove(self):
        self.rect.x = -20

    def set(self, snake_body):
        if self.rect.x == -20:
            while True:
                self.rect.left = random.choice(self.allposx)
                self.rect.top = random.choice(self.allposy)
                if not any(self.rect.colliderect(part) for part in snake_body):
                    break
            print(self.rect)

class Obstacle:
    def __init__(self):
        self.allposx = []
        self.allposy = []
        self.rect = pygame.Rect(-20, 20, 20, 20)
        for pos in range(0, SCREEN_X - 20, 20):
            self.allposx.append(pos)
        for pos in range(0, SCREEN_Y - 20, 20):
            self.allposy.append(pos)

    def remove(self):
        self.rect.x = -20

    def set(self, snake_body):
        if self.rect.x == -20:
            while True:
                self.rect.left = random.choice(self.allposx)
                self.rect.top = random.choice(self.allposy)
                if not any(self.rect.colliderect(part) for part in snake_body):
                    break
            print(self.rect)


def show_text(screen, pos, text, color, font_bold=False, font_size=50, font_italic=False):
    cur_font = pygame.font.SysFont("宋体", font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)

def main():
    pygame.init()
    screen = new_bg()
    pygame.display.set_caption('吴俊的Snake')
    clock = pygame.time.Clock()
    scores = 0
    isdead = False
    frame = 0
    time_s = 0

    # 蛇/食物
    snake = Snake()
    food = Food()
    obstacle = Obstacle()
    # 定义网格参数
    grid_size = 20
    grid_color = (200, 200, 200)
    #绘制表格
    def draw_grid():
        for y in range(0, SCREEN_Y, grid_size):
            pygame.draw.line(screen, grid_color, (0, y), (SCREEN_X, y))
        for x in range(0, SCREEN_X, grid_size):
            pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_Y))

    while True:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)
                if event.key == pygame.K_SPACE and isdead:
                    return main()

        # 清屏并绘制网格
        screen.fill((66, 188, 245))
        draw_grid()

        # 画蛇身 / 每一步+1分
        if not isdead or scores < 0:
            if frame in [10,20,30]:
                scores += 1
            snake.check_turn()
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)

        # 显示死亡文字
        isdead = snake.isdead()
        if isdead:
            show_text(screen, (200, 250), 'YOU DEAD!', (227, 29, 18), False, 100)
            show_text(screen, (260, 330), 'press space to try again...', (0, 0, 22), False, 30)

        # 食物处理 / 吃到+50分
        if food.rect == snake.body[0]:
            scores += 50
            food.remove()
            snake.addnode()

        if obstacle.rect == snake.body[0]:
            scores -= 50
            obstacle.remove()
            snake.delnode()

        # 食物投递
        food.set(snake.body)
        pygame.draw.rect(screen, (136, 0, 21), food.rect, 0)

        # 障碍物生成
        obstacle.set(snake.body)
        pygame.draw.rect(screen, (70, 70, 70), obstacle.rect, 0)

        # 显示分数文字
        show_text(screen, (10, 500), 'Scores: ' + str(scores), (223, 223, 223))
        show_text(screen, (10, 550), 'your position:' + str(snake.show_po()), (223, 223, 223))
        show_text(screen, (600,10), 'game time:' + str(time_s), (223, 223, 223))

        pygame.display.update()
        if frame == 30:
            frame = 0
            time_s += 1
        clock.tick(30)

if __name__ == '__main__':
    main()