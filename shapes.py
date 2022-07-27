# Name: Ankush Burman
# Section: Self
# Date: Started: Mar 16, 2022; 
# shapes.py

import graphics35 as gr

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
                    can_hold - type: Bool - Hold can only be used once per new shape spawn.
                                        This flag determines if hold has been used or not.
                                        This variable should be set to false when it the 
                                        shape is being re-created from the hold system. 
                    soft_lock - type: Bool - Determines if the shape is in soft_lock state
                                             or not.
                    soft_locks_left - type: int - Keeps track of the number of times the 
                                                 shape has been moved while in soft_lock
                                                 state. A shape can be moved a maximum of
                                                 15 times in soft_lock state.
                    self.rot_offset_used - type: int - Stores which of the 5 rotational
                                           offset was used, last time the shape was kicked
                                           into position.
                    self.last_move_rot - type: bool - Tracks the last successful move 
                                                  performed by the shape. If last move is 
                                                  a rotation then this variable is set to 
                                                  true. If last move is down, left, or right 
                                                  then this variable is set to false. 
                    KICK_OFFSET - type: 2 dimensional array - Holds the kick offset 
                                  values for J, L, S, T, Z shapes. Each row in the array
                                  corresponds to the rotational state of the shape. Each
                                  column is the offset test number which must be done in 
                                  that order. I shape has it's own unique offset values.
                                  O shape does not rotate.
    '''
    #Really for reference, the state numbers correspond to the rows in self.KICK_OFFSET array.
    ROTATION_STATES = {"spawn":0, "counter_clockwise":1, "consecutive":2, "clockwise":3}

    def __init__(self, coords, color, block_sz = Block.BLK_SIZE):
        self.blocks = [] 
        self.rotation_state = self.ROTATION_STATES["spawn"] 
        self.can_hold = True
        self.soft_lock = False
        self.soft_locks_left = 15
        self.rot_offset_used = 0
        self.last_move_rot = False 
        #The offset values are taken from the Tetris Guideline 2022. The signs of the y-axis  
        #are flipped relative to the sign of the values in the guideline because the y-axis
        #here is flipped.
        self.KICK_OFFSET = [[(0,0), (0,0), (0,0), (0,0), (0,0)],
                           [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
                           [(0,0), (0,0), (0,0), (0,0), (0,0)],
                           [(0,0), (1,0), (1,1), (0,-2), (1,-2)]]


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

    def can_move_down(self, board):
        ''' Parameters: board - type: Board
            
            Return value: type: bool

            checks to see if the shape can move down 
            or not.
        '''
        dx = 0
        dy = 1
        return self.can_move(board, dx, dy) 
    
    def do_move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
            
            Return value: None 
            
            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)
        return None 
    
    def set_move_states(self, last_move_rot):
        ''' Parameters: last_move_rot - type:bool
            Return: None
            
            Sets the variables that tracks the details of the
            last move. These variables are used in other functions 
            to determine the state of the shape.
        '''
        if self.soft_lock == True:
            self.soft_locks_left -= 1
        self.last_move_rot = last_move_rot 
        return None 

    def move(self, board, dx, dy):
        ''' Parameters: board - type: Board
                        dx - type: int
                        dy - type: int

            Return value: type: bool

            Controls the movement flow of the shape:
            1. If shape is in soft_lock state then substracts
               1 from soft_locks_left. Shape can only be moved a limited amount
               of times in soft_lock state, upto a maximum of 15 times.
            2. If the shape can be moved then moves the shape and returns true
            3. If shape can not be moved then does nothing and returns False
        '''
        if self.can_move(board, dx, dy) == True:
            self.do_move(dx, dy)
            self.set_move_states(False) 
            return True 
        return False     
    
    #Not using this function right now but keeping it in here since
    #I already wrote it.
    def can_rotate(self, board, direction):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated:
            1. Compute the position of each block after rotation 
            2. Check if the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        for block in self.blocks: 
            dx, dy = self.calc_rot_coords(block, direction)
            if block.can_move(board, dx, dy):
                continue
            else:
                return False
        return True 
        
    def do_rotate(self, direction):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Compute the position of each block after rotation
            2. Move the block to the new position    
        ''' 
        for block in self.blocks:
            dx, dy = self.calc_rot_coords(block, direction)
            block.move(dx, dy) 
        return None 
    
    def can_kick(self, board, direction, kick_offset): 
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated and kicked into the position
            determined by the kick offset: 
            1. Compute the position of each block after rotation and with the kick
            offset applied.
            2. Check if the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        #The rotation and kick_offset can be done in one go during the checking
        #phase because the center block is not being moved. The rotation formula
        #calc_rot_coords uses the center block as an origin point. If the center
        #block is moved before all the block's new rotational position is calculated
        #it throws of the calculation.
        for block in self.blocks: 
            dx, dy = self.calc_rot_coords(block, direction)
            kick_dx = dx + kick_offset[0]
            kick_dy = dy + kick_offset[1]
            if block.can_move(board, kick_dx, kick_dy):
                continue
            else:
                return False
        return True
    
    def do_kick(self, direction, kick_offset): 
        ''' Parameters: direction - type: int
                        kick_offset - type: int tuple 
            
            Return value: None 
            
            rotates and kicks the shape:
            1. Rotate the whole shape
            2. Compute the position of each block after kick with the 
               kick_offset 
            3. Move the block to the new position    
        ''' 
        #In this method the shape needs to be rotated first and then kicked, unlike
        #can_kick because the function calc_rot_coords uses the center block as an
        #origin point. If the center block is moved before all the other block's
        #new rotated positions are caluclated, it throws of the calculation for those
        #block.
        self.do_rotate(direction) 
        for block in self.blocks:
            #Not using tuple unpacking to keep the code similar
            #to the code in can_kick() function.
            kick_dx = kick_offset[0]
            kick_dy = kick_offset[1]
            block.move(kick_dx, kick_dy)
        return None

    def calc_kick_translation(self, curr_state, next_state, column):
        ''' Parameters: curr_state - type: int
                        next_state - type: int
                        column - type: int
            
            Return: kick_translation - type: int tuple 

            Calculates the kick offset of the current shape based on the
            current state and the next state. 
        '''
        tuple_current = self.KICK_OFFSET[curr_state][column]
        tuple_next = self.KICK_OFFSET[next_state][column]
        kick_translation = map(lambda c,n: c-n, tuple_current, tuple_next)
        kick_translation = tuple(kick_translation)
        return kick_translation

    def calc_rot_state(self, direction):
        ''' Parameters: direction - type: int
            
            Return: new_sate - type: int 
            
            Calculates the new rotation of the state by taking in the current state
            and the input. Input can only be 1 or -1. -1 for clockwise and 1 for 
            counter-clockwise.  Tetris guideline 2022 defines what all the rotation
            states are. Formula derived to satisfy these states. For the formula 
            (state+dir)%4 to work the spawn state needs to = 2 and the inputs must 
            be -1 for clockwise and 1 for counter-clockwise. Tetris guideline 2022 
            defines what all the rotation states are. 
            
            Rotaton states:
            Spawn =  0
            Counter-clockwise =  1
            Consecutive rotation =  2
            Clockwise =  3
        '''
        #Calculating the new state
        state_int = self.rotation_state
        #Derived the formula myself
        new_state = (state_int+direction)%4
        return new_state 

    def calc_rot_coords(self, block, direction):
        ''' Parameters: block - type: Block
            Return: type: int  
            Calculates a new position for each block based on the direction
            of rotation of the shape. Returns the difference between the old 
            coordinates and the new coordinates (Since all other move functions use
            dx and dy).
            The formula used was given in the assignment pdf.
        ''' 
        center_x, center_y = self.center_block.get_coords()
        rot_dir = direction
        block_x, block_y = block.get_coords()        
        
        new_x = center_x - rot_dir*center_y + rot_dir*block_y
        new_y = center_y + rot_dir*center_x - rot_dir*block_x
        
        dx = new_x - block_x
        dy = new_y - block_y  
        return (dx,dy)

    def set_rot_states(self, next_state, offset_used, last_move_rot):
        ''' Parameters: offset_used - type:int
                        next_state - type:int
                        last_move_rot - type:bool
            Return: None

            Sets the variables which tracks the last rotation in detail.
            this information is used in other functions.
        '''
        self.rot_offset_used = offset_used 
        self.rotation_state = next_state 
        self.last_move_rot = last_move_rot 
        if self.soft_lock == True:
            self.soft_locks_left -= 1
        return None

    def rotate(self, board, direction):
        ''' Parameters: board - type: Board object
                        direction - type: int 

            Return: None 
           
            The rotation system goes through offsets, after rotating the blocks around
            the center block, to see what position the shape can be rotated into. The
            first test for all shapes, except the I and O shape, are default rotation
            with no kick offset.
            The first offset that works is what the shape is rotated then kicked  into. 
            If none of the offsets work, then the shape is not rotated or kicked. Offsets 
            were taken from the "How SRS really works" from the SRS section of the Tetris 
            Guideline, 2022.
        '''
        curr_state = self.rotation_state
        next_state = self.calc_rot_state(direction)
        #Just a little sanity check
        len_current = len(self.KICK_OFFSET[curr_state])
        len_next = len(self.KICK_OFFSET[next_state]) 
        #Just a little sanity check
        if len_current == len_next:
            for j in range(len_current):
                kick_offset = self.calc_kick_translation(curr_state, next_state, j)  
                if self.can_kick(board, direction, kick_offset) == True:
                    self.do_kick(direction, kick_offset)
                    self.set_rot_states(next_state, j, True) 
                    break   
        return None
    
    def was_last_move_rot(self):
        ''' Parameters: None
            Return: type:bool - self.last_move_rot

            Returns the latest value of self.last_move_rot variable
        '''
        return self.last_move_rot

    def soft_lock_state(self):
        ''' Parameters: None
            Return: type: bool
            Returns true if shape is in soft lock state, false otherwise.
        '''
        return self.soft_lock

    def soft_lock_move(self):
        ''' Parameters: None
            Return: type: Bool 
            Returns true if the shape has any soft locks left, returns
            false otherwise.
        '''
        if self.soft_locks_left > 0:
            return True 
        return False

    def soft_lock_on(self):
        ''' Parameters: None
            Return: None
            Puts the shape in soft lock state by setting the self.soft_lock
            variable to True.
        '''
        self.soft_lock = True
        return None

    def soft_lock_reset(self):
         ''' Parameters: None
             Return: None
             Resets the soft_lock state of the shape
             to spawn conditions.
        '''
         self.soft_lock = False
         return None


