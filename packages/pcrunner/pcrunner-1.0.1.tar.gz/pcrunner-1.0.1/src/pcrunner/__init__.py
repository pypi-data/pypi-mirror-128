# pcrunner/__init__.py
# vim: ai et ts=4 sw=4 sts=4 ft=python fileencoding=utf-8

"""
pcrunner
--------

Main package for Passive Check Runner
"""

# Save package version set by setuptools_scm to pcrunner.__version__
try:
    from importlib.metadata import version

except ImportError:
    # Python version < 3.8
    from pkg_resources import get_distribution

    __version__ = get_distribution('pcrunner').version

else:
    __version__ = version('pcrunner')
