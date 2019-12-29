import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'
// import 'bootstrap/dist/css/bootstrap.min.css';

import * as React from "react";
import * as ReactDOM from "react-dom";

import {Tabs,Tab} from 'react-bootstrap';
// import TabComponent from './tab';
import ChartGalleryComponent from './chartGallery';
import CurrentViewComponent from './currentView';

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

    class ReactWidget extends React.Component<JupyterWidgetView,{value:any,graphSpec:any[],data:any[],activeTab:any}> {
      constructor(props:any){
        super(props);
        console.log("view:",props);
        this.state = {
          value: props.model.get("value"),
          graphSpec: view.model.get("graph_specs"),
          data: view.model.get("data"),
          activeTab: props.activeTab 
        }
        console.log("this.state:",this.state)
        // This binding is necessary to make `this` work in the callback
        this.changeHandler = this.changeHandler.bind(this);
        this.handleSelect = this.handleSelect.bind(this);
        
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
  
      handleSelect(selectedTab) {
        // The active tab must be set into the state so that
        // the Tabs component knows about the change and re-renders.
        this.setState({
          activeTab: selectedTab
        });
      }      

      render(){
        console.log("this.state.activeTab:",this.state.activeTab)
        function shuffle(array) {
          return array.sort(() => Math.random() - 0.5);
        }
        let possibleActions = ["Enhance","Filter","Distribution"]
        const tabItems = possibleActions.map((action,idx) =>
          <Tab eventKey={action} title={action} >
            <ChartGalleryComponent data={this.state.data} graphSpec={shuffle(this.state.graphSpec)}/> 
          </Tab>);
        
        return (<div id="widgetContainer">
                  <CurrentViewComponent data={this.state.data} currentViewSpec={this.state.graphSpec[0]}/>
                  <div id="tabBanner">
                    <Tabs activeKey={this.state.activeTab} id="tabBannerList" onSelect={this.handleSelect}>
                      {tabItems}
                    </Tabs>
                  </div>
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