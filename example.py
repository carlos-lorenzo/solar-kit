from solarkit import utils
from solarkit.viewer import Viewer

# Create a solar system using some data (sample data available on repository)
system = utils.load_system_from_csv(path="planet_data.csv")

# Create the viewer
system_viewer = Viewer(system=system)

# Create the figure where everything will be drawn on
system_viewer.initialise_plotter()

# Call any method
system_viewer.system_orbits()

# Add legend/grid/axes (optional)
system_viewer.add_grid()
system_viewer.add_legend()
system_viewer.lable_axes()

# Save figure to image
system_viewer.save_figure(path="Figures/", filename="orbits")

# Witness your creation!
system_viewer.show_plot()



