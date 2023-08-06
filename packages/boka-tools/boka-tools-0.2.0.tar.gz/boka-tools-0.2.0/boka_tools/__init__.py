from .utils.sql import server_connect
from . import soil_investigation
from . import planning

from pkg_resources import get_distribution

__version__ = get_distribution('boka_tools').version
