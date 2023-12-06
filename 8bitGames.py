#импорт библиотек и модулей
import pygame
import button
from fight_paint import FightPaintGame
from colors import Colors
from viewPort import ViewPort

#инициализация pygame 
pygame.init()

screen = pygame.display.set_mode((ViewPort.WIDTH, ViewPort.HEIGHT))
pygame.display.set_caption("8-bit games")


#загрузка изоброжений кнопок
resume_img = pygame.image.load("images/button_new_game.png").convert_alpha()
quit_img = pygame.image.load("images/button_exit.png").convert_alpha()
back_img = pygame.image.load('images/back.png').convert_alpha()
snake_button_img = pygame.image.load("images/snake.png").convert_alpha()
paint_fight_button_img = pygame.image.load("images/paint_fight.png").convert_alpha()
tanks_button_img = pygame.image.load("images/tanks.png").convert_alpha()

#присвоение координат кнопкам
resume_button = button.Button(304, 125, resume_img, 1)
quit_button = button.Button(334, 250, quit_img, 1)
back_button = button.Button(332, 500, back_img, 1)
snake_button = button.Button(300, 50, snake_button_img, 1)
paint_fight_button = button.Button(300, 200, paint_fight_button_img, 1)
tanks_button = button.Button(300, 350, tanks_button_img, 1)

#меню
run = True
menu_state = "main"
while run:
  screen.fill(Colors.LIME)
  #проверка состояние меню
  if menu_state == "main":
    #отрисовка кнопок меню и их выбор
    if resume_button.draw(screen):
      menu_state = "games"
    if quit_button.draw(screen):
      run = False
    #выбор игры и их запуск
  if menu_state == "games":
    if snake_button.draw(screen):
      snake_game() 
    if paint_fight_button.draw(screen):
      game = FightPaintGame(ViewPort, screen)
      game.play()
    if tanks_button.draw(screen):
      tanks()
    if back_button.draw(screen):
      menu_state = "main"   
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()