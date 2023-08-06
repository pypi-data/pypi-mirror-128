__author__ = "Team Atlas"
__email__ = 'team-atlas@esciencecenter.nl'

from .__version__ import __version__

import logging

from .configure import configure
from .stac_io import configure_stac_io
from .filesystem import configure_filesystem

logging.getLogger(__name__).addHandler(logging.NullHandler())

fs = None
stac_io = None
