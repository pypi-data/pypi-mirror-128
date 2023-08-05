##############################################
# Allow this code to be run from the examples
# directory without orbital installed.
from pathlib import Path
import sys

examples_dir = Path(__file__).parent.resolve()
orbital_dir = examples_dir.parent
sys.path.append(str(orbital_dir))
##############################################

from numpy import radians
from scipy.constants import kilo

from Orbital.orbites import earth, KeplerianElements, plot


# Create circular orbit with 90 minute period
orbit1 = KeplerianElements.with_period(90 * 60, body=earth)
plot(orbit1, title='Orbit 1')


# Create molniya orbit from period and eccentricity
from Orbital.orbites.constants import earth_sidereal_day
molniya1 = KeplerianElements.with_period(
    earth_sidereal_day / 2, e=0.741, i=radians(63.4), arg_pe=radians(270),
    body=earth)

plot(molniya1, title='Molniya 1')


# Create circular orbit at altitude 300 km
orbit2 = KeplerianElements.with_altitude(300 * kilo, body=earth)
plot(orbit2, title='Orbit 2')


# Create molniya orbit by specifying altitude at perigee.
# This works because M0=0 (perigee).
molniya2 = KeplerianElements.with_altitude(
    508 * kilo, e=0.741, i=radians(63.4), arg_pe=radians(270), body=earth)

plot(molniya2, title='Molniya 2')


# Create orbit by specifying apside altitudes.
# Note that order of apsides doesn't matter, smallest is used as pericenter
orbit3 = KeplerianElements.with_apside_altitudes(
    1000 * kilo, 400 * kilo, body=earth)

plot(orbit3, title='Orbit 3')


# Create molniya orbit using apside altitudes
molniya3 = KeplerianElements.with_apside_altitudes(
    39873 * kilo, 508 * kilo, i=radians(63.4), arg_pe=radians(270), body=earth)

plot(molniya3, title='Molniya 3')


# Create orbit using apside radii
orbit4 = KeplerianElements.with_apside_radii(7000 * kilo, 8400 * kilo, body=earth)
plot(orbit4, title='Orbit 4')


import matplotlib.pyplot as plt
plt.show()