# -*- coding: utf-8 -*-

from distutils.core import setup

import annotation_exporter

NAME = 'annotation_exporter'
VERSION = annotation_exporter.__version__
URL = 'https://github.com/Neubias-WG5/AnnotationExporter'
AUTHOR = "Romain Mormont"
AUTHOR_EMAIL = "r.mormont[_at_]uliege.be"
DESCRIPTION = 'Library containing annotation export functions'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering',
    'Topic :: Utilities'
]

if __name__ == '__main__':
    setup(name=NAME,
          version=VERSION,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          url=URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          classifiers=CLASSIFIERS,
          platforms='any',
          install_requires=['scikit-image', 'numpy', 'opencv-python-headless', 'shapely'],
          packages=['annotation_exporter'])