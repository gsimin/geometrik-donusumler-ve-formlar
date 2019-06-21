import simplegui
import math

class Rec:
    def __init__(self, pos):
        self.pos = pos
        self.initial_pos = pos
        self.origin = self.find_origin()
        
    def find_origin(self):
        x = (self.pos[0][0] + self.pos[2][0]) / 2
        y = (self.pos[0][1] + self.pos[2][1]) / 2
        return [x, y]
        
    def reset(self):
        self.pos = self.initial_pos 
        
    def rotate_rec(self, angle):
        new_position = []
        for pos in self.pos:
            x = pos[0] - self.origin[0]
            y = pos[1] - self.origin[1]
            new_x = x * math.cos(angle) - y * math.sin(angle) + self.origin[0]
            new_y = x * math.sin(angle) + y * math.cos(angle) + self.origin[1] 
            new_position.append([new_x, new_y])
        self.pos = new_position
            
    def draw(self, canvas):
        canvas.draw_polygon(self.pos, 4, "Orange")
        
def draw(canvas):
    rectangle.draw(canvas)
    
def set_angle(angle_inp):
    global angle
    angle = (float(angle_inp) % 360) * 2 * math.pi / 360
    
def rotate():
    global angle
    rectangle.rotate_rec(angle)
    
def reset():
    rectangle.reset()
    
def main():	
    global rectangle, angle
    rectangle = Rec([[200, 300], [200, 200], [300, 200], [300, 300]])
    frame = simplegui.create_frame("Rotate", 500, 500, 100)
    frame.set_draw_handler(draw)
    angle_input = frame.add_input("Angle", set_angle, 80)
    button_rotate = frame.add_button("Rotate", rotate, 80)
    button_reset = frame.add_button("Reset", reset, 80)
    angle = 2 * math.pi 
    frame.start()

main()
            