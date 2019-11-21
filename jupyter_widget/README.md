jupyter-widget-mockup
===============================

A Custom Jupyter Widget Library

Installation
------------

To install use pip:

    $ pip install jupyter_widget_mockup
    $ jupyter nbextension enable --py --sys-prefix jupyter_widget_mockup

To install for jupyterlab

    $ jupyter labextension install jupyter_widget_mockup

For a development installation (requires npm),

    $ git clone https://github.com//jupyter-widget-mockup.git
    $ cd jupyter-widget-mockup
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix jupyter_widget_mockup
    $ jupyter nbextension enable --py --sys-prefix jupyter_widget_mockup
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This take a minute or so to get started, but then allows you to hot-reload your javascript extension.
To see a change, save your javascript, watch the terminal for an update.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

