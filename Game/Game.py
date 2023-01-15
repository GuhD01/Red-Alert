import pygame
from . import settings
from .LevelManager import LevelManager
from .UI import Mouse, Font



pygame.init()
class Game:
    #Game class initalize the pygame display and load the scene
    def __init__(self):
        pygame.init()

        self.display_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.fullscreen_flag = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.fullscreen = False
        self._scale_screen = False

        self.display = pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT), self.display_flags)
        self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(settings.WIN_TITLE)

        self.exit_game = False
        Font.init()
        Mouse.init()

        
        self._scene = None
        self._scene_stack = []
        self.goto_scene("level_manager")

        

        self.clock = pygame.time.Clock()

    #load the scene by initialing the Level Genator
    def goto_scene(self, scene_name, *other_args):
        if scene_name == "quit":
            self.exit_game = True
     
        else:
            self.level=LevelManager(self.goto_scene)

    #render the Game screen to pygame display
    def render(self):
        self.level.render(self.screen)

      

        self.display.blit(pygame.transform.scale(self.screen, self.display.get_rect().size), (0, 0))
        Mouse.render(self.display)

        pygame.display.flip()

    #this method starts the mainloop of game
    def run(self):
        while not self.exit_game:

            self.render()
            
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                
                else:
                    self.level.handle_events(event)

            self.clock.tick(settings.FPS)
            delta_time = self.clock.get_time() / 1000
            self.level.update(delta_time)
        self.quit()
    
    #this method exit the game
    def quit(self):
        pygame.quit()