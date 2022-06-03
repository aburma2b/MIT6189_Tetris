# Name: Ankush Burman
# Section: Self
# Date: Started: Mar 16, 2022; 
# tetris.py


import graphics35 as gr
import random

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

    def __init__(self, pos, color, block_sz = BLK_SIZE):
        self.x = pos.x
        self.y = pos.y
        
        pixel_point1 = gr.Point(block_sz*pos.x, block_sz*pos.y)
        pixel_point2 = gr.Point(block_sz*pos.x+block_sz, block_sz*pos.y+block_sz)
        gr.Rectangle.__init__(self, pixel_point1, pixel_point2)
                                
        self.color = color.lower() 
        self.setFill(self.color)
                                                        
        self.setOutline(Block.OUTLINE_COLOR)
        self.setWidth(Block.OUTLINE_WIDTH)
        
    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''
        new_x = dx+self.x
        new_y = dy+self.y

        if board.can_move(new_x, new_y):
            return True
        else:
            return False 

        return False
        
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

    def get_coords(self):
        ''' Parameters: None
            Return value type: int 
            Returns the current x,y position of the block.
        '''
        return (self.x, self.y)
    

############################################################
# SHAPE CLASS
############################################################
class Shape(object):
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    hold - type: Bool - Hold can only be used once per new shape spawn.
                                        This flag determines if hold has been used or not.
                                        This variable should be set to false when it the 
                                        shape is being re-created from the hold system. 
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color, block_sz = Block.BLK_SIZE):
        self.blocks = []
        self.rotation_dir = 1
        self.hold = True
        self.soft_lock = False
        self.softlock_move = 15
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, color, block_sz))

    def get_blocks(self):
        '''returns the list of blocks
        '''
        return self.blocks
    
    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame
            Return: None 
            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)

        return None
    
    def undraw(self):
        ''' Parameter: None
            Return: None 
            Undraws the shape by undrawing each block
        '''
        for block in self.blocks:
            block.undraw()

        return None

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        if self.soft_lock == True:
            self.softlock_move -= 1

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
        for block in self.blocks:
            if block.can_move(board, dx, dy):
                continue 
            else:
                return False
        return True
            
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
        for block in self.blocks: 
            dx, dy = self.calc_rot_coords(block)
            if block.can_move(board, dx, dy):
                continue
            else:
                return False

        return True 
        
    def rotate(self):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position    
        '''
        if self.soft_lock == True:
            self.softlock_move -= 1

        for block in self.blocks:
            dx, dy = self.calc_rot_coords(block)
            block.move(dx, dy) 

        ### This should be at the END of your rotate code. 
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1
        
        return None 

    def calc_rot_coords(self, block):
        ''' Parameters: block - type: Block
            Return: type: int  
            Calculates a new position for each block based on the direction
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
        
    def softlock_reset(self):
         self.soft_lock = False
         self.softlock_move = 15

############################################################
# ALL SHAPE CLASSES
############################################################
#Each shape has a different center.
#The center is the one without any offset.
class I_shape(Shape):
    def __init__(self, center, color = 'cyan', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 2, center.y),
                  gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, color, block_sz)
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

class J_shape(Shape):
    def __init__(self, center, color = 'RoyalBlue', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, color, block_sz)         
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center, color = 'orange', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, color, block_sz)        
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center, color = 'yellow1', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x    , center.y),
                  gr.Point(center.x - 1, center.y),
                  gr.Point(center.x   , center.y + 1),
                  gr.Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, color, block_sz)
        self.center_block = self.blocks[0]

    def rotate(self):
        # Override Shape's rotate method since O_Shape does not rotate
        return None 

class S_shape(Shape):
    def __init__(self, center, color = 'chartreuse', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x    , center.y),
                  gr.Point(center.x    , center.y + 1),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, color, block_sz)
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1

class T_shape(Shape):
    def __init__(self, center, color = 'DarkViolet', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y),
                  gr.Point(center.x + 1, center.y),
                  gr.Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, color, block_sz)
        self.center_block = self.blocks[1]

