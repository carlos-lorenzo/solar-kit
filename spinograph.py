from dataclasses import dataclass
from typing import Dict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Objects
@dataclass
class Planet:
    """
    Holds planet data
    
    Args:
        Body(str):  Celestial's body name 
        m (float): Mass in Earth masses
        a (float): Semi-major axis (AU)
        ecc (float): Orbit eccentricity
        beta (float): Ortbital inclinaiton (deg)
        R (float): Radius (Earth radii)
        trot (float): Rotational period (days)
        P (float): Orbital period (years)
        c (str): colour in plot
    """
    
    name: str
    m: float
    a: float
    ecc: float
    beta: float
    R: float
    trot: float
    P: float
    c: str
    
# Functions
def create_planet(planet_data: pd.Series(object)) -> Planet:
    new_planet: Planet = Planet(name=planet_data["Body"],
                                m=planet_data["m"],
                                a=planet_data["a"],
                                ecc=planet_data["ecc"],
                                beta=planet_data["beta"],
                                R=planet_data["R"],
                                trot=planet_data["trot"],
                                P=planet_data["P"],
                                c=planet_data["colour"])
    return new_planet

def compute_orbit(planet: Planet, compute_3D: bool) -> Dict:
    """
    Compute the points for a planet's orbit

    Args:
        planet (Planet): Planet object
        compute_3D (bool): Compute the orbit using beta (inclination)

    Returns:
        Dict: {name: planet name, 
                x: list of points on x-axis., 
                y: list of points on y-axis,
                z: list of point on z-axis}
                
        (z only included if compute_3D)
    """
    
    
    theta: np.array([]) = np.linspace(0, 2*np.pi, 1000)
    
    # 2D Orbits
    r: np.array([]) = planet.a * (1 - planet.ecc**2) / (1 - planet.ecc * np.cos(theta))
    x: np.array([]) = r * np.cos(theta)
    y: np.array([]) = r * np.sin(theta)
    
    
    if compute_3D:
        # Beta to radians
        beta: float = planet.beta*np.pi/180
        
        # 3D orbits
        xx: np.array([]) = x * np.cos(beta)
        yy: np.array([]) = y
        zz: np.array([]) = x * np.sin(beta)
        
        return {"name": planet.name,
                "x": xx,
                "y": yy,
                "z": zz} 
    
    else:
        return {"name": planet.name,
                "x": x,
                "y": y}
        
def compute_planet(planet: Planet, compute_3D: bool, t: float) -> Dict:
    """
    Compute the points the planet will be in 

    Args:
        planet (Planet): Planet object
        compute_3D (bool): Compute the orbit using beta (inclination)
        t (float): The current time in the simulation

    Returns:
        Dict: {name: planet name, 
                x: list of points on x-axis., 
                y: list of points on y-axis,
                z: list of point on z-axis}
                
        (z only included if compute_3D)
    """
    
    # Planets
    planet_theta: float = (2*np.pi*t)/planet.P
    r: np.array([]) = planet.a * (1 - planet.ecc**2) / (1 - planet.ecc * np.cos(planet_theta))
    x: np.array([]) = r * np.cos(planet_theta)
    y : np.array([]) = r * np.sin(planet_theta)
    
    if compute_3D:
        # Beta to radians
        beta: float = planet.beta*np.pi/180
        
        # 3D orbits
        xx: np.array([]) = x * np.cos(beta)
        yy: np.array([]) = y
        zz: np.array([]) = x * np.sin(beta)
        
        return {"name": planet.name,
                "x": xx,
                "y": yy,
                "z": zz}
        
    else:
        return {"name": planet.name,
                "x": x,
                "y": y}

def plot_orbit(orbit_data: Dict, ax: plt.Axes, colour: str) -> plt.Axes:
    """
    Plots the orbit of a planet

    Args:
        orbit_data (Dict): Dictionary containing orbit data (planet name, x, y, z)
        ax (plt.Axes): Axes to draw the orbit on
        
    Returns:
        plt.Axes: Axes with new orbit drawn on
                
    """
    if "z" in orbit_data.keys():
        # Draw 3D
        ax.plot(orbit_data["x"], orbit_data["y"], orbit_data["z"], label=f"{orbit_data['name']}'s orbit", linewidth=5, c=colour)
    else:
        # Draw 2D
        ax.plot(orbit_data["x"], orbit_data["y"], label=f"{orbit_data['name']}'s orbit", linewidth=5, c=colour)
        
    return ax
    