############################################################
# ALL SHAPE CLASSES
############################################################
#Each shape has a different center.
#The center is the one without any offset.
class I_shape(Shape):
    def __init__(self, center, color = 'cyan', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    ),    
                  gr.Point(center.x + 2, center.y    )]
        Shape.__init__(self, coords, color, block_sz)
        #These need to be after shape class init
        self.center_block = self.blocks[1]
        #For reference, the state numbers correspond to the rows on the array:
        #ROTATION_STATES = {"spawn":0, "counter_clockwise":1, "consecutive":2, "clockwise":3}
        #The offset values are taken from the Tetris Guideline 2022. The signs of the y-axis 
        #offset values are flipped relative to the sign of the values in the guideline becaus
        #the y-axis here is flipped. 
        #Override shape class kick offset because I shape requires different offsets.
        self.KICK_OFFSET = [[(0,0), (-1,0), (2,0), (-1,0), (2,0)],
                           [(0,-1), (0,-1), (0,-1), (0,1), (0,-2)],
                           [(-1,-1), (1,-1), (-2,-1), (1,0), (-2,0)],
                           [(-1,0), (0,0), (0,0), (0,-1), (0,2)]]

class J_shape(Shape):
    def __init__(self, center, color = 'RoyalBlue', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y - 1),
                  gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    )]
        Shape.__init__(self, coords, color, block_sz)         
        #This needs to be after shape class init
        self.center_block = self.blocks[2]

