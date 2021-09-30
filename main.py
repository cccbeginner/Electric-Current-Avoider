import sys
import pygame
from pygame import Rect, mouse
from pygame import surface
from pygame.locals import QUIT

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (127, 127, 127)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    NOTHING = (255, 255, 255, 0)

background_color = Color.NOTHING
wall_color = Color.BLACK
path_color = Color.NOTHING
ball_save_color = Color.GREEN
ball_collide_color = Color.RED
ball_radius = 21
start_point = (40, 680)

class Ball(pygame.sprite.Sprite):

    STATUS_UNSTARTED = 111111
    STATUS_SAVED = 222222
    STATUS_CRACKED = 333333

    def __init__(self, color_save, color_crack, start_pos=(0,0)):
        self.pos = start_pos
        self.surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.color_save = color_save
        self.color_crack = color_crack
        self.status = Ball.STATUS_UNSTARTED
        self.mask = pygame.mask.Mask(self.surface.get_size())
        self.rect = self.mask.get_rect()
        self.update()

    def update(self):
        self.surface.fill(background_color)
        if self.status == Ball.STATUS_UNSTARTED:
            color = self.color_save
        elif self.status == Ball.STATUS_SAVED:
            color = self.color_save
            self.pos = mouse.get_pos()
        elif self.status == Ball.STATUS_CRACKED:
            color = self.color_crack
        pygame.draw.circle(self.surface, color, self.pos, ball_radius, 0)
        self.mask = pygame.mask.from_threshold(self.surface, color, (1,1,1,255))
        self.rect = self.mask.get_rect()
    
    def update_status(self, new_status):
        self.status = new_status
        self.update()

class Wall(pygame.sprite.Sprite):
    def __init__(self, img_file, wall_color):
        self.surface = pygame.image.load(img_file).convert_alpha()
        self.mask = pygame.mask.from_threshold(self.surface, wall_color, (1,1,1,255))
        self.rect = self.mask.get_rect()

class Button(pygame.sprite.Sprite):
    def __init__(self, text, text_size, text_color, back_color, point):
        font = pygame.font.SysFont('Comic Sans MS', text_size)
        text_surface = font.render(text, False, text_color)
        self.surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.surface.fill(background_color)
        self.rect = Rect(point[0], point[1], text_surface.get_width(), text_surface.get_height())
        pygame.draw.rect(self.surface, back_color, self.rect)
        self.surface.blit(text_surface, point)
    def mouse_touched(self):
        x,y = mouse.get_pos()
        if self.rect.collidepoint(x,y):
            return True
        else:
            return False

def setup_screen_size():
    global WIDTH, HEIGHT
    img = pygame.image.load('map.jpg')
    WIDTH, HEIGHT = img.get_size()

def main():

    pygame.init()
    pygame.font.init()

    setup_screen_size()
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('電流急急棒')

    # 設定時鐘
    clock = pygame.time.Clock()

    # define stuffs here
    ball = Ball(ball_save_color, ball_collide_color, (start_point))
    wall = Wall('map.jpg', wall_color)
    
    # make startup button
    start_btn = Button('START', 60, Color.YELLOW, Color.BLUE, (start_point[0]-20, start_point[1]-20))

    while True:

        # renew rate: 60 times/sec
        clock.tick(60)
        
        # background
        window_surface.fill(background_color)

        # wall_surface
        window_surface.blit(wall.surface, (0, 0))

        # ball surface
        window_surface.blit(ball.surface, (0, 0))

        # start btn surface
        if ball.status != Ball.STATUS_SAVED:
            window_surface.blit(start_btn.surface, (0, 0))

        # test collision
        if ball.status == Ball.STATUS_SAVED:
            if pygame.sprite.collide_mask(wall, ball):
                print("collide")
                ball.update_status(Ball.STATUS_CRACKED)
            else:
                print("save")
                ball.update()
        

        # Update only the area that we specified with the `update_rect`.
        pygame.display.update((0,0,WIDTH,HEIGHT))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.mouse_touched():
                    ball.update_status(Ball.STATUS_SAVED)
        

if __name__ == "__main__":
    main()