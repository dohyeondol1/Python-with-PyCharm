import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN= (0,255,0)
BLUE=(0,0,255)

pygame.init() #파이게임 초기화

pygame.display.set_caption("도현석")
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock=pygame.time.Clock()

check=False

while not check:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check = True

    screen.fill(WHITE)

    pygame.draw.line(screen, RED, [50, 50], [500, 50], 10)
    pygame.draw.rect(screen, GREEN, [50, 200, 150, 150], 5)

    font=pygame.font.SysFont('FixedSys', 40, True, False)
    text=font.render("ehgustjr", True, BLACK)
    screen.blit(text, [200, 500])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
