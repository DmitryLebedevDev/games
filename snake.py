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
    def is_lose(self, max_x, max_y, other_snake):
        head = self.head()
        if (head[0] < 0 or head[0] >= max_x or 
            head[1] < 0 or head[1] >= max_y):
                return True
        for i in range(1,len(self.body)):
            if self.body[i][0] == head[0] and self.body[i][1] == head[1]:
                return True
        for other_snake_part in other_snake.body:
            if other_snake_part[0] == head[0] and other_snake_part[1] == head[1]:
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
    def __init__(self, width, height, default_color, snakes, fruits, screen):
        self.width = width // PIXEL
        self.height = height // PIXEL
        self.default_color = default_color
        self.snakes = snakes
        self.fruits = fruits
        self.screen = screen

    def draw(self):
        self.screen.fill(self.default_color)
        for fruit in self.fruits:
            pygame.draw.rect(
                self.screen,fruit.color,
                (fruit.x*PIXEL, fruit.y*PIXEL, PIXEL, PIXEL)
            )
        for snake in self.snakes:
            for snake_part in snake.body:
                x, y = snake_part
                pygame.draw.rect(
                    self.screen,snake.color,
                    (x*PIXEL, y*PIXEL, PIXEL, PIXEL)
                )
            

class Snake_game(Game):
    def play(self):
        super().play()
        
        snake1 = Snake([(0,2),(0,1),(0,0)],Colors.BLUE)
        snake2 = Snake([(2,0),(1,0),(0,0)],Colors.RED)
        board=Board(
            self.view_port.WIDTH,
            self.view_port.HEIGHT,
            Colors.WHITE,
            [snake1, snake2],
            [Fruit(15,15,Colors.GREEN),Fruit(20,20,Colors.GREEN)],
            self.screen
        )

        p1_key = pygame.K_s
        p2_key = pygame.K_RIGHT
        while self.is_play:
            p1Enter = False
            p2Enter = False
            for event in pygame.event.get():
                super().handle_exit_btn_click(event)
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
            
            if snake1.is_lose(board.width, board.height, snake2):
                self.show_message('Игрок 2 победил!', snake2.color, duration=2.0, update=True)
                super().exit()
                continue
            if snake2.is_lose(board.width, board.height, snake1):
                self.show_message('Игрок 1 победил!', snake1.color, duration=2.0, update=True)
                super().exit()
                continue
            
            stayed_fruits = []
            for fruit in board.fruits:
                is_eated = False
                for snake in board.snakes:
                    head = snake.head()    
                    if fruit.x == head[0] and fruit.y == head[1]:
                        snake.add_body(fruit.x, fruit.y)
                        is_eated = True
                        break
                if not is_eated:
                    stayed_fruits.append(fruit)
            while len(board.fruits) != len(stayed_fruits):
                is_valid = True
                x = random.randint(0, board.width-1)
                y = random.randint(0, board.height-1)
                for snake in board.snakes:
                    for part in snake.body:
                        if part[0] == x and part[1] == y:
                            is_valid = False
                            break
                for fruit in stayed_fruits:
                    if fruit.x == x and fruit.y == y:
                        is_valid = False
                        break
                if is_valid:
                    stayed_fruits.append(Fruit(x,y,Colors.GREEN))
            board.fruits = stayed_fruits
            board.draw()
            
            pygame.display.update()
            time.sleep(0.25)
