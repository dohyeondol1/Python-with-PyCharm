import pygame
import os

SCREEN_WIDTH = 640
SCREEN_HEIGHT= 320

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN=(160, 120, 40)

pygame.init()  # 파이게임 초기화

pygame.display.set_caption("이미지") #프로그램 제목
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #
clock=pygame.time.Clock()

current_path=os.path.dirname(__file__)
img_path=os.path.join(current_path, 'set')

background_img = pygame.image.load(os.path.join(img_path, 'terrain.png'))
mush1=pygame.image.load(os.path.join(img_path, 'mushroom1.png'))
#mush2=pygame.image.load(os.path.join(img_path, 'mushroom2.png'))
#mush3=pygame.image.load(os.path.join(img_path, 'mushroom3.png'))

keyboard_x=int(SCREEN_WIDTH/2)
keyboard_y=int(SCREEN_WIDTH/2)
keyboard_dx=0
keyboard_dy=0

check=False

while not check:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check=True
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                keyboard_dx = -7
            elif event.key==pygame.K_RIGHT:
                keyboard_dx = 7
            elif event.key == pygame.K_UP:
                keyboard_dy = -7
            elif event.key==pygame.K_DOWN:
                keyboard_dy = 7
        elif event.type==pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                keyboard_dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                keyboard_dy = 0

    keyboard_x += keyboard_dx
    keyboard_y += keyboard_dy

    screen.fill(BROWN)
    screen.blit(background_img, [320, 160])

    screen.blit(mush1, [keyboard_x, keyboard_y])
    #screen.blit(mush2, [300, 100])
    #screen.blit(mush3, [450, 140])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
