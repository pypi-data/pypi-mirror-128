##############################################
# Allow this code to be run from the examples
# directory without orbital installed.
from pathlib import Path
import sys

import matplotlib

examples_dir = Path(__file__).parent.resolve()
orbital_dir = examples_dir.parent
sys.path.append(str(orbital_dir))
##############################################

from numpy import radians
from scipy.constants import kilo

from Orbital.orbites import earth, KeplerianElements, Maneuver, plot, plot3d

# Create molniya orbit from period and eccentricity
from Orbital.orbites.constants import earth_sidereal_day
molniya = KeplerianElements.with_period(
    earth_sidereal_day / 2, e=0.741, i=radians(63.4), arg_pe=radians(270),
    body=earth)

# Simple circular orbit
orbit = KeplerianElements.with_altitude(1000 * kilo, body=earth)


## Simple plots
plot(molniya)

plot3d(molniya)


## Animation
plot(molniya, title='Molniya 1', animate=True)

plot3d(molniya, title='Molniya 2', animate=True)


## Maneuvers
man = Maneuver.hohmann_transfer_to_altitude(10000 * kilo)

plot(orbit, title='Maneuver 1', maneuver=man)

plot3d(orbit, title='Maneuver 2', maneuver=man)

import matplotlib.pyplot as plt
plt.show()