class Z_shape(Shape):
    def __init__(self, center, color = 'red', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y),
                  gr.Point(center.x    , center.y), 
                  gr.Point(center.x    , center.y + 1),
                  gr.Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, color, block_sz)
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
                    total_lines - type:int - Total lines cleared in the current game
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
                    cleared_lines - keeps tracks of how many lines/rows have
                    been cleard
                    go_rect - type:gr.Rectangle - A rectangle within which the game over
                                                  text is shown.
                    go_text - type:gr.Text - The graphics object which holds the game over
                                             text.
    '''   
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.total_lines = 0
        # create a canvas to draw the tetris shapes on
        self.canvas = gr.CanvasFrame(win, self.width * Block.BLK_SIZE,
                                        self.height * Block.BLK_SIZE)
        self.canvas.setBackground('light gray')
        self.go_rect = None
        self.go_text = None 
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

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
            
        '''
        for block in shape.get_blocks():
           coords = block.get_coords()
           self.grid[coords] = block 
    
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
        for x in range(0, self.width):
            block = self.grid.pop((x,y))
            block.undraw()
                
        return None 

    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator) 
            if there is one square that is not occupied, return False
            otherwise return True
            
        '''
        for x in range(0, self.width):
            if (x, y) in self.grid:
                continue
            else:
                return False

        return True 
    
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
        ''' Paramters: None
            Return: None 
            Initializes the objects for the game over message
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
       '''Parameters: None
          Return: None 
          Draws the game over message
       '''
       self.go_rect.draw(self.canvas)
       self.go_text.draw(self.canvas)
       return None

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        self.gameover_init()
        self.gameover_draw()
        return None 


