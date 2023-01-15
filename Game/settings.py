import os



# General Settings
SCREEN_HEIGHT = 1200
SCREEN_WIDTH = int(SCREEN_HEIGHT * 16 / 9)

FINAL_HEIGHT = 720
FINAL_WIDTH = int(FINAL_HEIGHT * 16 / 9)




WIN_TITLE = "Red Alert"
FPS = 120

# Game Constants
jump_time = 0.75
jump_height = 365+200
t = jump_time
GRAVITY = int((2*jump_height)/(t*t))
PLAYER_JUMP_SPEED = int(1085)
PLAYER_WALK_SPEED = int(550)

# terminal velocity
TERMINAL_V = 130000000

MAX_COLLISION_STEP_SIZE = 8
MIN_SLOPE_DIST = 0


# Resource Folders

img_folder = os.path.join("Resources", 'images')
music_folder = os.path.join("Resources", 'music')
font_folder = os.path.join("Assets", 'Fonts')
levels_folder = os.path.join("Resources", 'levels')
