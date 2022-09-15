import pygame
import os
import sys
import random

# 게임 스크린 크기
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 색 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (20, 60, 120)
ORANGE = (250, 170, 70)
RED = (250, 0, 0)

FPS = 60

# 공 객체
class Ball(object):
    def __init__(self, bounce_sound):
        self.rect = pygame.Rect(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), 12, 12)
        self.bounce_sound = bounce_sound
        self.dx = 0
        self.dy = 5

    # 공 업데이트
    def update(self):
        self.rect.x +=self.dx
        self.rect.y +=self.dy

        # 공이 게임 화면 왼쪽으로 넘어갈 때
        if self.rect.left < 0:
            self.dx *= -1
            self.rect.left = 0
            self.bounce_sound.play()
        # 공이 게임 화면 오른쪽으로 넘어갈 때
        elif self.rect.right > SCREEN_WIDTH:
            self.dx *=-1
            self.rect.right =SCREEN_WIDTH:
            self.bounce_sound.play()

    # 공 리셋
    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.dx = random.randint(-3, 3)
        self.dy = 5

    # 공 그리기
    def draw(self, screen):
        pygame.draw.rect(screen, ORANGE, self.rect)


# 플레이어 객체
class Player(object):
    def __init__(self, ping_sound):
        self.rect = pygame.Rect(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 40, 50, 15)
        self.ping_sound = ping_sound
        self.dx = 0

    # 업데이트
    def update(self, ball):
        if self.rect.left <= 0 and self.dx < 0:
            self.dx =
        elif self.rect.right >= SCREEN_WIDTH and self.dx > 0:
            self.dx =
        # 플레이어가 공이랑 충돌한 경우
        if self.rect.colliderect(ball.rect):
            ball.dx = random.randint(-5, 5)
            ball.dy *=
            ball.rect.bottom = self.rect.top
            self.ping_sound.play()

        self.rect.x += self.dx

    # 그리기
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
