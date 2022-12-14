import pygame as pg
import CursedEngine as ce
from math import floor
from random import randint
from pygame.locals import *



grid_size = 10
width = 400
cell_size = width/grid_size
panel_height = 50
height = width+panel_height

offset = (0,panel_height)

# COLORS 
BLACK = (0,0,0)
BROWN = (215, 184, 153)
LIGHT_BROWN = (229, 194, 159)
GREEN = (162, 209, 73)
LIGHT_GREEN = (170, 215, 81)

flag_img = pg.image.load("flag.png")
flag_img = pg.transform.scale(flag_img, (cell_size, cell_size))

clock_img = pg.image.load("clock.png")
clock_img = pg.transform.scale(clock_img, (panel_height/1.5, panel_height/1.5))


screen = pg.display.set_mode((width,height))
pg.display.set_caption('Saper')

class Game_Object():
    
    Objects = []
    Coliders = []

    def Draw(self):
        # pg.draw.rect(screen,self.color,self.Rect)
        screen.blit(self.Img,self.Rect.topleft)

    def Update(delta=1):
        for Object in Game_Object.Objects:
            Object.Update(delta)
    
    def move(self, movement):
        self.Rect.x += movement[0]
        for object in Game_Object.Coliders:
            if object == self: continue
            if self.Rect.colliderect(object.Rect):
                if self.VelocityX > 0:
                    self.VelocityX = 0
                    self.Rect.right = object.Rect.left

                elif self.VelocityX < 0:
                    self.VelocityX = 0
                    self.Rect.left = object.Rect.right

        self.colide_with_ground = False
        self.Rect.y += movement[1]
        for object in Game_Object.Coliders:
            if object == self: continue
            if self.Rect.colliderect(object.Rect):
                if self.VelocityY > 0:
                    self.colide_with_ground = True
                    self.VelocityY = 0
                    self.Rect.bottom = object.Rect.top

                elif self.VelocityY < 0:
                    self.VelocityY = 0
                    self.Rect.top = object.Rect.bottom
    
    def remove(self):
        if self in Game_Object.Coliders:
            Game_Object.Coliders.remove(self)
        if self in Game_Object.Objects:
            Game_Object.Objects.remove(self)
    
    @staticmethod
    def remove_all():
        while len(Game_Object.Objects) != 0:
            for x in Game_Object.Objects:
                x.remove()

