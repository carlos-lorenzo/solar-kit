from dataclasses import dataclass, field
from typing import Dict, List


import numpy as np


# Objects
@dataclass
class Planet:
    """
    Holds planet data
    
    Args:
        name(str):  Planet's body name\n
        m (float): Mass in Earth masses\n
        a (float): Semi-major axis (AU)\n
        ecc (float): Orbit eccentricity\n
        beta (float): Ortbital inclinaiton (deg)\n
        R (float): Radius (Earth radii)\n
        trot (float): Rotational period (days)\n
        P (float): Orbital period (years)\n
        color (str): The colour it will have when viewing
    """
    
    name: str
    m: float
    a: float
    ecc: float
    beta: float
    R: float
    trot: float
    P: float
    colour: str = field(default="k")    
    
    def __str__(self) -> str:
        return self.name
    
    
    def compute_orbit(self, compute_3D: bool) -> Dict[str, List[float]]:
        """
        Compute the points for its orbit

        Args:
            compute_3D (bool): Compute the orbit using beta (inclination)

        Returns:
            Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis., 
                    y: list of points on y-axis,
                    z: list of point on z-axis}
                    
            (z only included if compute_3D)
        """
        
        
        theta = np.linspace(0, 2*np.pi, 1000)
        
        # 2D Orbits
        r = self.a * (1 - self.ecc**2) / (1 - self.ecc * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        
        if compute_3D:
            # Beta to radians
            beta: float = self.beta*np.pi/180
            
            # 3D orbits
            xx = x * np.cos(beta)
            yy = y
            zz = x * np.sin(beta)
            
            return {"name": self.name,
                    "c": self.colour,
                    "x": xx,
                    "y": yy,
                    "z": zz} 
        
        else:
            return {"name": self.name,
                    "c": self.colour,
                    "x": x,
                    "y": y}
            
            
    def compute_position(self, compute_3D: bool, t: float) -> Dict[str, float]:
        """
        Computes the point the planet will be in at a given time (t)

        Args:
            compute_3D (bool): Compute the orbit using beta (inclination)\n
            t (float): The time to simulate\n

        Returns:
            Dict: {name: planet name,
                    c: colour,
                    x: list of points on x-axis, 
                    y: list of points on y-axis,
                    z: list of point on z-axis}
                    
            (z only included if compute_3D)
        """
        
        # Planets
        planet_theta: float = (2*np.pi*t)/self.P
        r = self.a * (1 - self.ecc**2) / (1 - self.ecc * np.cos(planet_theta))
        x = r * np.cos(planet_theta)
        y = r * np.sin(planet_theta)
        
        if compute_3D:
            # Beta to radians
            beta: float = self.beta*np.pi/180
            
            # 3D orbits
            xx = x * np.cos(beta)
            yy = y
            zz = x * np.sin(beta)
            
            return {"name": self.name,
                    "c": self.colour,
                    "x": xx,
                    "y": yy,
                    "z": zz}
            
        else:
            return {"name": self.name,
                    "c": self.colour,
                    "x": x,
                    "y": y}
            

