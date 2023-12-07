#импорт библиотек
import pygame
import time
from game import Game
from colors import Colors

PIXEL = 5

# класс игрока
class Dg_player:
    def __init__(self,x,y,size,color,b_width,b_height):
        self.x=x 
        self.y=y
        self.size = size
        self.color = color
        self.b_width = b_width
        self.b_height = b_height

    # движение влево
    def to_left(self):
        if self.x-1 >= 0:
            self.x -= 1

    # движение вправо
    def to_right(self):
        if self.x+self.size+1 <= self.b_width:
            self.x += 1
# класс пули
class Dg_bullet:
    def __init__(self,x,y,color,offset):
        self.x=x 
        self.y=y
        self.color = color
        self.offset = offset
    # движение пули
    def move(self):
        self.y += self.offset
# класс игровой доски
class Dg_board:
    def __init__(self, width, height, default_color, players, bullets, screen):
        self.width = width // PIXEL
        self.height = height // PIXEL
        self.default_color = default_color
        self.players = players
        self.bullets = bullets
        self.screen = screen

    # отрисовка доски на экран
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

# класс мини игры
class Duel_game(Game):
    def play(self):
        super().play()
        clock = pygame.time.Clock()
        
        # создание доски
        self.board=Dg_board(
            self.view_port.WIDTH,
            self.view_port.HEIGHT,
            Colors.WHITE,
            [],
            [],
            self.screen
        )
        # создание игроков
        self.player1=Dg_player(0,0,5,Colors.BLUE,self.board.width,self.board.height)
        self.player2=Dg_player(0,115,5,Colors.RED,self.board.width,self.board.height)
        self.board.players.append(self.player1)
        self.board.players.append(self.player2)

        p1_left = None
        p1_right = None

        p2_left = None
        p2_right = None
        while self.is_play:
            events = pygame.event.get()
            # обработка нажатия клавишь
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
                        self.board.bullets.append(Dg_bullet(self.player1.x+self.player1.size//2,5,self.player1.color, 1))
                    if event.key == pygame.K_a:
                        p1_left = time.time()
                    elif event.key == pygame.K_d:
                        p1_right = time.time()

                    if event.key == pygame.K_RETURN:
                        self.board.bullets.append(Dg_bullet(self.player2.x+self.player2.size//2,115,self.player2.color, -1))
                    if event.key == pygame.K_LEFT:
                        p2_left = time.time()
                    elif event.key == pygame.K_RIGHT:
                        p2_right = time.time()
            
            # в зависимости от того какая кнопка нажата происходит движение
            if p1_left != None and p1_right != None:
                if p1_left > p1_right:
                    self.player1.to_left()
                else:
                    self.player1.to_right()
            elif p1_left != None:
                self.player1.to_left()
            elif p1_right != None:
                self.player1.to_right()
    
            if p2_left != None and p2_right != None:
                if p2_left > p2_right:
                    self.player2.to_left()
                else:
                    self.player2.to_right()
            elif p2_left != None:
                self.player2.to_left()
            elif p2_right != None:
                self.player2.to_right()
            
            # проверка попаданий
            bullets_in_board = []
            for bullet in self.board.bullets:
                bullet.move()
                if bullet.y >= 0 and bullet.y <= self.board.height:
                    bullets_in_board.append(bullet)
                if (
                   bullet.color != self.player1.color and
                   bullet.y <= self.player1.y and
                   bullet.x > self.player1.x and bullet.x < self.player1.x+self.player1.size
                ):
                    self.show_message('Игрок 2 победил!', self.player2.color, duration=2.0, update=True)
                    super().exit()
                    continue
                if (
                    bullet.color != self.player2.color and 
                    bullet.y > self.player2.y and 
                    bullet.x >= self.player2.x and bullet.x < self.player2.x+self.player2.size
                ):
                    self.show_message('Игрок 1 победил!', self.player1.color, duration=2.0, update=True)
                    super().exit()
                    continue
            self.board.bullets = bullets_in_board
            self.board.draw()

            pygame.display.update()
            clock.tick(60)