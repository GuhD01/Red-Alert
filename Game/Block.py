import pygame
import pytmx
from .Physics import ObstacleRect,ObstacleSlope


class Block:
    #Block Class is to load and store the subsection of endless level in level generation
    def __init__(self,x,y, filename):
        #loading TMX file as TileMap
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        
        #Block Position and Size
        self.x=x
        self.y=y
        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

        #Spawn point for sprites
        self.coin_spawns = []
        self.water_spawns=[]
        self.saw_spawns=[]
        self.collidables = []
        self.moving_saws=[]
        self.spikes = []
        
        #block rendering surfaces
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.fgsurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    #this method render the Block Terrain and static Sprites
    def render(self, surface):
        for layer in self.tmx.layers:
            #rendering level image
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if image:
                        
                        surface.blit(image, ( x * self.tmx.tilewidth,
                                                    (y + 1) * self.tmx.tileheight - image.get_rect().height))
            
            #rendering Static Sprites
            if layer.name in ["Tiles","Environment","Spikes"]:
                for obj in layer:
                    
                    x,y=obj.x,obj.y
                    image=self.tmx.get_tile_image_by_gid( obj.gid)
                    self.surface.blit(image, (x , (y + 1)  ))
           
    #this method load all the objects from Block file and add their spawns to their collection
    def load_obstacles(self):
        #cycling through each layer of block
        for layer in self.tmx.layers:
            if layer.name.startswith("Moving Saws"):
                moving_saw=[]
                for obj in layer:
                    moving_saw.append([obj.x,obj.y])
                self.moving_saws.append(moving_saw)

                    
        #cycling through each object of tmx block
        for obj in self.tmx.objects:
            if obj.name == 'spawn':
                self.spawn_point = (obj.x, obj.y)
          
           
            elif obj.name == 'End':
                self.end=pygame.Rect(obj.x, obj.y, obj.width, obj.height)
         
            elif obj.name == "Saw":
                self.saw_spawns.append((obj.x, obj.y))
            
            elif obj.name == "coin":
                self.coin_spawns.append((obj.x, obj.y))
            elif obj.name == "water":
                self.water_spawns.append((obj.x, obj.y))
            elif obj.name == "Spike":
                self.spikes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
          
            elif obj.name=="collider":
                self.collidables.append(ObstacleRect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name=="colliderslopleft":
                self.collidables.append(ObstacleSlope(obj.x, obj.y, obj.width, obj.height,"left"))
            elif obj.name=="colliderslopright":
                self.collidables.append(ObstacleSlope(obj.x, obj.y, obj.width, obj.height))

    #this method return rendered image of block 
    def make_map(self):
        
        self.render(self.surface)
        self.load_obstacles()
        return self.surface.convert_alpha(),self.fgsurface.convert_alpha()
