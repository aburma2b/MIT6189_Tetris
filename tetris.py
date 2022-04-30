# Name: Ankush Burman
# Section: Self
# Date: Started: Mar 16, 2022; 
# tetris.py


import graphics35 as gr
import random
import threading

############################################################
# BLOCK CLASS
############################################################
#Implements a block of tetris.
#Other shapes in tetris are made of blocks.
#The upper left point has to be passed to the init
#function so the black can be draw. The point coordinates
#must be given relative to a tetris board NOT pixels.
#One square on a tetris board is 30by30 pixels, at 
#tetris board has 10x20 squares.
class Block(gr.Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''
    #Determines the block size in terms of pixels
    BLK_SIZE = 30 
    #Determines the outline of each block in terms of pixels
    OUTLINE_WIDTH = 3
    #Sets the colour of the outline of the block
    OUTLINE_COLOR = "black"

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        #### Ankush Burman Code ####
        pixel_point1 = gr.Point(Block.BLK_SIZE*pos.x, Block.BLK_SIZE*pos.y)
        pixel_point2 = gr.Point(Block.BLK_SIZE*pos.x+30, Block.BLK_SIZE*pos.y+30)
        gr.Rectangle.__init__(self, pixel_point1, pixel_point2)
                                
        self.color = color.lower() 
        self.setFill(self.color)
                                                        
        self.setOutline(Block.OUTLINE_COLOR)
        self.setWidth(Block.OUTLINE_WIDTH)
        #### Ankush Burman Code ####

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''
        #### Ankush Burman Code ####
        new_x = dx+self.x
        new_y = dy+self.y

        if board.can_move(new_x, new_y):
            return True
        else:
            return False 

        return False
        #### Ankush Burman Code ####
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        self.x += dx
        self.y += dy

        gr.Rectangle.move(self, dx*Block.BLK_SIZE, dy*Block.BLK_SIZE)
        return None

    #### Ankush Burman Code ####
    def get_coords(self):
        return (self.x, self.y)
    #### Ankush Burman Code ####

############################################################
# SHAPE CLASS
############################################################

class Shape(object):
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, color))



    def get_blocks(self):
        '''returns the list of blocks
        '''
        #### Ankush Burman Code ####
        return self.blocks
        #### Ankush Burman Code ####
        pass

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)
        return None

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)
        return None

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise
           
        '''
        
        #### Ankush Burman Code ####
        for block in self.blocks:
            if block.can_move(board, dx, dy):
                continue 
            else:
                return False
        return True
        #### Ankush Burman Code ####
    
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            returns the current rotation direction
        '''
        return self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        #### Ankush Burman Code ####
        for block in self.blocks: 
            dx, dy = self.calc_rot_coords(block)
            if block.can_move(board, dx, dy):
                continue
            else:
                return False

        return True 
        #### Ankush Burman Code ####

    def rotate(self):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
            
        '''    
        #### Ankush Burman Code ####
        for block in self.blocks:
            dx, dy = self.calc_rot_coords(block)
            block.move(dx, dy)
        ####  Ankush Burman Code #####
        return None 

        ### This should be at the END of your rotate code. 
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1
        
        return None

    def calc_rot_coords(self, block):
        ''' Calculates a new position for each block based on the direction
            of rotation of the shape. Returns the difference between the old 
            coordinates and the new coordinates (Since all other move functions use
            dx and dy).
            The formula used was given in the assignment pdf.
        ''' 
        center_x, center_y = self.center_block.get_coords()
        rot_dir = self.get_rotation_dir() 
        block_x, block_y = block.get_coords()        
        
        new_x = center_x - rot_dir*center_y + rot_dir*block_y
        new_y = center_y + rot_dir*center_x - rot_dir*block_x
        
        dx = new_x - block_x
        dy = new_y - block_y 
        
        return (dx,dy) 
        

############################################################
# ALL SHAPE CLASSES
############################################################
#Each shape has a different center.
#The center is the one without any offset.

class I_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x - 2, center.y),
                  gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, "cyan")
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

class J_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, "RoyalBlue")        
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, "orange")        
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x    , center.y),
                  gr.Point(center.x - 1, center.y),
                  gr.Point(center.x   , center.y + 1),
                  gr.Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, "yellow1")
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return None 

class S_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x    , center.y),
                  gr.Point(center.x    , center.y + 1),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, "chartreuse")
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1

class T_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, "DarkViolet")
        self.center_block = self.blocks[1]

class Z_shape(Shape):
    def __init__(self, center):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y), 
                  gr.Point(center.x    , center.y + 1),
                  gr.Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, "red")
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      


############################################################
# BOARD CLASS
############################################################

class Board(object):
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
                    cleared_lines - keeps tracks of how many lines/rows have
                    been cleard
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.total_lines = 0
        # create a canvas to draw the tetris shapes on
        self.canvas = gr.CanvasFrame(win, self.width * Block.BLK_SIZE,
                                        self.height * Block.BLK_SIZE)
        self.canvas.setBackground('light gray')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}


    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True
            
        '''
            
        #### Ankush Burman Code ####
        pos_tuple = (x, y)

        #Checks if x variable within x-axis bounds of board
        x_check = 0  <= x < self.width 
        #Checks if y variable within y-axis bounds of board
        y_check = 0 <= y < self.height
        #Checks if (x,y) position is occupied or not
        occupy_check = (x,y) in self.grid 

        if x_check and y_check and not occupy_check:
            return True 
        else:
            return False
        
        return False
        #### Ankush Burman Code ####

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
            
        '''
        
        #### Ankush Burman Code ####
        for block in shape.get_blocks():
           coords = block.get_coords()
           self.grid[coords] = block 
        #### Ankush Burman Code ####
        return None

    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout
            
        '''
        
        #### Ankush Burman Code ####
        for x in range(0, self.width):
            block = self.grid.pop((x,y))
            block.undraw()
                
        return None 
      #### Ankush Burman Code ####

    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator) 
            if there is one square that is not occupied, return False
            otherwise return True
            
        '''
        
        #### Ankush Burman Code ####
        for x in range(0, self.width):
            if (x, y) in self.grid:
                continue
            else:
                return False

        return True 
        #### Ankush Burman Code ####
    
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        # -1 because range function stops before hitting the
        #last element. I need it to go to grid row 0 (y = 0).
        for y in range(y_start, -1, -1):
            for x in range(0, self.width):
                if (x, y) in self.grid:
                    block = self.grid.pop((x,y))
                    block.move(0, 1)
                    new_coords = block.get_coords()
                    self.grid[new_coords] = block

        return None 
    
    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    * delete the row
                    * add +1 to cleared_lines
                    * move all rows down starting at row y - 1
                  
        '''
        cleared_lines = 0 
        for y in range(0, self.height):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.total_lines += 1
                cleared_lines += 1
                self.move_down_rows(y-1)
            else:
                pass

        return cleared_lines  

    def gameover_init(self):
        '''Initializes the objects for the game over message
        '''
        #Game Over rectangle
        p1 = gr.Point(Block.BLK_SIZE*1, Block.BLK_SIZE*9)
        p2 = gr.Point(Block.BLK_SIZE*9, Block.BLK_SIZE*11)
        self.go_rect = gr.Rectangle(p1, p2)
        self.go_rect.setOutline("black")
        self.go_rect.setWidth(5)
        self.go_rect.setFill( "MediumAquamarine")
        #Game Over text
        center_point = self.go_rect.getCenter()
        self.go_text = gr.Text(center_point, "Game Over!")
        self.go_text.setSize(20)
        self.go_text.setStyle("bold")
        self.go_text.setOutline("black")
        return None 

    def gameover_draw(self):
       '''Draws the game over message
       '''
       self.go_rect.draw(self.canvas)
       self.go_text.draw(self.canvas)
       return None

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        
        #### Ankush Burman Code ####
        self.gameover_init()
        self.gameover_draw()
        return None
        #### Ankush Burman Code ####


