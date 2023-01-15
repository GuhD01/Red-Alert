import pygame
import os
from .Physics import RigidBody
from .Animation import Animation
from . import settings
import glob
from .ParticleSystem import ParticleSystem
from random import choice

class Player(RigidBody, pygame.sprite.Sprite):
    #States Class to store player state
    class State:
        idle = 0
        walking = 1
        running = 2
        jumping = 3
        falling = 4
        

    textures = None
    sounds = None
    

    #this method load all the textures of PLayer Animation
    def _load_resources(self):
       
        print("loading player textures")
        idle_texture=[]
        run_texture=[]
        #loading player textures
        idle_paths=sorted(glob.glob(os.path.join("Assets/Player",'Idle/*.png')), key=lambda x: int(os.path.basename(x).split(".")[0]))
        run_paths=sorted(glob.glob(os.path.join("Assets/Player",'Run/*.png')), key=lambda x: int(os.path.basename(x).split(".")[0]))
        for filename in idle_paths: #assuming gif
            idle_texture.append(pygame.image.load((filename)).convert_alpha())
        
        for filename in run_paths: #assuming gif
            run_texture.append(pygame.image.load((filename)).convert_alpha())
        
        #player texture dict
        Player.textures = {
            'player-idle': idle_texture,
            'player-run': run_texture,
            'player-jump': pygame.image.load(os.path.join("Assets/Player/Jump", 'Jump.png')).convert_alpha(),
            'player-fall': pygame.image.load(os.path.join("Assets/Player/Jump", 'Fall.png')).convert_alpha(),
            
        }
        #initializing Animation Object for player
        self.animation = Animation()
        #adding animtion states to player animation
        self.animation.add(self.State.idle, Player.textures['player-idle'], 12, 10, 'right', offset=(-4, -0),folder=True)
        self.animation.add(self.State.walking, Player.textures['player-run'], 18, 40, 'right', offset=(-10, -0),folder=True)
        self.animation.add(self.State.jumping, Player.textures['player-jump'], 1, 1, 'right', offset=(-10, -0))
        self.animation.add(self.State.falling, Player.textures['player-fall'], 1, 1, 'right', offset=(-10, -0))
        #checking whether player sounds are loaded or not
        if Player.sounds is None:
            #loading player sounds
            Player.sounds = {

                'jump': pygame.mixer.Sound(os.path.join("Assets","Sounds", 'Jump.wav')),
                'hurt': pygame.mixer.Sound(os.path.join(settings.music_folder, 'Sound_1.wav')),
                'water':pygame.mixer.Sound(os.path.join("Assets", "Sounds" ,  'Water splash.wav')),
                'spike':pygame.mixer.Sound(os.path.join("Assets", "Sounds" ,  'Spike.wav')),
                'saw':pygame.mixer.Sound(os.path.join("Assets", "Sounds" ,  'Saw Sawing.wav')),
                'walk':[]
            }
            #loading player sounds for footsteps
            for i in glob.glob(os.path.join("Assets/Sounds",'Footsteps/*.wav')):
                sound=pygame.mixer.Sound(i)
                sound.set_volume(0.1)
                Player.sounds["walk"].append(sound)
            
    #PLayer Class Manage all States of PLayer character
    def __init__(self, spawn_point, groups):
        #loading resources of the player
        self._load_resources()
        self.state = self.State.idle
        self.radius=61
       

        self._layer = 2
        RigidBody.__init__(self, *spawn_point, 70, 75)
        self.radius=5
        self.pushable = False
        pygame.sprite.Sprite.__init__(self, groups)

        #setting player attributes
        self.jump_speed = settings.PLAYER_JUMP_SPEED
        self.walk_speed = settings.PLAYER_WALK_SPEED
        self.climb_speed = settings.PLAYER_WALK_SPEED*2//3
        self.can_jump = True
        self.facing = self.animation.sprites[self.state].default_facing

        #setting player coins count and dead state
        self.coins = 0
        self.dead = False
        
        self.death_water=False
        #setting player image from animation current frame
        self.image=self.animation.get_image(self.facing)
        self.footstep_timer=0

    #sets the player position
    def set_pos(self, pos):
        self.rect.topleft = pos

    #hnadle all events for player character
    def _get_input(self):
        self.v_x = 0
        
        keys = pygame.key.get_pressed()
        #checking event for jump
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()
        
        #checking event for running to left
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) :
            self.v_x += -1
        #checking event for running to right
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) :
            self.v_x += 1
        #setting player facing by its velocity
        if self.v_x < 0 and self.facing != 'left':
            self.facing = 'left'
        if self.v_x > 0 and self.facing != 'right':
            self.facing = 'right'

        self.v_x *= self.walk_speed

    #this mwthod called when jump button pressed
    def jump(self):
        #checking whether player is on ground or not
        if self.can_jump:
            #playing jump sound
            Player.sounds["jump"].set_volume(0.5)
            Player.sounds['jump'].play()
            #setting player y velocity to its jump velocity
            self.v_y = -self.jump_speed
            self.can_jump = False
            self.ledge_grabbing = False
            self.climbing = False

    #this method simulate the physics of player and check its collision with Obstacles
    def do_physics(self, delta_time, collidables):
        colliding = RigidBody.do_physics(self, delta_time, collidables)
        #checking if player collided on bottom
        if colliding['bottom']:
            self.can_jump = True
        return colliding

    #calculate colliding point of collider with player
    def _obstacle_check(self, pt, collidables):
        #checking for collision with all colliders
        for obs in collidables:
            if obs.rect.collidepoint(pt):
                return True
        return False

    #change the state of player
    def _change_states(self):
        #setting player states by its x and y velocity
        if self.v_y < 0:
            self.state = self.State.jumping
        elif self.v_y > 100:
            self.state = self.State.falling
            self.can_jump = False
        else:
            if abs(self.v_x) > 0 and self.state != self.State.walking:
                self.state = self.State.walking
            elif abs(self.v_x) == 0 and self.state != self.State.idle:
                self.state = self.State.idle

    #Handle the collision of Saws with Player
    def _saw_collision(self,saw_group,level):
        
        collided_Saws = pygame.sprite.spritecollide(self, saw_group, False,pygame.sprite.collide_mask)
        #checking whether any saw collided with player or not
        if collided_Saws !=[]:

            #playing player saw collision sound
            self.sounds["saw"].set_volume(0.4)
            self.sounds["saw"].play()
            pygame.mixer.music.stop()
            self.dead=True
            #setting Game state to GameOver
            level.GameOver()
    
    #Handle the collision of SPikes with Player
    def _spikes_collision(self,spikes,level):
        collided_Spikes = pygame.sprite.spritecollide(self, spikes, False,pygame.sprite.collide_mask)
        #checking whether any spike collided with player or not
        if collided_Spikes !=[]:
            
            #playing player spike collision sound
            self.sounds["spike"].set_volume(0.4)
            self.sounds["spike"].play()
            pygame.mixer.music.stop()
            
            self.dead=True
            #setting Game state to GameOver
            level.GameOver()
    
    #Handle the collision of Coins with Player
    def _coin_collision(self, coin_group):
        coins = pygame.sprite.spritecollide(self, coin_group, False)
        #checking whether any coin collided with player or not
        for coin in coins:
            coin.pickup()
            self.coins += 1

    #Handle the collision of Water with Player
    def _water_collision(self, water_group,level):
        waterevet = pygame.sprite.spritecollide(self, water_group, False)
        #checking whether any water collided with player or not
        if waterevet !=[]:
            
            #playing player water collision sound
            self.sounds["water"].play()
            pygame.mixer.music.stop()
            self.dead=True
            #setting Game state to GameOver
            level.GameOver()
            self.death_water=True
   
   #update the Particle of player or water on  screen
    def update_particles(self, delta_time, blocks):
        colliders=[]
        allblocks=blocks
        if len(blocks)>1:
            allblocks=blocks[1:]
            first=blocks[0]
            for collidable in first[0].collidables:
                colliders.append(collidable)
        #checking the collision between blocks colliders and particles
        for block in allblocks:
            for collidable in block[0].collidables:
                colliders.append(collidable)
        self.death_particle.update(delta_time,colliders)
   
   #update the frame of player and check for its collision with other
    def update(self, delta_time, blocks,waters,saws,spikes, coin_group,level):
        self.image=self.animation.get_image(self.facing)
        #checking if player is not jumping
        if self.v_x!=0 and self.can_jump:
            self.footstep_timer+=delta_time
            if  self.footstep_timer>0.8:
                choice(self.sounds["walk"]).play()
                self.footstep_timer=0
        self.footstep_timer+=delta_time
        #updating the score
        if level.score<int((level.camera.get_relative_rect(self.rect).x+self.rect.x)/500)-1:
            level.score=int((level.camera.get_relative_rect(self.rect).x+self.rect.x)/500)-1
        
        
        self._coin_collision(coin_group)
        self._water_collision(waters,level)
        
        
        self._saw_collision(saws,level)
        self._spikes_collision(spikes,level)
        colliders=[]
        allblocks=blocks
        #checking if only start block is spawnd
        if len(level.blocks)>1:
            allblocks=blocks
            first=level.blocks[0]
            for collidable in first[0].collidables:
                
                colliders.append(collidable)
        #checking the collision between blocks colliders and player
        for block in allblocks:
           
            for collidable in block[0].collidables:
                colliders.append(collidable)
        
        
        self._get_input()
        self.do_physics(delta_time, colliders)
        self._change_states()
        self.animation.play(self.state, delta_time)
        #checking if player is dead
        if self.dead:
            rect=self.rect
            #checking whether to spawn blook particles or water particle
            if self.death_water:
                colors=["#84f4f4","#3cbff0","#51d2f4"]
                pos=rect.center[0],rect.bottom
                speedx=list(range(-10,10))
                speedy=list(range(-90,0))
                count=40
            else:
                colors=["#ef5350","#cc3f3c"]
                pos=rect.center[0],rect.center[1]
                speedx=list(range(-20,20))
                speedy=list(range(-20,10))
                count=20
            #initializing particle system to render blood or water particle
            self.death_particle = ParticleSystem(*pos,count,speedx,speedy,colors,list(range(10,20)))

    #render the player texture animation on screen
    def render(self, surface, camera):
        #checking if player is not dead
        if not self.dead:
            self.animation.render(surface, camera.get_relative_rect(self.rect), self.facing)
        else:
            #rendering player dead particles
            self.death_particle.render(surface,camera)

        

           

