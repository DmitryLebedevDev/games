import pygame
import time
import random
from game import Game
from colors import Colors

PIXEL = 25

class Snake:
    def __init__(self,body,color):
        self.body = body
        self.color = color
    def add_body(self, x, y):
        self.body.insert(0, (x, y))
    def to_left(self):
        self._movie(-1,0)
    def to_right(self):
        self._movie(1,0)
    def to_top(self):
        self._movie(0,-1)
    def to_bottom(self):
        self._movie(0,1)
    def head(self):
        return self.body[0]
    def isLose(self, maxX, maxY, otherSnake):
        head = self.head()
        if (head[0] < 0 or head[0] >= maxX or 
            head[1] < 0 or head[1] >= maxY):
                return True
        for i in range(1,len(self.body)):
            if self.body[i][0] == head[0] and self.body[i][1] == head[1]:
                return True
        for otherSnakePart in otherSnake.body:
            if otherSnakePart[0] == head[0] and otherSnakePart[1] == head[1]:
                return True
        return False
    def _movie(self, ox, oy):
        head = self.head()
        self.body.pop()
        self.body.insert(
            0,
            (head[0]+ox, head[1]+oy)
        )
class Fruit:
    def __init__(self,x,y,color):
        self.x=x 
        self.y=y 
        self.color = color

class Board:
    def __init__(self, width, height, defaultColor, snakes, fruits, screen):
        self.width = width // PIXEL
        self.height = height // PIXEL
        self.defaultColor = defaultColor
        self.snakes = snakes
        self.fruits = fruits
        self.screen = screen

    def draw(self):
        self.screen.fill(self.defaultColor)
        for fruit in self.fruits:
            pygame.draw.rect(
                self.screen,fruit.color,
                (fruit.x*PIXEL, fruit.y*PIXEL, PIXEL, PIXEL)
            )
        for snake in self.snakes:
            for snakePart in snake.body:
                x, y = snakePart
                pygame.draw.rect(
                    self.screen,snake.color,
                    (x*PIXEL, y*PIXEL, PIXEL, PIXEL)
                )
            

class SnakeGame(Game):
    def play(self):
        super().play()
        
        snake1 = Snake([(0,2),(0,1),(0,0)],Colors.BLUE)
        snake2 = Snake([(2,0),(1,0),(0,0)],Colors.RED)
        snakes = [snake1, snake2]
        fruits = [Fruit(15,15,Colors.GREEN),Fruit(20,20,Colors.GREEN)]
        board=Board(
            self.viewPort.WIDTH,
            self.viewPort.HEIGHT,
            Colors.WHITE,
            snakes,
            fruits,
            self.screen
        )

        p1_key = pygame.K_s
        p2_key = pygame.K_RIGHT
        while self.is_play:
            p1Enter = False
            p2Enter = False
            for event in pygame.event.get():
                super().handleExitBtnClick(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and p1_key != pygame.K_s and (not p1Enter):
                        p1Enter = True
                        p1_key = pygame.K_w
                    elif event.key == pygame.K_s and p1_key != pygame.K_w and (not p1Enter):
                        p1Enter = True
                        p1_key = pygame.K_s
                    elif event.key == pygame.K_a and p1_key != pygame.K_d and (not p1Enter):
                        p1Enter = True
                        p1_key = pygame.K_a
                    elif event.key == pygame.K_d and p1_key != pygame.K_a and (not p1Enter):
                        p1Enter = True
                        p1_key = pygame.K_d

                    if event.key == pygame.K_UP and p2_key != pygame.K_DOWN and (not p2Enter):
                        p2Enter = True
                        p2_key = pygame.K_UP
                    elif event.key == pygame.K_DOWN and p2_key != pygame.K_UP and (not p2Enter):
                        p2Enter = True
                        p2_key = pygame.K_DOWN
                    elif event.key == pygame.K_LEFT and p2_key != pygame.K_RIGHT and (not p2Enter):
                        p2Enter = True
                        p2_key = pygame.K_LEFT
                    elif event.key == pygame.K_RIGHT and p2_key != pygame.K_LEFT and (not p2Enter):
                        p2Enter = True
                        p2_key = pygame.K_RIGHT
                
            if p1_key == pygame.K_w:
                snake1.to_top()
            elif p1_key == pygame.K_s:
                snake1.to_bottom()
            elif p1_key == pygame.K_a:
                snake1.to_left()
            elif p1_key == pygame.K_d:
                snake1.to_right()
    
            if p2_key == pygame.K_UP:
                snake2.to_top()
            elif p2_key == pygame.K_DOWN:
                snake2.to_bottom()
            elif p2_key == pygame.K_LEFT:
                snake2.to_left()
            elif p2_key == pygame.K_RIGHT:
                snake2.to_right()
            
            if snake1.isLose(board.width, board.height, snake2):
                self.showMessage('Игрок 2 победил!', snake2.color, duration=2.0, update=True)
                super().exit()
                continue
            if snake2.isLose(board.width, board.height, snake1):
                self.showMessage('Игрок 1 победил!', snake1.color, duration=2.0, update=True)
                super().exit()
                continue
            
            stayedFruits = []
            for fruit in fruits:
                isEated = False
                for snake in snakes:
                    head = snake.head()    
                    if fruit.x == head[0] and fruit.y == head[1]:
                        snake.add_body(fruit.x, fruit.y)
                        isEated = True
                        break
                if not isEated:
                    stayedFruits.append(fruit)
            while len(fruits) != len(stayedFruits):
                isValid = True
                x = random.randint(0, board.width-1)
                y = random.randint(0, board.height-1)
                for snake in snakes:
                    for part in snake.body:
                        if part[0] == x and part[1] == y:
                            isValid = False
                            break
                for fruit in stayedFruits:
                    if fruit.x == x and fruit.y == y:
                        isValid = False
                        break
                if isValid:
                    stayedFruits.append(Fruit(x,y,Colors.GREEN))
            fruits = stayedFruits

            board.fruits = fruits
            board.draw()
            
            pygame.display.update()
            time.sleep(0.25)
