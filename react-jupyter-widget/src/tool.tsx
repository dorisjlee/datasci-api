import React, { Component } from 'react';

class ToolComponent extends Component {
    constructor(props:any) {
        super(props);
        // This binding is necessary to make `this` work in the callback
        this.starVis = this.starVis.bind(this);
    }
    starVis(){
        console.log("starred")
    }
    render() {
        return (
            // var tools = document.createElement("div");
            // tools.className = "toolDiv"
            // tools.id = "toolDiv-".concat(num.toString());
            // tools.innerHTML="<i class='fa-star fa' style='margin: 0px;font-size: 18px;' title='Mark visualization as Favorite'></i>"
            // tools.firstChild.onclick = function(){starVis(this)}
            // displayDiv.appendChild(tools)
            <div>tooldiv</div>
        );
    }
}
export default ToolComponent;