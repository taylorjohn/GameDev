#   Things that neeeded to be imported
import pygame
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

# pre start up tiles?
Tile.pre_init(screen)

#   Create an object to help track time
clock = pygame.time.Clock()
#    This number controls the clock tick clock.tick(FPS)
FPS = 20
# keep count of frames
total_frames = 0
# loads background image dungeon
dungeon = pygame.image.load('dungeon.jpg')
# the player image called survivor 32x32 pixels
survivor = Survivor(32*2, 32*4)
# begins the while true loop
while True:
    # screen.blit(sourceSurface, destinationRect, optionalSourceRect)
    # this draws the background image dungeon to the screen at position 0,0
    screen.blit(dungeon, (0, 0))
    #   calls the zombie character object class spawn
    Zombie.spawn(total_frames, FPS)

    #   calls the zombie character object class movement
    Zombie.movement()

    #   calls the surivor or player character object class movement
    survivor.movement()

    # bullet stop after hitting zombie or going off screen
    Bullet.super_massive_jumbo_loop(screen)
    # a star algo to screen, player, total frames and frames per sec
    A_Star(screen, survivor, total_frames, FPS)

    # passes the interaction to the screen, player
    interaction(screen, survivor)

    # draws the survivor or player to the screen
    survivor.draw(screen)
    # draws the zombies to te screen
    Zombie.draw_zombies(screen)
    #   Update the full display Surface to the screen
    pygame.display.flip()
    # the clock tick is equal to the FPS frames per second 20
    clock.tick(FPS)
    # Add one to the total frames
    total_frames += 1