class Grid(Game_Object):

    def __init__(self) -> None:
        super().__init__()
        self.cell_size = 32
        self.grid = []
        self.cell_neighbours = []
    
    def draw_grid(self):
        color_alter = 0
        for x in range(grid_size):
            color_alter+=1
            if color_alter > 1:
                color_alter = 0
            for y in range(grid_size):
                block = pg.Rect(x*self.cell_size+offset[0],y*self.cell_size+offset[1],cell_size,cell_size)
                color_alter+=1
                full_color = GREEN
                empty_color = BROWN
                if color_alter == 1:
                    full_color = GREEN
                    empty_color = LIGHT_BROWN
                else:
                    full_color = LIGHT_GREEN
                    empty_color = BROWN
                if self.grid[x][y] == 1:
                    pg.draw.rect(screen,full_color,block)
                elif self.grid[x][y] == 2:
                    pg.draw.rect(screen,full_color,block)
                elif self.grid[x][y] == 0:
                    pg.draw.rect(screen,empty_color,block)
                if color_alter > 1:
                    color_alter = 0

    def generate_grid(self,map_size,block_size):
        self.grid = []
        self.cell_neighbours = []
        self.cell_size = block_size
        for width in range(map_size[0]):
            self.grid.append([])
            self.cell_neighbours.append([])
            for height in range(map_size[1]):
                self.grid[width].append([])
                self.cell_neighbours[width].append([])
                self.grid[width][height] = 1
    
    def in_grid_range(self,position):
        if position[0] < 0 or position[0] >= len(self.grid):
            return False
        if position[1] < 0 or position[1] >= len(self.grid[0]):
            return False
        return True

    def get_neighbours(self,position):
        neighbours = []
        if self.in_grid_range((position[0]-1,position[1]-1)):
            neighbours.append(self.grid[position[0]-1][position[1]-1])
        if self.in_grid_range((position[0],position[1]-1)):
            neighbours.append(self.grid[position[0]][position[1]-1])
        if self.in_grid_range((position[0]+1,position[1]-1)):
            neighbours.append(self.grid[position[0]+1][position[1]-1])
        if self.in_grid_range((position[0]-1,position[1])):
            neighbours.append(self.grid[position[0]-1][position[1]])
        if self.in_grid_range((position[0]+1,position[1])):
            neighbours.append(self.grid[position[0]+1][position[1]])
        if self.in_grid_range((position[0]-1,position[1]+1)):
            neighbours.append(self.grid[position[0]-1][position[1]+1])
        if self.in_grid_range((position[0],position[1]+1)):
            neighbours.append(self.grid[position[0]][position[1]+1])
        if self.in_grid_range((position[0]+1,position[1]+1)):
            neighbours.append(self.grid[position[0]+1][position[1]+1])
        return neighbours
    
    def get_near_neighbours(self,position):
        neighbours = []
        if self.in_grid_range((position[0],position[1]-1)):
            neighbours.append(self.grid[position[0]][position[1]-1])
        if self.in_grid_range((position[0]-1,position[1])):
            neighbours.append(self.grid[position[0]-1][position[1]])
        if self.in_grid_range((position[0]+1,position[1])):
            neighbours.append(self.grid[position[0]+1][position[1]])
        if self.in_grid_range((position[0],position[1]+1)):
            neighbours.append(self.grid[position[0]][position[1]+1])
        return neighbours
    
    def get_neighbours_positions(self,position):
        neighbours = []
        if self.in_grid_range((position[0]-1,position[1]-1)):
            neighbours.append((position[0]-1,position[1]-1))
        if self.in_grid_range((position[0],position[1]-1)):
            neighbours.append((position[0],position[1]-1))
        if self.in_grid_range((position[0]+1,position[1]-1)):
            neighbours.append((position[0]+1,position[1]-1))
        if self.in_grid_range((position[0]-1,position[1])):
            neighbours.append((position[0]-1,position[1]))
        if self.in_grid_range((position[0]+1,position[1])):
            neighbours.append((position[0]+1,position[1]))
        if self.in_grid_range((position[0]-1,position[1]+1)):
            neighbours.append((position[0]-1,position[1]+1))
        if self.in_grid_range((position[0],position[1]+1)):
            neighbours.append((position[0],position[1]+1))
        if self.in_grid_range((position[0]+1,position[1]+1)):
            neighbours.append((position[0]+1,position[1]+1))
        return neighbours
    
    def get_near_neighbours_positions(self,position):
        neighbours = []
        if self.in_grid_range((position[0],position[1]-1)):
            neighbours.append((position[0],position[1]-1))
        if self.in_grid_range((position[0]-1,position[1])):
            neighbours.append((position[0]-1,position[1]))
        if self.in_grid_range((position[0]+1,position[1])):
            neighbours.append((position[0]+1,position[1]))
        if self.in_grid_range((position[0],position[1]+1)):
            neighbours.append((position[0],position[1]+1))
        return neighbours

    def get_cell(self,position):
        return self.grid[position[0]][position[1]]

    def near_bombs(self,position):
        near_bombs = 0
        for neighbours in self.cell_neighbours[position[0]][position[1]]:
            for z in neighbours:
                if z == 2:
                    near_bombs += 1
        return near_bombs

    def is_exposed(self,position):
        neighbours = self.get_neighbours_positions(position)
        near_clear_blocks = 0
        for pos in neighbours:
            if self.grid[pos[0]][pos[1]] == 2:
                continue
            if self.near_bombs((pos[0],pos[1])) == 0:
                near_clear_blocks += 1
        if near_clear_blocks > 0:
            return True
        return False

    def generate_bombs(self,bombs,start_pos):
        start_neighbours = self.get_neighbours_positions(start_pos)
        while bombs > 0:
            x_pos = randint(0,len(self.grid)-1)
            y_pos = randint(0,len(self.grid)-1)
            skip = False
            for cell in start_neighbours:
                if cell[0] == x_pos and cell[1] == y_pos:
                    skip = True
                    break
            if self.grid[x_pos][y_pos] == 1 and skip == False:
                self.grid[x_pos][y_pos] = 2
                bombs -= 1

    def destroy_near_empty(self,start_pos):
        temp_array = [start_pos]
        while len(temp_array) != 0:
            for pos in temp_array:
                for neighbour in self.get_neighbours_positions((pos[0],pos[1])):
                    if neighbour in temp_array: continue
                    if self.get_cell(neighbour) == 1 and self.near_bombs(neighbour) == 0:
                        temp_array.append(neighbour)
                for neighbour in self.get_neighbours_positions((pos[0],pos[1])):
                    self.grid[neighbour[0]][neighbour[1]] = 0
                temp_array.remove(pos)

        # ONLY WORKS FOR SMALL MAP !!!!
        # for neighbour in self.get_neighbours_positions((start_pos[0],start_pos[1])):
        #     if self.get_cell(neighbour) != 0:
        #         if self.near_bombs(neighbour) == 0:
        #             self.grid[neighbour[0]][neighbour[1]] = 0
        #             self.destroy_near_empty(neighbour)
        #             for pos in self.get_neighbours_positions(neighbour):
        #                 self.grid[pos[0]][pos[1]] = 0
        pass

    def world_to_grid(self,position):
        return (floor(position[0]/cell_size),floor(position[1]/cell_size))

    def grid_to_world(self,position):
        return (position[0]*cell_size,position[1]*cell_size)

    def win_check(self):
        full_block = 0
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] == 1:
                    full_block += 1
        if full_block == 0:
            return True
        return False

