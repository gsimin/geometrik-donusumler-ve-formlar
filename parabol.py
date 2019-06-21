"""
Program to draw parabola
"""

import simplegui
import math

# CLASSES
class Container:
    def __init__(self):
        self.points = []
        self.line = []
        self.parabolas = []			
        self.hidden = False			# when true hides reference drawings of parabolas
        self.edit = False			# when true enables edit mode
        self.division = 16			# number of division to construct parabola
        self.select_index = ""		# index of the selected parabola
    
    # sets the number of division
    def set_division(self, num):
        """
        Input:
        num: (int) number of division
        """
        self.division = num
    
    # sets self.edit to true if false, to false if true
    def set_edit(self):
        self.edit = not self.edit
    
    # adds point to self.points
    def add_point(self, position):
        """
        Input:
        position: (tuple) position of point to add
        """
        if position not in self.points:
            self.points.append(position)
        
        # there are two points -> add line
        if len(self.points) == 2:		
            self.line = [self.points[0], self.points[1]]
            
        # there ara three points -> add parabola    
        elif len(self.points) == 3:	
            self.parabolas.append(Parabola(self.points[0], self.points[1], self.points[2], self.division, self.hidden))
            self.points = []	# clear points
            self.line = []		# clear lines
        
    # selects the parabola to be editted
    def select_parabola(self, pos):
        """
        Input:
        pos: (tuple) coordinates of point of the parabola to be editted
        """
        index_parabola = 0		# index of parabolas in self.parabolas
        while index_parabola < len(self.parabolas):	
            points = self.parabolas[index_parabola].get_points()	# control_points of the parabola
            index_point = 0		# index of control_points in parabola  	
            while index_point < 3:
                # compare pos with control_points of parabola
                if math.fabs(points[index_point][0] - pos[0]) <= 5 and math.fabs(points[index_point][1] - pos[1]) <= 5:
                    self.parabolas[index_parabola].select_point(index_point)
                    self.select_index = index_parabola
                    break
                index_point += 1
            index_parabola += 1
    
    # sends the new coordinates of the selected point to parabola
    def edit_parabola(self, pos):
        """
        Input:
        pos: (tuple) new coordinates of the selected point
        """
        self.parabolas[self.select_index].edit(pos)
        self.select_index = ""
    
    # clears all drawings
    def clear(self):
        self.points = []
        self.line = []
        self.parabolas = []
    
    # hides/shows reference lines and points of parabolas
    def hide_show(self):
        self.hidden = not self.hidden
        for parabola in self.parabolas:
            parabola.set_status(self.hidden)
    
    # draws all points, lines and parabolas
    def draw(self, canvas):
        for point in self.points:
            canvas.draw_circle(point, 2, 1, 'Orange', 'Orange')
        if self.line != []:
            canvas.draw_line(self.line[0], self.line[1], 2, 'Blue')
        for parabola in self.parabolas:
            parabola.draw(canvas)

# -------------------------------------------------------------------------------
            
