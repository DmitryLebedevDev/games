#импорт библиотек
import pygame
import time
from game import Game
from colors import Colors

PIXEL = 5

class Player:
    def __init__(self,x,y,size,color,b_width,b_height):
        self.x=x 
        self.y=y
        self.size = size
        self.color = color
        self.b_width = b_width
        self.b_height = b_height

    def to_left(self):
        if self.x-1 >= 0:
            self.x -= 1

    def to_right(self):
        if self.x+self.size+1 <= self.b_width:
            self.x += 1

    def to_top(self):
        if self.y-1 >= 0:
            self.y -= 1

    def to_bottom(self):
        if self.y+self.size+1 <= self.b_height:
            self.y += 1
class Bullet:
    def __init__(self,x,y,color,offset):
        self.x=x 
        self.y=y
        self.color = color
        self.offset = offset
    def move(self):
        self.y += self.offset
class Board:
    def __init__(self, width, height, default_color, players, bullets, screen):
        self.width = width // PIXEL
        self.height = height // PIXEL
        self.default_color = default_color
        self.players = players
        self.bullets = bullets
        self.screen = screen

    def draw(self):
        self.screen.fill(self.default_color)
        for bullet in self.bullets:
            pygame.draw.rect(
                self.screen,bullet.color,
                (bullet.x*PIXEL, bullet.y*PIXEL, PIXEL, PIXEL)
            )
        for player in self.players:
            pygame.draw.rect(
                self.screen,player.color,
                (player.x*PIXEL, player.y*PIXEL, player.size*PIXEL, player.size*PIXEL)
            )

class Duel_game(Game):
    def play(self):
        super().play()
        clock = pygame.time.Clock()
        
        board=Board(
            self.view_port.WIDTH,
            self.view_port.HEIGHT,
            Colors.WHITE,
            [],
            [],
            self.screen
        )
        player1=Player(0,0,5,Colors.BLUE,board.width,board.height)
        player2=Player(0,115,5,Colors.RED,board.width,board.height)
        board.players.append(player1)
        board.players.append(player2)

        p1_left = None
        p1_right = None

        p2_left = None
        p2_right = None
        while self.is_play:
            events = pygame.event.get()
            for event in events:
                super().handle_exit_btn_click(event)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        p1_left = None
                    if event.key == pygame.K_d:
                        p1_right = None

                    if event.key == pygame.K_LEFT:
                        p2_left = None
                    if event.key == pygame.K_RIGHT:
                        p2_right = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        board.bullets.append(Bullet(player1.x+player1.size//2,5,player1.color, 1))
                    if event.key == pygame.K_a:
                        p1_left = time.time()
                    elif event.key == pygame.K_d:
                        p1_right = time.time()

                    if event.key == pygame.K_RETURN:
                        board.bullets.append(Bullet(player2.x+player2.size//2,115,player2.color, -1))
                    if event.key == pygame.K_LEFT:
                        p2_left = time.time()
                    elif event.key == pygame.K_RIGHT:
                        p2_right = time.time()
                
            if p1_left != None and p1_right != None:
                if p1_left > p1_right:
                    player1.to_left()
                else:
                    player1.to_right()
            elif p1_left != None:
                player1.to_left()
            elif p1_right != None:
                player1.to_right()
    
            if p2_left != None and p2_right != None:
                if p2_left > p2_right:
                    player2.to_left()
                else:
                    player2.to_right()
            elif p2_left != None:
                player2.to_left()
            elif p2_right != None:
                player2.to_right()
            
            bullets_in_board = []
            for bullet in board.bullets:
                bullet.move()
                if bullet.y >= 0 and bullet.y <= board.height:
                    bullets_in_board.append(bullet)
                if (
                   bullet.color != player1.color and
                   bullet.y <= player1.y and
                   bullet.x > player1.x and bullet.x < player1.x+player1.size
                ):
                    self.show_message('Игрок 2 победил!', player2.color, duration=2.0, update=True)
                    super().exit()
                    continue
                if (
                    bullet.color != player2.color and 
                    bullet.y > player2.y and 
                    bullet.x >= player2.x and bullet.x < player2.x+player2.size
                ):
                    self.show_message('Игрок 1 победил!', player1.color, duration=2.0, update=True)
                    super().exit()
                    continue
            board.bullets = bullets_in_board
            board.draw()

            pygame.display.update()
            clock.tick(60)