class L_shape(Shape):
    def __init__(self, center, color = 'orange', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    ),
                  gr.Point(center.x + 1, center.y - 1)]
        Shape.__init__(self, coords, color, block_sz)         
        #This needs to be after shape class init
        self.center_block = self.blocks[1]

class O_shape(Shape): 
    def __init__(self, center, color = 'yellow1', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x    , center.y - 1),
                  gr.Point(center.x + 1, center.y - 1),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    )]
        Shape.__init__(self, coords, color, block_sz)
        #These need to be after shape class init. 
        self.center_block = self.blocks[2]
        #For reference, the state numbers correspond to the rows on the array:
        #ROTATION_STATES = {"spawn":0, "counter_clockwise":1, "consecutive":2, "clockwise":3}
        #Yes, I know I can just override the rotation funciton of the 
        #main shape class but doing this keeps true to the guidelines.
        #and maybe who knows theres another niche game mechanic associated
        #with it. The O shape needs offsets because it's "true rotation"
        #has a wobble. This wobble is corrected by these offsets.
        #Y-axis is flipped here so I flipped the signs of the y-values.
        self.KICK_OFFSET = [[(0,0)],
                           [(-1,0)],
                           [(-1,1)],
                           [(0, 1)]] 
    
class S_shape(Shape):
    def __init__(self, center, color = 'chartreuse', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x    , center.y - 1),
                  gr.Point(center.x + 1, center.y - 1)]
        Shape.__init__(self, coords, color, block_sz)
        #This needs to be after shape class init
        self.center_block = self.blocks[1]

