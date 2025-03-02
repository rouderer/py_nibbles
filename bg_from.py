import pygame

def new_bg():
    # 初始化 Pygame
    pygame.init()

    # 设置屏幕大小
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    return screen