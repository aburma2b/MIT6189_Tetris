# Name: Ankush Burman
# Section: Self
# Date: Started: July 20, 2022; 
# tests.py

import graphics35 as gr
import shapes as sh
import boards as br
import tetris as te 

############################################################
# TEST SHAPES CLASSES
############################################################
class tspin_zero_shape(sh.Shape):
    '''Tspin single shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a full or
                                 mini t-spin zero line clear. (Mini t-spin
                                 is tested by rotating the shape counter-clockwise
                                 and then clockwise)
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group in row 16
        for x in range (6,8):
            if self.mirror == True:
                x = abs(9-x)
            y = 16
            self.coords.append(gr.Point(x, y)) 
        
        #Second group in row 17
        for x in range(1,4) + range(7,9):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x, y))

        #Fourth group in row 18
        for x in range(1,5) + range(6, 9):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))

        #Sixth group in all of row 19
        for x in range(1, 9):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None 

        
class tspin_single_shape(sh.Shape):
    '''Tspin single shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a full or
                                 mini t-spin single line clear. (Mini t-spin
                                 is tested by rotating the shape counter-clockwise
                                 and then clockwise)
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group in row 17
        for x in range(6,8):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x, y)) 
        
        #Second group in row 18
        for x in range(1,4) + range(7,9):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x, y))

        #Fourth group in row 19
        for x in range(5) + range(6, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None 


class tspin_double_shape(sh.Shape):
    '''Tspin double shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a full t-spin
                                 double clear. (Mini t-spin single line clear can 
                                 also be tested by rotating the shape counter-clockwise
                                 and then clockwise)
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''

    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group in row 17
        for x in range(6,8):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x, y)) 
        
        #Second group in row 18
        for x in range(4) + range(7,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x, y))

        #Fourth group in row 19
        for x in range(5) + range(6, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None 


class tspin_triple_shape(sh.Shape):
    '''Mini t-spin double line shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a full t-spin triple line
                                 clear.
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group: One block in row 15
        x = 1
        y = 15
        if self.mirror == True:
            x = abs(9-x) 
        self.coords.append(gr.Point(x,y))

        #Second group: column - 0 & from rows 15 to 19
        for y in range(15, 20):
            x = 0
            if self.mirror == True:
                x = abs(9-x)
            self.coords.append(gr.Point(x,y))

        #Thirs group in row 17
        for x in range(2,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x,y))

        #Third group in row 18
        for x in range(3, 10): 
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))

        #Fourth group in row 19
        for x in range(2, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None


class offset_tspin_double_shape(sh.Shape):
    '''Offset t-spin double line shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a  t-spin double line
                                 clear when the t-shape's center is moved 1 by 2 blocks
                                 (when the shape is kicked using the last kick offset)
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group: One block in row 15
        x = 1
        y = 15
        if self.mirror == True:
            x = abs(9-x)
        self.coords.append(gr.Point(x,y))

        #Second group: column - 0 & from rows 15 to 19
        for y in range(15, 20):
            x = 0
            if self.mirror == True:
                x = abs(9-x)
            self.coords.append(gr.Point(x,y))

        #Thirs group in row 17
        for x in range(2,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x,y))

        #Third group in row 18
        for x in range(3, 10): 
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))

        #Fourth group in row 19
        for x in range(3, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None


class wall_mini_single_shape(sh.Shape):
    '''Mini t-spin wall single line shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a mini t-spin single line
                                 clear when the shape is against the wall.
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First  group in row 19
        for x in range(1, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None


class mini_double_shape(sh.Shape):
    '''Mini t-spin wall single line shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a mini t-spin double line
                                 clear when the shape is against the wall.
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is True to align it with the rest of the test 
                                patterns.
     '''
    #Yes mirror = True so it aligns with the default alignment of all other shapes
    def __init__(self, mirror = True):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = not mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group in column 9
        for y in range(14, 20): 
            x = 9
            if self.mirror == True:
                x = abs(9-x)
            self.coords.append(gr.Point(x,y))

        #Second group in column 8
        for y in range(14, 16) + range(17,20):
            x = 8
            if self.mirror == True:
                x = abs(9-x)
            self.coords.append(gr.Point(x,y))

        #Third group: single block
        x = 7
        y = 15
        if self.mirror == True:
            x = abs(9-x)
        self.coords.append(gr.Point(x,y))

        #Fourth group: row 18
        for x in range(6):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))

        #Fifth group: row 19
        for x in range(7):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None


