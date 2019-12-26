import React, { Component } from 'react';
interface toolProps{
    graphIdx:number
}
class ToolComponent extends Component<toolProps,any> {
    constructor(props:toolProps) {
        super(props);
        // This binding is necessary to make `this` work in the callback
        this.starVis = this.starVis.bind(this);
    }
    starVis(){
        console.log("starred")
    }
    render() {
        let toolDivId = "toolDiv-".concat(this.props.graphIdx.toString())
        return (
            // var tools = document.createElement("div");
            // tools.className = "toolDiv"
            // tools.id = "toolDiv-".concat(num.toString());
            // tools.innerHTML="<i class='fa-star fa' style='margin: 0px;font-size: 18px;' title='Mark visualization as Favorite'></i>"
            // tools.firstChild.onclick = function(){starVis(this)}
            // displayDiv.appendChild(tools)
            <div className="toolDiv" id ={toolDivId}>
                {toolDivId}
            </div>
        );
    }
}
export default ToolComponent;