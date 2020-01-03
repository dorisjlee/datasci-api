import React, { Component } from 'react';
import { VegaLite } from 'react-vega';
interface currentViewProps{
    currentViewSpec: object
    data: object[]
}
class CurrentViewComponent extends Component<currentViewProps,any> {
    constructor(props:any) {
        super(props);
    }
    render() {
        const chartData = {chartData: this.props.data}
        return (
            <div id="mainVizContainer">
                <h2 id="mainVizTitle">Current View</h2>
                <div id="mainVizInnerContainer">
                    <VegaLite data={chartData} spec={this.props.currentViewSpec}
                              padding={{left: 30, top: 5, right: 5, bottom: 20}} />
                </div>
            </div>
        );
    }
}
export default CurrentViewComponent;