############################################################
# SCOREBOARD CLASS
############################################################

class ScoreBoard(object):
    ''' ScoreBoard class: it represents the score board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the score will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    lelvel - keeps track of the level of the game 
                    score - keeps track of the score of the game 
    '''

    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.level = 1
        self.gravity_up()
        self.score = 0

        # create a canvas to draw the tetris shapes on
        self.canvas = gr.CanvasFrame(win, self.width * Block.BLK_SIZE,
                                        self.height * Block.BLK_SIZE)
        self.canvas.setBackground('light gray')
        self.init_objects()
        self.draw()

    def init_rect(self):
        #Initializes a rectangle based on the self.pos variable.
        #Sets its outline and colour.
        canvas_w = self.canvas.getWidth()
        canvas_h = self.canvas.getHeight()
        origin = gr.Point(0, 0)
        self.point2 = gr.Point(canvas_w, canvas_h)
        self.rect = gr.Rectangle(origin, self.point2)
        self.rect.setOutline("black")
        self.rect.setWidth(5)
        self.rect.setFill( "MediumAquamarine")
        return None

    def init_text(self):
        lvl_num = str(self.level)
        lvltxt_pnt = gr.Point(Block.BLK_SIZE*5, Block.BLK_SIZE*0.7)
        self.lvl_text = gr.Text(lvltxt_pnt, "Level: " + lvl_num)
        score_num = str(self.score)
        scrtxt_pnt = gr.Point(Block.BLK_SIZE*5, Block.BLK_SIZE*1.5)
        self.scr_text = gr.Text(scrtxt_pnt, "Score: " + score_num)
        return None 

    def init_objects(self):
        self.init_rect()
        self.init_text()
        return None

    def draw(self):
        self.rect.draw(self.canvas)
        self.lvl_text.draw(self.canvas)
        self.scr_text.draw(self.canvas)
        return None 

    def level_up(self, total_lines):
        if total_lines > (5*self.level):
            self.level += 1
            self.gravity_up()
            lvl_num = str(self.level)
            self.lvl_text.setText("Level " + lvl_num)
            return self.gravity 
        else:
            pass

        return False

    def gravity_up(self):
        ''' Return type: None
            Calculates the gravity speed of the game
            based on the current level. Formula taken from 2022 tetris
            guideline. The unit of the solution is Seconds.
        '''
        lvl = self.level
        #Gravity formula for tetris as per tetris guideline 2022
        #multiplied by 1000 to yield the time in ms
        self.gravity = ((0.8 - ((lvl-1.0)*0.007))**(lvl-1.0))
        return None 

    def score_up(self, cleared_lines):
        """ Points per line cleared:
            1 line cleard: 100 * level
            2 lines cleared: 300 * level
            3 lines cleared: 500 * level
            4 lines cleared: 800 * level
            n lines cleared: line_score * level
        """
        n = cleared_lines
        #Figured out this formula myself. 
        #The calculation needs to be done in floating point.
        if cleared_lines > 0:
            line_score = (50.0/3.0)*(n**3)+(-100.0)*(n**2)+(1150.0/3.0)*(n)+(-200.0)
            points = line_score * self.level 
            self.score += points
            score_num = str(int(self.score))
            self.scr_text.setText("Score: " + score_num)
        
        return None

    def update(self, cleared_lines, total_lines):
        self.score_up(cleared_lines)
        return self.level_up(total_lines)
 

