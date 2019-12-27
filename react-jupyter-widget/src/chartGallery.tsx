import React, { Component } from 'react';
import ToolComponent from './tool';
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
        // var graphSpecs = [4,5,2,4,2]
        // const data1 = {
        //     myData: [
        //       { a: 'A', b: 20 },
        //       { a: 'B', b: 34 },
        //       { a: 'C', b: 55 },
        //       { a: 'D', b: 19 },
        //       { a: 'E', b: 40 },
        //       { a: 'F', b: 34 },
        //       { a: 'G', b: 91 },
        //       { a: 'H', b: 78 },
        //       { a: 'I', b: 25 },
        //     ],
        //   };
        // const spec1:VisualizationSpec = {
        //     data: { name: 'myData' },
        //     description: 'A simple bar chart with embedded data.',
        //     encoding: {
        //         x: { field: 'a', type: 'ordinal' },
        //         y: { field: 'b', type: 'quantitative' },
        //     },
        //     mark: 'bar',
        // };
        console.log("this.props.graphSpec:",this.props.graphSpec)
        const galleryItems = this.props.graphSpec.map((item,idx) =>
                <div key={idx.toString()}
                     id={"graph-container-".concat(idx.toString())}>
                    <VegaLite data={chartData} spec={item}/>,
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