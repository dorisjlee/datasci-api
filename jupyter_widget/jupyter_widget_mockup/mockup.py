import ipywidgets as widgets
from traitlets import Unicode, Int, List
import contextlib
import json
import uuid
import sys


@widgets.register
class Mockup(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('MockupView').tag(sync=True)
    _model_name = Unicode('MockupModel').tag(sync=True)
    _view_module = Unicode('jupyter-widget-mockup').tag(sync=True)
    _model_module = Unicode('jupyter-widget-mockup').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    _opt_source = Unicode('null').tag(sync=True)
    value = Unicode('null').tag(sync=True)
    numGraphs = Int(0).tag(sync=True)
    _graph_specs = List([]).tag(sync=True)
    
    def __init__(self, graphSpecs = None, spec=None, opt=None, **kwargs):
        super().__init__(**kwargs)
        self._opt_source = json.dumps(opt)
        graphs = []
        for i in range(0, len(graphSpecs)):
            #you cannot append to self._graph_specs, must fill out a list of graphs first
            #then set self._graph_specs to graphs
            graphs.append(json.dumps(graphSpecs[i]))
        self._graph_specs = graphs
        self.numGraphs = len(graphSpecs)
