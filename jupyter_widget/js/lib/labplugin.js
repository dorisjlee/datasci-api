var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'widgetDisplay',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'widgetDisplay',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

