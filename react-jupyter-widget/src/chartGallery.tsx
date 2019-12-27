import React, { Component } from 'react';
import ToolComponent from './tool';
var vegaEmbed = require('vega-embed');

class ChartGalleryComponent extends Component {
    constructor(props:any) {
        super(props);
        // const numbers = props.numbers;
    }
    componentDidMount(){
        // runs after the component output has been rendered to the DOM 
        // var spec = JSON.parse(this.model.get('_graph_specs')[num]);
        //     console.log(spec);
        let spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
            "description": "A simple bar chart with embedded data.",
            "data": {
              "values": [
                {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
                {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
                {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
              ]
            },
            "mark": "bar",
            "encoding": {
              "x": {"field": "a", "type": "ordinal"},
              "y": {"field": "b", "type": "quantitative"}
            }
          }
        vegaEmbed.default("#graph-container-0", spec);
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