import React, { Component } from 'react';

class ToolComponent extends Component {
    // constructor(props:any) {
    //     super(props);
    //     // This binding is necessary to make `this` work in the callback
    //     this.starVis = this.starVis.bind(this);
    // }
    // starVis(){
    //     console.log("starred")
    // }
    render() {
        return (
            <h1>TEST TOOL COMPONENT</h1>
        // <div className="toolDiv" id="toolDiv-${num.toString()}" onClick={this.starVis}>
        //     <i className='fa-star fa'  title='Mark visualization as Favorite'></i>
        //     {/* style='margin: 0px;font-size: 18px;' */}
        // </div>
        );
    }
}
export default ToolComponent;