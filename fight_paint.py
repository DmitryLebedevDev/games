#импорт библиотек
import pygame
import time
from game import Game
from colors import Colors

PIXEL = 5

# класс игрока
class Fpg_player:
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

    # движение вверх
    def to_top(self):
        if self.y-1 >= 0:
            self.y -= 1

    # движение вниз
    def to_bottom(self):
        if self.y+self.size+1 <= self.b_height:
            self.y += 1
# класс доски
class Fpg_board:
    def __init__(self, width, height, default_color, screen):
        self.width = width // PIXEL
        self.height = height // PIXEL
        self.field = [[default_color] * self.width for _ in range(self.height)]
        self.screen = screen

    # покрасить часть доски
    def put_player(self, player):
        for i in range(player.size):
            for j in range(player.size):
                self.field[player.y + i][player.x + j] = player.color

    #отрисовать доску
    def draw(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                pygame.draw.rect(
                    self.screen,self.field[i][j],
                    (j*PIXEL, i*PIXEL, PIXEL, PIXEL)
                )
# класс мини игры
class Fight_paint_game(Game):
    def play(self):
        super().play()
        clock = pygame.time.Clock()

        # таймер игры
        end_time = time.time() + 100
        
        # создание доски
        self.board=Fpg_board(
            self.view_port.WIDTH,
            self.view_port.HEIGHT,
            Colors.WHITE,
            self.screen
        )
        # создание игроков
        player1=Fpg_player(0,0,5,Colors.BLUE,self.board.width,self.board.height)
        player2=Fpg_player(0,0,5,Colors.RED,self.board.width,self.board.height)
        self.board.put_player(player1)
        self.board.put_player(player2)

        p1_key = pygame.K_s
        p2_key = pygame.K_RIGHT
        while self.is_play:
            # обработка нажатий клавишь
            for event in pygame.event.get():
                super().handle_exit_btn_click(event)
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
                
            # движение в зависимости от нажатых клавишь
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
                
            self.board.put_player(player1)
            self.board.put_player(player2)
            self.board.draw()
            
            # подсчет счетчиков
            player1_score = 0
            player2_score = 0
            for i in range(len(self.board.field)):
                for j in range(len(self.board.field[i])):
                    cell = self.board.field[i][j]
                    if cell == player1.color :
                        player1_score += 1
                    if cell == player2.color:
                        player2_score += 1
            
            # определение победителя по истечении таймера
            if time.time() >= end_time:
                if player1_score > player2_score:
                    self.show_message('Игрок 1 победил!', Colors.BLUE, duration=2.0, update=True)
                elif player2_score > player1_score:
                    self.show_message('Игрок 2 победил!', Colors.RED, duration=2.0, update=True)
                else:
                    self.show_message('Ничья', Colors.BLACK, duration=2.0, update=True)
                super().exit()
                continue

            # отображение статистики
            self.show_message(
                str(round(end_time - time.time())), 
                Colors.BLACK, center=(0,-280)
            )
            self.show_message(
                f'player1 - {player1_score} player2 - {player2_score}',
                Colors.BLACK, center=(0,-250)
            )
            
            pygame.display.update()
            clock.tick(60)



