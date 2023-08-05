from .longitudinal_profiles import LongitudinalProfileCoasting
from .longitudinal_profiles import LongitudinalProfileQGaussian

from .fieldmaps import TriLinearInterpolatedFieldMap
from .fieldmaps import BiGaussianFieldMap, mean_and_std

from .solvers.fftsolvers import FFTSolver3D

from .beam_elements.spacecharge import SpaceCharge3D, SpaceChargeBiGaussian
from .beam_elements.beambeam import BeamBeamBiGaussian2D
from .beam_elements.beambeam3d import BeamBeamBiGaussian3D

from .general import _pkg_root
from .config_tools import replace_spacecharge_with_quasi_frozen
from .config_tools import replace_spacecharge_with_PIC
from .config_tools import configure_orbit_dependent_parameters_for_bb

import xtrack as _xt

element_classes = tuple(
    v for v in globals().values()
    if isinstance(v, type) and issubclass(v, _xt.BeamElement)
)
del _xt
