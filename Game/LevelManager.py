import pygame
from .GameScene import GameScene
from .Player import Player

from .Coin import Coin
from .Saw import Saw,Moving_Saw
from .Spike import Spike
from .Water import Water
from .Block import Block
from .Camera import Camera
from .ParallaxBg import ParallaxLayer
from . import settings
import os
from .UI import Font, Mouse
from random import randint
from .UI import Button
from .Physics import ObstacleRect


class LevelManager(GameScene):
    #Constructor Method of Level Manager its Generate the Level as Player move on x axis
    #in constructor we are initailizing all the parameters and loading the start block that spawn on starting of the game
    def __init__(self, goto_scene):
        
        GameScene.__init__(self)
        #list of blocks for levelmanager to load from
        self.levels = [
            "Blocks/Start.tmx",
            "Blocks/Easy.tmx",
            "Blocks/Easy1.tmx",
            "Blocks/Plain.tmx",
            "Blocks/Medium.tmx",
            "Blocks/Medium1.tmx",
            "Blocks/Medium2.tmx",
            "Blocks/Medium3.tmx",
            "Blocks/Medium4.tmx",
            "Blocks/Hard1.tmx",
            "Blocks/Hard2.tmx",
            "Blocks/Hard3.tmx"
        ]
        

        self.score=0
        self.bestscore=0
        self._fadeout_timer = 0
        self._fadeout_time = 5
        self.all_sprites = pygame.sprite.LayeredUpdates()
        #loading background music
        pygame.mixer.music.load("Assets/Sounds/LoopMusic.mp3")
        pygame.mixer.music.set_volume(0)
        
        self.reset_Level()
        self.status="Menu"
        #adding player to all sprites group
        self.all_sprites.add(self.player)
        
        #loading UI icons
        self.parallax_fg = []
        play_icon=pygame.transform.smoothscale(pygame.image.load("Assets/UI/Play.png").convert_alpha(),(300,300))
        self.play_button=Button((settings.SCREEN_WIDTH/2,settings.SCREEN_HEIGHT/2),(300,300),play_icon,self.start_game)

        retry_icon=pygame.transform.smoothscale(pygame.image.load("Assets/UI/Restart.png").convert_alpha(),(300,300))
        self.retry_button=Button((settings.SCREEN_WIDTH/2,settings.SCREEN_HEIGHT/2),(300,300),retry_icon,self.reset_Level)

        exit_icon=pygame.transform.smoothscale(pygame.image.load("Assets/UI/Exit.png").convert_alpha(),(120,120))
        self.exit_button=Button((settings.SCREEN_WIDTH/2,(settings.SCREEN_HEIGHT/3)*2 +20),(120,120),exit_icon,lambda: goto_scene("quit"))

        self.visible_blocks=[self.blocks[0]]

        self.coin_icon=pygame.image.load("Assets/UI/Coin.png")
        self.coins_collected=0
        
    #this method will be called when player click the Play Button
    def start_game(self):
        self.status="Game"
        pygame.mixer.music.stop()      
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

    
    #this method will be called when player died
    def GameOver(self):
        self.status="GameOver"

    #this method reset the each parameter of level generation for new game and load starting block
    def reset_Level(self):
        self.status="Game"
        self.prev=[]
        self.player = Player((0, 0), groups=(self.all_sprites,))
        self.camera = Camera()
        
        self._fadeout_timer = 5
        #self._fadeout_time = 2

        # sprite groups
        self.player.coins=0
        self.waters = pygame.sprite.Group()
        self.saws = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()

        self.blocks=[]
        self._total_coins = 0
        
        self.x=0
        #reseting each sprite group
        self.all_sprites.empty()
        self.coins.empty()
        self.saws.empty()
        self.spikes.empty()
        
        
        self.visible_blocks=[]
        
        self.load_new_level(0)
        #adding collider so player cant go left of the level
        self.blocks[0][0].collidables.append(ObstacleRect(-50,0, 50, self.camera.camera_rect.height,True))
        self.camera.set_boundaries(self.block_img.get_rect())
        self.player.set_pos(self.blocks[0][0].spawn_point)
        
        
        
        #adding player to all sprite group
        self.all_sprites.add(self.player)
        if self.score>self.bestscore:
            self.bestscore=self.score
        self.score=0
        #background textures folder path
        parallax_folder = os.path.join("Assets","Backgrounds")
        self.textures = {
           }
        #loading background layers textures
        for i in [0,9,10]:
            self.textures[str(i)]= pygame.image.load(os.path.join(parallax_folder, f"{i}.png")).convert_alpha()
        
        # make parallax layers
        self.parallax_bg = []
        
        for i in [0,9,10]:
           self.parallax_bg.append(ParallaxLayer(self.textures[str(i)], i*0.08, self.camera, self.block.width, self.block.height))
        pygame.mixer.music.play(1)
    
    #load a block and initialing all its sprites and store it by given index 
    def load_new_level(self, level_num):
        #checking if new block is starting block
        if level_num!=0:
            if self.prev==[]:
                self.prev.append(level_num)
            else:
                a=self.prev[0]
                self.prev=[level_num,a]

            
        self.current_level=level_num
        
        #initializing Block
        self.block = Block(self.x,0,os.path.join( self.levels[level_num]))
        self.block_img,self.block_fg_img = self.block.make_map()
        #offsetting new block collider x by current block x
        for collider in self.block.collidables:
            collider.rect.x+=self.x
            
        self.block.end.x+=self.x

        # Initializing Water at water spawns
        for water_loc in self.block.water_spawns:
            Water(self.x+water_loc[0], water_loc[1], groups=(self.all_sprites, self.waters))
            
        # Initializing Saw at saw spawns
        
        for saw_loc in self.block.saw_spawns:
            Saw(self.x+saw_loc[0], saw_loc[1], groups=(self.all_sprites, self.saws))
        
        # Initializing Moving Saw at moving saw spawns
        for moving_saw in self.block.moving_saws:
            points=[]
            for point in moving_saw:
                pos=point
                pos[0]+=self.x
                points.append(pygame.Vector2(*pos))

            Moving_Saw(points,groups=(self.all_sprites,self.saws))

        # Initializing Spike at spikes spawns
        for spike_loc in self.block.spikes:
            Spike(self.x+spike_loc[0], spike_loc[1], groups=(self.all_sprites, self.spikes))
        
        # Initializing Coin at coins spawns
        for coin_loc in self.block.coin_spawns:
            Coin(self.x+coin_loc[0], coin_loc[1], groups=(self.all_sprites, self.coins))
            
        self.x+=self.block.width
        self.blocks.append([self.block,self.block_img,self.block_fg_img])
    #this method will render the background layer of the game on screen
    def render_backgrounds(self, surface):
        
        for i in range(len(self.parallax_bg)):
            self.parallax_bg[i].render(surface, self.camera)
    
    #this method will render the foreground layer of the game on screen
    def render_foregrounds(self, surface):
        for i in range(len(self.parallax_fg)):
            self.parallax_fg[i].render(surface, self.camera)

    #this method will render the HUD of the Game
    def render_hud(self, surface):
        x = 0
        y = surface.get_rect().height -118

        
        surface.blit(self.coin_icon,(30,30))
        Font.put_text(surface, "x"+str(self.player.coins), (188,25), (255, 255, 255),"u")

        Font.put_text(surface, str(self.bestscore)+ " m", (settings.SCREEN_WIDTH/2,60), (150, 150, 150),"huge",True)
        Font.put_text(surface, str(self.bestscore)+ " m", (settings.SCREEN_WIDTH/2,50), (255, 255, 255),"huge",True)
        Font.put_text(surface, str(self.score)+ " m", (settings.SCREEN_WIDTH/2,160), (150, 150, 150),"u",True)
        Font.put_text(surface, str(self.score)+ " m", (settings.SCREEN_WIDTH/2,150), (255, 255, 255),"u",True)

    #this method will render all the sprites of game and menu
    def render(self, surface):
        
        if Mouse.is_visible() and self.status=="Game":
            Mouse.set_visible(False)
        if not Mouse.is_visible() and self.status=="GameOver":
            Mouse.set_visible(True)
       
        
        self.render_backgrounds(surface)
        
        #rendering all visible blocks
        for block in self.visible_blocks:
            c=self.camera.camera_rect.copy()
            c.x-=block[0].x
            surface.blit(block[1], (0, 0), area=c)
            #rendering saw
            for saw in self.saws:
                saw.render(surface, self.camera)
            
           
        #rendering all sprites from all sprite layer(Group)
        for sprite in self.all_sprites:
            sprite.render(surface, self.camera)
        self.render_hud(surface)
        for block in self.blocks:
            for obs in block[0].collidables:
                obs.render(surface, self.camera)
        #rendering Start Menu Button
        if self.status=="Menu":
            self.play_button.render(surface)
            self.exit_button.render(surface)
        #rendering GameOVer Menu Button
        if self.status=="GameOver":
            self.retry_button.render(surface)
            self.exit_button.render(surface)

    #this method will update every entity of game for new frame of the game
    def update(self, delta_time):
        #checking whether the game is already over
        if self.status == "GameOver":
            self.player.update_particles(delta_time,self.blocks)
        
        if self.status=="Game":
            #updating camera position 
            self.camera.move_to(self.player.rect.center, delta_time)
            self.visible_blocks=[]
            #checking for visible block to camera
            for block in self.blocks:
                c=self.camera.camera_rect.copy()
                c.x-=block[0].x
                br=block[1].get_rect()
                br.x=block[0].x
                br=self.camera.get_relative_rect(br)
                
                if br.colliderect(self.camera.rect):
                    self.visible_blocks.append(block)
            #adding new block if camera collided with last block end collider
            if self.camera.get_relative_rect(self.blocks[-1][0].end).colliderect(self.camera.rect):
                while 1:
                    blockindex=randint(1,len(self.levels)-1)
                    if not blockindex in self.prev:
                        break
                print("loading new Chunk",blockindex)
                self.load_new_level(blockindex)
                
            self.player.update(delta_time, self.visible_blocks, self.waters,self.saws, self.spikes,self.coins,self)
        #updating coin ,saw and water sprites
        for coin in self.coins:
            coin.update(delta_time)
        for saw in self.saws:
            saw.update(delta_time)
        for water in self.waters:
            water.update(delta_time)

    #this method handles all the pygame event 
    def handle_events(self, event):
        #checking whether game is in Start Menu
        if self.status=="Menu":
            self.play_button.handle_events(event)
            self.exit_button.handle_events(event)
        #checking whether game is in GameOVer Menu
        if self.status=="GameOver":
            self.retry_button.handle_events(event)
            self.exit_button.handle_events(event)
       


