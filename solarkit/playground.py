from viewer import Viewer
from utils import load_system

system = load_system(path="solarkit\planet_data.csv")
system_viewer = Viewer(system=system, planets_to_use=["Mars", "Venus"], compute_3D=False)
system_viewer.heliocentric_model(origin_planet_name="Earth", save_figure=True)
