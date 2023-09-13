import pygame
import os
import math
import random

pygame.init()
mines = 30
numFlags = mines

WIDTH, HEIGHT = 500, 1050
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")


BLOCK_SIZE = 49
GRASS_DARK = (5, 56, 6)
GRASS_LIGHT = (3, 69, 5)
GRASS_DARK_HOVER = (7, 74, 8)
GRASS_LIGHT_HOVER = (5, 87, 7)

SCREEN.fill((112, 112, 112))

text_font = pygame.font.SysFont("Arial", 35, True)

FPS = 60



class Node:
      def __init__(node, discovered, mined, distance, flag):
            node.discovered = discovered
            node.mined = mined
            node.distance = distance
            node.flag = flag

arr = [[0 for j in range(10)] for i in range(20)]
for i in range(20):
      for j in range(10):
            arr[i][j] = Node(False, False, 0, False)

def reset():
      global mines
      global numFlags
      for i in range(20):
            for j in range(10):
                  arr[i][j] = Node(False, False, 0, False)
      mines = 30
      numFlags = mines
      SCREEN.fill((112, 112, 112))
      main()

def draw_window(mineClicked):
      global numFlags
      FONT = pygame.font.Font('freesansbold.ttf', 36)
 
      for y in range(20):
            for x in range(10):
                  a, b = getCoord()
                  
                  if mineClicked == True and arr[y][x].mined == True:
                        rect = pygame.Rect(x*(BLOCK_SIZE + 1), y*(BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE)
                        pygame.draw.rect(SCREEN, 'RED', rect)
                        winScreen()
                  elif (a != x or b != y) and arr[y][x].discovered == False:
                        rect = pygame.Rect(x*(BLOCK_SIZE + 1), y*(BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE)
                        if (x + y) % 2 == 0:
                              pygame.draw.rect(SCREEN, GRASS_DARK, rect)  
                        else:
                              pygame.draw.rect(SCREEN, GRASS_LIGHT, rect) 
                        if arr[y][x].flag == True:
                              place_text("X", text_font, (255, 0, 21), x, y) 
                  elif arr[y][x].discovered == True:
                        rect = pygame.Rect(x*(BLOCK_SIZE + 1), y*(BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE)
                        if (x + y) % 2 == 0:
                              pygame.draw.rect(SCREEN, 'GRAY', rect)  
                        else:
                              pygame.draw.rect(SCREEN, 'WHITE', rect)
                        if arr[y][x].distance > 0:
                              if arr[y][x].distance == 1:
                                    place_text("1", text_font, (18, 219, 28), x, y)
                              if arr[y][x].distance == 2:
                                    place_text("2", text_font, (10, 89, 168), x, y)
                              if arr[y][x].distance == 3:
                                    place_text("3", text_font, (211, 224, 27), x, y)
                              if arr[y][x].distance == 4:
                                    place_text("4", text_font, (209, 118, 33), x, y)
                              if arr[y][x].distance == 5:
                                    place_text("5", text_font, (194, 33, 12), x, y)
                              if arr[y][x].distance == 6:
                                    place_text("6", text_font, (148, 12, 139), x, y)
                              if arr[y][x].distance == 7:
                                    place_text("7", text_font, (105, 4, 44), x, y)
                              if arr[y][x].distance == 8:
                                    place_text("8", text_font, (74, 9, 1), x, y)    
                  elif arr[y][x].mined == False or mineClicked == False:
                        rect = pygame.Rect(a*(BLOCK_SIZE + 1), b*(BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE)
                        if (a + b) % 2 == 0:
                              pygame.draw.rect(SCREEN, GRASS_LIGHT_HOVER, rect)  
                        else:
                              pygame.draw.rect(SCREEN, GRASS_LIGHT_HOVER, rect)
                        if arr[y][x].flag == True:
                              place_text("X", text_font, (255, 0, 21), x, y)   
      pygame.display.update()

def place_text(text, font, color, x, y):
      img = font.render(text, True, color)
      SCREEN.blit(img, (x * 50 + 17, y * 50 + 2))

def getCoord():
      a,b = pygame.mouse.get_pos()
      a = math.floor(a/50)
      b = math.floor(b/50)
      return a, b

def initialize(a, b):
      

      i = 0
      while i in range(mines):
            x = random.randint(0, 9)
            y = random.randint(0, 19)
            if (x != a or y != b) and (arr[y][x].mined == False):
                  arr[y][x].mined = True
                  #print(x,y)
                  for c in range(-1, 2):
                        for d in range(-1, 2):
                              if (x + d) in range(0,10) and (y + c) in range(0,20):
                                    arr[y + c][x + d].distance = arr[y + c][x + d].distance + 1

                 
                  i = i + 1
            
      fill(a,b)
      

def fill(a, b):
      global numFlags
      if a >= 0 and b >= 0 and a <= 9 and b <= 19:
            arr[b][a].discovered = True
            if arr[b][a].flag == True:
                  arr[b][a].flag = False
                  numFlags = numFlags + 1
                  updateflag()
            rect = pygame.Rect(a*(BLOCK_SIZE + 1), b*(BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE)
            if (a + b) % 2 == 0:
                  pygame.draw.rect(SCREEN, 'WHITE', rect)  
            else:
                  pygame.draw.rect(SCREEN, 'GRAY', rect)
            if arr[b][a].distance == 0:
                  
                  for i in range(-1, 2):
                        for j in range(-1, 2):
                              if (a + j) in range(0,10) and (b + i) in range(0,20) and arr[b+i][a + j].discovered == False:
                                    fill(a + j, b + i)
            return
      return

def clicked(a, b):
      global numFlags
      if arr[b][a].mined == True:
            return True
      else:
            arr[b][a].discovered = True
            if arr[b][a].flag == True:
                  arr[b][a].flag = False
                  numFlags = numFlags + 1
                  updateflag()
            fill(a,b)
            return False
      
def flag(a, b):
      global numFlags
      if arr[b][a].discovered == False and arr[b][a].flag == False and numFlags > 0:
            arr[b][a].flag = True
            numFlags = numFlags - 1
      elif arr[b][a].discovered == False and arr[b][a].flag == True:
            arr[b][a].flag = False
            numFlags = numFlags + 1
      updateflag()

def updateflag():
      global numFlags
      rect = pygame.Rect(9*(BLOCK_SIZE + 1), 20*(BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE)
      pygame.draw.rect(SCREEN, (112, 112, 112), rect)  
      place_text(str(numFlags), text_font, (255, 0, 21), 9, 20)


def win():
      for i in range(20):
            for j in range(10):
                  if arr[i][j].discovered == False and arr[i][j].mined == False:
                        return False
      return True

def winScreen():
      global WIDTH, HEIGHT
      print("Win")
      rect = pygame.Rect(WIDTH/2 - 150, HEIGHT/2 - 50, 300, 100)

      pygame.draw.rect(SCREEN, (102, 255, 138), rect)  

def main():
      clock = pygame.time.Clock()
      run = True
      game_start = False
      mineClicked = False
      gameWon = False
      place_text(str(numFlags), text_font, (255, 0, 21), 9, 20)
      place_text("X  =", text_font, (0, 0, 0), 7.6, 20)
      while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                  a, b = getCoord()
                  if mineClicked == False and event.type == pygame.MOUSEBUTTONDOWN:
                        left = pygame.mouse.get_pressed()[0]
                        right = pygame.mouse.get_pressed()[2]
                        if left and game_start == False and a in range(0, 10) and b in range(0, 20):
                              
                              arr[b][a].discovered = True
                              for i in range(-1, 2):
                                    for j in range(-1, 2):
                                          if (a + j) in range(0,10) and (b + i) in range(0,20):
                                                arr[b + i][a + j].mined = True

                              initialize(a, b)
                              for i in range(-1, 2):
                                    for j in range(-1, 2):
                                          if (a + j) in range(0,10) and (b + i) in range(0,20):
                                                arr[b + i][a + j].mined = False
                              game_start = True
                        elif left and a in range(0, 10) and b in range(0, 20):
                              a, b = getCoord()
                              mineClicked = clicked(a, b)
                        elif right and game_start == True and a in range(0, 10) and b in range(0, 20):
                              flag(a, b)
                        
                              


                              
            if win() == True:
                  mineClicked = True
                  gameWon = True
            draw_window(mineClicked)
            if gameWon == True:
                  winScreen()

            
      
      pygame.quit()

if __name__ == "__main__":
      main()