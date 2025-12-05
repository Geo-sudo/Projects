# Binary Star System Simualtion

This is a framework for a realistic astrophysical simulation of a **Binary Star System**, written in `Python` using the `matplotlib` library. It has the orbit data of the [Sirius Binary System](https://en.wikipedia.org/wiki/Sirius), a random stable system, and you can enter your own data and try to find a stable orbit.

### Table of Contents

- [How To Run](#how-to-run)
- [Background On Binary Stars](#background-on-binary-stars)
- [The Physics](#the-physics)



# How To Run

**Run it like any Python file using:** <br>
`python Run_Binary_System.py`

The simulation has two modes: *viewing* and *saving*. `save=False` allows you to view the animation in a window, while `save=True` will, in addition to viewing the animation, save it in webm format in the current directory.

<br>

**Running the simulation will use these default values:** <br>
- `t=1e9` ---> Duration to run the animation in viewing mode in days.
- `save=False` ---> Defines whether you're using *viewing* or *saving* mode.
- `Sirius=False` ---> By default the used data is a random stable orbit. Setting this to True will use real-world data from the Sirius binary system.
- `size=50` ---> This defines the cubic size of the simulation world in AU.
- `dt=200` ---> The timestep taken for each calculation in days.

<br>

> Note: You can run the Sirius system example or the given stable one from the terminal. Using other data will require you to hard code it in the [Run_Binary_System.py](Run_Binary_System.py) as it will be cumbersome to pass that many arguments. <br>This also applies to the configuration of the animation in *saving* mode.



# Background On Binary Stars

Did you know that **Sirius** the brightes "star" in the nightsky isn't a star! It's a Binary Star System: two stars that are graviationally bound together ([Read More](https://en.wikipedia.org/wiki/Binary_star)). <br>
We see it as one source of light because of the massive distance between us and the star; when you look at your LED light bulb you don't see each LED, but you see their light as one source.

<figure>
  <p align="center" width="100%">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/This_artist’s_impression_shows_the_strange_object_AR_Scorpii.jpg/800px-This_artist’s_impression_shows_the_strange_object_AR_Scorpii.jpg" alt="Artist's impression of the binary star system AR Scorpii" width="50%">
  <figcaption align="center">Figure 1: Artist's impression of the binary star system AR Scorpii. By M. Garlick/University of Warwick/ESO - <a href="http://www.eso.org/public/images/eso1627a/">ESO</a>, CC BY 4.0.</figcaption>
  </p>
</figure>


<br>The way to detect these is by using precise equipment that can detect the faintest of brightness changes over time (see the image below) caused by eclipses. If the lumnisoity of the star changes *periodically*, then it's a star system. Further carefull analysis of the lumnisotiy over time graph will tell us if it's a Binary Star System or if it's a bigger party of "fireballs."

<figure>
  <p align="center" width="100%">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Light_curve_of_binary_star_Kepler-16.jpg" alt="Light curve of binary star Kepler-16" width="50%">
  <figcaption align="center">Figure 2: Light curve of binary star Kepler-16. By NASA, 2013.</figcaption>
  </p>
  <br>
</figure>

# The Physics

> The used units are AU, M0, and days for L, M, and T, respectively. <br>
> All of the physics is calculated using linear algebra as defined in [`Vectors.py`](Vectors.py).


A Lagrangian method is used to calculate the position of each body based on the forces of gravity inflicted by the surrounding bodies' mass and its mass in discrete timesteps `dt`. 


First, the bodies are initialized with pre-determined `position`, `velocity`, and `mass` as in the class [`Body()`](Binary_System.py#L53). <br>
Then, the during each timestep the change in velocity done by the forces of gravity acting on each body by the others are calculated using the [`acc_due_to_gravity()`](Binary_System.py#L111):


1. The relative path between the two bodies `r` is [calculated](Binary_System.py#L112) by subtracting the position vectors of the bodies (numbered 1 & 2) using the following formula: <br>

```math
  \begin{bmatrix} 
\hat{r}_{21} = \frac{\vec{r}_1 - \vec{r}_2}{|\vec{r}_1 - \vec{r}_2|}
 \end{bmatrix}
```

2. Then, the norm, or magnitude, of the relative path is [calculated](Binary_System.py#L113) by 
```math
  \begin{bmatrix}
\frac{\vec{r}_{21}}{|\vec{r}_{21}|} 
 \end{bmatrix}
```

3. The norm of the force of gravity is then [evaluated](Binary_System.py#L115) using Newton's Law of Universal Gravitation: <br>
```math
  \begin{bmatrix}
\vec{F}_{12} = -G \frac{m_1 m_2}{r_{21}^2} \hat{r}_{21}
 \end{bmatrix}
```


4. Then, the force vector is [computed](Binary_System.py#L116) by normalizing the relative path and multiplying it by the norm of the force, since the direction of the forces is colinear with the relative path along the centers of the bodies, as shown in Figure 3.

<figure>
<p align="center" width="100%">
  <img src="https://i.ibb.co/6NF0fDw/Gravity-Baby.png" width="40%" alt="Representation of Newton's Law of Universal Gravitation">
  <figcaption align="center">Figure 3: Representation of Newton's Law of Universal Gravitation. By GeeksforGeeks, 2024.</figcaption>
  </p>
  <br>
</figure>

5. The acceleration due to gravity on a body is then [calculated](Binary_System.py#L120) by dividing it by the bodie's mass. 
    >The `reverse` variable inverts the direction of the force as it calculates it for both bodies.


6. Finally, the velocity of the body is computed by multiplying the calculated acceleration "`acc`" and the set timestep "`dt`". 
And the position is calculated in the same fashion by multiplying the computed velocity by the timestep, which is then mapped using the [`draw()`](Binary_System.py#L46) function in `matplotlib`.

<br><br>

**Made with ❤️ by [Geo](https://github.com/Geo-sudo). <br> Live Life!**