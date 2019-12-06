from ._version import version_info, __version__

from .mockup import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-widget-mockup',
        'require': 'jupyter-widget-mockup/extension'
    }]
