import pygame


class AnimatedSprite:
    #AnimatedSprite Class is to used to draw Animated Sprite with given frames
    def __init__(self, frame_rate, loop=True, offset=(0, 0),center=True):
        self.frame_rate = frame_rate
        self.frame_time = 1.0 / frame_rate
        self.loop = loop
        self.offset = offset
        self.tocenter=center
        self.images = []

        self.current_frame = 0
        self.time_elapsed = 0

    #load frames from spritesheet
    def load_from_spritesheet(self, texture, frame_size, frame_count):
        self.frame_count = frame_count
        self.width, self.height = frame_size

        x = 0
        y = 0
        nw, nh = texture.get_rect().size
        nw /= self.width
        nh /= self.height
        for i in range(frame_count):
            if x >= nw:
                x = 0
                y += 1
                if y >= nh:
                    raise Exception("Image out of bounds")

            self.images.append(
                texture.subsurface(pygame.Rect(self.width * x, self.height * y, self.width, self.height)))

            x += 1

    #load frames from folder
    def load_from_images(self, imgs):
        self.images = imgs
        self.frame_count = len(self.images)
        self.width, self.height = self.images[0].get_rect().size

    #resets the animation to initial state
    def reset_animation(self):
        self.current_frame = 0
        self.time_elapsed = 0

    #set texture to next frame
    def next_frame(self, delta_time):
        if self.loop or self.current_frame < self.frame_count - 1:
            self.time_elapsed += delta_time
            if self.time_elapsed >= self.frame_time:
                self.current_frame = (self.current_frame + 1) % self.frame_count
                self.time_elapsed = 0

    #check whether the animation is over or not
    def is_over(self):
        if self.loop or self.current_frame < self.frame_count - 1:
            return False
        return True

    #get current frame from all frames
    def get_frame(self):
        return self.images[self.current_frame]

    #render the current frame to its position
    def render(self, surface, pos):
        centeroffset=0
        if self.tocenter:
            centeroffset=self.images[0].get_width()/2-self.get_frame().get_width()/2
        surface.blit(self.get_frame(), (pos[0]+centeroffset + self.offset[0], pos[1] + self.offset[1]))


class Animation:
    class SingleStateSprite(AnimatedSprite):
        def __init__(self, texture, frames=1, frame_rate=6, default_facing='right', loop=True, offset=(0, 0),folder=False):
            if not folder:
                t_w, t_h = texture.get_rect().size
            AnimatedSprite.__init__(self, frame_rate, loop, offset)
            if folder:
                self.load_from_images(texture)
            else:
                self.load_from_spritesheet(texture, (t_w // frames, t_h), frames)
            self.default_facing = default_facing

        def get_frame(self, facing='right'):
            f = AnimatedSprite.get_frame(self)
            if self.default_facing != facing:
                return pygame.transform.flip(f, True, False)
            return f

    #Animation Class is used to Handle MultiState Animated Sprite
    def __init__(self):
        self.sprites = {}
        self.playing = None

    #this method add new state to states of Animation
    def add(self, name, texture, frames=1, frame_rate=6, facing='right', loop=True, offset=(0, 0),folder=False):
        self.sprites[name] = Animation.SingleStateSprite(texture, frames, frame_rate, facing, loop, offset,folder)

    #this method play the given animation state
    def play(self, name, delta_time):
        if (self.playing is None) or (self.playing != name):
            self.playing = name
            self.sprites[self.playing].reset_animation()
        else:
            self.sprites[self.playing].next_frame(delta_time)

    #get the size of animation
    def get_size(self, name):
        return self.sprites[name].width, self.sprites[name].height

    #check whether the animation is over or not
    def is_over(self):
        return self.sprites[self.playing].is_over()

    #get current frame from all frames
    def get_image(self,facing):
        if self.playing:
            return self.sprites[self.playing].get_frame(facing)
        else:
            return self.sprites[0].get_frame(facing)

    #render the current frame of current animation state to its position
    def render(self, surface, rect, facing, invincibility=0):
        if self.playing is not None:
            img = self.get_image(facing)
            img_rect = img.get_rect()
            y_offset = self.sprites[self.playing].offset[1]
            x_offset = self.sprites[self.playing].offset[0] * [-1, 1][facing == self.sprites[self.playing].default_facing]
            y = rect.y + y_offset
            if facing == self.sprites[self.playing].default_facing:
                x = rect.x
            else:
                x = rect.right - img_rect.width
            x = x + x_offset

            if invincibility == 0:
                surface.blit(img, (x, y))
            else:
                img_copy = img.copy()
                k = (int(invincibility * 1000) % 200) + 20
                img_copy.fill((k, k, k), special_flags=pygame.BLEND_ADD)
                surface.blit(img_copy, (x, y))

