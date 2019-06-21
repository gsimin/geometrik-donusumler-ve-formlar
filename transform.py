import simplegui

def find_distance(point1, point2):
    distance_x = point2[0] - point1[0]
    distance_y = point2[1] - point1[1]
    return [distance_x, distance_y]

class Rectangle:
    def __init__(self, position):
        self.position = position
        self.initial_position = position
        
    def reset(self):
        self.position = self.initial_position
        
    def move(self, point):
        distance = find_distance(self.position[0], point)
        point_list = self.position[1:]
        new_position = [point]
        for point in point_list:
            x = point[0] + distance[0]
            y = point[1] + distance[1]
            new_position.append([x, y])
        self.position = new_position       
        
    def draw(self, canvas):
        canvas.draw_polygon(self.position, 4, "Orange")
        
def draw_handler(canvas):
    rectangle.draw(canvas)        
            
def reset():
    rectangle.reset()

def mouse_click(pos):
    rectangle.move(list(pos))
            
def main():
    frame = simplegui.create_frame("Move", 500, 500, 100)
    button_reset = frame.add_button("Reset", reset, 80)
    frame.set_mouseclick_handler(mouse_click)
    frame.set_draw_handler(draw_handler)
    frame.start()
    
rectangle = Rectangle([[200, 300], [200, 200], [300, 200], [300, 300]])
main()
    