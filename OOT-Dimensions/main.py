import pygame, sys
from random import randint
from gui import nbut
from pygame import mixer
import sounds
from time import sleep
mixer.init()
from pygame.locals import *
import sprites

class Tree(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image1 = pygame.image.load(sprites.Link.kid.empty.frontstay).convert_alpha()
        self.image = pygame.transform.scale(self.image1, (64, 80))
        
        self.image_sprites = []
    
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        self.Mouse_x, self.Mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.image1 = pygame.image.load(sprites.Link.kid.empty.backstay).convert_alpha()
            self.image = pygame.transform.scale(self.image1, (64, 80))
            
            
            
            
        elif keys[pygame.K_o]:
            print(self.Mouse_x, self.Mouse_y)
            
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.image1 = pygame.image.load(sprites.Link.kid.empty.frontstay).convert_alpha()
            self.image = pygame.transform.scale(self.image1, (64, 80))
            
            
        elif keys[pygame.K_9]:
                drawhitbox()
        else:
            self.direction.y = 0

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.image1 = pygame.image.load(sprites.Link.kid.empty.rightstay).convert_alpha()
            self.image = pygame.transform.scale(self.image1, (64, 80))
            
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.image1 = pygame.image.load(sprites.Link.kid.empty.leftstay).convert_alpha()
            self.image = pygame.transform.scale(self.image1, (64, 80))
        
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset 
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        # ground
        self.ground_surf = pygame.image.load('assets/Map1.jpg').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
        self.ground_surf = pygame.transform.scale(self.ground_surf, (1920, 1080))

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.2

        # zoom 
        self.zoom_scale = 1
        self.internal_surf_size = (2500,2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self,target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] : self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d] : self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())

        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border,mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border,mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
                pygame.mouse.set_pos((left_border,top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
                pygame.mouse.set_pos((right_border,top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
                pygame.mouse.set_pos((left_border,bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
                pygame.mouse.set_pos((right_border,bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x,top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x,bottom_border))

        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.1

    def custom_draw(self,player):
        
        # self.center_target_camera(player)
        # self.box_target_camera(player)
        # self.keyboard_control()
        

        self.internal_surf.fill('#71ddee')

        # ground 
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf,ground_offset)

        # active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image,offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

        self.display_surface.blit(scaled_surf,scaled_rect)


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.event.set_grab(True)

# setup 
moving = False
devmodevar = False

imgdev = pygame.image.load('assets/dev.jpg').convert_alpha()

imgdev = pygame.transform.scale(imgdev, (64, 80))
imgdev.convert()
hitboxdraw = False
camera_group = CameraGroup()
rect1 = imgdev.get_rect()
rect1.center = 1920//2, 1080//2
rectdev = imgdev.get_rect()

player = Player((1304,364
                 ),camera_group)
class gui:
    carImg1 = pygame.image.load('assets/guibu1.png')
    guibutton1 = pygame.transform.scale(carImg1, (356, 156))
    carImg2 = pygame.image.load('assets/guihe3.png')
    guiheart3 = pygame.transform.scale(carImg2, (168, 54))
class enemies(object):
    carImg1 = pygame.image.load('assets/Kokiriforestm1.png')
    guibutton1 = pygame.transform.scale(carImg1, (64, 80))
    hitbox = (1558, 543, 64, 80)

obstacle = pygame.Rect(400, 200, 80, 80)
for i in range(20):
    random_x = randint(1000,2000)
    random_y = randint(1000,2000)
    Tree((random_x,random_y),camera_group)
def drawhitbox():
    pygame.draw.rect(screen, (255,0,0), enemies.hitbox,2)
    pygame.draw.rect(screen,(0,255,255), player.rect,2)
def devmode():
    screen.blit(imgdev, rect1)
    pygame.draw.rect(screen, (0,0,255), rect1, 2)
mixer.music.load(sounds.music.LostWoods)
mixer.music.play()
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.K_o:
            
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    
    keys = pygame.key.get_pressed()
    screen.fill('#71ddee')

    camera_group.update()
    
    camera_group.custom_draw(player),	nbut(1558, 543, screen, enemies.guibutton1)
    
    nbut(1422,101,screen , gui.guibutton1 )
    nbut(152,85, screen, gui.guiheart3 )
   
    if player.rect.colliderect(enemies.hitbox):
        pygame.draw.rect(screen, (255,0,0), player.rect, 4)
    
    elif keys[pygame.K_F10]:
        hitboxdraw = True
    elif keys[pygame.K_F8]:
        print(rect1)
    elif keys[pygame.K_F9]:
        devmodevar= True
    
        
    elif devmodevar == True:
        devmode()
    elif hitboxdraw == True:
        drawhitbox()
    elif keys[pygame.K_F9]:
        pygame.draw.rect(screen, (0,0,255), rect1, 2)
    elif event.type == MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                moving = True
                
 
        # Set moving as False if you want 
        # to move the image only with the 
        # mouse click
        # Set moving as True if you want 
        # to move the image without the 
        # mouse click
    elif event.type == MOUSEBUTTONUP:
            moving = False
 
        # Make your image move continuously
    elif event.type == MOUSEMOTION and moving:
            rect1.move_ip(event.rel)
            
        # Set moving as False if you want 
        # to move the image only with the 
        # mouse click
        # Set moving as True if you want 
        # to move the image without the 
        # mouse click
    
 
        # Make your image move continuously
    
    
    pygame.display.update()
    clock.tick(60)
