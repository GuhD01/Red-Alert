import os
import pygame
from .Physics import Collidable
from .Animation import AnimatedSprite
import glob


class Coin(pygame.sprite.Sprite):

    texture = None
    pickup_sound = None

    #this static method load all the textures for Coin animation and store as Class Variable
    @staticmethod
    def _load_resources():
        #checking whether coin textures are loaded or not
        if Coin.texture is None:
            Coin.texture=[]
            paths= glob.glob(os.path.join("Assets",'Coin/*.png'))
            paths=sorted(paths, key=lambda x: int(os.path.basename(x).split(".")[0]))
            #loading all coin texture for animation
            for filename in paths: #assuming gif
                Coin.texture.append(pygame.image.load((filename)).convert_alpha())
        #checking whether coin sound is loaded or not
        if Coin.pickup_sound is None:
            Coin.pickup_sound = pygame.mixer.Sound(os.path.join("Assets","Sounds", "Coin.wav"))
            Coin.pickup_sound.set_volume(0.2)

    #Coin Class is use to Render Coin Animated Sprite on the screen at given position
    def __init__(self, x, y, groups):
        self._layer = 3
        self.rect = pygame.Rect(x, y, 64, 64)
        pygame.sprite.Sprite.__init__(self, groups)
        self._load_resources()
        #initializing animation sprite for coin
        self.animated_sprite = AnimatedSprite(20, loop=True)
        #loadining sprites from folder
        self.animated_sprite.load_from_images(Coin.texture)

    #this method update the Coin animation frame
    def update(self, delta_time):
        self.animated_sprite.next_frame(delta_time)

    #this method will be called when player collided with Coin 
    def pickup(self):
        #playing the coin sound
        Coin.pickup_sound.play()
        #destroying animation sprite
        self.kill()
    
    #this method draw current frame of Coin at given surface
    def render(self, surface, camera):
        self.animated_sprite.render(surface, camera.get_relative_pos(self.rect.x, self.rect.y))
        
