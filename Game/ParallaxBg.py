import pygame


class ParallaxLayer:
    #ParallaxLayer Class is Draw different depth layered image 
    def __init__(self, texture, parallax_multiplier, camera, map_width, map_height):
        self.parallax_multiplier = parallax_multiplier
        self.texture = texture
        self._scaled_texture = self._resize(texture, parallax_multiplier, camera, map_width, map_height)
        self.map_width=map_width
        self.camera=camera
        self.n=-1
    
    #this method resize the layer image
    def _resize(self, texture, parallax_multiplier, camera, map_width, map_height):
        w, h = texture.get_rect().size
        c_w, c_h = camera.camera_rect.size
        #calculating bg size
        scaled_h = (map_height - c_h) * parallax_multiplier + c_h
        scaled_w = w * scaled_h / h

        texture = pygame.transform.smoothscale(texture, (int(scaled_w), int(scaled_h)))
        
        return texture

    #draw the layer image
    def render(self, surface, camera):
        if camera.get_relative_pos(0, 0, self.parallax_multiplier)[0]<-self.map_width*self.n:
            self.n+=1
        
        #rendering bg layers
        surface.blit(self._scaled_texture, camera.get_relative_pos((self.n)*self.camera.camera_rect.width, 0, self.parallax_multiplier))
        surface.blit(self._scaled_texture, camera.get_relative_pos((self.n-1)*self.camera.camera_rect.width, 0, self.parallax_multiplier))
      
