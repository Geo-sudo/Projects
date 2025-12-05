from Vectors import Vector
import matplotlib.pyplot as plt
import numpy as np

class BinarySystem:
    def __init__(self, size, dt):
        self.size = size #in AU
        self.bodies = []
        self.dt = dt # in days
        self.fig, self.ax = plt.subplots(1, 1, subplot_kw={"projection":"3d"}, figsize=(self.size, self.size))
        self.fig.tight_layout()
        
        ticks = np.linspace(-self.size, self.size, num=5)
        self.tick_labels = {
            'x': [f"{tick:.1f} AU" for tick in ticks],
            'y': [f"{tick:.1f} AU" for tick in ticks],
            'z': [f"{tick:.1f} AU" for tick in ticks]
        }

        self.ax.view_init(10, 0)
    
    def add_body(self,body):
        self.bodies.append(body)

    def update_all(self):
        self.bodies.sort(key=lambda item: item.position[0])
        for body in self.bodies:
            body.move()

    def draw_all(self):
        self.ax.set_xlim([-self.size/2, self.size/2])
        self.ax.set_ylim([-self.size/2, self.size/2])
        self.ax.set_zlim([-self.size/2, self.size/2])
        plt.pause(0.001)
        self.ax.clear()

        ticks = np.linspace(-self.size/2, self.size/2, num=5)
        self.ax.set_xticks(ticks)
        self.ax.set_yticks(ticks)
        self.ax.set_zticks(ticks)
        self.ax.set_xticklabels(self.tick_labels['x'])
        self.ax.set_yticklabels(self.tick_labels['y'])
        self.ax.set_zticklabels(self.tick_labels['z'])

        for body in self.bodies:
            body.draw()
    
    def calc_gravity(self):
        for it, first in enumerate(self.bodies):
            for second in self.bodies[it+1:]:
                first.acc_due_to_gravity(second)

class Body:
    G = 1.32712e-7 #in AU^3 * M0^-1 * day^-2

    def __init__(self, binary_system: BinarySystem, mass, radius, position=(0,0,0), velocity=(0,0,0), colour="black", set_size=False, size=10):
        self.binary_system = binary_system
        self.mass = mass #in M0
        self.position = Vector(*position) #in AU
        self.velocity = Vector(*velocity) #in AU/day
        self.radius = radius # in AU
        self.size = size
        self.colour = colour

        if not set_size:
            self.display_size = max(
                self.radius*2,
                self.size
            )
        else: 
            self.display_size = self.size

        self.binary_system.add_body(self)

        self.plot, = self.binary_system.ax.plot(
            [self.position.x], [self.position.y], [self.position.z],
            marker="o",
            markersize=self.display_size,
            color=self.colour,
            zorder=2
        )
        self.shadow, = self.binary_system.ax.plot(
            [self.position.x], [self.position.y], [-self.binary_system.size / 2],
            marker="o",
            markersize=self.display_size / 2,
            color=(.5, .5, .5),
            zorder=1
        )

    def move(self):
        self.position += (self.velocity * self.binary_system.dt)
    
    def draw(self):
        self.binary_system.ax.plot(
            *self.position,
            marker="o",
            markersize=self.display_size + self.position[0]/30,
            color=self.colour,
            zorder = 2
        )
        self.binary_system.ax.plot(
                self.position[0],
                self.position[1],
                -self.binary_system.size / 2,
                marker="o",
                markersize=self.display_size / 2,
                color=(.5, .5, .5),
                zorder = 1
        )
    
    def acc_due_to_gravity(self, other):
        r = Vector(*other.position) - Vector(*self.position)
        r_norm = r.get_norm()

        force_norm = self.G * self.mass * other.mass / (r_norm**2) # in M0 * AU * day^-2
        force = r.normalize() * force_norm

        reverse = 1
        for body in self, other:
            acc = force/body.mass * reverse #in AU * day^-2
            body.velocity += acc * body.binary_system.dt
            reverse = -1

