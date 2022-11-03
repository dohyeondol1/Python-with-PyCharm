import sys
from math import sqrt
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE

BLOCK_DATA = (
   (
       (0, 0, 1, \
        1, 1, 1, \
        0, 0, 0),
       (0, 1, 0, \
        0, 1, 0, \
        0, 1, 1),
       (0, 0, 0, \
        1, 1, 1, \
        1, 0, 0),
       (1, 1, 0, \
        0, 1, 0, \
        0, 1, 0),
   ), (
       (2, 0, 0, \
        2, 2, 2, \
        0, 0, 0),
       (0, 2, 2, \
        0, 2, 0, \
        0, 2, 0),
       (0, 0, 0, \
        2, 2, 2, \
        0, 0, 2),
       (0, 2, 0, \
        0, 2, 0, \
        2, 2, 0)
   ), (
       (0, 3, 0, \
        3, 3, 3, \
        0, 0, 0),
       (0, 3, 0, \
        0, 3, 3, \
        0, 3, 0),
       (0, 0, 0, \
        3, 3, 3, \
        0, 3, 0),
       (0, 3, 0, \
        3, 3, 0, \
        0, 3, 0)
   ), (
       (4, 4, 0, \
        0, 4, 4, \
        0, 0, 0),
       (0, 0, 4, \
        0, 4, 4, \
        0, 4, 0),
       (0, 0, 0, \
        4, 4, 0, \
        0, 4, 4),
       (0, 4, 0, \
        4, 4, 0, \
        4, 0, 0)
   ), (
       (0, 5, 5, \
        5, 5, 0, \
        0, 0, 0),
       (0, 5, 0, \
        0, 5, 5, \
        0, 0, 5),
       (0, 0, 0, \
        0, 5, 5, \
        5, 5, 0),
       (5, 0, 0, \
        5, 5, 0, \
        0, 5, 0)
   ), (
       (6, 6, 6, 6),
       (6, 6, 6, 6),
       (6, 6, 6, 6),
       (6, 6, 6, 6)
   ), (
       (0, 7, 0, 0, \
        0, 7, 0, 0, \
        0, 7, 0, 0, \
        0, 7, 0, 0),
       (0, 0, 0, 0, \
        7, 7, 7, 7, \
        0, 0, 0, 0, \
        0, 0, 0, 0),
       (0, 0, 7, 0, \
        0, 0, 7, 0, \
        0, 0, 7, 0, \
        0, 0, 7, 0),
       (0, 0, 0, 0, \
        0, 0, 0, 0, \
        7, 7, 7, 7, \
        0, 0, 0, 0)
   )
)

class block:
   """ 블록 객체 """
   def __init__(self, count):
       self.turn = randint(0, 3) #블록의 방향
       self.type = BLOCK_DATA[randint(0, 6)] #블록의 타입(모양)
       self.data = self.type[self.turn] # 숫자 데이터
       self.size = int(sqrt(len(self.data)))
       self.xpos = randint(3, 8 - self.size)
       self.ypos = 3 - self.size
       self.fire = count + INTERVAL # 낙하 시작시간

   def update(self, count):
       """ 블록 상태 갱신 """
       erased = 0
       if is_overlapped(self.xpos, self.ypos + 1, self.turn):
           for y_offset in range(BLOCK.size):
               for x_offset in range(BLOCK.size):
                   if 0 <= self.xpos+x_offset < WIDTH and 0 <= self.ypos+y_offset < HEIGHT:
                       val = BLOCK.data[y_offset*BLOCK.size + x_offset]
                       if val != 0:
                           FIELD[self.ypos+y_offset][self.xpos+x_offset] = val

           erased = erase_line()
           go_next_block(count)

       if self.fire < count:
           self.fire = count + INTERVAL
           self.ypos += 1
       return erased

   def draw(self):
       """ 블록을 그린다 """
       for index in range(len(self.data)):
           xpos = index % self.size
           ypos = index // self.size
           val = self.data[index]
           if 0 <= ypos + self.ypos < HEIGHT and 0 <= xpos + self.xpos < WIDTH and val != 0:
               x_pos = 25 + (xpos + self.xpos) * 25
               y_pos = 25 + (ypos + self.ypos) * 25
               pygame.draw.rect(SURFACE, COLORS[val], (x_pos, y_pos, 24, 24))

