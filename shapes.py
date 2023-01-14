#Name: Ankush Burman
# Section: Self
# Date: Started: Mar 16, 2022; 
# shapes.py

import graphics35 as gr
import copy   

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
                    block_size - type:int - The size of blocks in terms of pixels
                    color - type:string - The color of the block 
        specify the position on the tetris board
        in terms of the square grid
    '''
    #Determines the block size in terms of pixels
    BLK_SIZE = 30 
    #Determines the outline of each block in terms of pixels
    OUTLINE_WIDTH = 3
    #Sets the colour of the outline of the block
    OUTLINE_COLOR = "black"

    def __init__(self, pos, color, block_size = BLK_SIZE):
        self.x = pos.x
        self.y = pos.y
        self.block_size = block_size  
        pixel_point1 = gr.Point(block_size*pos.x, block_size*pos.y)
        pixel_point2 = gr.Point(block_size*pos.x+block_size, block_size*pos.y+block_size)
        gr.Rectangle.__init__(self, pixel_point1, pixel_point2)
        
        if color:                        
            self.color = color.lower()
        else:
            self.color = ''
        
        self.setFill(self.color)
        self.setOutline(Block.OUTLINE_COLOR)
        self.setWidth(Block.OUTLINE_WIDTH)
    
    def get_coords(self):
        ''' Parameters: None
            Return value type: int tuple 
            Returns the current x,y position of the block.
        '''
        point_1 = self.getP1()
        x = point_1.getX()
        y = point_1.getY()
        x = (x/self.block_size)
        y = (y/self.block_size)
        return (x, y)
    
    def get_block_size(self):
        ''' Parameters: None
            Return: int 
            
            Returns the block size of the block in terms of pixels
        '''
        return self.block_size
    
    def can_move(self, board, dx, dy):
        ''' Parameters: board - type: PlayBoard
                        dx - type: int
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


############################################################
# SHAPE CLASS
############################################################
class Shape(object):
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: center_index - type:int - the index of where the center block is in 
                                              the list of blocks. 
                    blocks - type:list - the list of blocks making up the shape
                    rotation_sate - type:int - the current rotational state of the shape 
                    can_hold - type:Bool - Hold can only be used once per new shape spawn.
                                        This flag determines if hold has been used or not.
                                        This variable should be set to false when it the 
                                        shape is being re-created from the hold system. 
                    soft_lock - type:Bool - Determines if the shape is in soft_lock state
                                             or not.
                    soft_locks_left - type:int - Keeps track of the number of times the 
                                                 shape has been moved while in soft_lock
                                                 state. A shape can be moved a maximum of
                                                 15 times in soft_lock state.
                    self.rot_offset_used - type:int - Stores which of the 5 rotational
                                           offset was used, last time the shape was kicked
                                           into position.
                    self.last_move_rot - type:Bool - Tracks the last successful move 
                                                  performed by the shape. If last move is 
                                                  a rotation then this variable is set to 
                                                  true. If last move is down, left, or right 
                                                  then this variable is set to false. 
                    KICK_OFFSET - type:2 dimensional array - Holds the kick offset 
                                  values for J, L, S, T, Z shapes. Each row in the array
                                  corresponds to the rotational state of the shape. Each
                                  column is the offset test number which must be done in 
                                  that order. I shape has it's own unique offset values.
                                  O shape does not rotate.
                    center_block - type:block - The center block of the shape.
    '''
    #Really for reference, the state numbers correspond to the rows in self.KICK_OFFSET array.
    ROTATION_STATES = {"spawn":0, "counter_clockwise":1, "consecutive":2, "clockwise":3}

    def __init__(self, coords, center_index, color, block_size = Block.BLK_SIZE):
        self.center_index = center_index
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
            self.blocks.append(Block(pos, color, block_size))
        #This must be done AFTER the previous line
        self.center_block = self.blocks[center_index]

#############################################################
#Functions that return internal variables:

    def get_blocks(self):
        '''returns the list of blocks
        '''
        return self.blocks
    
    def get_center_index(self):
        ''' Parameters: None
            Return: None

            Returns the index of of the center block in the block list
        '''
        return self.center_index

    def get_center_block(self):
        ''' Parameters: None
            Return: None
            
            Returns the center block of the shape
        '''
        return self.center_block
    
    def get_rotation_state(self):
        ''' Parameters: None
            Return: None

            Returns the rotation state of the shape
        '''
        return self.rotation_state 
    
    def was_last_move_rot(self):
        ''' Parameters: None
            Return: type:bool - self.last_move_rot

            Returns the latest value of self.last_move_rot variable
        '''
        return self.last_move_rot

    def get_soft_lock_state(self):
        ''' Parameters: None
            Return: type: bool
            Returns true if shape is in soft lock state, false otherwise.
        '''
        return self.soft_lock


#############################################################
#Functions related to drawing on screen:
    
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
     
#############################################################
#Functions related to movement:

    def can_move(self, board, dx, dy):
        ''' Parameters: board - type: PlayBoard
                        dx - type: int
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
        ''' Parameters: board - type: PlayBoard
            
            Return value: type: bool

            checks to see if the shape can move down 
            or not.
        '''
        dx = 0
        dy = 1
        return self.can_move(board, dx, dy) 
    
    def soft_lock_can_move(self):
        ''' Parameters: None
            Return: type: Bool 
            Returns true if the shape has any soft locks left, returns
            false otherwise.
        '''
        if self.soft_locks_left > 0:
            return True 
        return False
    
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
        ''' Parameters: board - type: PlayBoard
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
    
#############################################################
#Functions related to rotation of the shape:
    
    #Not using this function right now but keeping it in here since
    #I already wrote it.
    def can_rotate(self, board, direction):
        ''' Parameters: board - type: PlayBoard 
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
        ''' Parameters: board - type: PlayBoard

            rotates the shape:
            1. Compute the position of each block after rotation
            2. Move the block to the new position    
        ''' 
        for block in self.blocks:
            dx, dy = self.calc_rot_coords(block, direction)
            block.move(dx, dy) 
        return None 
    
    def can_kick(self, board, direction, kick_offset): 
        ''' Parameters: board - type: PlayBoard
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
        ''' Parameters: board - type: PlayBoard
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
    

