import pygame
import time
from colors import Colors

class Game():
    def __init__(self, viewPort, screen):
        self.is_play = False
        self.viewPort = viewPort
        self.screen = screen
    def play(self):
        self.is_play = True
        self.screen.fill(Colors.WHITE)
    def exit(self):
        self.is_play = False
    
    def showMessage(
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
        renderedText = font.render(message, True, colour)
        textArea = renderedText.get_rect()
        textArea.center = (
            self.viewPort.WIDTH//2+center[0],
            self.viewPort.HEIGHT//2+center[1]
        )
        self.screen.blit(renderedText, textArea)
        if update:
            pygame.display.update()
        if duration > 0:
          time.sleep(duration)
    def handleExitBtnClick(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit()
    
