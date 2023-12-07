#импорт библиотек и модулей
import pygame
import button
from snake import Snake_game
from fight_paint import Fight_paint_game
from duel import Duel_game
from colors import Colors
from view_port import View_port

class Main:
    def run(self):
        #инициализация pygame 
        pygame.init()

        self.screen = pygame.display.set_mode((View_port.WIDTH, View_port.HEIGHT))
        pygame.display.set_caption("8-bit games")


        #загрузка изоброжений кнопок
        resume_img = pygame.image.load("images/button_new_game.png").convert_alpha()
        quit_img = pygame.image.load("images/button_exit.png").convert_alpha()
        back_img = pygame.image.load('images/back.png').convert_alpha()
        snake_button_img = pygame.image.load("images/snake.png").convert_alpha()
        paint_fight_button_img = pygame.image.load("images/paint_fight.png").convert_alpha()
        duel_button_img = pygame.image.load("images/duel.png").convert_alpha()

        #присвоение координат кнопкам
        self.resume_button = button.Button(304, 125, resume_img, 1)
        self.quit_button = button.Button(334, 250, quit_img, 1)
        self.back_button = button.Button(332, 500, back_img, 1)
        self.snake_button = button.Button(300, 50, snake_button_img, 1)
        self.paint_fight_button = button.Button(300, 200, paint_fight_button_img, 1)
        self.duel_button = button.Button(300, 350, duel_button_img, 1)

        #меню
        run = True
        menu_state = "main"
        while run:
            self.screen.fill(Colors.LIME)
            #проверка состояние меню
            if menu_state == "main":
                #отрисовка кнопок меню и их выбор
                if self.resume_button.draw(self.screen):
                    menu_state = "games"
                if self.quit_button.draw(self.screen):
                    run = False
                #выбор игры и их запуск
            if menu_state == "games":
                game = None
                if self.snake_button.draw(self.screen):
                    game = Snake_game(View_port, self.screen)
                if self.paint_fight_button.draw(self.screen):
                    game = Fight_paint_game(View_port, self.screen)
                if self.duel_button.draw(self.screen):
                    game = Duel_game(View_port, self.screen)
                if self.back_button.draw(self.screen):
                    menu_state = "main"
                if game != None:
                    game.play()
            
            # событие выхода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            # обновление экрана
            pygame.display.update()

#запуск игры
Main().run()