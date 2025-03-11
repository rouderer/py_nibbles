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
        self.add_num = 0
        self.target_direction = pygame.K_RIGHT
        self.direction = pygame.K_RIGHT
        self.speed = 4
        self.body = []
        for x in range(10):
            self.addnode()

    def speed_plus(self, scores):
        if self.speed == 4:
            if scores > 500:
                self.speed = 5
        elif self.speed == 5:
            if scores > 1500:
                self.speed = 10

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
        if self.add_num == 0:
            self.delnode()
        else:
            self.add_num -= 1

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

    def add_new(self):
        self.add_num = 5

# 食物类
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-20, 0, 20, 20)
        self.allposx = []
        self.allposy = []
        self.surtime = 20
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
    def sur_time(self):
        self.surtime -= 1
        if self.surtime == 0:
            return True
        else:
            return False

class Obstacle:
    def __init__(self):
        self.allposx = []
        self.allposy = []
        self.surtime = 20
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

    def sur_time(self):
        self.surtime -= 1
        if self.surtime == 0:
            return True
        else:
            return False

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
    food_list = []
    obstacle_list = []
    # 蛇/食物/障碍物
    snake = Snake()
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

        if frame == 1:
            snake.speed_plus(scores)

        # 画蛇身 / 每一步+1分
        if scores < 0 or not isdead:
            if frame in [10, 20, 30]:
                scores += 1
            snake.check_turn()
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)



        # 食物投递
        if time_s % 5 == 0 and frame == 2:
            food = Food()
            food.set(snake.body)
            food_list.append(food)
            # 障碍物生成
        if time_s % 8 == 0 and frame == 2:
            obstacle = Obstacle()
            obstacle.set(snake.body)
            obstacle_list.append(obstacle)

        # 食物处理 / 吃到+50分
        for fd in food_list:
            pygame.draw.rect(screen, (136, 0, 21), fd.rect, 0)
            if fd.rect == snake.body[0] or (frame == 1 and fd.sur_time()):
                if fd.rect == snake.body[0]:
                    scores += 50
                fd.remove()
                food_ln = [item for item in food_list if item != fd]
                food_list = food_ln
                snake.add_new()

        # 显示死亡文字
        isdead = snake.isdead()
        if isdead:
                show_text(screen, (200, 250), 'YOU DEAD!', (227, 29, 18), False, 100)
                show_text(screen, (260, 330), 'press space to try again...', (0, 0, 22), False, 30)

        for ob in obstacle_list:
            pygame.draw.rect(screen, (70, 70, 70), ob.rect, 0)
            if ob.rect == snake.body[0] or (frame == 1 and ob.sur_time()):
                if ob.rect == snake.body[0]:
                    scores -= 50
                ob.remove()
                obstacle_ln = [item for item in obstacle_list if item != ob]
                obstacle_list = obstacle_ln
                for i in range(5): snake.delnode()

        # 显示分数文字
        show_text(screen, (10, 500), 'Scores: ' + str(scores), (223, 223, 223))
        show_text(screen, (10, 550), 'your position:' + str(snake.show_po()), (223, 223, 223))
        show_text(screen, (550, 10), 'game time:' + str(time_s), (223, 223, 223))
        #模式区分显示
        if snake.speed == 4:
            show_text(screen, (10, 10), 'easy', (223, 223, 223))
        elif snake.speed == 5:
            show_text(screen, (10, 10), 'normal', (223, 223, 0))
        else:
            show_text(screen, (10, 10), 'hard', (225, 0, 0))
        pygame.display.update()
        if frame == 30:
            frame = 0
            time_s += 1
        clock.tick(30)

if __name__ == '__main__':
    main()