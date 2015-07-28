#   Things that neeeded to be imported
import pygame
#import sys
from Funk import *
#   file that contains the tile class
from tileC import Tile
#   file that contains the object class
from object_classes import *
#   file that contains the event and interaction class
from interaction import interaction
#   file that contains the A star algo for enemy pathfinding
from A_Star import A_Star

#   Before you can do much with pygame, you will need to initialize it
pygame.init()
#   initialize fonts
pygame.font.init()
#   initialize the mixer module
pygame.mixer.init()
#   Load a music file for playback
pygame.mixer.music.load('./audio/zombie_theme.ogg')
#   Start the playback of the music stream
pygame.mixer.music.play(-1)
#   Initialize a window or screen for display
screen = pygame.display.set_mode((704, 448))  # 32, 32 tiles are 32 by 32

Tile.pre_init(screen)

#   Create an object to help track time
clock = pygame.time.Clock()
#    This number controls the clock tick clock.tick(FPS)
FPS = 20
total_frames = 0
dungeon = pygame.image.load('dungeon.jpg')
survivor = Survivor(32 * 2, 32 * 4)


while True:
    #   draw images to the screen screen.blit(sourceSurface, destinationRect, optionalSourceRect)
    #   this draws the background image dungeon to the screen at position 0,0
    screen.blit(dungeon, (0,0) )
    #   calls the zombie character object class spawn 
    Zombie.spawn(total_frames, FPS)
    #   calls the zombie character object class movement 
    Zombie.movement()
    #   calls the surivor or player character object class movement
    survivor.movement()

    Bullet.super_massive_jumbo_loop(screen)

    A_Star(screen, survivor, total_frames, FPS)
    interaction(screen, survivor)

    survivor.draw(screen)
    Zombie.draw_zombies(screen)
     
    #   Update the full display Surface to the screen
    pygame.display.flip()
    clock.tick(FPS)
    total_frames += 1