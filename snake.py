#импорт библиотек
import pygame
import time
from game import Game
from colors import Colors

PIXEL = 5

class Player:
    def __init__(self,x,y,size,color,bWidth,bHeight):
        self.x=x 
        self.y=y 
        self.size = size
        self.color = color 
        self.bWidth = bWidth
        self.bHeight = bHeight
    def to_left(self):
        if self.x-1 >= 0:
            self.x -= 1
    def to_right(self):
        if self.x+self.size+1 <= self.bWidth:
            self.x += 1
    def to_top(self):
        if self.y-1 >= 0:
            self.y -= 1
    def to_bottom(self):
        if self.y+self.size+1 <= self.bHeight:
            self.y += 1
class Board:
    def __init__(self, width, height, defaultColor):
        self.width = width // PIXEL
        self.height = height // PIXEL
        self.field = [[defaultColor] * self.width for _ in range(self.height)]

    def put_player(self, player):
        for i in range(player.size):
            for j in range(player.size):
                self.field[player.y + i][player.x + j] = player.color

class FightPaint(Game):
    def play(self):
        super().play()
        clock = pygame.time.Clock()
        end_time = time.time() + 100
        
        board=Board(
            self.viewPort.WIDTH,
            self.viewPort.HEIGHT,
            Colors.WHITE
        )
        player1=Player(0,0,PIXEL,Colors.BLUE,board.width,board.height)
        player2=Player(0,0,PIXEL,Colors.RED,board.width,board.height)

        p1_key = pygame.K_s
        p2_key = pygame.K_RIGHT
        while self.is_play:
            for event in pygame.event.get():
                super().handleExitBtnClick(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        p1_key = pygame.K_w
                    elif event.key == pygame.K_s:
                        p1_key = pygame.K_s
                    elif event.key == pygame.K_a:
                        p1_key = pygame.K_a
                    elif event.key == pygame.K_d:
                        p1_key = pygame.K_d

                    if event.key == pygame.K_UP:
                        p2_key = pygame.K_UP
                    elif event.key == pygame.K_DOWN:
                        p2_key = pygame.K_DOWN
                    elif event.key == pygame.K_LEFT:
                        p2_key = pygame.K_LEFT
                    elif event.key == pygame.K_RIGHT:
                        p2_key = pygame.K_RIGHT
                
            if p1_key == pygame.K_w:
                player1.to_top()
            elif p1_key == pygame.K_s:
                player1.to_bottom()
            elif p1_key == pygame.K_a:
                player1.to_left()
            elif p1_key == pygame.K_d:
                player1.to_right()
    
            if p2_key == pygame.K_UP:
                player2.to_top()
            elif p2_key == pygame.K_DOWN:
                player2.to_bottom()
            elif p2_key == pygame.K_LEFT:
                player2.to_left()
            elif p2_key == pygame.K_RIGHT:
                player2.to_right()
                
            board.put_player(player1)
            board.put_player(player2)
            for i in range(len(board.field)):
                for j in range(len(board.field[i])):
                    pygame.draw.rect(
                        self.screen,board.field[i][j],
                        (j*PIXEL, i*PIXEL, PIXEL, PIXEL)
                    )
            
            player1_score = 0
            player2_score = 0
            for i in range(len(board.field)):
                for j in range(len(board.field[i])):
                    cell = board.field[i][j]
                    if cell == player1.color :
                        player1_score += 1
                    if cell == player2.color:
                        player2_score += 1
                        
            if time.time() >= end_time:
                if player1_score > player2_score:
                    self.showMessage('Игрок 1 победил!', Colors.BLUE, duration=2.0, update=True)
                elif player2_score > player1_score:
                    self.showMessage('Игрок 2 победил!', Colors.RED, duration=2.0, update=True)
                else:
                    self.showMessage('Ничья', Colors.BLACK, duration=2.0, update=True)
                super().exit()

            self.showMessage(
                str(round(end_time - time.time())), 
                Colors.BLACK, center=(0,-280)
            )
            self.showMessage(
                f'player1 - {player1_score} player2 - {player2_score}',
                Colors.BLACK, center=(0,-250)
            )
            
            pygame.display.update()
            clock.tick(60)
