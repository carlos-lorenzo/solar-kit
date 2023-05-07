from dataclasses import dataclass, field
from typing import Optional, List, Dict
import os

import matplotlib.pyplot as plt
import numpy as np

from solar_system import Solar_System
from planet import Planet


@dataclass
class Viewer:
    """
    Visualise (& more) a Solar_System object

    Args:
        system (Solar_System): A Solar_System object\n
        planets_to_use (List[str]): Select speficif planets (leave blank for all)\n
        compute_3D (bool): Show in 3D\n
        target_fps (int): Animation's fps\n
    """
    system: Solar_System
    planets_to_use: List[str] = field(default_factory=list)
    compute_3D: Optional[bool] = field(default= False)
    target_fps: Optional[int] = field(default=30)
    
    orbit_data: Dict[str, Dict[str, List[float]]] = field(init=False, default_factory=dict)
    chosen_planets: List[Planet] = field(init=False, default=list)
    
    
    fig: plt.figure = field(init=False)
    ax: plt.Axes = field(init=False)
    
    tmax: float = field(init=False)
    dt: float = field(init=False)
    t: float = field(init=False, default=0)
    
    
    def __post_init__(self):
        
        if not self.planets_to_use:
            self.planets_to_use = list(self.system.planets.keys())
            
        
        self.system.planets = dict(sorted(self.system.planets.items(), key=lambda planet: planet[1].P))
        
        self.chosen_planets = list(map(self.system.planets.get, self.planets_to_use))
        
        self.orbit_data = [planet.compute_orbit(compute_3D=self.compute_3D) for planet in self.chosen_planets]

    
        
        self.tmax = 4 * self.chosen_planets[-1].P
        self.dt = self.tmax/2500
        
    def __str__(self) -> str:
        return f"Planets: {self.system.__str__()}\n3D: {self.compute_3D}\nAnimation FPS: {self.target_fps}"
    
    
    
    def initialise_plotter(self) -> None:
        """
        Initalises the area where everythin will be drawn on. Call every time you want to draw a new model
        """
        
        if self.compute_3D:
            self.fig: plt.figure = plt.figure()
            self.ax: plt.Axes = self.fig.add_subplot(projection='3d')
            self.ax.view_init(None, 225)
          
        else:
            self.fig, self.ax = plt.subplots()
            
            #set aspect ratio to 1
            RATIO = 1.0
            x_left, x_right = self.ax.get_xlim()
            y_low, y_high = self.ax.get_ylim()
            self.ax.set_aspect(abs((x_right - x_left)/(y_low - y_high)) * RATIO)
    
    
    def add_grid(self):
        """
        Adds a grid
        """
        plt.grid()
    
    def add_legend(self):
        """
        Adds a legend
        """
        plt.legend()
    
    def lable_axes(self, x_lable: str = " x (AU)", y_lable: str = "y (AU)", z_lable: str = "z (AU)"):
        """
        Adds lables to axes. Call to override default axes' lables

        Args:
            x_lable (str, optional): x lable. Defaults to " x (AU)".
            y_lable (str, optional): y lable. Defaults to "y (AU)".
            z_lable (str, optional): z lable. Defaults to "z (AU)".
        """
        
        self.ax.set_xlabel(x_lable)
        self.ax.set_ylabel(y_lable)
        if self.compute_3D:
            self.ax.set_zlabel(z_lable)
    
    def show_plot(self):
        """
        Show drawn figure (calls plt.show())
        """
        plt.show()
    
    def save_figure(self, filename: str) -> None:
        """_summary_

        Args:
            filename (str): _description_
        """
        

        if not os.path.exists("figures"):
            os.mkdir("figures")
        
        plt.savefig(f"figures/{filename}", dpi=250)
        
          
    def plot_orbit(self, orbit_data: Dict[str, List[float]]) -> None:
        """
        Plots the orbit of a planet

        Args:
            orbit_data Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis, 
                    y: list of points on y-axis,
                    z: list of point on z-axis}\n
                    
            ax (plt.Axes): Axes to draw the orbit on\n
            
        Returns:
            plt.Axes: Axes with new orbit drawn on
                    
        """
        
        if "z" in orbit_data.keys(): # if self.compute_3D
            
            self.ax.plot(orbit_data["x"], orbit_data["y"], orbit_data["z"], label=f"{orbit_data['name']}'s orbit", c=orbit_data["c"])
        else:
            self.ax.plot(orbit_data["x"], orbit_data["y"], label=f"{orbit_data['name']}'s orbit", c=orbit_data["c"])
    
            
    def plot_planet(self, planet_data: Dict[str, float]) -> None:
        """
        Plots a planet on self.ax
        
        Args:
            planet_data Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis, 
                    y: list of points on y-axis,
                    z: list of point on z-axis}
                    
        """
        if "z" in planet_data.keys(): # if self.compute_3D
            
            self.ax.scatter(planet_data["x"], planet_data["y"], planet_data["z"], label=planet_data["name"], s=25, c=planet_data["c"])
        else:
            # Draw 2D
            self.ax.scatter(planet_data["x"], planet_data["y"], label=planet_data["name"], s=25, c=planet_data["c"])
   
             
    def plot_centre(self, name: str, colour: str) -> None:
        """
        Draw the centre of the model, can be a sun or a planet when using heliocentric model

        Args:
            name (str): Legend label
            colour (str): Plot colour
        """

        if self.compute_3D:
            self.ax.scatter(0, 0, 0, s=100, label=name, c=colour)
            
        else:
            self.ax.scatter(0, 0, s=100, label=name, c=colour)
      

    
    def third_law(self):
        """
        Proves Kepler's third law
        """
        
        
        x = [planet.a**3 for planet in  self.system.planets.values()]
        y = [planet.P**2 for planet in  self.system.planets.values()]
        

        plt.scatter(x, y, c="#4F81BD", marker="D", label="Kepler's third law")
        plt.plot(x, y, c="r", label="Linear (Kepler's third law)")


        plt.title("Kepler's third law")
        self.lable_axes(x_lable="a (AU)", y_lable="P (Yr)")
        
        
        
    def system_orbits(self) -> None:
        """
        Plot the orbits of the selected planets
        """
        self.plot_centre(name="Sun", colour="y")
        
        for planet_orbit_data in self.orbit_data:
            self.plot_orbit(orbit_data=planet_orbit_data)  
        
        plt.title("Planet orbits")
        self.lable_axes()
        
            
        
            
    def animate_orbits(self) -> None:
        """
        Animate the orbits of the selected planets
        """
        
        while self.t < self.tmax:
            self.plot_centre(name="Sun", colour="y")
            
            for planet_orbit_data in self.orbit_data:
                self.plot_orbit(orbit_data=planet_orbit_data)    

            planet_data = [planet.compute_position(compute_3D=self.compute_3D, t=self.t) for planet in self.chosen_planets]
            for planet_planet_data in planet_data:
                self.plot_planet(planet_data=planet_planet_data)

            self.t += self.dt
            
            plt.title("Planet orbits")
            self.lable_axes()
            
            plt.legend()
            plt.grid()
            
            plt.pause(1/self.target_fps)
            plt.cla()
    
    
    def spinograph(self) -> None:
        """
        Draw a spinograph with the chosen planets        
        """
        
        self.tmax *= 10
        self.dt = self.tmax / 1234
        
        
        while self.t < self.tmax:
            planet_data = [planet.compute_position(compute_3D=self.compute_3D, t=self.t) for planet in self.chosen_planets]
            
            x = [data["x"] for data in planet_data]
            y = [data["y"] for data in planet_data]
            
            if self.compute_3D:
                z = [data["z"] for data in planet_data]
                self.ax.plot(x, y, z, c="k")
            else:
                self.ax.plot(x, y, c="k")
            
            
            self.t += self.dt
        
        for planet_orbit_data in self.orbit_data:
            self.plot_orbit(orbit_data=planet_orbit_data)
        
        
        plt.title(f"{self.system.system_name}'s spinograph")
        self.lable_axes()
        
        
    def animate_spinograph(self) -> None:
        """
        Animate the drawing of a spinograph with the chosen planets            
        """
        
        self.tmax *= 10
        self.dt = self.tmax / 1234
        
        
        while self.t < self.tmax:
            planet_data = [planet.compute_position(compute_3D=self.compute_3D, t=self.t) for planet in self.chosen_planets]
            
            x = [data["x"] for data in planet_data]
            y = [data["y"] for data in planet_data]
            
            if self.compute_3D:
                z = [data["z"] for data in planet_data]
                self.ax.plot(x, y, z, c="k")
            else:
                self.ax.plot(x, y, c="k")
            
            self.t += self.dt
        
            for planet_orbit_data in self.orbit_data:
                self.plot_orbit(orbit_data=planet_orbit_data)
        
            
            plt.pause(1/self.target_fps)
        
        plt.title(f"{self.system.system_name}'s spinograph")
        self.lable_axes()
        
              
    def heliocentric_model(self, origin_planet_name: str) -> None:
        """
        Compute the heliocentric using origin_planet_name as centre

        Args:
            origin_planet_name (str): Name of centre planet (from planets in self.system.planets).
        """
        
        num_points = 3000
        
        self.tmax *= 20
        self.dt = self.tmax / num_points
        
        
        
        x = np.zeros((len(self.chosen_planets), num_points))
        y = np.zeros((len(self.chosen_planets), num_points))

        if self.compute_3D:
            z = np.zeros((len(self.chosen_planets), num_points))
        
        for i in range(num_points):
            origin_planet_data = self.system.planets[origin_planet_name].compute_position(compute_3D=self.compute_3D, t=self.t)
            
            planets_data = [planet.compute_position(compute_3D=self.compute_3D, t=self.t) for planet in self.chosen_planets]
            
            relative_planets_data = [self.system.compute_relative_vector(origin_planet_data=origin_planet_data, target_planet_data=target_planet_data) for target_planet_data in planets_data]
            
            # Improvement: compute all positions and then plot
            for j, planet_data in enumerate(relative_planets_data):
                x[j][i] = planet_data["x"]
                y[j][i] = planet_data["y"]
                
                if self.compute_3D:
                    z[j][i] = planet_data["z"]
                    
            self.t += self.dt
        

        
        if self.compute_3D:
            for planet_x, planet_y, planet_z, planet in zip(x, y, z, self.chosen_planets):
                self.ax.plot(planet_x, planet_y, planet_z, label=planet.name, c=planet.colour)
                
            
                
        else:
            for planet_x, planet_y, planet in zip(x, y, self.chosen_planets):
                self.ax.plot(planet_x, planet_y, label=planet.name, c=planet.colour)
            

        self.plot_centre(name=origin_planet_name, colour=origin_planet_data["c"])

        
        plt.title(f"{origin_planet_name}'s heliocentric model")
        self.lable_axes()
        
                    
    