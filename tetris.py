# Name: Ankush Burman
# Section: Self
# Date: Started: Mar 16, 2022; 
# tetris.py

import graphics35 as gr
import boards as br
import shapes as sh
import random

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
            prv_board - type:br.PreviewBoard - the board which displays preview and hold
                                             shapes.
            board - type:br.PlayBoard - the tetris board
            scr_board - type:br.ScoreBoard - Does all the calculations for score, levels,
                                           and gravity. Also displays the current 
                                           score and level.
            win - type:gr.Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            seven_bag - type: list - Holds a list of next seven shapes
            next_bag - type: list - Holds a list of shuffled shapes to feed into
                                    seven_bag (needed for preview to work). 
            current_shapes - type:sh.Shape - the current moving shape on the board
            hold_shape - type:sh.Shape - Holds the information for the "hold" shape.
            hold_flag - type: Bool - Hold can only be used once per new shape spawn.
                                     This flag determines if hold has been used or not.
            animation - type: tk.after - Holds the tk.after function in a variable so it 
                                         can be cancelled later on.
    '''
    
    SHAPES = (sh.I_shape, sh.J_shape, sh.L_shape, sh.O_shape, sh.S_shape, 
                                                   sh.T_shape, sh.Z_shape)
    HOLD_KEYS = ("c", "shift_l", "shift_r")
    FLOW_CONTROL_KEYS = HOLD_KEYS + ("p", "r")
    #MOVE_KEYS = ("up", "right", "left", "down", "space", "animate") 
    DIR_KEYS = ("right", "left", "down")
    ROTATION_KEYS = ("up", "x", "control_l", "control_r", "z")
    MOVE_KEYS = DIR_KEYS + ROTATION_KEYS + ("space", "animate") 
    LOCK_KEYS = ("space", "down")
    DIRECTION = {'left':(-1, 0), 'right':(1, 0), 'down':(0, 1), 'animate':(0, 1)}
    ROTATION_DIRECTION = {"up":-1, "x":-1, "control_l":1, "control_r":1, "z":1}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    PLAYFIELD_HEIGHT = 40
    SCR_BOARD_WIDTH = 10
    SCR_BOARD_HEIGHT = 2

    def __init__(self, win):
        self.prv_board = br.PreviewBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                         sh.Block.BLK_SIZE)
        self.board = br.PlayBoard(win, self.BOARD_WIDTH, 
                                  self.BOARD_HEIGHT, sh.Block.BLK_SIZE, self.PLAYFIELD_HEIGHT)
        self.scr_board = br.ScoreBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                       sh.Block.BLK_SIZE)
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
        self.start_animation()
       
        #NOTE############ FOR TESTING ONLY ############NOTE 
        #test_x = int(self.BOARD_WIDTH/2)
        #test_y = 0 
        #self.test_shape = I_shape(gr.Point(test_x, test_y))

        #self.TEST_SHAPES = [I_shape, I_shape, I_shape]
        #self.prv_board.draw(self.TEST_SHAPES, self.test_shape)

    def create_new_shape(self):
        ''' Parameters: None 
            Return value: new_shape -  type: Shape

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
        #One is substracted from board_width/2 because x = 4 
        #is the actual centre of the board since counting starts
        #from zero.
        x = int((self.BOARD_WIDTH/2)-1)
        y = 0
        list_len = len(Tetris.SHAPES)
        
        if len(self.seven_bag) == 0 and len(self.next_bag) == 0:
            self.seven_bag = random.sample(Tetris.SHAPES, list_len)
            self.next_bag = random.sample(Tetris.SHAPES, list_len)
        elif len(self.next_bag) == 0:
            self.next_bag = random.sample(Tetris.SHAPES, list_len)

        new_shape = self.seven_bag.pop(0)(gr.Point(x, y))
        self.seven_bag.append(self.next_bag.pop(0))
        self.prv_board.draw_preview(self.seven_bag)
        return new_shape

    def hold_new(self):
        ''' Parameters: None
            Return: None

            This function is for when there is no shape being held.
            It stores the current shape as the hold shape and creates
            a new shape:
            1. Sets the current shape to hold shape
            2. Undraws the current shape
            3. Sets the current shape to a new shape 
        '''
        self.hold_shape = self.current_shape
        self.current_shape.undraw() 
        self.current_shape = self.create_new_shape()
        return None 

    def hold_swap(self):
        ''' Parameters: None
            Return: none 

            This function swaps the hold shape with the current shape:
            1. Holds the current hold shape in temp
            2. Sets the hold shape to the current shape
            3. Initializes a new shape based on the type of previously
               held shape.
            4. All shapes re-created by hold have their internal hold variable
               set to false.
        '''
        #One is substracted from board_width/2 because x = 4 
        #is the actual centre of the board since counting starts
        #from zero.
        x = int((self.BOARD_WIDTH/2)-1)
        y = 0

        temp = self.hold_shape
        self.hold_shape = self.current_shape
        self.current_shape.undraw()
        temp = temp.__class__(gr.Point(x, y))
        temp.can_hold = False 
        self.current_shape = temp 
        return None

    def hold(self):
        ''' Parameters: None
            Return: None

            * If there is no hold shape:
                - Stores the current shape as hold shape 
            * If there is a shape already being held:
                - Swaps the current shape with the hold shape 
            * Draws the new hold shape on the preview board
            * Draws the new current shape
        '''
        #print "HOLDING" #NOTE NOTE NOTE
        if self.current_shape.soft_lock_state() == True:
            #print "Hold disabling soft lock" NOTE NOTE NOTE
            self.soft_lock_disable()

        if self.hold_shape == None:
            self.hold_new() 
        else:
            self.hold_swap()

        self.prv_board.draw_hold(self.hold_shape) 
        if self.board.draw_shape(self.current_shape) == False:
            #print "Hold game over" NOTE NOTE NOTE
            self.board.game_over()
        #print "Hold created new shape" NOTE NOTE NOTE
        return None
    
    def add_clear_score(self):
        ''' Parameters: None
            Return: None

            Adds the shape to the board, cleares full lines from the board, and
            updates the score, level and speed (if needed).
        '''
        self.board.add_shape(self.current_shape) 
        clrd_lines = self.board.remove_complete_rows()
        new_gravity = self.scr_board.update(clrd_lines, self.board.total_line_clears())
        
        if new_gravity is not False:
            self.update_speed(new_gravity)
        return None 
    
    def tspin_add_clear_score(self):
        ''' Parameters: None
            Return: None

            For when a t-spin is detected, this method adds the shape to the board,
            clears full lines from the board, and updates the score, level, and 
            speed (if needed). The current shape needs to be a T-shape for this 
            method to work.
        '''
        self.board.add_shape(self.current_shape) 
        full_or_mini = self.current_shape.full_or_mini(self.board) 
        clrd_lines = self.board.remove_complete_rows()
        ttl_lines = self.board.total_line_clears()  
        new_gravity = self.scr_board.tspin_update(clrd_lines, ttl_lines, 
                                                               full_or_mini)
        if new_gravity is not False:
            self.update_speed(new_gravity)
        return None
    
    def tspin_detect(self):
        ''' Parameters: None
            Return: type:bool

            Detects if a tspin has occured and returns True if it has, returns 
            False otherwise.
        '''
        if self.current_shape.__class__ == sh.T_shape:
            if self.current_shape.was_last_move_rot() == True:
                if self.current_shape.tspin(self.board) == True:
                    return True
        return False 
           
    def shape_lock(self):
        ''' Parameters: None
            Return: None

            Adds board to shape updates scoreboard, gravity (if there is a level up),
            and spawns new shape on the board if there is space.
            Sets game to over if there is no space for new shape.
        '''
        #import pdb;  pdb.set_trace() #############NOTE NOTE NOTE############
        #print "shape lock called" NOTE NOTE NOTE
        soft_lock = self.current_shape.soft_lock_state() 
        soft_lock_move = self.current_shape.soft_lock_move() 
        if soft_lock == True or soft_lock_move == False:
           
           #Sometimes the shape can end up "floating" because of the SRS'
           #kick mechanism. Don't want the shape to lock in mid air.
            while self.do_move("down"):
                pass
            
            if self.tspin_detect() == True:
                self.tspin_add_clear_score()
            else: 
                self.add_clear_score()

            self.current_shape = self.create_new_shape()
            #NOTE self.prv_board.draw_preview(self.seven_bag)
            #NOTE for testing: self.prv_board.draw(self.TEST_SHAPES, self.test_shape)  #NOTE 
            if self.board.draw_shape(self.current_shape) == True:
                self.soft_lock_disable() #NOTE THIS MIGHT BREAK THINGS #NOTE   
            else:
                self.board.game_over()
                self.cancel_animation()
        return None 
 
    def update_speed(self, gravity):
        ''' Parameters: gravity - type:float
            Return: None

            Updates the delay variable which controls the speed
            of the down animation of the tetrominoes. 
            Gravity is in Seconds and tkinter likes ms for the after function.
            Therefore gravity is multiplied by 1000 to yield ms. 
        '''
        self.delay = gravity*1000 
        self.delay = int(self.delay)
        return None

    def animate_shape(self):
        ''' Parameters: None
            Return: None

            animate the shape - move down at equal intervals
            specified by the delay attribute
        ''' 
        self.tetris_control("animate")
        #print self.delay NOTE NOTE NOTE
        self.animation = self.win.after(self.delay, self.animate_shape)
        return None
    
    def cancel_animation(self):
        ''' Parameters: None
            Return: None

            Cancels and disables the main animation if it is
            running or exists
        '''
        if self.animation:
            self.win.after_cancel(self.animation)
            self.animation = None
        return None

    def start_animation(self):
        ''' Parameters: None
            Return: None

            Starts the main animation
            Always good practice to check and cancel
            any previous animation (win.after) before starting
            a new one. So they don't get stacked. 
        '''
        self.cancel_animation()
        self.animate_shape()
        return None

    def cancel_lock_delay(self):
        ''' Parameters: None
            Return: None

            Cancels the lock delay timer if it is running/ exists
        '''
        if self.lock_delay:
            self.win.after_cancel(self.lock_delay)
            self.lock_delay = None
        return None

    def start_lock_delay(self):
        ''' Parameters: None
            Return: None

            Starts the lock delay timer after cancelling
            any previous lock delay timers. Lock delay is 
            set at 500 ms (0.5 s) 
        '''
        self.cancel_lock_delay() 
        self.lock_delay = self.win.after(500, self.shape_lock)
        return None 

    def do_rotate(self, direction):
        ''' Parameters: direction - type:string
            Rreturn: None 

            Checks if the current_shape can be rotated and
            rotates if it can
        ''' 
        rot_dir = Tetris.ROTATION_DIRECTION[direction]
        self.current_shape.rotate(self.board, rot_dir) 
        return None
    
    def normal_rotate(self, key):
        ''' Parameters: key - type:string
            Return: None

            Handles the rotation of the shape when shape is NOT in soft lock state.
            Checks to see if the shape can move down after every rotation.
            If shape can not move down, soft locks the shape.
        '''
        self.do_rotate(key)
        if self.current_shape.can_move_down(self.board) == False:
            self.soft_lock_enable()
        return None

    def soft_lock_rotate(self, key):
        ''' Paramters: key - type:string
            Return: None

            Handles the rotation of the shape when shape is IN soft lock state.
            Everytime the shape is attempted to be rotated in soft lock state, 
            the soft lock timer is reset.
        '''
        #When shape is in soft lock state, any attempt at rotation resets the
        #the soft lock timer. Which is different from the behaviour for the
        #left and right movement of the shape in the soft lock state.
        self.cancel_lock_delay()
        self.do_rotate(key)
        if self.current_shape.can_move_down(self.board) == True:
            self.soft_lock_disable()
        else:
            self.start_lock_delay()
        return None

    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            else return False. 
        ''' 
        direction = direction.lower()
        dx, dy = Tetris.DIRECTION[direction]
        #print "do_move", dx, dy  #NOTE #NOTE #NOTE 
        return self.current_shape.move(self.board, dx, dy)

    def do_slam(self):
        ''' Parameters: None
            Return: None

            "Slams" the shape shape down and instantly locks in 
            the shape. No soft lock if shape is slammed.
        '''
        while self.do_move("down"):
            pass
        self.current_shape.soft_lock_on()
        self.shape_lock()
        return None
    
    def normal_move(self, key):
        ''' Parameters: key - type:string
            Return: None

            Handles movement of shape when shape is NOT in soft lock state.
            Checks to see if shape can move down after every move. 
            If shape can not move down, soft locks the shape. 
        '''
        self.do_move(key)
        if self.current_shape.can_move_down(self.board) == False:
            self.soft_lock_enable()
        return None

    def soft_lock_move(self, key):
        ''' Parameters: key - type:string
            Return: None

            Handles the movement of the shape when shape is IN soft lock state.
            Everytime the shape is moved in soft lock state, the soft lock
            timer is reset. If the shape can not be moved due to an obstruction
            then the timer does not reset.
        '''
        #When the shape is in soft lock state, the shape needs to be SUCCESSFULLY
        #moved for the soft lock timer to be reset. The timer does not reset if
        #the shape can not be moved due to an obstruction. Yes, this behaviour
        #is intentionally different from rotation in the soft lock state.
        if self.do_move(key) == True:
            self.cancel_lock_delay()
            if self.current_shape.can_move_down(self.board) == True:
                self.soft_lock_disable()  
            else:      
                self.start_lock_delay()
        return None
 
    def soft_lock_enable(self):
        ''' Parameters: None
            Return: None

            Puts tetris and the shape in soft lock mode.
            Main tetris animation is cancelled,
            shape is put into soft lock state, and the lock
            delay timer is started.
        '''
        #print self.animation #NOTE NOTE NOTE
        #print "soft locking shape" #NOTE NOTE NOTE
        self.current_shape.soft_lock_on()
        #print self.current_shape.soft_lock NOTE NOTE NOTE
        self.start_lock_delay()  
        return None

    def soft_lock_disable(self):
        ''' Parameters: None
            Return: None

            Takes tetris and the shape out of soft lock state.
            Lock delay timer is cancelled, shape's soft lock state is reset,
            and the main animation is restarted
        '''
        self.cancel_lock_delay() 
        self.current_shape.soft_lock_reset()
        return None 

    def flow_control(self, key):
        ''' Parameters: key - type:string
            Return: None

            Deals with the flow control keys.
            Holds shape, pauses game, resets game
        '''
        if key in Tetris.HOLD_KEYS:
            if self.current_shape.can_hold == True:
                self.hold()
        return None 

    def normal_control(self, key):
        ''' Parameters: key - type:string
            Return: None

            Deals with the movement keys when game and shape are NOT in
            soft lock state
        '''
        if key == "space":
            self.do_slam() 
        elif key in Tetris.ROTATION_KEYS:
            self.normal_rotate(key)
        elif key in Tetris.DIR_KEYS or key == "animate":
            self.normal_move(key)
        return None 

    def soft_lock_control(self, key):
        ''' Parameters: key - type:string
            Return: None

            Deals with the movement keys when game and shape are IN
            soft lock state. lock delay timer needs to be reset after 
            every move, lock keys instantly lock the shape.
        '''
        #print "Tetris control soft_lock == true" NOTE NOTE NOTE
        if key in  Tetris.LOCK_KEYS:
            self.shape_lock()   
        elif key in Tetris.ROTATION_KEYS:
            self.soft_lock_rotate(key)
        elif key == "animate":
            pass 
        elif key in Tetris.DIR_KEYS:
            self.soft_lock_move(key)
        return None 

    def tetris_control(self, key):
        ''' Parameters: key - type:string
            Return: None

            Deals with all keys and what should be done with them
        '''
        key = key.lower() 
        if key in Tetris.FLOW_CONTROL_KEYS:
            self.flow_control(key)
        elif key in Tetris.MOVE_KEYS:
            if self.current_shape.soft_lock_state() == False:
                self.normal_control(key)
            if self.current_shape.soft_lock_state() == True:
                self.soft_lock_control(key)  
         
        if self.current_shape.soft_lock_move() == False: 
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
        #NOTE for debugging
        print key #NOTE NOTE NOTE
        self.tetris_control(key)
        return None 
       

################################################################
# Start the game
################################################################
if __name__ == '__main__':
    win = gr.Window("Tetris")
    game = Tetris(win)
    win.mainloop()
