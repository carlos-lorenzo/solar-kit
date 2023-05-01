from dataclasses import dataclass, field
from typing import Dict, Optional

from planet import Planet


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
    
    
    def add(self, planet: Planet) -> None:
        """
        Add a planet to the system

        Args:
            planet (Planet): A Planet object
        
        The planet's .a property must be greater than 0 for it to be added
        """
        
        if planet.a > 0:
            self.planets[planet.name] = planet
