import pygame
import os
from .Mouse import Mouse
from .. import settings


class Button:
    select_sound = None
    click_sound = None
    #this method load the texture of button
    @staticmethod
    def _load_resources():
        if Button.select_sound is None:
            Button.select_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'zipclick.wav'))
            Button.click_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'klick1.wav'))
            Button.click_sound.set_volume(0.5)

    #Button Class Handle Button look and functionality of image butthon
    def __init__(self, pos, size, image, callback, bttn_color=(48, 59, 77), text_color=(255,255,255)):
        self._load_resources()
        self.rect = pygame.Rect(pos, size)
        
        self._color = bttn_color
        # k = 20
        # self._color_hover = ((bttn_color[0]+k)%256, (bttn_color[1]+k)%256, (bttn_color[2]+k)%256)
        self._color_hover = (87, 149, 230)
        self._image=image
        self.image_rect=image.get_rect()
        self._text_color = text_color
        self._callback = callback
        self._mouse_in_rect = False
        self.image_rect.center=pos
    
    #render the texture of buttton 
    def render(self, surface):
        if self._mouse_in_rect:
           surface.blit(self._image, self.image_rect)

        else:
            surface.blit(self._image, self.image_rect)

    #handle the event when button clicked
    def handle_events(self, event):
        # if self.rect.collidepoint(*pygame.mouse.get_pos()):
        if self.image_rect.collidepoint(*Mouse.get_pos()):
            if self._mouse_in_rect is False:
                self.select_sound.play()
                self._mouse_in_rect = True

        else:
            self._mouse_in_rect = False
        if self._mouse_in_rect and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click_sound.play()
            self._callback()