#############################################################
#Functions that turn soft lock on or off:
    
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
# GHOSTSHAPE CLASS
############################################################
class Ghost_shape(Shape):
    ''' A child of the shape class which implements the ghost shape functionality
        Attributes: coords - type: list of type: Point - Holds the coords of the main shape
                    center_index: type: Point - Holds the center coordinate of the main shape
                    color: type: String - Holds the colour of the ghost shape
                    outline: type: String - Holds the colour of the outline of the ghost shape 
                    target_coords: type: list - Holds the final coords that the ghost shape
                                                shape should occupy.
    '''

    def __init__(self, board, main_shape, block_size = Block.BLK_SIZE):
        coords = self.extract_coords(main_shape)
        center_index = main_shape.get_center_index()
        self.color = ''
        self.outline = "SlateGrey"
        self.target_coords = None 
        Shape.__init__(self, coords, center_index, self.color, block_size)   
        self.init_ghost(board, main_shape)

    def init_ghost(self, board, main_shape):
        ''' Paramters: board - type: PlayBoard
                       main_shape - type: Shape
            
            Return: None

            Initializes the ghost shape after instance is created.
            Sets the outline color of all blocks.
            Updates the position based on main shape's position
        '''
        for block in self.blocks:
            block.setOutline(self.outline)

        self.update(board, main_shape) 
        return None 

    #Note: Not using this function right now
    #but leaving it in since I already wrote it. 
    #Might need it in the future.
    def extract_coords(self, shape):
        ''' Paramters: shape: type - shape
            
            Return: curr_coords: type - list of Point

            Given a shape, returns a list of the coordinates of all it's
            blocks as Point variables.
        '''
        curr_coords = []
        coord_list = self.copy_coords(shape)
        for coord in coord_list:
            x, y = coord
            coord_point = gr.Point(x, y) 
            curr_coords.append(coord_point)
        return curr_coords

    def copy_coords(self, shape):
        ''' Parameters: shape - type: Shape
            
            Return: coords - type: list of tuples

            Given a shape, returns a list of the coordinates of 
            all it's blocks.
        '''
        blocks_list = shape.get_blocks()
        coords = []
        for block in blocks_list:
            x, y = block.get_coords()
            coords.append((x,y))
        return coords
    
    def calc_dx_dy(self, coord, target):
        ''' Parameters: coord - type: tuple of int
                        target- type: tuple of int

            return: dx, dy - type: tuple of int

            Calculates the difference between two sets of
            coordinates.
        '''
        x, y = coord
        new_x, new_y = target
        dx = new_x - x
        dy = new_y - y
        return dx, dy
    
    def check_coords(self, board, target_coords):
        ''' Parameter: board - type: PlayBoard
                       target_coords - type: List of tuples

            Return: type - Bool

            Given a list of coordinates, checks to see if the 
            coordinates are viable and that blocks can be moved 
            into these coordinates.
        '''
        for coord in target_coords:
            x, y = coord 
            if board.can_move(x, y) == True: 
                continue
            else:
                return False
        return True 

    def position_sync_better(self, board, target_coords):
        ''' Paramters: board - type: PlayBoard
                       target_coords - type: List of tuples
            
            Return: None

            Moves the ghost shape (self) to the target coords.
            "Poisition and rotation syncs with the main shape"
            In quotation because the ghost shape does not exactly share
            the same coordinates as the main shape, shares the same x-coordinates.
        '''
        block_list = self.get_blocks() 
        #A little sanity check 
        if len(target_coords) != len(block_list):
            raise RuntimeError("Target coords list length does not match blocks list length")
        else:
            for target, block in zip(target_coords, block_list):
                block_coord = block.get_coords()
                dx, dy = self.calc_dx_dy(block_coord, target) 
                block.move(dx, dy)
        return None 
    
    def calc_delta_y(self, board, coord_list):
        ''' Paramters: board - type: PlayBoard
                       coord_list - type: list of tuples
            
            Return: delta_y - type: int

            Calculates the smallest delta in the y-direction between 
            the all the coordinates in the coord_list and the highest block
            on the tetris board.
        '''
        highest_blocks = board.get_highest_blocks()
        
        #Set delta_y 
        board_height = board.get_height()
        total_board_height = board.get_total_height()
        #Intial delta_y can be set to any high number, should be
        #larger than the difference of shape spawn y-coord and board height
        delta_y = total_board_height + 1000 
        
        for coord in coord_list:
             x = coord[0]
             y = coord[1]
             if x in highest_blocks:
                 #1 is substracted because the ghost shape
                 #needs to end up above the highest block
                 #in the column
                 delta = highest_blocks[x] - y - 1
                 if delta < delta_y:
                     delta_y = delta
             else: 
                 #1 is substracted because board_height is set to "20"
                 #while the index for the rows begin at 0 and go to 19
                 #making 20 rows. 
                 delta = board_height - y - 1
                 if delta < delta_y:
                     delta_y = delta 
        return delta_y 

    def calc_target_coords_better(self, board, shape):
        ''' Parameters: board: type - PlayBoard
                        shape: type - Shape

            Return: new_list - type: list

            Calculates target coords for the ghost shape based
            on the shape that is passed to this function.
            Target coords are calculated by copying the current coordinates
            of the shape and then calculating the lowest y-position the 
            shape can occupy.
        '''
        new_list = []
        coord_list = self.copy_coords(shape) 
        delta_y = self.calc_delta_y(board, coord_list) 

        for coord in coord_list:
            x = coord[0]
            y = coord[1] + delta_y 
            new_list.append((x,y)) 
        return new_list 

    def update(self, board, main_shape):
        ''' Parameters: board: type - PlayBoard
                        main_shape: type - Shape

            Updates the ghost shape's position and rotation in regards
            to the main shape.
        '''
        if main_shape.can_move_down(board) == True:
            target_coords = self.calc_target_coords_better(board, main_shape)
        else:
            target_coords = self.copy_coords(main_shape)

        if self.check_coords(board, target_coords) == True:
            self.position_sync_better(board, target_coords)
        return None  
       

