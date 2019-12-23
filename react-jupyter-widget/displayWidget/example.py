#!/usr/bin/env python
# coding: utf-8
from ipywidgets import DOMWidget
from traitlets import Unicode, Int, List
from ._frontend import module_name, module_version
import json

class ExampleWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('JupyterWidgetView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)
    selected_graphID = List([]).tag(sync=True)
    _graph_specs = List([]).tag(sync=True)
    # def __init__(self, graphSpecs = None, spec=None, opt=None, **kwargs):
    #     super().__init__(**kwargs)
    #     self._opt_source = json.dumps(opt)
    #     graphs = []
    #     for i in range(0, len(graphSpecs)):
    #         #you cannot append to self._graph_specs, must fill out a list of graphs first
    #         #then set self._graph_specs to graphs
    #         graphs.append(json.dumps(graphSpecs[i]))
    #     self.selected_graphID = []
    #     self._graph_specs = graphs
    #     self.numGraphs = len(graphSpecs)