def erase_line():
    """ 행이 모두 찬 단을 지운다 """
    erased = 0
    ypos = 20
    while ypos >= 0:
        if all(FIELD[ypos]):
            erased += 1
            del FIELD[ypos]
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
        else:
            ypos -= 1
    return erased

def is_game_over():
    """ 게임 오버인지 아닌지 """
    filled = 0
    for cell in FIELD[0]:
        if cell != 0:
            filled += 1
    return filled > 2  # 2 = 좌우의 벽

def go_next_block(count):
   """ 다음 블록으로 전환한다 """
   global BLOCK, NEXT_BLOCK
   BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else block(count)
   NEXT_BLOCK = block(count)

def is_overlapped(xpos, ypos, turn):
    """ 블록이 벽이나 땅의 블록과 충돌하는지 아닌지 """
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos + x_offset < WIDTH and \
                    0 <= ypos + y_offset < HEIGHT:
                if data[y_offset * BLOCK.size + x_offset] != 0 and \
                        FIELD[ypos + y_offset][xpos + x_offset] != 0:
                    return True
    return False

# 전역 변수
pygame.init()
pygame.key.set_repeat(300, 3000)
SURFACE = pygame.display.set_mode([600, 600])
CLOCK = pygame.time.Clock()
WIDTH = 12
HEIGHT = 22
INTERVAL = 20 #속도 결정
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), \
         (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BLOCK = None
NEXT_BLOCK = None

def main():
   """ 메인 루틴 """
   global INTERVAL
   count = 0
   score = 0
   game_over = False
   smallfont = pygame.font.SysFont(None, 36)
   largefont = pygame.font.SysFont(None, 72)
   message_over = largefont.render("GAME OVER!!",True, (0, 255, 225))
   message_rect = message_over.get_rect()
   message_rect.center = (300, 300)

   go_next_block(INTERVAL)

   # 필드구성
   for ypos in range(HEIGHT):
       for xpos in range(WIDTH):
           if xpos ==  0 or xpos == 11:
               FIELD[ypos][xpos] = 8
           else:
               FIELD[ypos][xpos] = 0

   for index in range(WIDTH):
       FIELD[HEIGHT-1][index] = 8

   check = False
   while True:
       key = None
       for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
           elif event.type == KEYDOWN:
               key = event.key
           elif event.type == KEYUP:
               check = False

       game_over = is_game_over()
       if not game_over:
           count += 5
           if count % 1000 == 0:
               INTERVAL = max(1, INTERVAL - 2)
           erased = BLOCK.update(count)

           if erased > 0:
               score += (2 ** erased) * 100

           # 키 이벤트 처리
           next_x, next_y, next_t = BLOCK.xpos, BLOCK.ypos, BLOCK.turn

           if key == K_SPACE and check == False:
               next_t = (next_t + 1) % 4
               check = True
           elif key == K_RIGHT:
               next_x += 1
           elif key == K_LEFT:
               next_x -= 1
           elif key == K_DOWN:
               next_y += 1

           if not is_overlapped(next_x, next_y, next_t):
               BLOCK.xpos = next_x
               BLOCK.ypos = next_y
               BLOCK.turn = next_t
               BLOCK.data = BLOCK.type[BLOCK.turn]

       # 전체&낙하 중인 블록 그리기
       SURFACE.fill((0, 0, 0))
       for ypos in range(HEIGHT):
           for xpos in range(WIDTH):
               val = FIELD[ypos][xpos]
               pygame.draw.rect(SURFACE, COLORS[val],
                                (xpos*25 + 25, ypos*25 + 25, 24, 24))
       BLOCK.draw()

       # 다음 블록 그리기
       for ypos in range(NEXT_BLOCK.size):
           for xpos in range(NEXT_BLOCK.size):
               val = NEXT_BLOCK.data[xpos + ypos*NEXT_BLOCK.size]
               pygame.draw.rect(SURFACE, COLORS[val], (xpos*25 + 460, ypos*25 + 100, 24, 24))

       # 점수 나타내기
       score_str = str(score).zfill(6)
       score_image = smallfont.render(score_str, True, (0, 255, 0))
       SURFACE.blit(score_image, (500, 30))

       if game_over:
           SURFACE.blit(message_over, message_rect)

       pygame.display.update()
       CLOCK.tick(5)

if __name__ == '__main__':
   main()
