from viewer import Viewer
from utils import load_system

system = load_system(path="solarkit\planet_data.csv")
system_viewer = Viewer(system=system, planets_to_use=["Mercury", "Venus"])
system_viewer.animate_orbits(save_anim=True)
