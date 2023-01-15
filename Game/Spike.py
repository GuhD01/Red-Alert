import os
import pygame



class Spike(pygame.sprite.Sprite):

    texture = None
    pickup_sound = None
    #this static method load texture for Spike and store as Class Variable
    @staticmethod
    def _load_resources():
        
        if Spike.texture is None:
            #loading spike texture
            path= os.path.join("Assets","Enemies",'Spike_Up.png')
            
            Spike.texture=(pygame.image.load((path)).convert_alpha())
                
    #Spike Class is used to Render Spike Sprite on the screen at given position
    def __init__(self, x, y, groups):
        self._layer = 3
        self.rect = pygame.Rect(x, y, 70, 70)
        #initializing sprite for spike
        pygame.sprite.Sprite.__init__(self, groups)
        #loadining spike resources
        self._load_resources()
        self.image=Spike.texture
    
    #this method draws the Spike Texture at given surface
    def render(self, surface, camera):  
        surface.blit(Spike.texture,camera.get_relative_pos(self.rect.x,self.rect.y))
        


