import pygame
import time
from colors import Colors

# базовый класс игр
class Game():
    def __init__(self, view_port, screen):
        self.is_play = False
        self.view_port = view_port
        self.screen = screen
    # запуск игры
    def play(self):
        self.is_play = True
        self.screen.fill(Colors.WHITE)
    # выход из игры
    def exit(self):
        self.is_play = False
    
    # отображение сообщения на скрине
    def show_message(
        self,
        message, 
        colour,
        center=(0,0),
        duration=0,
        size=25, font="dejavusansmono",
        update = False,
    ):
        if update:
            self.screen.fill(Colors.WHITE)
        font = pygame.font.SysFont(font, size)
        rendered_text = font.render(message, True, colour)
        text_area = rendered_text.get_rect()
        text_area.center = (
            self.view_port.WIDTH//2+center[0],
            self.view_port.HEIGHT//2+center[1]
        )
        self.screen.blit(rendered_text, text_area)
        if update:
            pygame.display.update()
        if duration > 0:
          time.sleep(duration)
    # обработка выхода
    def handle_exit_btn_click(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit()
    
