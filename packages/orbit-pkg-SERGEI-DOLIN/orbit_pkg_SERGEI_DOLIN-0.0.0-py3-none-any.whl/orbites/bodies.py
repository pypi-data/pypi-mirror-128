from __future__ import absolute_import, division, print_function

from represent import RepresentationMixin

from . import constants as oc

__all__ = [
    'earth',
# etc.
]


class Body(RepresentationMixin, object):
    r"""Reference body for a Keplerian orbit.
    :param float mass: Mass (:math:`m`) [kg]
    :param float mu: Standard gravitational parameter (:math:`\mu`) [m\ :sup:`3`\ ·s\ :sup:`-2`]
    :param float mean_radius: Mean radius (:math:`r_\text{mean}`) [m]
    :param float equatorial_radius: Equatorial radius (:math:`r_\text{equat}`) [m]
    :param float polar_radius: Polar radius (:math:`r_\text{polar}`) [m]
    :param apoapsis_names: Specific apoapsis name(s) for body. E.g. `apogee` for earth.
    :type apoapsis_names: String, or list of strings.
    :param periapsis_names: Specific periapsis name(s) for body.
    :type apoapsis_names: String, or list of strings.
    :param plot_color: Color understood by Matplotlib, e.g. '#FF0000' or 'r'
    """
    def __init__(self, mass, mu, mean_radius, equatorial_radius, polar_radius, apoapsis_names=None, periapsis_names=None, plot_color=None):
        self.mass = mass
        self.mu = mu
        self.mean_radius = mean_radius
        self.equatorial_radius = equatorial_radius
        self.polar_radius = polar_radius
        self.apoapsis_names = apoapsis_names
        self.periapsis_names = periapsis_names
        self.plot_color = plot_color

        super(Body, self).__init__()

    @property
    def apoapsis_names(self):
        return self._apoapsis_names

    @apoapsis_names.setter
    def apoapsis_names(self, value):
        if isinstance(value, str):
            self._apoapsis_names = [value]
        elif value is None:
            self._apoapsis_names = []
        else:
            self._apoapsis_names = value

    @property
    def periapsis_names(self):
        return self._periapsis_names

    @periapsis_names.setter
    def periapsis_names(self, value):
        if isinstance(value, str):
            self._periapsis_names = [value]
        elif value is None:
            self._periapsis_names = []
        else:
            self._periapsis_names = value

    def __repr__(self):
        # Intercept __repr__ from RepresentationMixin to
        # use orbital.bodies.<planet> for the defaults.
        if __name__ == 'orbital.bodies':
            for name, instance in _defaults.items():
                if self is instance:
                    return __name__ + '.' + name
        return super(Body, self).__repr__()

    def _repr_pretty_(self, p, cycle):
        # Intercept _repr_pretty_ from RepresentationMixin to
        # use orbital.bodies.<planet> for the defaults.
        if __name__ == 'orbital.bodies':
            for name, instance in _defaults.items():
                if self is instance:
                    p.text(__name__ + '.' + name)
                    return

        super(Body, self)._repr_pretty_(p, cycle)

earth = Body(
    mass=oc.earth_mass,
    mu=oc.earth_mu,
    mean_radius=oc.earth_radius_mean,
    equatorial_radius=oc.earth_radius_equatorial,
    polar_radius=oc.earth_radius_polar,
    apoapsis_names='apogee',
    periapsis_names='perigee',
    plot_color='#4e82ff'
)

_defaults = {
    'earth': earth}