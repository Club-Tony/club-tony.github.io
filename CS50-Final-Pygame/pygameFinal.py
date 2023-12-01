# import pygame library, also sys to allow for smooth program termination and cleanup operations
import pygame
import sys

# initialize all pygame modules
pygame.init()

# set clock and fps so game runs at intended speed, set night cycle clock
clock = pygame.time.Clock()
FPS = 60

nighttime = 0
fade_black = 0

# get display info/set default width/height of game screen
resolution = pygame.display.Info()

screen_width = 1920
screen_height = 1080

# if user resolution is lower than default, change it
if resolution.current_w < 1920 and resolution.current_h < 1080:
    screen_width = resolution.current_w
    screen_height = resolution.current_h

# set display, name display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sunset Run")

# Boolean fullscreen check variable so I can toggle between fs and windowed in game loop
fullscreen_toggle = False

# define game variables(scrolling)
scroll = 0

# load sprite
sprite = pygame.image.load("Player/1.png").convert_alpha()
sprite_width = sprite.get_width()
sprite_height = sprite.get_height()
# include another copy of sprite width and height for use later in game loop when adjusting - 
# window size since sprite_width and sprite_height values get changed
initial_sprite_width = sprite.get_width()
initial_sprite_height = sprite.get_height()

# set adjust percentage for height of sprite adjustment
y_adjust_percentage = 0.09
y_adjust = int(screen_height * y_adjust_percentage)

# define sprite_position for this initial draw (pre using fullscreen toggle)
sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height - sprite_height - y_adjust)
    
# draw sprite
def draw_sprite(screen_width, screen_height, sprite_position):
    
    # resize sprite to account for toggle fullscreen
    width_adjust = int(sprite_width * (screen_width / 1920))
    height_adjust = int(sprite_height * (screen_height / 1080))   
    resized_sprite = pygame.transform.scale(sprite, (width_adjust, height_adjust))
    
    # use sprite_position to draw sprite
    screen.blit(resized_sprite, sprite_position)

# load backgrounds starting with ground:
# note: loading all 1 by 1 instead of list so I have full control over individual .png scrolling speed
ground_image = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L5.png").convert_alpha()

# get ground background width and height(do this for others also)
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# load water with mountains
water_mountains = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L3.png").convert_alpha()
water_mountains_width = water_mountains.get_width()
water_mountains_height = water_mountains.get_height()

# load water with trees
water_trees = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L4.png").convert_alpha()
water_trees_width = water_trees.get_width()
water_trees_height = water_trees.get_height()

# load custom L2 (clouds) note: made clouds with GIMP software to adjust transparency so it worked seamlessly
clouds = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L2.png").convert_alpha()
clouds_width = clouds.get_width()
clouds_height = clouds.get_height()

# load mountains background (L1.png)
far_mountains = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L1.png").convert_alpha()
far_mountains_width = far_mountains.get_width()
far_mountains_height = far_mountains.get_height()

# load sun 
sun = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L6.png").convert_alpha()
sun_width = sun.get_width()
sun_height = sun.get_height()
            
# draw images including resized versions of these to implement later for fullscreen toggle
# range of 101 is arbitrary, just making sure it's enough without being too much
def draw_far_mountains(images):
    for x in range(101):
        screen.blit(images[0], ((x * images[0].get_width()) - scroll * 0.4, 0))

def draw_ground(images):
    for x in range(101):
        screen.blit(images[4], ((x * images[4].get_width()) - scroll * 6, 0))

def draw_water_mountains(images):
    for x in range(101):
        screen.blit(images[2], ((x * images[2].get_width()) - scroll * 1.2, 0))

def draw_water_trees(images):
    for x in range(101):
        screen.blit(images[3], ((x * images[3].get_width()) - scroll * 1.2, 0))

def draw_clouds(images):
    for x in range(101):
        screen.blit(images[1], ((x * images[1].get_width()) - scroll * 0.2, 0))

def draw_sun(images):
    for x in range(101):
        screen.blit(images[5], ((x * images[5].get_width()) - scroll * 0.00001, 0))
        
# make list of loaded images to simplify transform.scale
images_list = [far_mountains, clouds, water_mountains, water_trees, ground_image, sun]

# resize images with screen toggle: blank list, the for loop for transform/scale/append
def resize_images(images, screen_width, screen_height):
    resized_images = []
    for image in images:
        resized_image = pygame.transform.scale(image, (screen_width, screen_height))
        resized_images.append(resized_image)
    return resized_images

resized_images = resize_images(images_list, screen_width, screen_height)

# NIGHTTIME
# transparent tint with same size as screen (double parentheses for representing rgb values)
night_tint = pygame.Surface((screen_width, screen_height))

# dark blue color for tint 
night_tint.fill((0, 0, 128))

# alpha value of tint to set transparency, create variable to use in if statement in game loop
# max_opacity = 218 so so it matches max alpha_value
max_opacity = 218