class Parabola:
    def __init__(self, point1, point2, point3, division, hidden):
        self.division = division	# number of disvision to construct parabola
        self.select_index = ""		# index of the selected point to edit
        self.control_points = [point1, point2, point3]		# points to construct parabola
        self.control_lines = [[self.control_points[0], self.control_points[1]], 
                              [self.control_points[1], self.control_points[2]]] 	# lines between control points
        self.div_points = []	# points that divides control_lines	
        self.ref_lines = []		# lines that connects dividing points of control_lines
        self.ref_points = []	# intersection points of ref_lines         
        self.hidden = hidden	# when true hides reference drawings of parabola except control_points
        self.divide_and_connect_lines()
    
    # helper function to access self.divide() and self.connect_lines()
    def divide_and_connect_lines(self):
        for line in self.control_lines:
            self.divide(line)
        self.connect_lines()
    
    # divides the line into specified number (self.division) of pieces
    def divide(self, line):
        """
        Input:
        line: (list) coordinates of the line to be divided
        """
        point1 = line[0]
        point2 = line[1]
        t = 1 / self.division
        while t < 1:
            x = point1[0] * (1 - t) + point2[0] * t
            y = point1[1] * (1 - t) + point2[1] * t
            self.div_points.append([x, y])
            t += 1 / self.division
    
    # connects the points in self.div_points 
    def connect_lines(self):
        index1 = 0					# index of first div_point of first control_line
        index2 = self.division - 1	# index of first div_point of second control_line
    
        while index1 < (self.division - 1):
            self.ref_lines.append([self.div_points[index1], self.div_points[index2]])
            index1 += 1				
            index2 += 1				
        self.construct_parabola()
    
    # finds points to construct parabola
    def construct_parabola(self):
        index = 0
        temp_m = ""
        temp_a = ""
        first_point = self.ref_lines[0][0] # starting point of parabola
        last_point = self.ref_lines[-1][1] # end point of parabola
        self.ref_points += [first_point]
        
        while index < len(self.ref_lines) - 1:
            # prevent to run find.ma() twice for the same line 
            if temp_m == "":
                m0, a0 = self.find_ma(self.ref_lines[index])
                m1, a1 = self.find_ma(self.ref_lines[index+1])
                temp_m = m1
                temp_a = a1              
            else:
                m0, a0 = temp_m, temp_a
                m1, a1 = self.find_ma(self.ref_lines[index+1])
                temp_m = m1
                temp_a = a1
                
            # at intersection point: a0 + m0.x = a1 + m1.x 
            x = (a0 - a1) / (m1 - m0)	# x coordinate at intersection point
            y = x * m0 + a0				# y coordinate at intersection point
            
            self.ref_points.append([x, y])
            index += 1
            
        self.ref_points.append(last_point)
        
    # finds slope and constant of the line (y = a + mx)
    def find_ma(self, line):
        """ 
        Input:
        line: (list) coordinates of line [point1, point2]
        Output:
        m: (float) slope of the line
        a: (float) constant
        """
        point1 = line[0]	# first point of the line
        point2 = line[1]	# second point of the line
        
        x0 = point1[0]
        x1 = point2[0]
        y0 = point1[1]
        y1 = point2[1]
    
        m = (y1 - y0) / (x1 - x0)
        a = y0 - m * x0
    
        return [m, a] 
    
    # sets self.hidden
    def set_status(self, ishidden):
        self.hidden = ishidden
    
    # returns self.control_points to container
    def get_points(self):
        """
        Output: (list) coordinates of reference points 
        """
        return self.control_points
    
    # sets self.select_index to the index of selected point
    def select_point(self, index):
        """
        Input:
        index: (int) index of the selected point
        """
        self.select_index = index
    
    # edits the parabola according to new coordinates
    def edit(self, pos):
        """
        Input: 
        pos: (list) new coordinates of the selected point
        """
        self.control_points[self.select_index] = pos
        self.control_lines = [[self.control_points[0], self.control_points[1]], 
                              [self.control_points[1], self.control_points[2]]]
        self.div_points = []
        self.ref_points = []
        self.ref_lines = []
        self.divide_and_connect_lines()
        self.select_index = ""
    
    # draws parabola, reference and control points and lines onto canvas
    def draw(self, canvas):         
        if not self.hidden: 
            for line in self.control_lines:	
                canvas.draw_line(line[0], line[1], 2, 'Blue')
            
            for point in self.control_points:                
                if not container.edit:
                    canvas.draw_circle(point, 2, 1, 'Orange', 'Orange')
            
            for line in self.ref_lines:
                canvas.draw_line(line[0], line[1], 2, 'Blue')
                
            for point in self.div_points:
                canvas.draw_circle(point, 2, 1, 'Orange', 'Orange')
                
        for point in self.control_points:
            if container.edit:
                canvas.draw_circle(point, 4, 1, 'Red', 'Red')
                if self.select_index != "":
                    canvas.draw_circle(self.control_points[self.select_index], 6, 1, "Red", "Red")
                    
        canvas.draw_polyline(self.ref_points, 4, 'Green')
                
        if not self.hidden:
            for point in self.ref_points:
                canvas.draw_circle(point, 2, 1, 'Orange', 'Orange')        

# EVENT HANDLERS

# event handler for button_clear
def clear():
    container.clear()

# event handler for button_hide    
def hide_show():
    container.hide_show()
    if container.hidden:
        button_hide.set_text("Show")
    else:
        button_hide.set_text("Hide")

# event handler for button_edit
def edit():
    container.set_edit()
    if container.edit:
        button_edit.set_text("Draw")
    else:
        button_edit.set_text("Edit")

# event handler for div_input (to set number of division)
def input_handler(num):
    div_num = 0
    try:
        div_num = int(num)
    except:
        return
    if div_num > 1 and div_num < 65:
        container.set_division(div_num)

# event handler for mouse click
def mouse_handler(position):
    if not container.edit:					# in draw mode
        container.add_point(position)
    elif container.select_index == "":		# in edit mode, no point selected 
        container.select_parabola(position)
    else:									# in edit mode, a point is selected
        container.edit_parabola(position)

# event handler for canvas        
def draw_handler(canvas):
    container.draw(canvas)

# function to start program
def start():
    global button_hide, button_edit 
    frame = simplegui.create_frame("Draw Parabola", 500, 500, 120)
    div_input = frame.add_input("Division(2-64)", input_handler, 100)
    button_clear = frame.add_button("Clear", clear, 100)
    button_hide = frame.add_button("Hide", hide_show, 100)
    button_edit = frame.add_button("Edit", edit, 100)
    frame.set_mouseclick_handler(mouse_handler)
    frame.set_draw_handler(draw_handler)
    frame.start()
    
container = Container()
start()