############################################################
# TETRIS CLASS
############################################################

class Tetris(object):
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''
    
    SHAPES = (I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape)
    INPUT_KEYS = ("Right", "Left", "Down")
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    SCR_BOARD_WIDTH = 10
    SCR_BOARD_HEIGHT = 2

    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.scr_board = ScoreBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        #### Ankush Burman Code ####
        self.board.draw_shape(self.current_shape)
        ####  Ankush Burman Code ####

        # For Step 9:  animate the shape!
        self.animate_shape()


    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        #### Ankush Burman Code ####
        x = int(self.BOARD_WIDTH/2)
        y = 0
        shape = random.choice(Tetris.SHAPES)(gr.Point(x, y))
        return shape 
        #### Ankush Burman Code ####
    
    def update_speed(self, gravity):
        ''' Return type: None
            Updates the delay variable which controls the speed
            of the down animation of the tetrominoes. 
            Gravity is in Seconds and tkinter likes ms for after function.
            Therefore gravity is multiplied by 1000 to yield ms. 
        '''
        self.delay = gravity*1000 
        self.delay = int(self.delay)
        return None

    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        
        self.do_move('Down')
        self.win.after(self.delay, self.animate_shape)
        return None

    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False

        ''' 
        #### Ankush Burman Code ####
        direction = direction.lower()
        dx = 0 
        dy = 0

        if direction == "right":
            dx = int(1)
            dy = int(0) 
        elif direction == "left":
            dx = int(-1)
            dy = int(0)  
        elif direction == "down":
            dx = int(0)
            dy = int(1)
        else:
            pass 
        
        if self.current_shape.can_move(self.board, dx, dy): 
            self.current_shape.move(dx, dy) 
            return True
        elif direction == "down":
            self.board.add_shape(self.current_shape)
            self.current_shape = self.create_new_shape()
            
            if not self.board.draw_shape(self.current_shape):
                self.board.game_over()

            clrd_lines = self.board.remove_complete_rows()
            lvl_check = self.scr_board.update(clrd_lines, self.board.total_lines)
            if lvl_check:
                self.update_speed(self.scr_board.gravity)
            else:
                pass

            return False

        else:
            return False

        return False


    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        ''' 
        #### Ankush Burman Code ####
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate()
        else:
            return None

        return None 
        #### Ankush Burman Code ####
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currenly just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
            
        #### Ankush Burman Code ####

        key = event.keysym #event.keysym is a tkinter function

        if key in Tetris.INPUT_KEYS:
            self.do_move(key)
        elif key == "space":
            while self.do_move("down"):
                pass
        elif key == "Up":
            self.do_rotate()
        else:
            pass 

        return None 
       
################################################################
# Start the game
################################################################

win = gr.Window("Tetris")
game = Tetris(win)
win.mainloop()
