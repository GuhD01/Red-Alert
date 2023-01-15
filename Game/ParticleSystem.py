import pygame
from random import choice
from .Physics import RigidBody
class Particle(RigidBody):
    #Particle Class is draw particle on screen at simulated position
    def __init__(self, x,y,vx,vy,color,size) -> None:
        RigidBody.__init__(self, x,y, size,size)
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x,self.y-size,size*2,size*2)
        self.rect.topleft=self.x-size,self.y-size
        self.vx=vx
        self.vy=vy
        self.color=color
        self.size=size
    
    #update the particle position
    def update(self,delta_time,collidables):
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        self.vx*=0.95
        self.vy*=0.95
        coll= self.do_physics(delta_time,collidables,False)
        if coll["top"] or coll["bottom"]:
            self.vy=0
            self.vx=0
        if coll["left"] or coll["right"]:
            self.vy=0
            self.vx=0
    
    #render the particle on screen
    def render(self,surface,camera):

        pygame.draw.circle(surface,self.color,camera.get_relative_pos(*self.rect.topleft),self.size)
        

class ParticleSystem:
    #ParticleSystem Spawn the Particle and manage their states
    def __init__(self,x,y,n,velocity_x_range,velocity_y_range,colors,sizes) -> None:
        self.particles=[]
        for i in range(n):
            self.particles.append(Particle(x,y,choice(velocity_x_range),choice(velocity_y_range),choice(colors),choice(sizes)))
    
    #update all of it particles position
    def update(self,delta_time,collidables):
        for particle in self.particles:
            particle.update(delta_time,collidables)

    #render all of it particle on screen
    def render(self,surface,camera):
        for particle in self.particles:
            particle.render(surface,camera)