class crazy_tspin_triple_shape(sh.Shape):
    '''crazy t-spin triple line shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a "crazy" setup for 
                                 a full t-spin triple line clear.
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First row: 14
        for x in range(2) + range(4,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 14
            self.coords.append(gr.Point(x,y))

        #Second row: 15
        for x in range(1) + range(4,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 15
            self.coords.append(gr.Point(x,y))

        #Third row: 16
        for x in range(10):
            if self.mirror == True:
                x = abs(9-x)
            y = 16
            self.coords.append(gr.Point(x,y))

        #Fourth row: 17
        for x in range(3) + range(4,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x,y))

        #Fifth row: 18
        for x in range(3) + range(5,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))

        #Sixth row: 19
        for x in range(3) + range(4,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None


class combo_test_shape(sh.Shape):
    '''combo test shape class: A pattern of blocks which can be used to test combos

       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First row: 14
        for y in range(3, 20):
            for x in range(8):
                if self.mirror == True:
                    x = abs(9-x)
                self.coords.append(gr.Point(x,y))


class backtoback_test_shape(sh.Shape):
    '''backtoback test shape class: A pattern of blocks which can be used to test 
                                    back-to-back bonuses.

       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First row: 14
        for y in range(3, 20):
            for x in range(9):
                if self.mirror == True:
                    x = abs(9-x)
                self.coords.append(gr.Point(x,y))


class tspin_combo_break_shape(sh.Shape):
    '''Tspin combo break shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test a combo break
                                 with a full or mini t-spin zero line clear (Mini t-spin
                                 is tested by rotating the shape counter-clockwise
                                 and then clockwise).
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror 
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''
        #First group in row 15
        for x in range (6,8):
            if self.mirror == True:
                x = abs(9-x)
            y = 15
            self.coords.append(gr.Point(x, y)) 
        
        #Second group in row 16
        for x in range(2,4) + range(7,8):
            if self.mirror == True:
                x = abs(9-x)
            y = 16
            self.coords.append(gr.Point(x, y))

        #Fourth group in row 17
        for x in range(2,5) + range(6, 8):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x,y))

        #Sixth group in all of row 18
        for x in range(2, 9):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))
        
        #Seventh group in all of row 19
        for x in range(1, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None 


class tspin_combo_continue_shape(sh.Shape):
    '''Tspin combo continue shape class: A pattern of blocks at the bottom of the 
                                 board which can be used to test continuing a combo
                                 with full or mini t-spin single line clear. (Mini t-spin
                                 is tested by rotating the shape counter-clockwise
                                 and then clockwise)
       Attributes:
           color - type:string - The color of the blocks of this test shape
           coords - type:list - The list of coordinates of all the blocks stores
                                as gr.Point objects.
           mirror - type:bool - Holds the selected value for the test pattern to be mirrored
                                default is False. 
     '''
    def __init__(self, mirror = False):
        self.color = "SlateGray"
        self.coords = []
        self.mirror = mirror
        self.init_coords()
        center_index = 1
        sh.Shape.__init__(self, self.coords, center_index, self.color) 

    def init_coords(self):
        ''' Parameters: None
            Return: None

            Initializes all the coordinates as gr.Point objects for the
            shape.
        '''

        #First group in all of row 15
        for x in range(0, 9):
            if self.mirror == True:
                x = abs(9-x)
            y = 15
            self.coords.append(gr.Point(x,y)) 
        
        #First group in row 16
        for x in range(6,8):
            if self.mirror == True:
                x = abs(9-x)
            y = 16
            self.coords.append(gr.Point(x, y)) 
        
        #Second group in row 17
        for x in range(2,4) + range(7,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 17
            self.coords.append(gr.Point(x, y))

        #Fourth group in row 18
        for x in range(2,5) + range(6, 10):
            if self.mirror == True:
                x = abs(9-x)
            y = 18
            self.coords.append(gr.Point(x,y))

        #Fifth group in row 19
        for x in range(1,10):
            if self.mirror == True:
                x = abs(9-x)
            y = 19
            self.coords.append(gr.Point(x,y))
        return None


############################################################
# TEST TETRIS CLASSES
############################################################
class Test_tetris(te.Tetris):
    ''' Test_tetris class:
        A child class of the Tetris class with additional functionality
        which makes setting up tests easier.

        Attributes: test_shape - type:Shape - A test block pattern which is
                                              initially deposited on the board for
                                              testing purposes depending on the test.
                    test_current_shape - type:Shape - The tetromino with which the test
                                                      will be conducting. Some tests like
                                                      T-spin tests can only be done with
                                                      a T-tetromino. This variable is mainly
                                                      used when the test is being reset.
                    mirror - type:Bool - Holds the variable to determine if the test
                                         should me mirrored or not.
    '''
    def __init__(self, win, test_shape = None):
        self.test_shape = test_shape
        self.test_current_shape = None
        self.mirror = False 
        te.Tetris.__init__(self, win)
    
    def set_test_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return None

            Sets the test_shape variable
        '''
        self.test_shape = shape
        return None

    def set_test_current_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return: None

            Sets the test_current_shape variable
        '''
        self.test_current_shape = shape
        return None
    
    def set_current_shape(self, shape):
        ''' Parameters: shape - type: Shape
           Return None
           
           Sets the current active shape on the board
        '''
        #Undrawing ghost shape as a precuation
        self.ghost_shape.undraw() 
        self.current_shape = shape
        self.ghost_shape = sh.Ghost_shape(self.board, self.current_shape)
        return None

    def set_mirror(self, mirror):
        ''' Parameters: mirror - type: Bool
            Return: None

            Sets the mirror variable
        '''
        self.mirror = mirror
        return None
    
    def set_shapes(self, shape_tuple):
        ''' Parameters: shape_tuple - type: Tuple of type: Shape
            Return: None

            Changes the internal SHAPES tuple where active tetrominos are
            drawn.
        '''
        self.SHAPES = shape_tuple
        return None

    def get_test_shape(self):
        ''' Parameters: None
            Return valu: self.test_shape - type: Shape
            
            Returns the test_shape variable.
        '''
        return self.test_shape

    def get_test_current_shape(self):
        ''' Parameters: None
            Return variable: self.test_current_shape - type: Shape

            Returns the test_current_shape variable
        '''
        return self.test_current_shape

    def get_current_shape(self):
        ''' Parameters: None
            Return variable: self.current_shape - type: Shape

            Returns the current_shape variable
        '''
        return self.current_shape

    def get_mirror_status(self):
        ''' Parameters: None
            Return variable: self.mirror - type: Bool

            Returns the mirror variable.
        '''
        return self.mirror
    
    def clear_shape_bags(self):
        ''' Parameters: None
            Return: None

            Clears the internal seven_bag and next_bag variables
        '''
        self.seven_bag = []
        self.next_bag = []
        return None

    def draw_test_shape(self):
        ''' Parameters: None
            Return: None

            Draws and adds the test_shape block pattern to the board
        '''
        self.board.draw_shape(self.test_shape)
        self.board.add_shape(self.test_shape)
        return None

    def create_shape(self, shape):
        ''' Parameters: shape - type: type  
            Return: shape - type: Shape

            Given a type of Shape class, creates that type of Shape and 
            initializes it.
        '''
        x = int(self.BOARD_WIDTH/2-1)
        y = -1
        shape = shape(gr.Point(x, y))
        return shape 
    
    def re_create_shape(self, shape):
        ''' Parameters: shape - type: Shape 
            Return: new_old_shape - type: Shape

            Given a tetromino shape, recreates it at the top center of the board
            If the shape is a test pattern shape then just re-creates, the position
            of the test pattern shapes are built into them.
        '''
        if shape.__class__ in te.Tetris.SHAPES:
            x = int(self.BOARD_WIDTH/2)
            y = -1
            new_old_shape = shape.__class__(gr.Point(x, y))
        else:
           new_old_shape = shape.__class__(self.mirror) 
        return new_old_shape

    def create_t_shape(self):
        ''' Parameters: None
            Return: type:sh.T_shape - t_shape 

            Creates a t-shape at the default starting point of tetris
            and returns it.
        '''
        x = int(self.BOARD_WIDTH/2)
        y = -1
        t_shape = sh.T_shape(gr.Point(x, y))
        return t_shape 
    
    def init_tetris(self):
        ''' Parameters: None
            Return: None

            Prepares tetris and the tetris board for test shape
            setup by stopping the animation and undrawing the randomly
            generated first shape. The first shape should be determined 
            by the test, after test is picked, for easier testing.
        '''
        self.cancel_animation()
        self.current_shape.undraw()
        self.ghost_shape.undraw()
        return None

    def start_tetris(self):
        ''' Parameters: None
            Return: None

            Draws the current shape, which should be determined by the test,
            and then starts running tetris.
        '''
        so_it_does_not_error = self.create_new_shape()
        self.board.draw_shape(self.ghost_shape)
        self.board.draw_shape(self.current_shape)
        
        
        #NOTE THIS NEEDS TO GO AFTER THE GHOST SHAPE HAS BEEN DRAWN
        #Because the ghost shape is created alongside the current_shape
        #which is created before the test shape is added or drawn
        #Therefore the initial ghost shape target coords will clash
        #with the test shape resulting in the test shape not getting draw.
        #(The board does not draw the shape if there are blocks occupying the
        #the space). And there is only one call to draw the shape. If the 
        #ghost shape does not initially get drawn then it will never get draw.
        #Add and draw test shapes
        if not self.test_shape == None:
            self.draw_test_shape()
        
        self.start_animation()
        return None
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            else return False. For testing purposes the score awarded for soft drops
            is disabled. This way it is easier to see if the other moves are being
            score properly.
        ''' 
        direction = direction.lower()
        dx, dy = self.DIRECTION[direction]
        result = self.current_shape.move(self.board, dx, dy)
        self.ghost_shape.update(self.board, self.current_shape)
        if result == True and direction == 'down':
            #self.scr_board.softdrop_score_up()
            pass
        return result
    
    def do_slam(self):
        ''' Parameters: None
            Return: None

            "Slams" the shape shape down and instantly locks in 
            the shape. No soft lock if shape is slammed. For
            testing purposes the score awarded for hard drops is
            disabled. This way it is easier to see if all the other moves
            are being scored properly.
        '''
        while self.do_move("down"):
            #self.scr_board.harddrop_score_up()
            pass
        self.current_shape.soft_lock_on()
        self.shape_lock()
        return None
    
    def key_pressed(self, event):
        ''' Parameters: event - type:event
            Return: None

            this function is called when a key is pressed on the keyboard
            Passes key to tetris control.
        '''
        key = event.keysym #event.keysym is a tkinter function
        key = key.lower()
        print key #NOTE
        self.tetris_control(key)
        return None 
    
    def reset(self):
        ''' Parameters: None
            Return: None

            Resets the whole game and re-starts it.
        '''
        self.cancel_animation()
        self.close_boards()
        self.delete_internal_obj()
        self.prv_board = br.PreviewBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                         sh.Block.BLK_SIZE)
        self.board = br.PlayBoard(win, self.BOARD_WIDTH, 
                                  self.BOARD_HEIGHT, sh.Block.BLK_SIZE, self.PLAYFIELD_HEIGHT)
        self.scr_board = br.ScoreBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                       sh.Block.BLK_SIZE)
        #self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        #self.win.bind_all('<Key>', self.key_pressed)

        # Re-initialize the seven bag system
        # Re-set-up test shapes (if it exists)
        self.seven_bag = []
        self.next_bag = []
        so_it_does_not_error = self.create_new_shape()
        if not self.test_shape == None:
            self.test_shape = self.re_create_shape(self.test_shape)
        self.current_shape = self.re_create_shape(self.test_current_shape) 
        self.ghost_shape = sh.Ghost_shape(self.board, self.current_shape)

        #Re-initialize the hold system
        self.hold_shape = None 

        #Used for controlling lock delay
        self.lock_delay = None

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.ghost_shape) 
        self.board.draw_shape(self.current_shape)
        self.prv_board.draw_preview(self.seven_bag) 
        
        #NOTE THIS NEEDS TO GO AFTER THE GHOST SHAPE HAS BEEN DRAWN
        #Because the ghost shape is created alongside the current_shape
        #which is created before the test shape is added or drawn
        #Therefore the initial ghost shape target coords will clash
        #with the test shape resulting in the test shape not getting draw.
        #(The board does not draw the shape if there are blocks occupying the
        #the space). And there is only one call to draw the shape. If the 
        #ghost shape does not initially get drawn then it will never get draw.
        #Add and draw test shapes
        if not self.test_shape == None:
            self.draw_test_shape()
        
        # Re-start the animation
        self.animation = None 
        self.start_animation()


class Run_test_tetris(object):
    ''' Test_tetris class: The main class which sets up test_tetris and the test_tetris board
                           with initiall test shapes for different scenarios to be tests.
                           And runs the tests.

        Attributes:
            INPUT_LIST - type:tuple - Holds the list of all valid inputs.
            TESTS - type:dictionary - Holds a dictionary of all the tests available
                                      and the corresponding input to run them.
            win - type:gr.Window - the window for the test tetris game
            tetris - type:te.Tetris - the tetris object which all the tests will be run on
            user_test - type:string - Holds the selected value for the test to be run.
    '''

    INPUT_LIST = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
    TESTS = ("Tests:",
             "0: mini or full t-spin zero",
             "1: mini or full t-spin single",
             "2: full t-spin double",
             "3: full t-spin triple",
             "4: offset t-spin double",
             "5: wall mini t-spin single",
             "6: mini t-spin double",
             "7: crazy t-spin triple",
             "8: soft lock test",
             "9: combo test",
             "10: back-to-back bonus test",
             "11: t-spin combo test 1: combo break",
             "12: t-spin combo test 2: combo continue")



    def __init__(self, win, user_input):
        self.win = win  
        self.tetris = Test_tetris(win)
        #self.test_shape = None   
        self.tetris.set_mirror(user_input[1]) 
        self.tetris.init_tetris()
        self.user_test =  user_input[0]
        self.run_input(self.user_test) 

    @staticmethod 
    def get_input():
        ''' Parameters: None
            Return: type:string - user_input

            A static method that polls the user for a valid input,
            that can be accessed without insantiating the class.
            Returns the user_input whena valid input is received.
        '''
        while True:
            user_test = raw_input("Select Test: ")
            if user_test in Run_test_tetris.INPUT_LIST:
                break
            else:
                print "Not a valid input!"

        while True: 
            mirror = raw_input("Mirror test pattern? (Y/n): ")
            if mirror == 'Y':
                mirror = True
                break 
            elif mirror == 'n':
                mirror = False 
                break
            elif mirror == None or mirror == '':
                mirror = False
                break
            else:
                print "Not a valid input!"
        return user_test, mirror 

    def run_input(self, user_input):
        ''' Parameters: type:string - user_input
            Return: None

            Runs the appropriate test depending on the user_input
        '''
        mirror = self.tetris.get_mirror_status()
        if user_input == '0':
            self.tspin_test(tspin_zero_shape(mirror)) 
        elif user_input == '1':
            self.tspin_test(tspin_single_shape(mirror))
        elif user_input == '2':
            self.tspin_test(tspin_double_shape(mirror))
        elif user_input == '3':
            self.tspin_test(tspin_triple_shape(mirror))
        elif user_input == '4':
            self.tspin_test(offset_tspin_double_shape(mirror))
        elif user_input == '5':
            self.tspin_test(wall_mini_single_shape(mirror))
        elif user_input == '6':
            self.tspin_test(mini_double_shape(mirror))
        elif user_input == '7':
            print "Warning crazy t-spin does not work with true SRS!"
            self.tspin_test(crazy_tspin_triple_shape(mirror))
        elif user_input == '8':
            self.soft_lock_test(mirror)
        elif user_input == '9':
            self.combo_test(mirror, combo_test_shape(mirror))
        elif user_input == '10':
            self.backtoback_test(backtoback_test_shape(mirror))
        elif user_input == '11':
            self.tspin_combo_test(tspin_combo_break_shape(mirror))
        elif user_input == '12':
            self.tspin_combo_test(tspin_combo_continue_shape(mirror))
        return None 
   
    def tspin_test(self, shape):
        ''' Parameters: None
            Return: None

            Sets up tetris and the board for testing full or mini
            t-sping single line clears.
        '''
        self.tetris.set_test_shape(shape)
        self.tetris.set_test_current_shape(self.tetris.create_t_shape())
        self.tetris.set_current_shape(self.tetris.get_test_current_shape())
        self.tetris.start_tetris()
        return None

    def soft_lock_test(self, mirror):
        ''' Parameters: None
            Return: None

            Sets up tetris and the board for testing soft lock, rotation soft
            lock test mainly. Easiest to test with T or L/J shapes.
        '''
        if mirror == True:
            test_shape_tuple = (sh.L_shape, sh.T_shape, sh.L_shape, sh.T_shape, sh.L_shape, 
                                                                 sh.T_shape, sh.L_shape)
        else:
            test_shape_tuple = (sh.J_shape, sh.T_shape, sh.J_shape, sh.T_shape, sh.J_shape, 
                                                                    sh.T_shape, sh.J_shape)

        test_current_shape = self.tetris.create_shape(test_shape_tuple[0])

        self.tetris.clear_shape_bags()
        self.tetris.set_shapes(test_shape_tuple)
        self.tetris.create_new_shape()
        self.tetris.set_test_current_shape(test_current_shape)
        self.tetris.set_current_shape(test_current_shape)
        self.tetris.start_tetris()

    def combo_test(self, mirror, shape):
        ''' Parameters: None
            Return: None

            Sets up tetris and the board for testing combos with S or Z
            shapes.
        '''
        if mirror == True:
            test_shape_tuple = (sh.Z_shape, sh.Z_shape, sh.Z_shape, sh.Z_shape, sh.Z_shape,
                                                                    sh.Z_shape, sh.Z_shape)
        else:
            test_shape_tuple = (sh.S_shape, sh.S_shape, sh.S_shape, sh.S_shape, sh.S_shape, 
                                                                     sh.S_shape, sh.S_shape)
        
        test_current_shape = self.tetris.create_shape(test_shape_tuple[0])
        
        self.tetris.set_test_shape(shape)
        self.tetris.set_test_current_shape(test_current_shape)
        self.tetris.set_shapes(test_shape_tuple)
        self.tetris.clear_shape_bags()
        self.tetris.create_new_shape()
        self.tetris.set_current_shape(test_current_shape)
        self.tetris.start_tetris()


    def backtoback_test(self, shape):
        ''' Parameters: None
            Return: None

            Sets up tetris and the board for testing back-to-back bonuses
            with the I shape.
        '''
        test_shape_tuple = (sh.I_shape, sh.I_shape, sh.I_shape, sh.I_shape, sh.I_shape, 
                                                                     sh.I_shape, sh.I_shape)
        
        test_current_shape = self.tetris.create_shape(test_shape_tuple[0])
        
        self.tetris.set_test_shape(shape)
        self.tetris.set_test_current_shape(test_current_shape)
        self.tetris.set_shapes(test_shape_tuple)
        self.tetris.clear_shape_bags()
        self.tetris.create_new_shape()
        self.tetris.set_current_shape(test_current_shape)
        self.tetris.start_tetris()


    def tspin_combo_test(self, shape):
        ''' Parameters: None
            Return: None

            Sets up tetris and the board for testing t-spin combos with S or Z
            shapes.
        '''
        
        test_shape_tuple = (sh.T_shape, sh.T_shape, sh.T_shape, sh.T_shape, sh.T_shape,
                                                                sh.T_shape, sh.T_shape)
        
        test_current_shape = self.tetris.create_shape(test_shape_tuple[0])
        
        self.tetris.set_test_shape(shape)
        self.tetris.set_test_current_shape(test_current_shape)
        self.tetris.set_shapes(test_shape_tuple)
        self.tetris.clear_shape_bags()
        self.tetris.create_new_shape()
        self.tetris.set_current_shape(test_current_shape)
        self.tetris.start_tetris()


############################################################
# MAIN
############################################################
if __name__ == "__main__":
    #Print list of available tests
    for item in Run_test_tetris.TESTS:
        print item 
    #Gets user input and then runs the test
    user_input = Run_test_tetris.get_input() 
    win = gr.Window("Test Tetris")
    #tetris = Test_tetris(win)
    test = Run_test_tetris(win, user_input)
    win.mainloop()