# TODO ADD FLAGS BREAKING AFTER BLOCKS UNDER THEM HAVE BEEN DESTROYED

class Flags(Game_Object):
    def __init__(self,position) -> None:
        self.Img = flag_img
        self.Rect = pg.Rect(position[0],position[1],cell_size,cell_size)
        Game_Object.Objects.append(self)

complete_time = 0
first_press = True
near_bombs_texts = []
grid = Grid()

def Restart_Game():
    global complete_time
    global first_press
    global near_bombs_texts
    grid.generate_grid((grid_size,grid_size),cell_size)
    first_press = True
    near_bombs_texts = []
    Game_Object.remove_all()
    complete_time = 0

def main():
    Clock = pg.time.Clock()
    global complete_time
    global first_press
    global near_bombs_texts
    
    clock_time = ce.Center_Text((width/2,panel_height/2),str(complete_time),(0,0,0),50)
    clock_rect = pg.Rect(0,0,cell_size,cell_size)
    clock_rect.center = (clock_time.rect.x-clock_img.get_width()/2,clock_time.rect.y)

    #=========SOUNDS============
    press_sound = pg.mixer.Sound("sounds/press.wav")
    press_sound.set_volume(0.2)
    flag_place_sound = pg.mixer.Sound("sounds/flag_place.wav")
    flag_place_sound.set_volume(0.2)
    flag_destroy_sound = pg.mixer.Sound("sounds/flag_destroy.wav")
    flag_destroy_sound.set_volume(0.2)
    explode_sound = pg.mixer.Sound("sounds/explode.wav")
    explode_sound.set_volume(0.2)
    #===========================

    panel = ce.Panel((0,0),(width,panel_height),(74, 117, 44))
    panel.z_sort = -1

    
    grid.generate_grid((grid_size,grid_size),cell_size)

    is_running = True
    while is_running:
        ce.events.clear()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    # RESTART GAME
                    Win_text.visible = False
                    Restart_Game()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                grid_pos = grid.world_to_grid((mouse_pos[0]-offset[0],mouse_pos[1]-offset[1]))
                if pg.mouse.get_pressed()[2]:
                    if grid.grid[grid_pos[0]][grid_pos[1]] == 0:
                        continue
                    colide = False
                    for x in Game_Object.Objects:
                        if x.Rect.collidepoint(mouse_pos[0],mouse_pos[1]):
                            colide = True
                            flag_destroy_sound.play()
                            x.remove()
                            break
                    if colide == False:
                        flag_pos = grid.grid_to_world(grid_pos)
                        Flags((flag_pos[0]+offset[0],flag_pos[1]+offset[1]))
                        flag_place_sound.play()
                        
                if pg.mouse.get_pressed()[0]:
                    colide = False
                    for x in Game_Object.Objects:
                        if x.Rect.collidepoint(mouse_pos[0],mouse_pos[1]):
                            colide = True
                            break
                    if grid.grid[grid_pos[0]][grid_pos[1]] != 0 and grid.grid[grid_pos[0]][grid_pos[1]] != 3 and colide == False:
                        if grid.grid[grid_pos[0]][grid_pos[1]] == 2:
                            # RESTART GAME AFTER PRESSING A BOMB
                            explode_sound.play()
                            Win_text.visible = False
                            Restart_Game()
                            continue

                        grid.grid[grid_pos[0]][grid_pos[1]] = 0
                        press_sound.play()

                        if first_press:
                            first_press = False
                            grid.generate_bombs(16,grid_pos)
                            # TODO PLACE IT IN SEPARATE FUNCTION
                            for x in range(len(grid.grid)):
                                for y in range(len(grid.grid[x])):
                                    neighbours = grid.get_neighbours((x,y))
                                    grid.cell_neighbours[x][y].append(neighbours)
                            #===================================

                        if grid.near_bombs(grid_pos) == 0:
                            grid.destroy_near_empty(grid_pos)
        
        screen.fill((0,0,0))
        delta = Clock.tick(60)/1000
        ce.UI.Update()

        near_bombs_texts = []
        for x in range(len(grid.grid)):
            for y in range(len(grid.grid[x])):
                if grid.grid[x][y] == 2 or grid.grid[x][y] == 1: continue
                near_bombs = grid.near_bombs((x,y))
                if near_bombs > 0:
                    text_color = (0,0,0)
                    if near_bombs == 1: text_color = (83, 142, 201)
                    if near_bombs == 2: text_color = (56, 142, 60)
                    if near_bombs == 3: text_color = (211, 47, 47)
                    if near_bombs == 4: text_color = (123, 31, 162)
                    if near_bombs == 5: text_color = (200,200,0)
                    if near_bombs == 6: text_color = (0,200,200)
                    text_pos = grid.grid_to_world((x,y))
                    text = ce.Center_Text((text_pos[0]+cell_size/2+offset[0],text_pos[1]+cell_size/2+offset[1]),str(near_bombs),text_color,int(cell_size*1.2))
                    near_bombs_texts.append(text)

        grid.draw_grid()

        for x in Game_Object.Objects:
            x.Draw()

        Win_text = ce.Center_Text((width/2+offset[0],height/2+offset[1]),"YOU WON",(22, 130, 87),100,visible=False)
        if grid.win_check():
            Win_text.visible = True
        else:
            complete_time+=delta
            if complete_time > 999:
                complete_time = 999
        
        time_formated = floor(complete_time)
        if time_formated/100 >= 1: time_formated = str(time_formated)
        elif time_formated/10 >= 1: time_formated = "0"+str(time_formated)
        else: time_formated = "00"+str(time_formated)
        clock_time.text = str(time_formated)
        clock_time.rect.center = (width/2+clock_time.rect.width/2,panel_height/2)

        ce.UI.Draw(screen)
        screen.blit(clock_img,clock_rect)
        Win_text.Remove()
        for x in near_bombs_texts:
            x.Remove()


        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    pg.init()
    pg.mixer.init()
    main()