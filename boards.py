#Name: Ankush Burman
# Section: Self
# Date: Started: Mar 16, 2022; 
# boards.py

import graphics35 as gr

############################################################
# BOARD CLASS
############################################################
class Board(object):
    ''' Board class: Base class for all the boards. 

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    block_size - type:str - The size of tetris blocks in pixels
                    canvas - type:gr.CanvasFrame - where the score will be drawn 
    '''             

    def __init__(self, win, width, height, block_size, background):
        self.width = width
        self.height = height 
        self.block_size = block_size 
        # create a canvas to draw the tetris shapes on
        self.canvas = gr.CanvasFrame(win, self.width * self.block_size, 
                                            self.height * self.block_size)
        self.canvas.setBackground(background)
        
    def make_rect(self, start_coord, end_coord, out_width, out_color, fill_color):
        ''' Parameters: start_coord - type: int tuple
                        end_coord - type: int tuple
                        out_width - type: int
                        out_color - type: string
                        fill_color - type: string

            Makes a rectangle with the given arguments and returns it.
        '''
        x1 , y1 = start_coord
        x2, y2 = end_coord 
        point_1 = gr.Point(x1, y1)
        point_2 = gr.Point(x2, y2)
        new_rect = gr.Rectangle(point_1, point_2)
        new_rect.setOutline(out_color)
        new_rect.setWidth(out_width)
        new_rect.setFill(fill_color)
        return new_rect
    
    def make_line(self, start_coord, end_coord):
        ''' Parameters: start_coord - type: int tuple
                        end_coord - type: int tuple

            Makes a line object with the given arguments and returns it.
        '''
        start_x , start_y = start_coord
        end_x, end_y = end_coord
        start_point = gr.Point(start_x, start_y)
        end_point = gr.Point(end_x, end_y)
        new_line = gr.Line(start_point, end_point)
        return new_line 

    def make_text(self, center_coord, string, size, style='normal', color='black'):
        ''' Paramters: center_coord - type: int tuple
                       string - type: string
                       style - type: string
                       color - type: string

            Makes a graphics text object with the given arguments and returns it.
        '''
        cntr_x, cntr_y = center_coord
        cntr_point = gr.Point(cntr_x, cntr_y)
        new_text = gr.Text(cntr_point, string)
        new_text.setSize(size)
        new_text.setStyle(style)
        new_text.setTextColor(color)
        return new_text 


