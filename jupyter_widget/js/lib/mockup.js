var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var vegaEmbed = require('vega-embed');
require("@fortawesome/fontawesome-free");
require("./main.css");


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
// 
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.

// Custom View. Renders the widget model.

var MockupModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'MockupModel',
        _view_name : 'MockupView',
        _model_module : 'widgetDisplay',
        _view_module : 'widgetDisplay',
        _model_module_version : '^0.1.0',
        _view_module_version : '^0.1.0',

        value : ""
    })
});

var MockupView = widgets.DOMWidgetView.extend({
    callback:function(inputEvent, formElement){
        this.model.set({'value':formElement[0].value})    // update the JS model with the current view value
        this.touch()   // sync the JS model with the Python backend
    },

    render: function() {
        this.model.on('change:value', this.value_changed, this);
        // this.listenTo(this.model, 'change:selected_graphID', this.selected_graphID, this);
        let view = this;
        var current_selected_graphID_list = []
        let clickTriggerEvent = function(graphID){
            // Note weird bug here, the object that is modified is REQUIRED to be a new object, otherwise the update does not happen, update only on a object replacement basis
            var newLst = current_selected_graphID_list.slice()
            newLst.push(graphID)
            current_selected_graphID_list = newLst
            // Could probably replace this with jquery get all checked vizzes
            view.model.set('selected_graphID',newLst) // working (as a list)
            view.touch()
        }
        let starVis = function(node){
            console.log("starVis")
            var graphID = parseInt(node.parentElement.id.replace("toolDiv-",""))
            var isStarred = node.getAttribute("isStarred") === 'true'
            isStarred = !isStarred;
            var newLst = current_selected_graphID_list.slice()
            if (isStarred){
                // Add to list of selected ID
                newLst.push(graphID)
                node.style.color = "#ffc000"
            }else{
                //remove starred vis
                // TODO modify selected_graphID
                var index = newLst.indexOf(graphID);
                if (index > -1) {newLst.splice(index, 1);}
                node.style.color = "grey"
            }
            current_selected_graphID_list = newLst
            node.setAttribute("isStarred",isStarred)
            view.model.set('selected_graphID',newLst)
            view.touch()
          }

        //displayDiv.className = "recommendationContentOuter";
        let staticDiv = document.createElement('div');
        staticDiv.id = "staticOuterDiv";
        staticDiv.className = "recommendationStaticContentOuter";
        this.el.appendChild(staticDiv);

        let displayDiv = document.createElement('div');
        displayDiv.id = "mult-graph-container";
        displayDiv.className = "recommendationContentInner";

        //document.getElementById("staticOuterDiv").appendChild(displayDiv);
        staticDiv.appendChild(displayDiv);

        for(let num = 0; num < this.model.get('numGraphs'); num++){
            //creates div object to hold each individual graph
            let newDiv = document.createElement('div');
            newDiv.id = "graph-container-".concat(num.toString());
            newDiv.onclick = function(){clickTriggerEvent(num)}
            displayDiv.appendChild(newDiv);

            // add star as favorite
            var tools = document.createElement("div");
            tools.className = "toolDiv"
            tools.id = "toolDiv-".concat(num.toString());
            tools.innerHTML="<i class='fas fa-star' style='margin: 0 5px 0 5px;font-size: 18px;' title='Mark visualization as Favorite'></i>"
            tools.firstChild.onclick = function(){starVis(this)}
            displayDiv.appendChild(tools)

            //parses each JSON spec, generates VEGA graphs, and inputs them into appropriate div object
            var spec = JSON.parse(this.model.get('_graph_specs')[num]);
            console.log(spec);
            vegaEmbed.default(newDiv, spec);
        }

        console.log(vegaEmbed);
    }
});

module.exports = {
    MockupModel : MockupModel,
    MockupView : MockupView
};
