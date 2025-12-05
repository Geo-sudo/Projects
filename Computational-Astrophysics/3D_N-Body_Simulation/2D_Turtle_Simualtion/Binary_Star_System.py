import turtle
import math
import os

class BinarySystemBody(turtle.Turtle):
    minDisplaySize = 20
    displayLogBase = 1.1

    def __init__(self, Binary_System, mass, position=(0,0), velocity=(0,0)):
        super().__init__()
        self.mass=mass
        self.setposition(position)
        self.velocity = velocity
        self.display_size = max(math.log(self.mass, self.displayLogBase), self.minDisplaySize)

        self.penup()
        self.hideturtle()

        Binary_System.addBody(self)
    
    def draw(self):
        self.clear()
        self.dot(self.display_size)
    def move(self):
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])

class Star(BinarySystemBody):
    def __init__(self, Binary_System, mass, position=(0,0), velocity=(5,0), color="blue"):
        super().__init__(Binary_System, mass, position, velocity)
        self.color(color)


class BinarySystem:
    def __init__(self, width, height):
        self.Binary_System = turtle.Screen()
        self.Binary_System.tracer(0)
        self.Binary_System.setup(width,height)
        self.Binary_System.bgcolor("black")

        self.bodies = []

    def addBody(self, body):
        self.bodies.append(body)

    def removeBody(self, body):
        self.bodies.remove(body)

    def update_all(self):
        for body in self.bodies:
            body.move()
            body.draw()
            self.adjust_size()
            self.Binary_System.update()

    def adjust_size(self):
        min_x = min(body.xcor() for body in self.bodies)
        max_x = max(body.xcor() for body in self.bodies)
        min_y = min(body.ycor() for body in self.bodies)
        max_y = max(body.ycor() for body in self.bodies)

        padding = 1000
        width = (max_x-min_x) + padding
        height = (max_y-min_y) + padding
        if max(abs(max_x), abs(min_x) ) > 150 or max(abs(max_y), abs(min_y)) > 150:
            self.Binary_System.screensize(width,height)

    @staticmethod
    def gravity_baby(first: BinarySystemBody, second: BinarySystemBody):
        force = (first.mass*second.mass)/(first.distance(second)**2)
        angle = math.radians(first.towards(second))
        reverse = 1
        for body in first,second:
            acc = force/body.mass
            acc_x = acc * math.cos(angle)
            acc_y = acc * math.sin(angle)
            body.velocity = (body.velocity[0] + (reverse*acc_x), body.velocity[1] + (reverse*acc_y))
            reverse = -1  
    def save_frame(self, filename):
        frames_dir = "frames"
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)

        frames = os.path.join(frames_dir,filename)
        canvas = self.Binary_System.getcanvas()
        canvas.postscript(file=frames)