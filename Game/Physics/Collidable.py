import pygame


class Collidable:
    #Collidable class is used as collider for 2D physics
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    #return overlap x of Collidable
    def get_overlap_x(self, rect: pygame.Rect):
        # return overlap value, direction or None
        if not self.rect.colliderect(rect):
            return 0, None
        if self.rect.x < rect.x < self.rect.right < rect.right:
            return rect.x - self.rect.right, 'left'
        elif rect.x < self.rect.x < rect.right < self.rect.right:
            return rect.right - self.rect.x, 'right'
        else:
            
            return 0, None
    
    #return overlap y of Collidable
    def get_overlap_y(self, rect: pygame.Rect):
        # return overlap value, direction or None
        if not self.rect.colliderect(rect):
            return 0, None

        if self.rect.y < rect.y < self.rect.bottom < rect.bottom:
            return rect.y - self.rect.bottom, 'top'
        elif rect.y < self.rect.y < rect.bottom < self.rect.bottom:
            return rect.bottom - self.rect.y, 'bottom'
        else:
            
            return 0, None
            
