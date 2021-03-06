#   Things that neeeded to be imported
import pygame
from tileC import Tile
from random import randint 


#character class
class Character(pygame.Rect):
    #size of the character rect same as tile size
    width, height = 32, 32

    def __init__(self, x, y):
        #character location x & y and size on tiles
        self.tx, self.ty = None, None
        pygame.Rect.__init__(self, x, y, Character.width, Character.height)

    def __str__(self):
        return str(self.get_number())

    # sets up the next tile
    def set_target(self, next_tile):
        if self.tx == None and self.ty == None:
            self.tx = next_tile.x
            self.ty = next_tile.y

    def get_number(self):
        # made into int
        return ((self.x // self.width) + Tile.H) + ((self.y // self.height) * Tile.V)

    def get_tile(self):

        return Tile.get_tile(self.get_number())

    def rotate(self, direction, original_img):

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                south = pygame.transform.rotate(original_img, 90) # CCW
                self.img = pygame.transform.flip(south, False, True)

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = pygame.transform.rotate(original_img, 90) # CCW

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = pygame.transform.flip(original_img, True, False)

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = original_img

class Zombie(Character):

    List = []
    spawn_tiles = (9,42,91,134,193,219,274)
    original_img = pygame.image.load('images/zombie.png')
    health = 100


    def __init__(self, x, y):

        self.direction = 'w'
        self.health = Zombie.health
        self.img = Zombie.original_img
        Character.__init__(self, x, y)
        Zombie.List.append(self)

    @staticmethod
    def update(screen, survivor):

        for zombie in Zombie.List:
            
            screen.blit(zombie.img, (zombie.x, zombie.y))

            if survivor.x % Tile.width == 0 and survivor.y % Tile.height == 0:
                if zombie.x % Tile.width == 0 and zombie.y % Tile.height == 0:

                    tn = survivor.get_number()

                    N = tn + -(Tile.V)
                    S = tn +  (Tile.V)
                    E = tn +  (Tile.H)
                    W = tn + -(Tile.H)

                    NSEW = [N, S, E, W, tn]

                    if zombie.get_number() in NSEW:
                        survivor.health -= 5

            if zombie.health <= 0:
                Zombie.List.remove(zombie)

            if zombie.tx is not None and zombie.ty is not None:  # Target is set

                X = zombie.x - zombie.tx
                Y = zombie.y - zombie.ty

                vel = 4
                if X < 0: # --->
                    zombie.x += vel
                    zombie.rotate('e', Zombie.original_img)

                elif X > 0: # <----
                    zombie.x -= vel
                    zombie.rotate('w', Zombie.original_img)

                if Y > 0: # up
                    zombie.y -= vel
                    zombie.rotate('n', Zombie.original_img)

                elif Y < 0: # dopwn
                    zombie.y += vel
                    zombie.rotate('s', Zombie.original_img)

                if X == 0 and Y == 0:
                    zombie.tx, zombie.ty = None, None
 
    @staticmethod
    def spawn(total_frames, FPS):
        if total_frames % (FPS) == 0:

            if total_frames % (FPS * 6) == 0:

                r = randint(0, 2)
                sounds = [pygame.mixer.Sound('audio/zs1.ogg'),
                        pygame.mixer.Sound('audio/zs2.ogg'),
                        pygame.mixer.Sound('audio/zs3.ogg')]
                sound = sounds[ r ]
                sound.play()

            r = randint(0, len(Zombie.spawn_tiles) - 1)
            tile_num = Zombie.spawn_tiles[r]
            spawn_node = Tile.get_tile(tile_num)
            Zombie(spawn_node.x, spawn_node.y)


class Survivor(Character):

    guns_img =[pygame.image.load('images/pistol.png'),
                pygame.image.load('images/shotgun.png'),
                pygame.image.load('images/automatic.png')]

    def __init__(self, x, y):

        self.health = 1000
        self.current = 0 # 0 -> pistol, 1 -> shotgun, 2 -> automatic
        self.direction = 'w'
        self.img = pygame.image.load('images/survivor_w.png')

        Character.__init__(self, x, y)

    def get_bullet_type(self):

        if self.current == 0:
            return 'pistol'
        elif self.current == 1:
            return 'shotgun'
        elif self.current == 2:
            return 'automatic'

    def movement(self):
        # self target x-axis & y-axis
        if self.tx is not None and self.ty is not None: # Target is set
            #   x-axis is a horizontal line x position minus the target x pos
            X = self.x - self.tx
            #   y-axis is a vertical line y position minus the target y pos
            Y = self.y - self.ty
            #   velocity in the game
            vel = 8
            #   If horizontal position is less then zero
            if X < 0: # --->
                # move horizontal at velocity
                self.x += vel
            #   if horizontal ppsition is greater then zero
            elif X > 0: # <----
                #   move horizontal at neg velocity
                self.x -= vel
            #   If vertical position is less then zero
            if Y > 0: # up
                #   move vertical at velocity
                self.y -= vel
            elif Y < 0: # dopwn
                self.y += vel

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    def draw(self, screen):

        screen.blit(self.img, (self.x, self.y))

        h = self.width / 2
        img = Survivor.guns_img[self.current]
        # If direction is w display screen image horizontal post,
        #vert pos plus self.width divided by 2
        if self.direction == 'w':
            screen.blit(img, (self.x, self.y + h))

        elif self.direction == 'e':
            img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x + h, self.y + h))            

        elif self.direction == 's':
            img = pygame.transform.rotate(img, 90) # CCW
            screen.blit(img, (self.x + h, self.y + h))            

        elif self.direction == 'n':
            south = pygame.transform.rotate(img, 90)
            img = pygame.transform.flip(south, False, True)
            screen.blit(img, (self.x + h, self.y - h))

    def rotate(self, direction):

        path = 'images/survivor_'
        png = '.png'

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = pygame.image.load(path + self.direction + png)