# fade to black
black_tint = pygame.Surface((screen_width, screen_height))

# game over text
# create font object None makes it pygame default font, otherwise need to use loaded font, 2nd arg = size
game_over = pygame.font.Font(None, 50)

# ...

# GAME LOOP, with forever repeating while loop (when run = true)
run = True
while run:
    # cap frame rate
    clock.tick(FPS)
    
    # increment night cycle
    nighttime += 11.03 
    
    # min function takes any # of arguments, returns the smallest of arguments provided
    color_value = min(nighttime, 128)
    alpha_value = min(nighttime, 218)
    
    # update night tint with color and alpha value on each iteration
    night_tint.fill((0, 0, color_value))
    night_tint.set_alpha(alpha_value)
    
    # increment fade to black when night is at its darkest
    if alpha_value >= max_opacity:
        # if statement so fade_black doesn't exceed 255
        if fade_black < 255:
            fade_black += 1
        
    black_alpha_value = min(fade_black, 255) # 255 for full opacity
        
    # update black tint
    black_tint.fill((0, 0, 0))
    black_tint.set_alpha(black_alpha_value)
    
    # event handler for ending loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Keybinds: 
        # make a limit so you can only go left a certain amount (since images only properly scroll right)
        # 0 for left so can't go left unless already travelled to the right a given amount
        # 192,000 for right because this pixel count matches the set range for x of 100 (# of layers side-by-side)    
        # loop with pygame.keydown so keybind will only trigger once when key is pressed
        elif event.type == pygame.KEYDOWN:
            
            # system controls:
            # quit
            if event.key == pygame.K_ESCAPE:
                run = False
            
            # pygame.key.get_mods to check the state of modifier keys, i.e. the alt keys
            elif event.key in [pygame.K_F11] or (event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                
                # not makes this False boolean variable True
                fullscreen_toggle = not fullscreen_toggle 
                
                # toggle windowed/fullscreen
                if fullscreen_toggle:
                    screen_width = 1920 * 0.5
                    screen_height = 1080 * 0.5
                        
                elif resolution.current_w < 1920 and resolution.current_h < 1080:
                    screen_width = resolution.current_w
                    screen_height = resolution.current_h
                        
                else:
                    screen_width = 1920
                    screen_height = 1080

                # draw background layers for if fullscreen button toggled
                # resized images variable for including images list with screen height and width
                resized_images = resize_images(images_list, screen_width, screen_height)
                
                # Adjust sprite position if screen size is reduced
                # start by specifically adjusting its height since it's scuffed
                if screen_width < 1920:
                    sprite_height = 130
                    # calculate what the corresponding new width would be to avoid distoring the image
                    initial_sprite_aspect_ratio = initial_sprite_width / initial_sprite_height
                    sprite_width = sprite_height * initial_sprite_aspect_ratio
                else:
                    sprite_width = initial_sprite_width
                    sprite_height = initial_sprite_height
                    
                if screen_width == 1920 * 0.5 and screen_height == 1080 * 0.5:
                    sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height * 0.78)  
                else: 
                    sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height - sprite_height - y_adjust)
                    
                # set display mode after determining screen width/height changes, but before drawing
                pygame.display.set_mode((screen_width, screen_height))          
                         
                draw_far_mountains(resized_images)
                draw_sun(resized_images)
                draw_clouds(resized_images)
                draw_water_mountains(resized_images)
                draw_water_trees(resized_images)
                draw_ground(resized_images)
                # draw sprite
                draw_sprite(screen_width, screen_height, sprite_position)
            
    # enable double-buffering (for smoother rendering), start by clearing screen with a white or black bg
    # note: double buffering didn't end up being the fix for the earlier image blending issue but keeping it in anyway
    screen.fill((0, 0, 0))
    
    # draw background layers (these are how they're drawn by default, before the user toggles fullscreen)
    draw_far_mountains(resized_images)
    draw_sun(resized_images)
    draw_clouds(resized_images)
    draw_water_mountains(resized_images)
    draw_water_trees(resized_images)    
    draw_ground(resized_images)
    # draw sprite
    draw_sprite(screen_width, screen_height, sprite_position)

    # draw night tint and fade to black: 0, 0 makes it draw from the top left of the screen
    screen.blit(night_tint, (0, 0))
    screen.blit(black_tint, (0, 0))

    # update display (.flip since implemented double buffering)
    pygame.display.flip()

# draw the game over text outside the main loop
game_over_render = game_over.render("You're lost, and can't find your way back", True, (255, 255, 255))
screen.blit(game_over_render, (0, 0))
pygame.display.flip()

# wait for a few seconds to display the game over text
pygame.time.delay(5000)

# if the loop ends, the game quits, sys.exit for smooth program termination and cleanup operations   
pygame.quit()
sys.exit()