############################################################
# SCOREBOARD CLASS
############################################################
class ScoreBoard(object):
    ''' ScoreBoard class: it represents the score board. Does all the
        calculations associated with leveling up, score, and game gravity. 

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:gr.CanvasFrame - where the score will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    level - type:int - keeps track of the level of the game
                    gravity - type:int - keeps track of the gravity of the game
                    score - type:int - keeps track of the score of the game
                    rect - type:gr.Rectangle - Holds the rectangle object which
                                               acts as a border and canvas.
                    lvl_text - type:gr.Text - Holds the level text object
                    scr_text - type:gr.Text - Holds the score text object 
    '''             

    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.level = 1
        self.gravity = 1
        self.score = 0

        # create a canvas to draw the tetris shapes on
        self.canvas = gr.CanvasFrame(win, self.width * Block.BLK_SIZE,
                                        self.height * Block.BLK_SIZE)
        self.canvas.setBackground('light gray')
        self.rect = None
        self.lvl_text = None
        self.scr_text = None

        self.gravity_up() 
        self.init_objects()
        self.draw()

    def init_rect(self):
        ''' Parameters: None
            Return type: None
            Initializes a rectangle to serve as a border and
            as a canvas for the canvas frame. Sets it's border, 
            border color, and fill color. This needs to be initialized
            and drawn first because everything else is drawn on top of 
            it. 
        '''
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
        ''' Parameters: None
            Return: None 
            Initializes all the text that is displayed on the
            scoreboard, which are "Hold" and "Preview". 
        '''
        lvl_num = str(self.level)
        lvltxt_pnt = gr.Point(Block.BLK_SIZE*5, Block.BLK_SIZE*0.7)
        self.lvl_text = gr.Text(lvltxt_pnt, "Level: " + lvl_num)
        score_num = str(self.score)
        scrtxt_pnt = gr.Point(Block.BLK_SIZE*5, Block.BLK_SIZE*1.5)
        self.scr_text = gr.Text(scrtxt_pnt, "Score: " + score_num)
        return None 

    def init_objects(self):
        ''' Parameters: None
            Return: None
            Initializes all the objects that are to displayed on
            the Score Board.
        '''
        self.init_rect()
        self.init_text()
        return None

    def draw(self):
        ''' Parameters: None
            Return: None
            Draws all the objects that are to be displayed
        '''
        self.rect.draw(self.canvas)
        self.lvl_text.draw(self.canvas)
        self.scr_text.draw(self.canvas)
        return None 

    def level_up(self, total_lines):
        ''' Paramters: type:int - Total lines cleared
            Return: types: int/Bool
            1. Checks if total lines meet the goal
            2. If it does then: 
                - the level is incremented by one
                - Gravity is updated (gravity is level dependent)
                - The internal level attribute is updated 
                - The new level is drawn
                - The new gravity is returned (this is used in the tetris
                  class to update delay)
        '''
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
        ''' Parameters: None 
            Return type: None
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
        ''' Parameters: type:int - Number of cleared lines
            Return: None
            1. Calculates the score depending on the number of lines
               cleared in one go.
            2. Increments the total score by the amount of new points 
               earned.
            3. Draws the new score on the screen

            Points per line cleared:
            1 line cleard: 100 * level
            2 lines cleared: 300 * level
            3 lines cleared: 500 * level
            4 lines cleared: 800 * level
            n lines cleared: line_score * level
        '''
        n = cleared_lines
        #Figured out this formula myself. The formula calculates 
        #the line score depending on the number of lines cleared.
        #The calculation needs to be done in floating point.
        if cleared_lines > 0:
            line_score = (50.0/3.0)*(n**3)+(-100.0)*(n**2)+(1150.0/3.0)*(n)+(-200.0)
            points = line_score * self.level 
            self.score += points
            score_num = str(int(self.score))
            self.scr_text.setText("Score: " + score_num)
        
        return None

    def update(self, cleared_lines, total_lines):
        ''' Paremeters: type: int - Cleared lines and total lines cleared
            Return: type:int/Bool If there is a level increment: 
                                    - Returns the new gravity
                                  If there is no level change then:
                                    - Returns False
            Updates the score and level based on cleared lines in one go and
            total cleared lines.
        '''
        self.score_up(cleared_lines)
        return self.level_up(total_lines)


############################################################
# PREVIEWBOARD CLASS
############################################################
class PreviewBoard(object):
    ''' PreviewBoard class: it shows pieces which are held and a
        preview of next three pieces. 

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:gr.CanvasFrame - where the score will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    hld_shape - type:None/Shape -  keeps track of the hold piece 
                    prv_list - type:list - keeps track of the preview of next three 
                                           pieces. 
                    rect - type:gr.Rectangle - Holds the rectangle which acts as 
                                               a border and "canvas"
                    hld_txt - type:gr.Text - Holds the "Hold" text object
                    prv_txt - type:gr.Text - Holds the "Preview" text object
                    hld_line - type:gr.Line - Holds the line object which acts as an
                                              underline to the "Hold" text.
                    prv_line - type:gr.Line - Holds the line object which acts as an
                                              underline to the "Preview" text. 
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.hld_shape = None
        self.prv_list = []
        # create a canvas to draw the tetris shapes on
        self.canvas = gr.CanvasFrame(win, self.width * Block.BLK_SIZE,
                                        self.height * Block.BLK_SIZE)
        self.canvas.setBackground('light gray')
        self.rect = None
        self.hld_txt = None
        self.prv_txt = None
        self.hld_line = None
        self.prv_line = None

        self.init_static()
        self.draw_static()

    def init_rect(self):
        ''' Parameters: None
            Return type: None
            Initializes a rectangle to serve as a border and
            as a canvas for the canvas frame. Sets it's border, 
            border color, and fill color. This needs to be initialized
            and drawn first because everything else is drawn on top of 
            it. 
        '''
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
        ''' Parameters: None
            Return: None 
            Initializes all the text objects that is displayed on the
            scoreboard, which are "Hold" and "Preview". 
        '''
        #Got coordinates after trial and error
        #10 represents the block size. Easier to think
        #in terms of blocks because the whole game works on a block
        #coordinate system.
        hld_x = 2.4*10
        hld_y = 1.4*10
        hld_center = gr.Point(hld_x, hld_y)
        self.hld_txt = gr.Text(hld_center, "Hold")
        self.hld_txt.setSize(9)
        #self.hld_txt.setStyle("bold")

        #Got coordinates after trial and error
        #10 represent the block size. Easier to think
        #in terms of blocks because the whole game works on a block
        #coordinate system.
        prv_x = 13.65*10
        prv_y = 1.4*10
        prv_center = gr.Point(prv_x, prv_y) 
        self.prv_txt = gr.Text(prv_center, "Preview")
        self.prv_txt.setSize(9)
        #self.prv_txt.setStyle("bold")

        return None

    def init_lines(self):
        ''' Parameters: None
            Return: None
            Initializes lines which are displayed underneath 
            the text as astylized underline
        '''
        #Determined coordinates after trial and error
        hld_x1 = 1.15*10
        hld_x2 = 6.9*10
        hld_y = 1.9*10
        hld_p1 = gr.Point(hld_x1, hld_y)
        hld_p2 = gr.Point(hld_x2, hld_y)
        self.hld_line = gr.Line(hld_p1, hld_p2)
        
        #Determined coordinates after tril and error
        prv_x1 = 11.45*10
        prv_x2 = 28.9*10
        prv_y = 1.9*10
        prv_p1 = gr.Point(prv_x1, prv_y)
        prv_p2 = gr.Point(prv_x2, prv_y)
        self.prv_line = gr.Line(prv_p1, prv_p2)
        return None

    def init_preview(self, shape_list):
        ''' Parameters: type: list - A list of shapes
            Return: None
            Initializes the next three shapes.
            These shapes are initialized with a block size of 10,
            to make them smaller and to fit all of them onto the 
            preview board. This is done for aesthetic purposes.
            The colour is also set for aesthetic purposes.
            The shapes are initialized with positions, which are the 
            positions the shapes will be displayed at on the Preview Board. 
        '''
        shape_col = 'MediumAquamarine'
        #Got the coordinates after trial and error
        prv_x = 14.65 
        prv_y = 2.75 
        for i in range(3):
            prv_center = gr.Point(prv_x, prv_y) 
            new_shape = shape_list[i](prv_center, shape_col, 10)
            self.prv_list.append(new_shape)
            prv_x += 6

        return None 

    def init_hold(self, hold_shape = None):
        ''' Parameters: type: Shape - The shape which is being held
            Return: None
            Initializes the "hold" shape.
            The shapes' class is used to initialize a new shape 
            which has a block size of 10 (makes it smaller) and a new
            fill colour. This is done for aesthetic purposes. The argument
            can not be used as is because it contains position data which is
            relevant to the Tetris Board. That is also why a new shape needs to 
            be initialized with a new position. This position is where  the shape
            will be displayed on the Preview Board. 
       '''
        shape_col = 'MediumAquamarine'
        #Got the coordinates after trial and error
        hld_x = 4.65
        hld_y = 2.75
        hld_center = gr.Point(hld_x, hld_y) 
        if hold_shape != None:
            shape_type = hold_shape.__class__ 
            self.hld_shape = shape_type(hld_center, shape_col, 10) 
        
        return None

    def init_static(self):
        ''' Parameters: None
            Return: None
            Initializes all the static shapes and text which are to be
            displayed on the Preview Board.
        '''
        self.init_rect()
        self.init_text()
        self.init_lines()
        return None

    def undraw_preview(self):
        ''' Parameters: None
            Return: None
            Undraws the currentl preview shapes if they exist
            and are displayed.
        '''
        if self.prv_list != []:
            list_len = len(self.prv_list)
            for i in range(list_len):
                if self.prv_list[i]:
                    self.prv_list[i].undraw()
            self.prv_list = []

        return None
    
    def draw_static(self):
        ''' Parameters: None
            Return: None
            Draws the static shapes and text which are to
            be displayed on the preview board.
        '''
        self.rect.draw(self.canvas) 
        self.hld_txt.draw(self.canvas)
        self.prv_txt.draw(self.canvas)
        self.hld_line.draw(self.canvas)
        self.prv_line.draw(self.canvas)
        return None

    def draw_preview(self, shape_list):
        ''' Paramters: type: list - A list of shapes to be drawn
            Return: None
            1. Undraws the current preview shapes
            2. Initializes the new preview shapes for the preview board 
            3. Draws the new preview shapes
        '''
        self.undraw_preview()
        self.init_preview(shape_list) 
        
        for i in range(3):
            self.prv_list[i].draw(self.canvas)
        
        return None

    def draw_hold(self, hold_shape = None):
        ''' Parameters: type: Shape - The "hold" shape
            Return: None
            1. Undraws the current hold shape if it exists
            2. Initializes the new hold shape for the preview board
            3. Draws the new hold shape
        '''
        if self.hld_shape != None:
            self.hld_shape.undraw()
         
        self.init_hold(hold_shape)
        if self.hld_shape != None:
            self.hld_shape.draw(self.canvas)

        return None


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
            SCR_BOARD_WIDTH - type:int - the width of the preview and score boards
            SCR_BOARD_HEIGHT - type:int - the height of the preview and score boards
            prv_board - type: PreviewBoard - the board which displays preview and hold
                                             shapes.
            board - type:Board - the tetris board
            scr_board - type: ScoreBoard - Does all the calculations for score, levels,
                                           and gravity. Also displays the current 
                                           score and level.
            win - type:gr.Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            seven_bag - type: list - Holds a list of next seven shapes
            next_bag - type: list - Holds a list of shuffled shapes to feed into
                                    seven_bag (needed for preview to work). 
            current_shapes - type: Shape - the current moving shape on the board
            hold_shape - type: Shape - Holds the information for the "hold" shape.
            hold_flag - type: Bool - Hold can only be used once per new shape spawn.
                                     This flag determines if hold has been used or not.
            animation - type: tk.after - Holds the tk.after function in a variable so it 
                                         can be cancelled later on.
    '''
    
    SHAPES = (I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape)
    DIR_KEYS = ("right", "left", "down")
    LOCK_KEYS = ("space", "down")
    SOFTLOCK_KEYS = ("space", "down", "animate")
    DIRECTION = {'left':(-1, 0), 'right':(1, 0), 'down':(0, 1), 'animate':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    SCR_BOARD_WIDTH = 10
    SCR_BOARD_HEIGHT = 2

    def __init__(self, win):
        self.prv_board = PreviewBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT)
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.scr_board = ScoreBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # Initialize the seven bag system
        # Create new shape and sets the current shape to the new
        # shape
        self.seven_bag = []
        self.next_bag = []
        self.current_shape = self.create_new_shape()
        
        #Initialize the hold system
        self.hold_shape = None 

        #Used for controlling lock delay
        self.lock_delay = None

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.current_shape)
        self.prv_board.draw_preview(self.seven_bag) 
        
        #Set the state of the game
        

        # For Step 9:  animate the shape
        self.animation = None 
        self.animate_shape()
       
        #NOTE############ FOR TESTING ONLY ############NOTE 
        #test_x = int(self.BOARD_WIDTH/2)
        #test_y = 0 
        #self.test_shape = I_shape(gr.Point(test_x, test_y))

        #self.TEST_SHAPES = [I_shape, I_shape, I_shape]
        #self.prv_board.draw(self.TEST_SHAPES, self.test_shape)

    def create_new_shape(self):
        ''' Return value: type: Shape
            Uses the 7bag system to generate shapes.
            1a. First run: Takes list of all shapes and 
               shuffles it to fill seven_bag and next_bag individually. 
               (seven_bag always need to be populated) 
            1b. Subsequent runs: 
               Picks a shape from new seven_bag list and
               removes it from the list. 
            2. Adds a shape to the list from the next_bag 
            3. Creates a new shape, which was picked from seven_bag,
               that is centered at y = 0 and x = int(self.BOARD_WIDTH/2)
            4. returns the shape
        '''
        x = int(self.BOARD_WIDTH/2)
        y = 0
        list_len = len(Tetris.SHAPES)
        
        if len(self.seven_bag) == 0 and len(self.next_bag) == 0:
            self.seven_bag = random.sample(Tetris.SHAPES, list_len)
            self.next_bag = random.sample(Tetris.SHAPES, list_len)
        elif len(self.next_bag) == 0:
            self.next_bag = random.sample(Tetris.SHAPES, list_len)

        shape = self.seven_bag.pop(0)(gr.Point(x, y))
        self.seven_bag.append(self.next_bag.pop(0))

        return shape 
        
    def update_speed(self, gravity):
        ''' Return type: None
            Updates the delay variable which controls the speed
            of the down animation of the tetrominoes. 
            Gravity is in Seconds and tkinter likes ms for the after function.
            Therefore gravity is multiplied by 1000 to yield ms. 
        '''
        self.delay = gravity*1000 
        self.delay = int(self.delay)
        return None

    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        ''' 
        self.tetris_control("animate")
        print self.delay
        self.animation = self.win.after(self.delay, self.animate_shape)
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
        direction = direction.lower()
        dx, dy = Tetris.DIRECTION[direction]
        print "do_move", dx, dy  #NOTE  
        if self.current_shape.can_move(self.board, dx, dy): 
            self.current_shape.move(dx, dy) 
            return True
        else:
            return False

        return False
    
    def normal_move(self, key):
        direction = key.lower()
        dx, dy = Tetris.DIRECTION[direction]
        if self.current_shape.can_move(self.board, dx, dy):
            self.current_shape.move(dx, dy)
        elif key in Tetris.SOFTLOCK_KEYS:
            print self.animation
            self.win.after_cancel(self.animation)
            self.animation = None
            print "soft locking shape"
            self.current_shape.soft_lock = True
            print self.current_shape.soft_lock
            self.lock_delay = self.win.after(500, self.shape_lock)
    
    def softlock_move(self, key):
        if self.lock_delay:
            print "Cancelling lock_delay"
            self.win.after_cancel(self.lock_delay)
            self.lock_delay = None

        if self.do_move(key) == True:
            dx, dy = Tetris.DIRECTION["down"]
            if self.current_shape.can_move(self.board, dx, dy):
                if self.lock_delay:
                    self.win.after_cancel(self.lock_delay)
                    self.lock_delay = None 

                self.current_shape.softlock_reset()
                        
                if self.animation:
                    self.win.after_cancel(self.animation)
                    self.animation = None
                self.animate_shape()
                return None
            
        self.lock_delay = self.win.after(500, self.shape_lock)

    def shape_lock(self):
        #import pdb; pdb.set_trace() #############NOTE NOTE NOTE############
        print "shape lock called"
        self.board.add_shape(self.current_shape) 
        clrd_lines = self.board.remove_complete_rows()
        lvl_check = self.scr_board.update(clrd_lines, self.board.total_lines)
        if lvl_check:
            self.update_speed(self.scr_board.gravity)

        self.current_shape = self.create_new_shape()
        self.prv_board.draw_preview(self.seven_bag)
        #NOTE for testing: self.prv_board.draw(self.TEST_SHAPES, self.test_shape)  #NOTE 
        if self.board.draw_shape(self.current_shape):
            if self.animation:
                self.win.after_cancel(self.animation)
                self.animation = None

            self.animate_shape()  
        else:
            self.board.game_over()
            self.win.after_cancel(self.animation)

        return None 

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        ''' 
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate()
        else:
            return None

        return None 

    def hold(self):
        ''' Parameters: None
            Return: None
            * If there is no hold shape:
                1. Sets the current shape to hold shape
                2. Undraws the current shape
                3. Sets the current shape to a new shape 
            * If there is a shape already being held:
                1. Holds the current hold shape in temp
                2. Sets the hold shape to the current shape
                3. Initializes a new shape based on the type of previously
                   held shape.
                4. All shapes re-created by hold have their internal hold variable
                   set to false.
            * Draws the new current shape
            * Draws the new hold shape on the preview board
            * Sets hold flag to false (hold can only be used once per new shape spawn)
        '''
        x = int(self.BOARD_WIDTH/2)
        y = 0

        if self.hold_shape == None:
            self.hold_shape = self.current_shape
            self.current_shape.undraw() 
            self.current_shape = self.create_new_shape()
        else:
            temp = self.hold_shape
            self.hold_shape = self.current_shape
            self.current_shape.undraw()
            temp = temp.__class__(gr.Point(x, y))
            temp.hold = False 
            self.current_shape = temp 

        if not self.board.draw_shape(self.current_shape):
            self.board.game_over()

        self.prv_board.draw_hold(self.hold_shape) 
        return None


    def tetris_control(self, key):
        key = key.lower()
        #soft_lock = self.current_shape.soft_lock
        print self.current_shape.soft_lock 
        
        if key == 'h':
            if self.current_shape.hold == True:
                self.hold()

        if self.current_shape.soft_lock == False:  
            if key == "space":
                while self.do_move("down"):
                    pass 
            elif key == "up":
                self.do_rotate()
            elif key in Tetris.DIR_KEYS or key == "animate":
                self.normal_move(key)

        if self.current_shape.soft_lock == True:
            print "Tetris control soft_lock == true"
            if key in  Tetris.LOCK_KEYS:
                if self.lock_delay:
                    self.win.after_cancel(self.lock_delay)
                    self.lock_delay = None

                self.shape_lock() 
            elif key == "up":
                if self.lock_delay:
                    self.win.after_cancel(self.lock_delay)
                    self.lock_delay = None

                self.do_rotate()

                self.lock_delay = self.win.after(500, self.shape_lock)
            elif key == "animate":
                pass 
            elif key in Tetris.DIR_KEYS:
                if self.lock_delay:
                    print "Cancelling lock_delay"
                    self.win.after_cancel(self.lock_delay)
                    self.lock_delay = None

                if self.do_move(key) == True:
                    dx, dy = Tetris.DIRECTION["down"]
                    if self.current_shape.can_move(self.board, dx, dy):
                        if self.lock_delay:
                            self.win.after_cancel(self.lock_delay)
                            self.lock_delay = None 

                        self.current_shape.softlock_reset()
                        
                        if self.animation:
                            self.win.after_cancel(self.animation)
                            self.animation = None
                        self.animate_shape()
                        return None
            
                self.lock_delay = self.win.after(500, self.shape_lock)
        
            if self.current_shape.softlock_move <= 0:
                if self.lock_delay:
                    self.win.after_cancel(self.lock_delay)
                    self.lock_delay = None

                self.shape_lock()
            
        #if self.state == "unlock":
            #self.state = "play"
            #self.animate_shape()

        #if self.state == "game_over":
            #self.win.after_cancel(self.animation)
            #self.board.game_over()
        
        #print self.state
        return None


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

            if the user presses the 'h' key, the shape is held

        '''
        key = event.keysym #event.keysym is a tkinter function
        key = key.lower()
        
        self.tetris_control(key)
#        if key in Tetris.DIR_KEYS:
#            self.do_move(key)
#        elif key == "space":
#            while self.do_move("down"):
#                pass
#        elif key == "Up":
#            self.do_rotate()
#        elif key == 'h':
#            if self.current_shape.hold == True:
#                self.hold()
#        else:
#            pass 

        return None 
       

################################################################
# Start the game
################################################################
win = gr.Window("Tetris")
game = Tetris(win)
win.mainloop()
