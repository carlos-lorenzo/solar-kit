from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np
from scipy.interpolate import interp1d

from solarkit.planet import Planet


@dataclass
class Solar_System:
    """
    Solar system class

    Holds the planet data
    """
    system_name: Optional[str] = field(default="Solar System")
    planets: Dict[str, Planet] = field(init=False, default_factory=dict)
    
    
    def __str__(self):
        return f"{self.system_name}({', '.join([planet_name for planet_name in self.planets])})"
    
    
    def add(self, planet: Planet, force_add: bool = False) -> None:
        """
        Add a planet to the system

        Args:
            planet (Planet): A Planet object\n
            force_add (bool): Ignore the constraint
        
        The planet's .a property must be greater than 0 for it to be added
        """
        
        if planet.a > 0 or force_add:
            self.planets[planet.name] = planet
            
    def compute_relative_vector(self, origin_planet_data: Dict[str, float], target_planet_data: Dict[str, float]) -> Dict[str, float]:
        """
        Comput the vector between two planets

        Args:
            origin_planet_data Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis, 
                    y: list of points on y-axis,
                    z: list of point on z-axis}: The position of the planet to be used as a centre\n
                    
            target_planet_data Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis., 
                    y: list of points on y-axis,
                    z: list of point on z-axis}: The position of the planet you want to calculate the offset with respect to the planet at the origin\n
            
            
        Returns:
            Dict: {name (str): planet name, 
                    c (str): colour,
                    x (float): list of points on x-axis., 
                    y (float): list of points on y-axis,
                    z (float): list of point on z-axis}
        """
        
        if "z" in origin_planet_data.keys() and "z" in target_planet_data.keys():
            return {"name": target_planet_data["name"],
                    "c": target_planet_data["c"],
                    "x": (target_planet_data["x"] - origin_planet_data["x"]),
                    "y": (target_planet_data["y"] - origin_planet_data["y"]),
                    "z": (target_planet_data["z"] - origin_planet_data["z"])}
        else:
            return {"name": target_planet_data["name"],
                    "c": target_planet_data["c"],
                    "x": (target_planet_data["x"] - origin_planet_data["x"]),
                    "y": (target_planet_data["y"] - origin_planet_data["y"])} 
    
    
    def compute_angle_vs_time(self, t: np.ndarray, P: float, ecc: float, theta0: float) -> np.ndarray:
        """
        Calculate the polar angle as a function of time using Simpson's rule.
        
        (Translated from matlab to python from: https://www.dropbox.com/s/dot9l0igz7x1ija/Comp%20Challenge%20%202023%20Solar%20System%20orbits%20-%20presentation.pdf?dl=0)

        Args:
            t (np.ndarray): Array of time values.
            P (float): Orbital period in years.
            ecc (float): Eccentricity of the orbit.
            theta0 (float): Initial polar angle in radians.

        Returns:
            np.ndarray: Array of polar angles corresponding to the input time values in radians.
        """
        
        # Angle step for Simpson's rule
        dtheta = 1 / 1000

        # Number of orbits
        N = np.ceil(t[-1] / P)

        # Define array of polar angles for orbits
        theta = np.arange(theta0, 2 * np.pi * N + theta0 + dtheta, dtheta)

        # Evaluate integrand of time integral
        f = (1 - ecc * np.cos(theta)) ** -2

        # Define Simpson's rule coefficients 
        L = len(theta)
        isodd = np.remainder(np.arange(1, L - 1), 2)
        isodd[isodd == 1] = 4
        isodd[isodd == 0] = 2
        c = np.concatenate(([1], isodd, [1]))

        # Calculate array of times
        tt = P * (1 - ecc ** 2) ** (3 / 2) * (1 / (2 * np.pi)) * dtheta * (1 / 3) * np.cumsum(c * f)

        # Interpolate the polar angles for the eccentric orbit at the circular orbit times
        theta_interp = interp1d(tt, theta, kind='cubic')
        theta_result = theta_interp(t)

        return theta_result
            
