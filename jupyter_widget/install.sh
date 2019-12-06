# Instructions from https://github.com/ocoudray/first-widget
cd js/
npm install
cd ..
pip install -e .
jupyter nbextension install --py --symlink --sys-prefix jupyter_widget_mockup
jupyter nbextension enable --py --sys-prefix jupyter_widget_mockup
