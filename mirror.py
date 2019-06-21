import simplegui
import math

    
def find_ma(points):
    point1 = points[0]	
    point2 = points[1]	
        
    x0 = point1[0]
    x1 = point2[0]
    y0 = point1[1]
    y1 = point2[1]
    
    m = (y1 - y0) / (x1 - x0)
    a = find_a([x0, y0], m)
    a = y0 - m * x0    
    return m, a 

def find_a(point, m):
    return point[1] - point[0] * m

def find_intersection(m1, a1, m2, a2):
    x = (a2 - a1) / (m1 - m2)
    y = m1 * x + a1
    return [x, y]

def check_vertical(point1, point2):
    x0, y0 = point1[0], point1[1]
    x1, y1 = point2[0], point2[1]
    return math.fabs(y0 - y1) > math.fabs(x0 - x1)

class Rectangle:
    def __init__(self, position):
        self.position = position
        self.initial_position = position
        
    def reset(self):
        self.position = self.initial_position
        
    def find_line_type(self, points):
        point1 = points[0]
        point2 = points[1]
        
        x0, y0 = point1[0], point1[1]
        x1, y1 = point2[0], point2[1]
        
        if y1 - y0 == 0:
            self.mirror_horizontal(point1)    
        elif x1 - x0 == 0:
            self.mirror_vertical(point1)
        else:
            self.mirror(points)
        
    def mirror_horizontal(self, point):
        new_position = []
        y0 = point[1]
        for pos in self.position:
            y1 = pos[1]
            distance = y0 - y1
            y_new = 2 * distance + y1
            new_position.append([pos[0], y_new])
        self.position = new_position            
    
    def mirror_vertical(self, point):
        new_position = []
        x0 = point[0]
        for pos in self.position:
            x1 = pos[0]
            distance = x0 - x1
            x_new = 2 * distance + x1
            new_position.append([x_new, pos[1]])
        self.position = new_position
        
    def mirror(self, points):
        new_position = []
        m1, a1 = find_ma(points)
        m2 = -1 * (m1 ** -1)
        for pos in self.position:
            a2 = find_a(pos, m2)
            intersection = find_intersection(m1, a1, m2, a2)
            dist_x = intersection[0] - pos[0]
            dist_y = intersection[1] - pos[1]
            new_x = pos[0] + 2 * dist_x
            new_y = pos[1] + 2 * dist_y
            new_position.append([new_x, new_y])
        self.position = new_position     
        
    def draw(self, canvas):
        canvas.draw_polygon(self.position, 4, "Orange")
        
def draw_handler(canvas):
    global mirror_line
    rectangle.draw(canvas)
    if len(mirror_line) == 1:
        canvas.draw_circle(mirror_line[0], 2, 1, "Blue", "Blue")
    elif len(mirror_line) == 2:
        canvas.draw_line(mirror_line[0], mirror_line[1], 2, "Blue")
        
def mouse_click(pos):
    global mirror_line, rectangle, ortho_on
    if len(mirror_line) == 0:
        mirror_line.append(pos)
    elif len(mirror_line) == 1:
        if pos != mirror_line[0]:
            if ortho_on:
                vertical = check_vertical(mirror_line[0], pos)
                if vertical:
                    point = [mirror_line[0][0], pos[1]]
                    mirror_line.append(point)
                else:
                    point = [pos[0], mirror_line[0][1]]
                    mirror_line.append(point)
            else:
                mirror_line.append(pos)
            rectangle.find_line_type(mirror_line)
            mirror_line = []
            
def reset():
    rectangle.reset()
    
def set_ortho():
    global ortho_on, button_ortho
    if ortho_on:
        ortho_on = False
        button_ortho.set_text("Ortho on")
    else:
        ortho_on = True
        button_ortho.set_text("Ortho off")
        
def main():
    global rectangle, mirror_line, button_reset, button_ortho, ortho_on
    frame = simplegui.create_frame("Mirror", 500, 500, 100)
    button_reset = frame.add_button("Reset",reset, 85)
    button_ortho = frame.add_button("Ortho on", set_ortho, 85)
    frame.set_draw_handler(draw_handler)
    frame.set_mouseclick_handler(mouse_click)
    rectangle = Rectangle([[50, 400], [150, 400], [150, 475], [50, 475]])
    mirror_line = []
    ortho_on = False
    frame.start()
    
main()
    