############################################################
# TETROMINO SHAPE CLASSES
############################################################
#Each shape has a different center.
#The center is the one without any offset.
class I_shape(Shape):
    def __init__(self, center, color = 'cyan', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    ),    
                  gr.Point(center.x + 2, center.y    )]
        center_index = 1
        Shape.__init__(self, coords, center_index, color, block_size)
        #These need to be after shape class init  
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
    def __init__(self, center, color = 'RoyalBlue', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y - 1),
                  gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    )]
        center_index = 2
        Shape.__init__(self, coords, center_index, color, block_size)         

class L_shape(Shape):
    def __init__(self, center, color = 'orange', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    ),
                  gr.Point(center.x + 1, center.y - 1)]
        center_index = 1 
        Shape.__init__(self, coords, center_index, color, block_size)         

class O_shape(Shape): 
    def __init__(self, center, color = 'yellow1', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x    , center.y - 1),
                  gr.Point(center.x + 1, center.y - 1),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    )]
        center_index = 2
        Shape.__init__(self, coords, center_index, color, block_size)
        #These need to be after shape class init.  
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
    def __init__(self, center, color = 'chartreuse', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x    , center.y - 1),
                  gr.Point(center.x + 1, center.y - 1)]
        center_index = 1
        Shape.__init__(self, coords, center_index, color, block_size)