def plot_planet(planet_data: Dict, ax: plt.Axes, colour: str) -> plt.Axes:
    """
    Plots a planet

    Args:
        orbit_data (Dict): Dictionary containing planet data (planet name, x, y, z)
        ax (plt.Axes): Axes to draw the orbit on
        
    Returns:
        plt.Axes: Axes with new planet drawn on
                
    """
    if "z" in planet_data.keys():
        # Draw 3D
        ax.scatter(planet_data["x"], planet_data["y"], planet_data["z"], label=planet_data["name"], s=25, c=colour)
    else:
        # Draw 2D
        ax.scatter(planet_data["x"], planet_data["y"], label=planet_data["name"], s=25, c=colour)
        
    return ax 


# Main
df = pd.read_csv("Personal\planet_data.csv")

PLANET_NAME_TO_INDEX: Dict[str, int] = {"Sun": 0,
                              "Mercury": 1,
                              "Venus": 2,
                              "Earth": 3,
                              "Mars": 4,
                              "Jupiter": 5,
                              "Saturn": 6,
                              "Uranus": 7,
                              "Neptune":8,
                              "Pluto": 9}

# Settings
PLANETS_TO_PLOT: np.array([str]) = ["Venus", "Earth"]
COMPUTE_3D: bool = False
ANIM: bool = False
TARGET_FPS: int = 30 # Can be lower if system not powerful enough
N_ORBITS = 10

planet_indexi: np.array([int]) = np.sort(np.array([PLANET_NAME_TO_INDEX[planet_name] for planet_name in PLANETS_TO_PLOT]))

planets: np.array([Planet]) = np.array([create_planet(planet_data=planet_data) for i, planet_data in df.iloc[planet_indexi].iterrows()])

tmax: float = planets[-1].P * N_ORBITS
dt: float = tmax / 1234
t: int = 0


if COMPUTE_3D:
    fig: plt.figure = plt.figure()
    ax: plt.Axes = fig.add_subplot(projection='3d')
    ax.view_init(None, 225)
    ax.set_zlabel('z (AU)')
          
else:
    fix, ax = plt.subplots()
    
    #set aspect ratio to 1
    RATIO = 1.0
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * RATIO)


plt.title(f"{' & '.join(PLANETS_TO_PLOT)} Spinograph")
plt.xlabel("x (AU)")
plt.ylabel("y (AU)")

   
# For efficiency, to stop it from computing every iteration
orbit_data  = [compute_orbit(planet=planet, compute_3D=COMPUTE_3D) for planet in planets]

if ANIM:
    # Plot planets
    while t < tmax:
        planet_data = [compute_planet(planet=planet, compute_3D=COMPUTE_3D, t=t) for planet in planets]
        
        x = [planet_planet_data["x"] for planet_planet_data in planet_data]
        y = [planet_planet_data["y"] for planet_planet_data in planet_data]
        
        if COMPUTE_3D:
            z = [planet_planet_data["z"] for planet_planet_data in planet_data]
            ax.plot(x, y, z, c="k")
        else:
            ax.plot(x, y, c="k")
            
        t += dt

        # Plot orbits
        
        for i, planet_orbit_data in enumerate(orbit_data):
            ax = plot_orbit(orbit_data=planet_orbit_data, ax=ax, colour=planets[i].c)

        plt.pause(1/TARGET_FPS)
        
else:

    # Plot planets
    while t < tmax:
        planet_data = [compute_planet(planet=planet, compute_3D=COMPUTE_3D, t=t) for planet in planets]
    
        x = [planet_planet_data["x"] for planet_planet_data in planet_data]
        y = [planet_planet_data["y"] for planet_planet_data in planet_data]
        
        if COMPUTE_3D:
            z = [planet_planet_data["z"] for planet_planet_data in planet_data]
            ax.plot(x, y, z, c="k")
        else:
            ax.plot(x, y, c="k")
            
        t += dt

    # Plot orbits
    for i, planet_orbit_data in enumerate(orbit_data):
        ax = plot_orbit(orbit_data=planet_orbit_data, ax=ax, colour=planets[i].c)

        
    plt.legend()
    plt.show()