
# BMO uses pathlib2 in python 2, in preparation to become python3-only.
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

import yaml

# Inits the logging system. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(name).
from .utils import get_logger

# Monkeypatches formatwarning and error handling

import click
import warnings

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):

    basename = pathlib.Path(filename).name
    category_colour = click.style('[{}]'.format(category.__name__), fg='yellow')

    return '{}: {} ({}:{})\n'.format(category_colour, message, basename, lineno)


warnings.formatwarning = warning_on_one_line

warnings.filterwarnings(
    'ignore', 'Matplotlib is building the font cache using fc-list. This may take a moment.')


# Loads config
try:
    config = yaml.load(open(str(pathlib.Path(__file__).parent / 'etc/alerts.cfg')), 
                        Loader=yaml.FullLoader)

    alertActions = yaml.load(open(str(pathlib.Path(__file__).parent / 'etc/alertActions.yml')), 
                        Loader=yaml.UnsafeLoader)
except AttributeError:
    # using pyyaml < 5, enforce old behavior
    config = yaml.load(open(str(pathlib.Path(__file__).parent / 'etc/alerts.cfg')))

    alertActions = yaml.load(open(str(pathlib.Path(__file__).parent / 'etc/alertActions.yml')))

__version__ = '0.0.1'
