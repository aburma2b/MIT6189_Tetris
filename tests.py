# Name: Ankush Burman
# Section: Self
# Date: Started: July 20, 2022; 
# tests.py

import graphics35 as gr
import shapes as sh 
import tetris as te 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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
        sh.Shape.__init__(self, self.coords, self.color) 

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

class Test_tetris(object):
    ''' Test_tetris class: The main class which sets up tetris and the tetris board
                           with initiall test shapes for different scenarios to be testes.

        Attributes:
            INPUT_LIST - type:tuple - Holds the list of all valid inputs.
            TESTS - type:dictionary - Holds a dictionary of all the tests available
                                      and the corresponding input to run them.
            win - type:gr.Window - the window for the test tetris game
            tetris - type:te.Tetris - the tetris object which all the tests will be run on
            test_shape - type:sh.Shape - the initial test shape that will be drawn and
                                         added to the tetris board to test different scenarios.
                                         Test shapes are initialized and added when a test is
                                         picked.
            user_test - type:string - Holds the selected value for the test to be run.
            self.mirror - type:bool - Holds the selected value for mirroring the test pattern.
    '''

    INPUT_LIST = ('0', '1', '2', '3', '4', '5', '6', '7')
    TESTS = ("Tests:",
             "0: mini or full t-spin zero",
             "1: mini or full t-spin single",
             "2: full t-spin double",
             "3: full t-spin triple",
             "4: offset t-spin double",
             "5: wall mini t-spin single",
             "6: mini t-spin double",
             "7: crazy t-spin triple")


    def __init__(self, win, tetris, user_input):
        self.win = win  
        self.tetris = tetris
        self.test_shape = None   
        self.user_test =  user_input[0]
        self.mirror = user_input[1] 
        self.init_tetris()
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
            if user_test in Test_tetris.INPUT_LIST:
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
        if user_input == '0':
            self.tspin_test(tspin_zero_shape(self.mirror)) 
        elif user_input == '1':
            self.tspin_test(tspin_single_shape(self.mirror))
        elif user_input == '2':
            self.tspin_test(tspin_double_shape(self.mirror))
        elif user_input == '3':
            self.tspin_test(tspin_triple_shape(self.mirror))
        elif user_input == '4':
            self.tspin_test(offset_tspin_double_shape(self.mirror))
        elif user_input == '5':
            self.tspin_test(wall_mini_single_shape(self.mirror))
        elif user_input == '6':
            self.tspin_test(mini_double_shape(self.mirror))
        elif user_input == '7':
            print "Warning crazy t-spin does not work with true SRS!"
            self.tspin_test(crazy_tspin_triple_shape(self.mirror))

        return None 
   
    def init_tetris(self):
        ''' Parameters: None
            Return: None

            Prepares tetris and the tetris board for test shape
            setup by stopping the animation and undrawing the randomly
            generated first shape. The first shape should be determined 
            by the test, after test is picked, for easier testing.
        '''
        self.tetris.cancel_animation()
        self.tetris.current_shape.undraw() 
        return None

    def start_tetris(self):
        ''' Parameters: None
            Return: None

            Draws the current shape, which should be determined by the test,
            and then starts running tetris.
        '''
        self.tetris.board.draw_shape(self.tetris.current_shape)
        self.tetris.start_animation()
        return None

    def create_t_shape(self):
        ''' Parameters: None
            Return: type:sh.T_shape - t_shape 

            Creates a t-shape at the default starting point of tetris
            and returns it.
        '''
        x = int(self.tetris.BOARD_WIDTH/2)
        y = 0
        t_shape = sh.T_shape(gr.Point(x, y))
        return t_shape 
    
    def tspin_test(self, shape):
        ''' Parameters: None
            Return: None

            Sets up tetris and the board for testing full or mini
            t-sping single line clears.
        '''
        self.test_shape = shape 
        self.tetris.board.draw_shape(self.test_shape)
        self.tetris.board.add_shape(self.test_shape) 
        self.tetris.current_shape = self.create_t_shape()
        self.start_tetris()
        return None


if __name__ == "__main__":
    #Print list of available tests
    for item in Test_tetris.TESTS:
        print item 
    #Gets user input and then runs the test
    user_input = Test_tetris.get_input() 
    win = gr.Window("Test")
    tetris = te.Tetris(win)
    test = Test_tetris(win, tetris, user_input)
    win.mainloop()
