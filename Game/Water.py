import os
import pygame
from .Animation import AnimatedSprite
from . import settings
import glob


class Water(pygame.sprite.Sprite):

    texture = None
    splash_sound = None
    #this static method load all the textures for water animation and store as Class Variable
    @staticmethod
    def _load_resources():
        #checking whether water textures are loaded or not
        if Water.texture is None:
            Water.texture=[]
            paths= glob.glob(os.path.join("Assets",'Water/*.png'))
            paths=sorted(paths, key=lambda x: int(os.path.basename(x).split(".")[0]))
            #loading all water texture for animation
            for filename in paths: #assuming gif
                Water.texture.append(pygame.image.load((filename)).convert_alpha())
        #checking whether water splash sound is loaded or not
        if Water.splash_sound is None:
            Water.splash_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, "Retro PickUp Coin 04.wav"))
            Water.splash_sound.set_volume(0.2)

    #Water Class is use to Render Water Animated Sprite on the screen at given position
    def __init__(self, x, y, groups):
        self._layer = 3
        self.rect = pygame.Rect(x, y, 130, 200)
        pygame.sprite.Sprite.__init__(self, groups)
        self._load_resources()
        #initializing animation sprite for water
        self.animated_sprite = AnimatedSprite(17, loop=True,center=False)
        #loadining sprites from folder
        self.animated_sprite.load_from_images(Water.texture)

    #this method update the Water animation frame
    def update(self, delta_time):
        self.animated_sprite.next_frame(delta_time)

    
    #this method draw current frame of water at given surface
    def render(self, surface, camera):
        self.animated_sprite.render(surface, camera.get_relative_pos(self.rect.x, self.rect.y))


