"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
 
Explanation video: http://youtu.be/5-SbFanyUkQ
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""
import pygame
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
gravity=.05
 


def clip(val, minval, maxval):
    return min(max(val, minval), maxval)
 
class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """
 
    def __init__(self, x, y, width, height, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super(Wall,self).__init__()
 
        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super(Ladder,self).__init__()
 
        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
ladder_set=pygame.sprite.Group([Ladder(360,50,20,500,WHITE)])
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls """
 
    # Set speed vector
    change_x = 0
    change_y = 0
 
    def __init__(self, x, y):
        """ Constructor function """
 
        # Call the parent's constructor
        super(Player,self).__init__()
 
        # Set height, width
        # self.image = pygame.Surface([15, 15])
        self.image=pygame.image.load('Mario_Sprite.png')
        self.image=pygame.transform.scale(self.image, (15,30))
        # self.image.fill(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        area = pygame.display.get_surface().get_rect()
        self.screenwidth, self.screenheight = area.width, area.height
        self.onladder=False
 
    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y
    def setspeed(self,x,y):
        self.change_x=x
        self.change_y=y
 
    def move(self, walls,ladders):
        """ Find a new position for the player """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if not self.onladder:
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
        
        #check to see if we're at any ladders
        ladder_list=pygame.sprite.spritecollide(self,ladders,False)
        # Move up/down
        self.rect.y += self.change_y

        if ladder_list!=[]:
            # if self.change_y > 0:
            #     self.onladder=True
            #     self.rect.bottom = ladder_list[0].rect.top
            # else:
            #     self.rect.top = ladder_list[0].rect.bottom
            if not self.onladder:
                self.change_y=min(self.change_y,0)
            self.onladder=True
        else:
            self.onladder=False
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
    
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if not self.onladder:
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom


        # if self.rect.left < 0 or self.rect.right > self.screenwidth:
        #     self.change_x = -self.change_x
        # if self.rect.top < 0 or self.rect.bottom > self.screenheight:
        #     self.change_y = -self.change_y
        self.rect.left = clip(self.rect.left, 0, self.screenwidth)
        self.rect.right = clip(self.rect.right, 0, self.screenwidth)        
        self.rect.top = clip(self.rect.top, 0, self.screenheight)
        self.rect.bottom = clip(self.rect.bottom, 0, self.screenheight) 
 
 
class Room(object):
    """ Base class for all rooms. """
 
    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None
 
    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
 
 
class Room1(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        super(Room1,self).__init__()
        # Make the walls. (x_pos, y_pos, width, height)
 
        # This is a list of walls. Each is in the form [x, y, width, height]
        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE],
                 [20, 0, 760, 20, WHITE],
                 [20, 580, 760, 20, WHITE],
                 # [390, 50, 20, 500, BLUE]
                ]

 
        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
 

 
class Room2(Room):
    """This creates all the walls in room 2"""
    def __init__(self):
        super(Room2,self).__init__()
 
        walls = [[0, 0, 20, 250, RED],
                 [0, 350, 20, 250, RED],
                 [780, 0, 20, 250, RED],
                 [780, 350, 20, 250, RED],
                 [20, 0, 760, 20, RED],
                 [20, 580, 760, 20, RED],
                 [190, 50, 20, 500, GREEN],
                 [590, 50, 20, 500, GREEN]
                ]
 
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
 
 
class Room3(Room):
    """This creates all the walls in room 3"""
    def __init__(self):
        super(Room3,self).__init__()
 
        walls = [[0, 0, 20, 250, PURPLE],
                 [0, 350, 20, 250, PURPLE],
                 [780, 0, 20, 250, PURPLE],
                 [780, 350, 20, 250, PURPLE],
                 [20, 0, 760, 20, PURPLE],
                 [20, 580, 760, 20, PURPLE]
                ]
 
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
 
        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)
 
        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, WHITE)
            self.wall_list.add(wall)
 
 
def main():
    """ Main Program """
 
    # Call this function so the Pygame library can initialize itself
    pygame.init()
 
    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])
 
    # Set the title of the window
    pygame.display.set_caption('mario_climber')
 
    # Create the player paddle object
    player = Player(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
 
    rooms = []
 
    room = Room1()
    rooms.append(room)
 
    room = Room2()
    rooms.append(room)
 
    room = Room3()
    rooms.append(room)
 
    current_room_no = 0
    current_room = rooms[current_room_no]
 
    clock = pygame.time.Clock()
 
    done = False
 
    while not done:
 
        # --- Event Processing ---
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-3, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(3, 0)
                if event.key == pygame.K_UP:
                    player.setspeed(player.change_x, -3)
                if event.key == pygame.K_DOWN:
                    player.setspeed(player.change_x, 3)
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(3, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-3, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 3)
                if event.key == pygame.K_DOWN:
                    player.setspeed(player.change_x, 0)
            print player.change_x,player.change_y

            
        
        # else:
        #     player.setspeed()
        # --- Game Logic ---
 
        player.move(current_room.wall_list,ladder_set)
        if not player.onladder:
            player.changespeed(0,gravity)
 
        # if player.rect.x < -15:
        #     if current_room_no == 0:
        #         current_room_no = 2
        #         current_room = rooms[current_room_no]
        #         player.rect.x = 790
        #     elif current_room_no == 2:
        #         current_room_no = 1
        #         current_room = rooms[current_room_no]
        #         player.rect.x = 790
        #     else:
        #         current_room_no = 0
        #         current_room = rooms[current_room_no]
        #         player.rect.x = 790
 
        # if player.rect.x > 801:
        #     if current_room_no == 0:
        #         current_room_no = 1
        #         current_room = rooms[current_room_no]
        #         player.rect.x = 0
        #     elif current_room_no == 1:
        #         current_room_no = 2
        #         current_room = rooms[current_room_no]
        #         player.rect.x = 0
        #     else:
        #         current_room_no = 0
        #         current_room = rooms[current_room_no]
        #         player.rect.x = 0
 
        # --- Drawing ---
        screen.fill(BLACK)
 
        
        current_room.wall_list.draw(screen)
        ladder_set.draw(screen)
        movingsprites.draw(screen)
 
        pygame.display.flip()
 
        clock.tick(60)
 
    pygame.quit()
 
if __name__ == "__main__":
    main()