############################################################
# PLAYBOARD CLASS
############################################################
class PlayBoard(Board):
    ''' PlayBoard class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    block_size - type:int - The size of tetris blocks in pixels
                    background - type:str - The background color of the canvas frame 
                    total_lines - type:int - Total lines cleared in the current game
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    been cleard
                    go_rect - type:gr.Rectangle - A rectangle within which the game over
                                                  text is shown.
                    go_text - type:gr.Text - The graphics object which holds the game over
                                             text.
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
                    highest_block - type:Dictionary - keeps track of the highest block
                    for every x-value (horizontal position) 
    '''   
    def __init__(self, win, width, height, block_size, total_height):
        self.width = width
        self.height = height
        self.block_size = block_size 
        self.background = "light gray"
        self.total_height = total_height
        #The tetris playfield is actually 40 blocks high and 10 blocks high.
        #Only 20x10 playfield is visible and the other 20 cells ABOVE the playfield
        #is buffer. The y-axis is flipped here that is why the coordinates go into
        #the negatives for height to be added above the playfield. 
        self.buffer_height = self.height - self.total_height 
        self.total_lines = 0
        self.go_rect = None
        self.go_text = None 
        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}
        self.highest_blocks  = {}
        Board.__init__(self, win, self.width, self.height, self.block_size, self.background) 
    
    def get_height(self):
        ''' Parameters: None
            Return: type - int 

            Returns the height of the PlayBoard
        '''
        return self.height
    
    def get_total_height(self):
        ''' Parameters: None
            Return: type - int

            Returns the total height of the playboard
        '''
        return self.total_height
    
    def get_highest_blocks(self):
        ''' Parameters: None
            Return: type: dictionary

            Returns the dictionary of the highest blocks on the PlayBoard
        '''
        return self.highest_blocks 

    def get_total_line_clears(self):
        ''' Parameters: None
            Return: type:int - self.total_lines
         
            Returns the latest value of variable self.total_lines
        '''
        return self.total_lines
    
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
        #Checks if x variable within x-axis bounds of board
        x_check = 0  <= x < self.width 
        #Checks if y variable within y-axis bounds of board
        y_check = self.buffer_height <= y < self.height
        #Checks if (x,y) position is occupied or not
        occupy_check = (x,y) in self.grid 
        if x_check and y_check and not occupy_check:
            return True 
        return False 

    def update_highest_blocks(self):
        ''' Parameters: None
            Return: None

            Updates the dictionary of current highest blocks
            on the PlayBoard. 
            Goes through every column on the PlayBoard and finds
            the highest block, in this case it is the "lowest block"
            because the y-coordinate on the PlayBoard is flipped.
            If there are no blocks in the column then the entry
            corresponding to that column is emptied. 
        '''
        occupied = self.grid.keys()
        for x in range(self.width):
            occupied_in_col = [pos for pos in occupied if pos[0] == x]
            if occupied_in_col != []:
                max_pos = min(occupied_in_col) 
                self.highest_blocks[max_pos[0]] = max_pos[1] 
            elif x in self.highest_blocks:
                self.highest_blocks.pop(x) 
        return None 

    def add_block(self, block):
        ''' Parameter: shape - type:Shape
            Return: None

            add a block to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key
        '''
        coords = block.get_coords()
        self.grid[coords] = block
        return None
    
    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
        '''
        for block in shape.get_blocks():
            self.add_block(block)
        self.update_highest_blocks() 
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
            Return: None

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position
        '''
        # -1 because range function stops before hitting the
        #last element. I need it to go to grid row 0 (y = 0).
        for y in range(y_start, self.buffer_height-1, -1):
            for x in range(self.width):
                if (x, y) in self.grid:
                    block = self.grid.pop((x,y))
                    block.move(0, 1)
                    new_coords = block.get_coords()
                    self.grid[new_coords] = block
        return None 
    
    def remove_complete_rows(self):
        ''' Parameters: None
            Return: None

            removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    * delete the row
                    * add +1 to cleared_lines
                    * move all rows down starting at row y - 1
                    * Update dictionary of highest blocks 
        '''
        cleared_lines = 0 
        for y in range(self.buffer_height, self.height):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.total_lines += 1
                cleared_lines += 1
                self.move_down_rows(y-1)
                self.update_highest_blocks()
        return cleared_lines  
    
    def lock_out_check(self, shape):
        ''' Paramters: None
            Return: None
           
           Checks to see if any blocks of the shape are in the play area
           This is needed to determine if a shape satisfied the conditions
           of a "lock out" game over condition.
           Returns False if any blocks are still in the play area,
           returns True otherwise.
        '''

        for block in shape.get_blocks():
            coords = block.get_coords()
            x,y = coords
            #Grid rows 0 to 19 are the play area
            if y < 0:
                continue
            else:
                return False 
        return True 

    def game_over_check(self, new_shape, current_shape = None): 
        ''' Parameters: new_shape - type: Shape
                        current_shape - type: Shape or None

            Return: type: Bool

            Checks to see if either of the two game over conditions
            have been met.
            If either one is met then Returns True, otherwise 
            returns False.
        '''
        if current_shape != None: 
            lock_out = self.lock_out_check(current_shape)
        else:
            lock_out = False 
        
        #These are the coordinates on which new shapes spawn.
        #shape_spawn_x_coord = int((self.width/2)-1)
        #shape_spawn_y_coord = -1
        #the shape.can_move function takes in delta x and delta y
        #Hence the below function is given the coordinate of 0,0
        #Basically to see if the new_shape can occupy it's spawn location
        #or if it is occupied by another shape
        block_out = new_shape.can_move(self, 0, 0)

        if lock_out == True or block_out == False:
            return True
        return False

    def gameover_init(self):
        ''' Paramters: None
            Return: None 
            Initializes the objects for the game over message
        '''
        #Game Over rectangle
        start_coord = (30, 270)
        end_coord = (270, 330)
        self.go_rect = self.make_rect(start_coord, end_coord, 5, "black", "MediumAquamarine") 
        #Game Over text
        center_point = self.go_rect.getCenter()
        x = center_point.getX()
        y = center_point.getY()
        self.go_text = self.make_text((x,y), "Game Over!", 20, "bold")
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
class ScoreBoard(Board):
    ''' ScoreBoard class: it represents the score board. Does all the
        calculations associated with leveling up, score, and game gravity. 

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:gr.CanvasFrame - where the score will be drawn
                    block_size - type:int - Size of tetris blocks in pixels
                    background - type:str - The background color of the canvas frame 
                    level - type:int - keeps track of the level of the game
                    gravity - type:int - keeps track of the gravity of the game
                    score - type:int - keeps track of the score of the game
                    combo - type:int - keeps track of the combo counter
                    backtoback_count - type:int - keeps track of the back-to-back counter
                                                  counter needs to reach 2 for back-to-back
                                                  bonus to be enabled
                    backtoback - type:Bool - keep tracks of status of back-to-back bonus
                    rect - type:gr.Rectangle - Holds the rectangle object which
                                               acts as a border and canvas.
                    lvl_text - type:gr.Text - Holds the level text object
                    lvl_num - type:gr.Text - The graphics text object of the level number
                    lvl_line - type:gr.Line - The line that is drawn underneath lvl_text 
                    scr_text - type:gr.Text - Holds the score text object 
                    scr_num - type:gr.Text - The graphics text object of the score number
                    scr_line - type:gr.Line - The line that is drawn underneath scr_text
                    combo_text - type:gr.Text - Holds the combo text object
                    backtoback_text - type:gr.text - Holds the b2b text object
    '''             

    def __init__(self, win, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size 
        self.background = "light gray"
        self.level = 1
        self.gravity = 1
        self.score = 0
        self.combo = -1
        self.backtoback_count = 0 
        self.backtoback = False

        self.rect = None
        self.lvl_text = None
        self.lvl_num = None
        self.lvl_line = None
        self.scr_text = None
        self.scr_num = None
        self.scr_line = None
        self.combo_text = None
        self.backtoback_text = None 
        Board.__init__(self, win, self.width, self.height, self.block_size, self.background)
        #Important: These must be done after parent class initialization
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
        origin = (0, 0)
        point2 = (canvas_w, canvas_h)
        self.rect = self.make_rect(origin, point2, 5, "black", "MediumAquamarine")
        return None

    def init_scr_text(self):
        ''' Parameters: None
            Return: None
            Initializes all the text that is associated with the score
        '''
        #Got coordinates after trial and error
        self.scr_text = self.make_text((131.0,14.0), "Score", 9)
        #Got coordinates after trial and error
        score_str = str(self.score)
        self.scr_num = self.make_text((201.75,37.0), score_str, 11)
        return None

    def init_lvl_text(self):
        ''' Parameters: None
            Return: None
            Initializes all the text that is associated with the level
        '''
        #Got coordinates after trial and error
        self.lvl_text = self.make_text((26.5,14.0), "Level", 9)
        #Got coordinates after trial and error
        lvl_str = str(self.level)
        self.lvl_num = self.make_text((40.25,37.0), lvl_str, 11) 
        return None
    
    def init_combo_text(self):
        '''Parameters: None
           Return: None
           Initializes text for displaying combo"
        '''
        #Got coordinates after trial and error
        self.combo_text = self.make_text((227.0, 14.0), "Combo", 9)
        self.combo_text.setTextColor('') 
        return None 

    def init_backtoback_text(self):
        ''' Paramters: None
            Return: None
            Initializes text for displaying if back-to-back bonus is active
        '''
        #Got coordinates after trial and error
        self.backtoback_text = self.make_text((277.0, 14.0), "B2B", 9)
        self.backtoback_text.setTextColor('') 
        return None

    def init_text(self):
        ''' Parameters: None
            Return: None 
            Initializes all the text that is displayed on the
            scoreboard. 
        '''
        self.init_lvl_text() 
        self.init_scr_text() 
        self.init_combo_text()   
        self.init_backtoback_text()
        return None 

    def init_lines(self):
        ''' Parameters: None
            Return: None
            Initializes lines which are displayed underneath 
            the text as a stylized underline
        '''
        #Determined coordinates after trial and error
        self.lvl_line = self.make_line((11.5,19.0), (69.0,19.0))
        #Determined coordinates after trial and error
        self.scr_line = self.make_line((114.5, 19.0), (289.0,19.0))
        return None 

    def init_objects(self):
        ''' Parameters: None
            Return: None
            Initializes all the objects that are to displayed on
            the Score Board.
        '''
        self.init_rect()
        self.init_text()
        self.init_lines()
        return None

    def draw(self):
        ''' Parameters: None
            Return: None
            Draws all the objects that are to be displayed
        '''
        self.rect.draw(self.canvas)
        self.lvl_text.draw(self.canvas)
        self.lvl_num.draw(self.canvas)
        self.lvl_line.draw(self.canvas)
        self.scr_text.draw(self.canvas)
        self.scr_num.draw(self.canvas)
        self.scr_line.draw(self.canvas)
        self.combo_text.draw(self.canvas)
        self.backtoback_text.draw(self.canvas)
        return None 
    
    def set_combo(self): 
        ''' Parameters: None
            Return: None
            Ticks the combo counter up by 1 when called
            Displays the combo text and combo count on the scoreboard if 
            the combo counter goes above 0, meaning combo bonus is active
        '''
        self.combo += 1
        if self.combo > 0:
            combo_num = str(self.combo)
            self.combo_text.setText("Combo x"+combo_num)
            self.combo_text.setTextColor("Black")
        return None

    def disable_combo(self):
        ''' Parameters: None
            Return: None

            Resets all the variabls associated with tracking
            and enabling the combo bonus back to default state,
            disabling the combo bonus.
        '''
        self.combo = -1
        self.combo_text.setTextColor('') 
        return None

    def set_backtoback(self):
        ''' Parameters: None
            Return None
            
            When backtoback bonus is set to False this function
            ticks backtoback_counter up by 1.
            When the counter equals 2, the backtoback variable is set 
            to True and displays the "B2B" text on the scoreboard,
            enabling back-t--back bonus.
        ''' 
        if self.backtoback == False and self.backtoback_count < 2:
            self.backtoback_count += 1 
        
        #This is an if statement and not elif because I want it to 
        #run everytime after the previous statement
        if self.backtoback == False and self.backtoback_count >= 2:
            self.backtoback_count = 0
            self.backtoback = True
            self.backtoback_text.setTextColor("Black")
        return None

    def disable_backtoback(self):  
        ''' Parameters: None
            Return: None

            Resets all the variables associated with tracking and enabling
            the back-to-back bonus to defualt state, disabling the the
            back-to-back bonus.
        '''
        self.backtoback_count = 0
        self.backtoback = False
        self.backtoback_text.setTextColor('') 
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
        if total_lines > (10*self.level):
            self.level += 1
            self.gravity_up()
            lvl_str = str(self.level)
            self.lvl_num.setText(lvl_str)
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
    
    def softdrop_score_up(self): 
        ''' Parameters: None
            Return: None

            Soft drops awards players 1 point per manual down movement
            This function adds 1 to the score every time it is called.
        '''
        self.score += 1
        score_str = str(int(self.score))
        self.scr_num.setText(score_str)
        return None
    
    def harddrop_score_up(self): 
        ''' Parameters: None
            Return: None

            Hard drops awards players 2 points per down movement
            This function adds 2 to the score every time it is called.
        '''
        self.score += 2
        score_str = str(int(self.score))
        self.scr_num.setText(score_str)
        return None

    def score_up(self, cleared_lines):
        ''' Parameters: type:int - Number of cleared lines
            Return: None
            If there lines are cleared:
            1. Calculates the score depending on the number of lines
               cleared in one go.
            2. Increments the total score by the amount of new points 
               earned.
            3. Draws the new score on the screen
            4. Sets the combo (combo counts up by 1)
            Otherwise if there are no line clears:
            Disables combo

            Points per line cleared:
            1 line cleared: 100 * level
            2 lines cleared: 300 * level
            3 lines cleared: 500 * level
            4 lines cleared: 800 * level
            n lines cleared: line_score * level
        '''
        #Figured out this formula myself. The formula calculates 
        #the line score depending on the number of lines cleared.
        #The calculation needs to be done in floating point.
        #I know I could used a dictionary but this is more fun.
        n = cleared_lines 
        if cleared_lines > 0:
            line_score = (50.0/3.0)*(n**3)+(-100.0)*(n**2)+(1150.0/3.0)*(n)+(-200.0)
            if self.backtoback == True:
                line_score = 1.5 * line_score
           
            #Combo only kicks in when combo count greater than zero
            points = line_score * self.level 
            if self.combo > 0:
                points += 50 * self.combo * self.level
            self.score += points
            score_str = str(int(self.score))
            self.scr_num.setText(score_str)
            self.set_combo() 
        else:
            self.disable_combo() 
        return None

    def tspin_score_up(self, cleared_lines):
        ''' Parameters: type:int - Number of cleared lines
            Return: None 
            
            If lines are cleared with a t-spin, the points awarded are different
            from normal line clears. Points are awarded even if no lines are cleared.
            The combo is set (combo counter counted up by 1) if there are any line 
            clears. It is disabled otherwise.

            Points per full t-spin lines cleared:
            0 lines cleared: 400
            1 line cleared:  800
            2 lines cleared: 1200
            3 lines cleared: 1600
        '''
        #A simple formula for a straight line.
        #Maybe best to use float for the calculation
        #I know I could have used a dictionary but a little
        #math practive never hurt anyone.
        n = cleared_lines 
        tspin_score = (400.0*n)+400.0
        if self.backtoback == True:
            tspin_score = 1.5 * tspin_score
        
        #Combo only kicks in when combo count greater than zero
        points = tspin_score * self.level
        if self.combo > 0:
            points += 50 * self.combo * self.level 
        
        self.score += points 
        score_str = str(int(self.score))
        self.scr_num.setText(score_str)
        
        if cleared_lines > 0: 
            self.set_combo() 
        else:
            self.disable_combo() 
        return None

    def mini_tspin_score_up(self, cleared_lines):
        ''' Parameters: type:int - Number of cleared lines
            Return: None

            Mini t-spin without any lines cleared awards points.
            If lines are cleared with a mini t-spin that also
            awards points, which is different than normal line clears
            and full t-spin awards. Hence this function.
            The combo is set (combo counter counts up by 1) if there 
            are any line clears. Combo is disabled if there are zero
            lines cleared.

            Points per mini t-spin lines cleared:
            0 lines: 100
            1 line: 200
            2 lines: 400
            3 lines: Impossible with a mini t-spin 
        '''
        #Derived the formula myself.
        #I know a dictionary works in this case
        #but wanted to do a little math practice 
        n = cleared_lines
        mini_score = ((50.0)*(n**2))+((50.0)*(n))+(100.0)
        if self.backtoback == True:
            mini_score = 1.5 * mini_score
        
        #Combo only kicks in when combo count greater than zero
        points = mini_score * self.level
        if self.combo > 0:
            points += 50 * self.combo * self.level
        
        self.score += points 
        score_str = str(int(self.score))
        self.scr_num.setText(score_str)
        
        if cleared_lines > 0:
            self.set_combo() 
        else:
            self.disable_combo() 
        return None

    def update(self, cleared_lines, total_lines):
        ''' Paremeters: type: int - cleared_lines (cleared lines) 
                        type: int - total_lines (total lines cleared) 
            Return: type:int/Bool If there is a level increment: 
                                    - Returns the new gravity
                                  If there is no level change then:
                                    - Returns False
            
            Updates the score and level based on cleared lines in one go and
            total cleared lines. Also tracks the back-to-back bonus. 4 line
            clears keep the back-to-back bonus alive, clears of less than 4 lines
            results in the back-to-back bonus being disabled. Also keeps track
            of the back-to-back bonus. 
        '''
        if cleared_lines >= 4:
            self.set_backtoback()
        elif cleared_lines >= 1 and cleared_lines <= 3:
            self.disable_backtoback() 

        self.score_up(cleared_lines)
        return self.level_up(total_lines)

    def tspin_update(self, cleared_lines, total_lines, full):
        ''' Paramters: type: int - cleared_lines (cleared lines)  
                       type: int - total_lines (total lines cleared) 
                       type: bool - Full t-spin: true, mini t-spin: false

            Updates the score and level based on cleared lines and total cleared
            lines if a t-spin is performed. Every t-spin keeps back-to-back bonus 
            alive, hence the call to the set_backtoback() function. T-spins
            keep back-to-back bonus alive.
        '''
        self.set_backtoback()
        if full == False:
            self.mini_tspin_score_up(cleared_lines)
            return self.level_up(total_lines)
        
        self.tspin_score_up(cleared_lines)
        return self.level_up(total_lines)


############################################################
# PREVIEWBOARD CLASS
############################################################
class PreviewBoard(Board):
    ''' PreviewBoard class: it shows pieces which are held and a
        preview of next three pieces. 

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    block_size - type:int - size of tetris blocks in pixels
                    background - type:str - the colour of the background of the canvas 
                                            frame 
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
    
    def __init__(self, win, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size 
        self.background = "light gray"
        self.hld_shape = None
        self.prv_list = []
        
        self.rect = None
        self.hld_txt = None
        self.prv_txt = None
        self.hld_line = None
        self.prv_line = None
        Board.__init__(self, win, self.width, self.height, self.block_size, self.background)  
        #Important: These must be done after parent class initialization
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
        origin = (0.0,0.0)
        point_2 = (canvas_w, canvas_h)
        self.rect = self.make_rect(origin, point_2, 5, "black", "MediumAquamarine")
        return None
     
    def init_text(self):
        ''' Parameters: None
            Return: None 
            Initializes all the text objects that is displayed on the
            scoreboard, which are "Hold" and "Preview". 
        '''
        #Got coordinates after trial and error
        self.hld_txt = self.make_text((24.5, 14.0), "Hold", 9) 
        #Got coordinates after trial and error
        self.prv_txt = self.make_text((136.5, 14.0), "Preview", 9)
        return None
    
    def init_lines(self):
        ''' Parameters: None
            Return: None
            Initializes lines which are displayed underneath 
            the text as a stylized underline
        '''
        #Determined coordinates after trial and error
        self.hld_line = self.make_line((11.5,19.0), (69.0,19.0))
        #Determined coordinates after trial and error
        self.prv_line = self.make_line((114.5,19.0), (289.0,19.0)) 
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
        #Got the coordinates after trial and error
        prv_x = 14.65 
        prv_y = 3.75 
        
        for i in range(3):
            prv_center = gr.Point(prv_x, prv_y) 
            new_shape = shape_list[i](center=prv_center, block_size=10)
            self.prv_list.append(new_shape)
            #Got 5.49 after trial and error
            prv_x += 5.49 
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
        #Got the coordinates after trial and error
        hld_x = 4.65
        hld_y = 3.75 #3.25 #3 #2.75
        hld_center = gr.Point(hld_x, hld_y) 

        if hold_shape != None:
            shape_type = hold_shape.__class__ 
            self.hld_shape = shape_type(center=hld_center, block_size=10) 
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

    def undraw_preview(self):
        ''' Parameters: None
            Return: None
            Undraws the currently preview shapes if they exist
            and are displayed.
        '''
        if self.prv_list != []:
            list_len = len(self.prv_list)
            for i in range(list_len):
                if self.prv_list[i]:
                    self.prv_list[i].undraw()
            self.prv_list = []
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
# END OF FILE                                              #
############################################################
