import React, { Component } from 'react';
// import ReactDOM from 'react-dom';
// import ToolComponent from './tool';
import { VegaLite } from 'react-vega';
// import { VisualizationSpec } from 'vega-embed';
interface chartGalleryProps{
    graphSpec: any[]
    data: any[]
}
class ChartGalleryComponent extends Component<chartGalleryProps,any> {
    constructor(props:any) {
        super(props);
    }
    render() {
        const chartData = {chartData: this.props.data}
        console.log("this.props.graphSpec:",this.props.graphSpec)
        const galleryItems = this.props.graphSpec.map((item,idx) =>
                <div key={idx.toString()}
                     className="graph-container"
                     id={"graph-container-".concat(idx.toString())}>
                    <VegaLite data={chartData} spec={item}  
                              padding={{left: 30, top: 5, right: 5, bottom: 20}} />
                    {/* <ToolComponent graphIdx={idx}/> */}
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