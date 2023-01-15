import os
import pygame
from .Animation import AnimatedSprite
import glob


class Saw(pygame.sprite.Sprite):

    texture = None
    pickup_sound = None

    #this static method load all the textures for Saw animation and store as Class Variable
    @staticmethod
    def _load_resources():
        #checking whether saw textures are loaded or not
        if Saw.texture is None:
            Saw.texture=[]
            paths= glob.glob(os.path.join("Assets","Enemies",'Saw/*.png'))
            paths=sorted(paths, key=lambda x: int(os.path.basename(x).split(".")[0]))
            #loading all saw textures for animation
            for filename in paths: #assuming gif
                Saw.texture.append(pygame.image.load((filename)).convert_alpha())
                
        

    #Saw Class is use to Render Saw Animated Sprite on the screen at given position
    def __init__(self, x, y, groups):
        self._layer = 3
        self.rect = pygame.Rect(x, y, 90, 90)
        self.radius=49
        pygame.sprite.Sprite.__init__(self, groups)
        self._load_resources()
        #initializing animation sprite for saw
        self.animated_sprite = AnimatedSprite(60, loop=True,center=False)
        #loadining sprites from folder
        self.animated_sprite.load_from_images(Saw.texture)
        self.image=self.animated_sprite.get_frame()

    #this method update the Saw animation frame
    #animated_sprite object is called with the delta_time as the parameter. This updates the current frame of the animation to be rendered.
    def update(self, delta_time):
        self.animated_sprite.next_frame(delta_time)

   

    #this method draw current frame of Saw at given surface
    def render(self, surface, camera):
        self.animated_sprite.render(surface, camera.get_relative_pos(self.rect.x, self.rect.y))
    # animated_sprite object is called, passing the surface and camera position as parameters. This renders the current frame of the animation to the surface. 
    
        


class Moving_Saw(pygame.sprite.Sprite):

    texture = None
    pickup_sound = None

    #this static method load all the textures for Moving Saw animation and store as Class Variable
    @staticmethod
    def _load_resources():
        #checking whether saw textures are loaded or not
        if Saw.texture is None:
            Saw.texture=[]
            paths= glob.glob(os.path.join("Assets","Enemies",'Saw/*.png'))
            paths=sorted(paths, key=lambda x: int(os.path.basename(x).split(".")[0]))
            #loading all saw texture for animation
            for filename in paths: #assuming gif
                Saw.texture.append(pygame.image.load((filename)).convert_alpha())
                

        

    #Moving Saw Class is use to Render Moving Saw with Animated Sprite on the screen at given position
    def __init__(self, points, groups):
        self._layer = 3
        self.points=points
       
        self.current_point=points[0]
        self.rect = pygame.Rect(self.current_point.x, self.current_point.y, 90, 90)
        #loading points of patrolling
        if len(points)>1:
            self.target_index=1
            self.target_point=points[self.target_index]
        
        self.radius=49
        
        pygame.sprite.Sprite.__init__(self, groups)
        self._load_resources()
        #initializing animated sprites for moving saw
        self.animated_sprite = AnimatedSprite(60, loop=True,center=False)
        #loadining sprites from folder
        self.animated_sprite.load_from_images(Saw.texture)
        #setting movement duration counter and timer
        self.duration_counter=0
        self.duration=1
        self.image=self.animated_sprite.get_frame()

    #this method update the Moving Saw animation frame and calculating its position
    def update(self, delta_time):
        #updating saw position by time spend
        if self.duration_counter>=1:
            self.new_pos=self.current_point.lerp(self.target_point,1)
            self.rect = pygame.Rect(0, 0, 90, 90)
            self.rect.center=(self.new_pos)
            self.current_point=self.points[self.target_index]
            self.target_index=(self.target_index+1)%len(self.points)
            self.target_point=self.points[self.target_index]
            self.duration_counter=0
        else:
            self.new_pos=self.current_point.lerp(self.target_point,self.duration_counter)
            self.rect.center=(self.new_pos)
        #updating saw image to next frame
        self.animated_sprite.next_frame(delta_time)
        self.duration_counter+=delta_time*2
    
   
    #this method draw current frame of Moving Saw at given surface
    def render(self, surface, camera):
        self.animated_sprite.render(surface, camera.get_relative_pos(self.rect.x, self.rect.y))
        