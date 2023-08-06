#!/usr/bin/env python
"""
hook that make it possible to modify general statistics table
"""

from setuptools import setup, find_packages

version = '0.2'

setup(
    name = 'multiqc_cgs',
    version = version,
    author = 'Patrik Smeds',
    author_email = 'patrik.smeds@scilifelab.uu.se',
    description = "make it possible to add more information to general statisticsn",
    long_description = __doc__,
    keywords = 'bioinformatics',
    url = '',
    download_url = '',
    license = 'GPL3',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'multiqc'
    ],
    entry_points = {
        'multiqc.hooks.v1': [
            'after_modules = multiqc_cgs.hooks:after_modules'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
