import argparse
import matplotlib.pyplot as plt
from Binary_System import BinarySystem, Body
from matplotlib.animation import FuncAnimation

#Units are in AU, M0, and days

def main():
    parser = argparse.ArgumentParser(description='Run Binary Star System')
    
    parser.add_argument('--t', type=int, default=1e9, help='Run for how many days')
    parser.add_argument('--save', action='store_true', default=False, help='Save the animation in the local directory')
    parser.add_argument('--Sirius', action='store_true', default=False, help='Use Sirius example system')
    parser.add_argument('--size', type=int, default=50, help='Size of the binary system')
    parser.add_argument('--dt', type=int, default=200, help='Time step in days')

    args = parser.parse_args()
    current_t=0
    t = args.t
    save = args.save
    Sirius = args.Sirius
    size = args.size
    dt = args.dt

    binary_system = BinarySystem(size=size, dt=dt)
    
    if Sirius:
        # Sirius Example:
        Sirius_A = Body(binary_system, 2.063, 0.007952299, position=(-5.958, 0, 0), velocity=(0.0000702, -0.0000702, 0), colour="blue", set_size=True, size=25)
        Sirius_B = Body(binary_system, 1.018, 3.720374e-5, position=(14.042, 0, 0), velocity=(-0.0000458, 0.0000458, 0), colour="cyan", set_size=True, size=25)
    else:
        # Random Stable System:
        star1 = Body(binary_system, 1, 4.6491e-3, colour="blue", set_size=True, size=20)
        star2 = Body(binary_system, 3.00274e-6, 4.2588e-5, position=(5, 0, 2), velocity=(0, 0.000172, 0), colour="yellow", set_size=True, size=15)
    
    if save:
        # Saving Animation:
        def animate(n):
            binary_system.calc_gravity()
            binary_system.update_all()
            binary_system.draw_all()
            return binary_system.ax.artists
        
        anim = FuncAnimation(fig=binary_system.fig, func=animate, frames=240, interval=100, repeat=True)
        anim.save('A.mp4', fps=24, dpi=300)
        
    else:
        # Testing Animation:
        while current_t < t:
            binary_system.calc_gravity()
            binary_system.update_all()
            binary_system.draw_all()
            current_t += binary_system.dt

if __name__ == '__main__':
    main()