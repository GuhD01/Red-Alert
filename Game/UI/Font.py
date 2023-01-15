import pygame
import os
from .. import settings


class Font:
    _font = {}
    antialiasing = True
    #Font CLass handles the font side of text that we show on the screen
    @staticmethod
    def init():
        Font._font["normal"] = pygame.font.Font(os.path.join(settings.font_folder, 'Baloo-Regular.ttf'), 24)
        Font._font["small"] = pygame.font.Font(os.path.join(settings.font_folder, 'Baloo-Regular.ttf'), 14)
        Font._font["big"] = pygame.font.Font(os.path.join(settings.font_folder, 'Baloo-Regular.ttf'), 40)
        Font._font["huge"] = pygame.font.Font(os.path.join(settings.font_folder, 'Baloo-Regular.ttf'), 60)
        Font._font["u"] = pygame.font.Font(os.path.join(settings.font_folder, 'Baloo-Regular.ttf'), 80)

    #get the text surface of given text
    @staticmethod
    def get_render(text, color=(255, 255, 255), size='normal'):
        return Font._font[size].render(text, Font.antialiasing, color)

    #Draw the Text on the Screen with given text , size and color
    @staticmethod
    def put_text(surface, text, pos, color=(255, 255, 255), size='normal',center=False):
        f = Font.get_render(text, color, size)
        position=pos
        if center:
            position=(pos[0]-f.get_width()/2,pos[1]-f.get_height()/2)
        surface.blit(f, position)