class T_shape(Shape):
    def __init__(self, center, color = 'DarkViolet', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x    , center.y - 1),
                  gr.Point(center.x + 1, center.y )]
        Shape.__init__(self, coords, color, block_sz)
        #Only this one line below needs to be after shape class init 
        self.center_block = self.blocks[1]
        #All the coordinates that need to be checked to satisfy the conditions
        #of a T-Spin. At least three of these coordinates, relative to the center
        #block, must be occupied for the move to count as a T-Spin.
        self.T_SPIN_CHECK = [(-1,-1),(1,-1),(-1,1),(1,1)] 
        #For reference, the state numbers correspond to the rows on the array:
        #ROTATION_STATES = {"spawn":0, "counter_clockwise":1, "consecutive":2, "clockwise":3}
        #The "front" of the t-mino is defined by where the sticking out mino is.
        #The front changes based on the rotational state of the mino. Each row
        #corresponds to the state of the mino (0,1,2,3) and the two coordinates
        #are the front corners of the mino in that rotational state, relative 
        #to the center block's position.
        self.FRONT = [[(-1,-1) , (1,-1)],
                     [ (-1,-1) , (-1,1)],
                     [ (-1,1)  ,  (1,1)],
                     [ (1,-1)  ,  (1,1)]]

    def tspin(self, board):
        i = 0
        for pos in self.T_SPIN_CHECK:
            dx, dy = pos
            print dx, dy #NOTE NOTE NOTE
            if self.center_block.can_move(board, dx, dy) == False:
                i += 1 
            
        if i >= 3:
            print i #NOTE NOTE NOTE
            return True
        return False

    def full_or_mini(self, board):
        i = 0 
        state = self.rotation_state 
        for pos in self.FRONT[state]:
            dx, dy = pos
            print dx, dy #NOTE NOTE NOTE 
            print self.center_block.can_move(board, dx, dy) #NOTE NOTE NOTE
            if self.center_block.can_move(board, dx, dy) == False:
                i += 1

        print i #NOTE NOTE NOTE
        print "rot offset used", self.rot_offset_used #NOTE NOTE NOTE
        if i == 2:
            return True
        elif self.rot_offset_used == 4:
        #From the Tetris guidelines. Even if only one of the front corners
        #of the T-mino is occupied, it still counts as a full t-spin if
        #the last rotation moved the center of the T-mino 1 block left or right and 
        #2 blocks up or down (i.e. if the last offset rotational offset is used).
            return True
        return False 

class Z_shape(Shape):
    def __init__(self, center, color = 'red', block_sz = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y - 1),
                  gr.Point(center.x    , center.y - 1), 
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    )]
        Shape.__init__(self, coords, color, block_sz)
        #This needs to be after shape class init 
        self.center_block = self.blocks[2]


