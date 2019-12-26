import React, { Component } from 'react';
import ToolComponent from './tool';
// var vegaEmbed = require('vega-embed');

class ChartGalleryComponent extends Component {
    constructor(props:any) {
        super(props);
        // const numbers = props.numbers;
    }
    render() {
        var graphSpecs = [4,5,2,4,2]
        const galleryItems = graphSpecs.map((item,idx) =>
                <div key={idx.toString()}
                     id={"graph-container-".concat(idx.toString())}>
                    {item}
                    <ToolComponent graphIdx={idx}/>
                </div>
                
            );
        return (
            <div id="staticOuterDiv" className="recommendationStaticContentOuter">
                <div id="mult-graph-container" className= "recommendationContentInner">
                    {galleryItems}
                </div>
            </div>
        );
    }
}
export default ChartGalleryComponent;