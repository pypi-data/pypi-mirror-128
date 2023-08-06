#!/usr/bin/env python

from pkg_resources import get_distribution
from multiqc.utils import config

__version__ = get_distribution("multiqc_cgs").version
config.multiqc_cgs_version = __version__
