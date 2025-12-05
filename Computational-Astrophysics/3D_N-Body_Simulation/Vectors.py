import math

class Vector:
    def __init__(self, x: float=0, y: float=0, z: float=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"{self.x}î + {self.y}ĵ + {self.z}k̂"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __iter__(self):
        return iter((self.x,self.y,self.z))
    
    def __getitem__(self, it):
        if it == 0:
            return self.x
        elif it == 1:
            return self.y
        elif it == 2:
            return self.z
        else:
            raise IndexError(f"Out-Of-Bounds index! Inputted index is {it}.")
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x*other.x + self.y*other.y + self.z*other.z
        elif isinstance(other, (int, float)):
            return Vector(self.x*other, self.y*other, self.z*other)
        else:
            raise TypeError(f"Can't deal with data type! Inputted data type is {type(other)}.")

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("Seriously man?!")
        elif isinstance(other, (int, float)):
            return Vector(self.x/other, self.y/other, self.z/other)
        else:
            raise TypeError(f"Can't deal with data type! Inputted data type is {type(other)}.")

    def get_norm(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        mag = self.get_norm()
        return Vector(self.x/mag, self.y/mag, self.z/mag)



