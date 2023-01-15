import pygame
from .Collidable import Collidable


class ObstacleRect(Collidable):
    #ObstacleRect class is used to detect collision in the rect
    def __init__(self, x, y, width, height,static=False):
        Collidable.__init__(self, x, y, width, height)
        self.static=static

    #render the obstacle rect on screen
    def render(self, surface, camera):
        if self.static:
                
                self.rect.x=camera.camera_rect.x-50
                rect=self.rect
            
        


class ObstacleSlope(Collidable):
    #ObstacleRect class is used to detect collision of slop
    def __init__(self, x, y, width, height, direction='right'):
        if direction=="left":
            Collidable.__init__(self, x, y, width, height)
        else:
            Collidable.__init__(self, x, y-height, width, height)

        self.direction = direction
        self.slope = height / width
        if direction == 'left':
            self.slope *= -1

    #return overlap x of slop collider
    def get_overlap_x(self, rect: pygame.Rect) :
        # if not self.rect.colliderect(rect):
        return 0, None

    #return overlap y of slop collider
    def get_overlap_y(self, rect: pygame.Rect) :
        if not self.rect.colliderect(rect):
            return 0, None

        if self.slope > 0:
            if rect.right >= self.rect.right:  # top of slope condition
                return rect.bottom - self.rect.top, 'bottom'
            # calculating x wrt bottom left
            x = rect.right - self.rect.x

        else:
            if rect.left <= self.rect.left:  # top of slope condition
                return rect.bottom - self.rect.top, 'bottom'
            # calculating x wrt bottom left
            x = rect.left - self.rect.right

        y = self.rect.bottom - self.slope * x

        if y - rect.bottom > 0:
            return 0, None
        return rect.bottom - y, 'bottom'

    #render the obstacle slop on screen
    def render(self, surface, camera):

        r = camera.get_relative_rect(self.rect)
        if self.slope > 0:
            pt3 = r.topright
        else:
            pt3 = r.topleft
       