class Bullet(pygame.Rect):
    
    width, height = 7, 10
    List = []

    imgs = {'pistol': pygame.image.load('images/pistol_b.png'),
            'shotgun': pygame.image.load('images/shotgun_b.png'),
            'automatic': pygame.image.load('images/automatic_b.png') }

    gun_dmg = {'pistol': (Zombie.health // 3) + 1,
                'shotgun': Zombie.health // 2,
                'automatic': (Zombie.health // 6) + 1 }

    def __init__(self, x, y, velx, vely, direction, type_):

        if type_ == 'shotgun' or type_ == 'pistol':
            try:
                
                dx = abs(Bullet.List[-1].x - x)
                dy = abs(Bullet.List[-1].y - y)

                if dx < 50 and dy < 50 and type_ == 'shotgun':
                    return

                if dx < 30 and dy < 30 and type_ == 'pistol':
                    return

            except: pass


        self.type = type_
        self.direction = direction
        self.velx, self.vely = velx, vely

        if direction == 'n':
            south = pygame.transform.rotate(Bullet.imgs[type_], 90) # CCW
            self.img = pygame.transform.flip(south, False, True)

        if direction == 's':
            self.img = pygame.transform.rotate(Bullet.imgs[type_], 90) # CCW

        if direction == 'e':
            self.img = pygame.transform.flip(Bullet.imgs[type_], True, False)

        if direction == 'w':
            self.img = Bullet.imgs[type_]

        pygame.Rect.__init__(self, x, y, Bullet.width, Bullet.height)

        Bullet.List.append(self)

        # draw
        # update
        # collision --> zombies, tiles

    def offscreen(self, screen):
        # defines off screen demensions
        if self.x < 0:
            return True
        elif self.y < 0:
            return True
        elif self.x + self.width > screen.get_width(): # -->
            return True
        elif self.y + self.height > screen.get_height():
            return True
        return False


    @staticmethod
    def super_massive_jumbo_loop(screen):

        for bullet in Bullet.List:
            #bullet direction and speed
            bullet.x += bullet.velx
            bullet.y += bullet.vely
            #display bullet to screen x & y position
            screen.blit(bullet.img, (bullet.x, bullet.y))
            # if the bullet goes off display area remove it
            if bullet.offscreen(screen):
                Bullet.List.remove(bullet)
                continue
            # if bullet collides with zombie remove i
            for zombie in Zombie.List:
                if bullet.colliderect(zombie):

                    """
                    The same bullet cannot be used to kill
                    multiple zombies and as the bullet was 
                    no longer in Bullet.List error was raised
                    """

                    zombie.health -= Bullet.gun_dmg[bullet.type]                
                    Bullet.List.remove(bullet)
                    break

            for tile in Tile.List:
                
                if bullet.colliderect(tile) and not(tile.walkable):
                    try:
                        Bullet.List.remove(bullet)
                    except:
                        break # if bullet cannot be removed, then GTFO





































































































