class T_shape(Shape):
    def __init__(self, center, color = 'DarkViolet', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y    ),
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x    , center.y - 1),
                  gr.Point(center.x + 1, center.y )]
        center_index = 1
        Shape.__init__(self, coords, center_index, color, block_size)
        #All the coordinates that need to be checked to satisfy the conditions
        #of a T-Spin. At least three of these coordinates, relative to the center
        #block, must be occupied for the move to count as a T-Spin.
        self.T_SPIN_CHECK = [(-1,-1),(1,-1),(-1,1),(1,1)] 
        #For reference, the state numbers correspond to the rows on the array:
        #ROTATION_STATES = {"spawn":0, "counter_clockwise":1, "consecutive":2, "clockwise":3}
        #The "front" of the t-mino is defined by where the sticking out block is.
        #The front changes based on the rotational state of the mino. Each row
        #corresponds to the state of the mino (0,1,2,3) and the two coordinates
        #are the front two blocks (next to the sticking out block) of the mino in 
        #that rotational state, relative to the center block's position.
        self.FRONT = [[(-1,-1) , (1,-1)],
                     [ (-1,-1) , (-1,1)],
                     [ (-1,1)  ,  (1,1)],
                     [ (1,-1)  ,  (1,1)]]

    def tspin(self, board):
        ''' Parameters: board: type - PlayBoard 
            
            Return: Bool

            Detects if a "t-spin" move has been performed on this
            instance of the t-shape. T-spin move detection algorithm 
            according to Tetris guideline 2022. 
        '''
        i = 0
        for pos in self.T_SPIN_CHECK:
            dx, dy = pos
            if self.center_block.can_move(board, dx, dy) == False:
                i += 1 
            
        if i >= 3:
            return True
        return False
    
    def calc_front_full(self, board):
        ''' Parameters: board - type: PlayBoard

            Return: i - type: int

            Calculates the number of "front" blocks which are 
            occupied in regards to the t-shape. Front blocks dependend
            on rotational state and the positions, in regards to the t-shape,
            are defined in the init function of this shape.
        '''
        i = 0 
        state = self.rotation_state 
        for pos in self.FRONT[state]:
            dx, dy = pos
            if self.center_block.can_move(board, dx, dy) == False:
                i += 1
        return i

    def full_or_mini(self, board):
        ''' Parameters: board: type: Playboard
           
           Return: Bool - True (if full t-spin)
                          False (if mini t-spin)

           Detects if the t-spin move was a full t-spin or a mini
           t-spin. Mini or full detection based on tetris guideline 2022
        '''
        i = self.calc_front_full(board) 
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
    def __init__(self, center, color = 'red', block_size = Block.BLK_SIZE):
        coords = [gr.Point(center.x - 1, center.y - 1),
                  gr.Point(center.x    , center.y - 1), 
                  gr.Point(center.x    , center.y    ),    #Centre
                  gr.Point(center.x + 1, center.y    )]
        center_index = 2 
        Shape.__init__(self, coords, center_index, color, block_size)


############################################################
# END OF FILE                                              # 
############################################################
