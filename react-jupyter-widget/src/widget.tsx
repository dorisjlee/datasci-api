import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'

import * as React from "react";
import * as ReactDOM from "react-dom";

import ChartGalleryComponent from './chartGallery';

export class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      value : 'Hello World'
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'JupyterWidgetView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  
}

export class JupyterWidgetView extends DOMWidgetView {
  initialize(){    
    let view = this;

    class ReactWidget extends React.Component<JupyterWidgetView,{value:any,graphSpec:any[],data:any[]}> {
      constructor(props:any){
        super(props);
        console.log("view:",props);
        this.state = {
          value: props.model.get("value"),
          graphSpec: view.model.get("graph_specs"),
          data: view.model.get("data")
        }
        console.log("this.state:",this.state)
        // This binding is necessary to make `this` work in the callback
        this.changeHandler = this.changeHandler.bind(this);
        
      }
  
      onChange(model:any){// called when the variable is changed in the view.model
        this.setState(model.changed);
      }
      componentDidMount(){ //triggered when component is mounted (i.e., when widget first rendered)
        view.listenTo(view.model,"change",this.onChange.bind(this));
      }
      componentDidUpdate(){ //triggered after component is updated
        console.log(view.model.get("value"));
        view.model.save_changes(); // instead of touch (which leads to callback issues), we have to use save_changes
      }
  
      render(){
        return (<div id="widgetContainer">
                  <ChartGalleryComponent data={this.state.data} graphSpec={this.state.graphSpec}/>
                </div>);
      }
      changeHandler(event:any){
        var inputVal = event.target.value
        this.setState(state => ({
          value: inputVal
        }));
        view.model.set('value',inputVal);
      }
    }
    const $app = document.createElement("div");
    const App = React.createElement(ReactWidget,view);
    ReactDOM.render(App,$app);
    view.el.append($app);
  }
}