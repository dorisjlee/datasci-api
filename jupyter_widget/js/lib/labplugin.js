var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'jupyter-widget-mockup',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'jupyter-widget-mockup',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

