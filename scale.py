import simplegui

def find_distance(point1, point2):
    distance_x = point2[0] - point1[0]
    distance_y = point2[1] - point1[1]
    return [distance_x, distance_y]

def find_scaled_distance(point1, point2, factor):
    distance = find_distance(point1, point2)
    return [distance[0] * factor, distance[1] * factor]

def find_position(point1, point2):
    x = point1[0] + point2[0]
    y = point1[1] + point2[1]
    return [x, y]    
    
class Rectangle:
    def __init__(self, position):
        self.position = position
        self.initial_position = position
        
    def reset(self):
        self.position = self.initial_position
        
    def scale(self, factor):
        point_list = self.position[1:]
        new_position = [self.position[0]]
        for point in point_list:
            scaled_distance = find_scaled_distance(self.position[0], point, factor)
            position = find_position(self.position[0], scaled_distance)
            new_position.append(position)
        self.position = new_position       
        
    def draw(self, canvas):
        canvas.draw_polygon(self.position, 4, "Orange")
        
def draw_handler(canvas):
    rectangle.draw(canvas)        
            
def reset():
    rectangle.reset()

def set_scale(scale_inp):
    global scale_factor, scale_input
    scale_factor = float(scale_inp)
    
def scale():
    global scale_factor
    rectangle.scale(scale_factor)
            
def main():
    global rectangle, button_reset, buton_scale, scale_input, scale_factor
    frame = simplegui.create_frame("Scale", 500, 500, 100)
    scale_input = frame.add_input("Scale factor", set_scale, 85)
    button_scale = frame.add_button("Scale", scale, 85)
    button_reset = frame.add_button("Reset",reset, 85)
    frame.set_draw_handler(draw_handler)
    rectangle = Rectangle([[200, 300], [200, 200], [300, 200], [300, 300]])
    scale_factor = 1
    frame.start()
    
main()
    