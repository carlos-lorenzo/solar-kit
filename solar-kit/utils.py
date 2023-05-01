import pandas as pd

from planet import Planet
from solar_system import Solar_System


def create_planet(planet_data: pd.Series(object)) -> Planet:
    
    """
    Creates a planet from a pd.Series(object) containing the required data (reference Planet object parameters)

    Returns:
        Planet: A Planet object using planet_data
    """
    
    new_planet: Planet = Planet(name=planet_data["name"],
                                m=planet_data["m"],
                                a=planet_data["a"],
                                ecc=planet_data["ecc"],
                                beta=planet_data["beta"],
                                R=planet_data["R"],
                                trot=planet_data["trot"],
                                P=planet_data["P"])
    
    return new_planet

def load_system(path: str):
    """
    Creates a system from a csv. Each row contains the required data (reference Planet object parameters)

    Args:
        path (str): The path to a .csv file

    Returns:
        Solar_System: Solar system object
    """
    
    system_data = pd.read_csv(path)
    system = Solar_System()
    
    for i, planet_data in system_data.iterrows():
        # If a is smaller than 0, simulation would break trying to draw it. It is a sun, it will be manually added during the simulation
        
        system.add(create_planet(planet_data=planet_data))
        
    return system