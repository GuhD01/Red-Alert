import pygame
from .settings import *


class Camera:
    #Camera Class Track the horizontal and vertical movement of player and Leve
    def __init__(self):
        self.camera_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._half_width = self.camera_rect.width//2
        self._half_height = self.camera_rect.height//2

        self.init_x = self.camera_rect.centerx
        self.init_y = self.camera_rect.centery
        self.x = self.init_x
        self.y = self.init_y
        self.rect=pygame.Rect(self.x,self.y,self._half_width*2,self._half_height*2)
        self.rect.center=self.x,self.y

        self.smoothness = 10
        self.smoothness_limit = 0.2

        self.boundaries = None

    #this method set the boundries of the camera to move in
    def set_boundaries(self, rect):
        self.boundaries = rect

    #set the position of the camera
    def set_pos(self, pos):
        self.x, self.y = pos
        self.camera_rect.center = (self.x, self.y)
        self._limit_movement()  # don't move outside map boundaries

    #goto the position by given deltatime
    def move_to(self, pos, delta_time):
        x, y = pos
        dx = (x - self.x) * delta_time*30
        dy = (y - self.y) * delta_time*30
        
        if abs(dx) > 0 or abs(dy) > 0:
            if abs(dx) > self.smoothness_limit:
                dx /= self.smoothness
            if abs(dy) > self.smoothness_limit:
                dy /= self.smoothness
            # print(dx, dy)
            self.x += dx
            self.y += dy

        self.camera_rect.center = (self.x, self.y)
        if self.boundaries.x<self.camera_rect.x:
            self.boundaries.x=self.camera_rect.x
        self._limit_movement()      # don't move outside map boundaries

    #this method limit the movement of the camera by defined boundries
    def _limit_movement(self):
        if self.boundaries is not None:
            if self.camera_rect.left < self.boundaries.left:
                self.camera_rect.left = self.boundaries.left
            

            if self.camera_rect.top < self.boundaries.top:
                self.camera_rect.top = self.boundaries.top
            elif self.camera_rect.bottom > self.boundaries.bottom:
                self.camera_rect.bottom = self.boundaries.bottom

            self.x, self.y = self.camera_rect.center    

    #return relative position to camera position on scene of given position
    def get_relative_pos(self, x, y, parallax_multiplier=1):
        return (int(x - (self.x - self.init_x)*parallax_multiplier),
                int(y - (self.y - self.init_y)*parallax_multiplier))

    #return reverse relative position to camera position on scene of given position
    def get_reverse_relative_pos(self, X, Y, parallax_multiplier=1):
        return (int(X + (self.x - self.init_x)*parallax_multiplier),
                int(Y + (self.y - self.init_y)*parallax_multiplier))

    #return relative rect to camera position on scene of given rect
    def get_relative_rect(self, rect, parallax_multiplier=1):
        return pygame.Rect(self.get_relative_pos(rect.x, rect.y, parallax_multiplier),
                           (rect.width, rect.height))

