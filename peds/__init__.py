from pkg_resources import get_distribution

__version__ = get_distribution('peds').version

from peds.person import Person
from peds.family import Family
from peds.ped import open_ped
from peds.utils import get_trios, get_probands
