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
    FLOW_CONTROL_KEYS = HOLD_KEYS + ("p", "escape")
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
        #Intializes the three boards
        self.prv_board = br.PreviewBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                         sh.Block.BLK_SIZE)
        self.board = br.PlayBoard(win, self.BOARD_WIDTH, self.BOARD_HEIGHT, sh.Block.BLK_SIZE, 
                                                                         self.PLAYFIELD_HEIGHT)
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
        self.ghost_shape = None 
        self.current_shape = self.create_new_shape() 
        
        #Initialize the hold system
        self.hold_shape = None 

        #Used for controlling lock delay
        self.lock_delay = None

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.ghost_shape) 
        self.board.draw_shape(self.current_shape)
        self.prv_board.draw_preview(self.seven_bag) 
        
        #Starting animation
        self.animation = None 
        self.start_animation()
    
    def fisher_yates_shuffle(self, any_list):
        ''' Parameters: n - type: int
            Return:: shuffle_list - type: list or tuple

            This function generates random permutations with uniform
            probability of generating each permutation. I know that python
            uses the Fisher-Yates shuffle for random.shuffle and random.sample
            but I explicitly wanted to use this shufflei since have an equal
            probability of getting any permutation of Tetrominos is a core mechanic
            of the 7-bag system. Also I don't have to worry about future changes to python.
        '''
        shuffle_list = list(any_list) 
        n = len(shuffle_list)
        for j in range(n-1, 0, -1):
            p = random.randint(0, j)
            swap = shuffle_list[j]
            shuffle_list[j] = shuffle_list[p]
            shuffle_list[p] = swap
        return shuffle_list 
    
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
               that is centered at y = -2 and x = int((self.BOARD_WIDTH/2)-1)
            4. Creates new ghost shape based on the newly created shape 
            5. Adds a new shape to the end of 7-bag from next bag
            6. Updates preview board 
            7. returns the shape
        '''
        #One is substracted from board_width/2 because x = 4 
        #is the actual centre of the board since counting starts
        #from zero.
        #According to the tetris guidelines the shape should spawn
        #on the 21-22 rows and then move down.

        #I know that python uses the Fisher-Yates shuffle for random.shuffle 
        #and random.sample but I explicitly wanted to use this shufflei since 
        #have an equal probability of getting any permutation of Tetrominos is 
        #a core mechanic of the 7-bag system.

        x = int((self.BOARD_WIDTH/2)-1)
        y = -1 
        list_len = len(self.SHAPES)
        
        if len(self.seven_bag) == 0 and len(self.next_bag) == 0:
            self.seven_bag = self.fisher_yates_shuffle(self.SHAPES)
            self.next_bag = self.fisher_yates_shuffle(self.SHAPES)
        elif len(self.next_bag) == 0:
            self.next_bag = self.fisher_yates_shuffle(self.SHAPES)
        
        new_shape = self.seven_bag.pop(0)(gr.Point(x, y))
        self.ghost_shape = sh.Ghost_shape(self.board, new_shape) 
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
        #According to the tetris guidelines the shape should spawn
        #on the 21-22 rows and then move down.
        x = int((self.BOARD_WIDTH/2)-1)
        y = -1 
        temp = self.hold_shape
        self.hold_shape = self.current_shape
        self.current_shape.undraw()
        temp = temp.__class__(gr.Point(x, y))
        temp.can_hold = False 
        self.current_shape = temp
        self.ghost_shape = sh.Ghost_shape(self.board, self.current_shape)
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
        self.ghost_shape.undraw()
        if self.current_shape.get_soft_lock_state() == True:
            self.soft_lock_disable()

        if self.hold_shape == None:
            self.hold_new() 
        else:
            self.hold_swap()

        if self.board.game_over_check(self.current_shape) == True:
            self.board.game_over()
            self.cancel_animation()
        else:
            self.prv_board.draw_hold(self.hold_shape)
            #Ghost shape should always be drawn before current shape
            self.board.draw_shape(self.ghost_shape)
            self.board.draw_shape(self.current_shape)
        return None
    
    def clearlines_upscore(self):
        ''' Parameters: None
            Return: None

            Adds the shape to the board, cleares full lines from the board, and
            updates the score, level and speed (if needed).
        '''
        clrd_lines = self.board.remove_complete_rows()
        new_gravity = self.scr_board.update(clrd_lines, self.board.get_total_line_clears())
        
        if new_gravity is not False:
            self.update_speed(new_gravity)
        return None 
    
    def tspin_clearlines_upscore(self):
        ''' Parameters: None
            Return: None

            For when a t-spin is detected, this method adds the shape to the board,
            clears full lines from the board, and updates the score, level, and 
            speed (if needed). The current shape needs to be a T-shape for this 
            method to work.
        '''
        full_or_mini = self.current_shape.full_or_mini(self.board) 
        clrd_lines = self.board.remove_complete_rows()
        ttl_lines = self.board.get_total_line_clears()  
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

            Adds shape to board updates scores, gravity (if there is a level up),
            and spawns new shape on the board if there is space.
            Sets game to over if there is no space for new shape.
        '''
        soft_lock_state = self.current_shape.get_soft_lock_state() 
        soft_lock_can_move = self.current_shape.soft_lock_can_move() 
        if soft_lock_state == True or soft_lock_can_move == False:
           self.board.add_shape(self.current_shape)
           self.ghost_shape.undraw()
           new_shape = self.create_new_shape() 
           if self.board.game_over_check(new_shape, self.current_shape) == True:
               self.board.game_over()
               self.cancel_animation()
           else:
                if self.tspin_detect() == True:
                    self.tspin_clearlines_upscore()
                else: 
                    self.clearlines_upscore()

                self.current_shape = new_shape
                #Ghost shape needs to be updated before being drawn because
                #lines might have moved down above, if there were completed
                #lines. This ghost shape is created when a new main shape
                #is created
                self.ghost_shape.update(self.board, self.current_shape)
                #Ghost shape should always be drawn before main shape 
                self.board.draw_shape(self.ghost_shape) 
                if self.board.draw_shape(self.current_shape) == True:
                    self.soft_lock_disable()   
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

    def soft_lock_enable(self):
        ''' Parameters: None
            Return: None

            Puts tetris and the shape in soft lock mode.
            Main tetris animation is cancelled,
            shape is put into soft lock state, and the lock
            delay timer is started.
        '''
        self.current_shape.soft_lock_on()
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
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            else return False. 
        ''' 
        direction = direction.lower()
        dx, dy = Tetris.DIRECTION[direction]
        result = self.current_shape.move(self.board, dx, dy)
        self.ghost_shape.update(self.board, self.current_shape)
        if result == True and direction == 'down':
            self.scr_board.softdrop_score_up() 
        return result

    def do_slam(self):
        ''' Parameters: None
            Return: None

            "Slams" the shape shape down and instantly locks in 
            the shape. No soft lock if shape is slammed.
        '''
        while self.do_move("down"):
            self.scr_board.harddrop_score_up()
            pass
        self.current_shape.soft_lock_on()
        self.shape_lock()
        return None
    
    def do_rotate(self, direction):
        ''' Parameters: direction - type:string
            Rreturn: None 

            Checks if the current_shape can be rotated and
            rotates if it can
        ''' 
        rot_dir = Tetris.ROTATION_DIRECTION[direction]
        self.current_shape.rotate(self.board, rot_dir)
        self.ghost_shape.update(self.board, self.current_shape)
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
 
    def flow_control(self, key):
        ''' Parameters: key - type:string
            Return: None

            Deals with the flow control keys.
            Holds shape, pauses game, resets game
        '''
        if key in Tetris.HOLD_KEYS:
            if self.current_shape.can_hold == True:
                self.hold()
        elif key == 'escape':
            self.reset()
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
            #Two consecutive if statements on purpose instead of
            #if - elif - else
            if self.current_shape.get_soft_lock_state() == False:
                self.normal_control(key)
            if self.current_shape.get_soft_lock_state() == True:
                self.soft_lock_control(key)  
      
        #This works here the best in terms of gameplay mechanics.
        #(Decided after lots of testing)
        #Can't just lock the shape even if it's soft lock state
        #move count is zero if it can still move down. Can only
        #lock the shape if and when it is in a position where it 
        #can not move down anymore. 
        soft_lock_can_move = self.current_shape.soft_lock_can_move() 
        can_move_down = self.current_shape.can_move_down(self.board)
        if soft_lock_can_move == False and can_move_down == False:
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
        self.tetris_control(key)
        return None 
    
    def close_boards(self): 
        ''' Paramters: None
            Return: None

            Destroys the preview board, score board, and play board.
        '''
        self.prv_board.canvas.canvas.pack_forget()
        self.prv_board.canvas.canvas.destroy()
        self.prv_board.canvas.destroy()
        self.board.canvas.canvas.pack_forget()
        self.board.canvas.canvas.destroy()
        self.board.canvas.destroy()
        self.scr_board.canvas.canvas.pack_forget()
        self.scr_board.canvas.canvas.destroy()
        self.scr_board.canvas.destroy()
    
    def delete_internal_obj(self):
        ''' Parameters: None
            Return: None

            Deletes internal objects. Don't know if it is really necessary
            but still doing it.
        '''
        del self.prv_board
        del self.board
        del self.scr_board
        del self.delay
        del self.seven_bag
        del self.next_bag
        del self.ghost_shape
        del self.current_shape
        del self.hold_shape
        del self.lock_delay
        del self.animation

    def reset(self):
        ''' Parameters: None
            Return: None

            Resets the whole game and re-starts it.
        '''
        #Cancel animation
        self.cancel_animation()
        
        #Close boards, delete all internal objects
        self.close_boards()
        self.delete_internal_obj()

        #Re-initialization
        self.prv_board = br.PreviewBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                         sh.Block.BLK_SIZE)
        self.board = br.PlayBoard(win, self.BOARD_WIDTH, 
                                  self.BOARD_HEIGHT, sh.Block.BLK_SIZE, self.PLAYFIELD_HEIGHT)
        self.scr_board = br.ScoreBoard(win, self.SCR_BOARD_WIDTH, self.SCR_BOARD_HEIGHT, 
                                                                       sh.Block.BLK_SIZE)
        #self.win = win
        self.delay = 1000 #ms

        #Don't think I have to re-do this
        #I will leave it in but commented out
        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        #self.win.bind_all('<Key>', self.key_pressed)

        # Re-initialize the seven bag system
        # Create new shape and sets the current shape to the new
        # shape
        self.seven_bag = []
        self.next_bag = []
        self.ghost_shape = None 
        self.current_shape = self.create_new_shape() 
        
        #Re-initialize the hold system
        self.hold_shape = None 

        #Used for controlling lock delay
        self.lock_delay = None

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.ghost_shape) 
        self.board.draw_shape(self.current_shape)
        self.prv_board.draw_preview(self.seven_bag) 
        
        # Re-start animation
        self.animation = None 
        self.start_animation()


################################################################
# Start the game
################################################################
if __name__ == '__main__':
    win = gr.Window("Tetris")
    game = Tetris(win)
    win.mainloop()
