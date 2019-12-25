import React, { Component } from 'react';
// var vegaEmbed = require('vega-embed');

class ChartGalleryComponent extends Component {
    constructor(props:any) {
        super(props);
        // const numbers = props.numbers;
    }
    render() {
        var graphSpecs = [4,5,2,4,2]
        const graphSpecItems = graphSpecs.map((item,idx) =>
                <li key={idx.toString()}
                     id={"graph-container-".concat(idx.toString())}>
                    {item}
                </li>
            );
        console.log(graphSpecItems)
        return (
            <ul>{graphSpecItems}</ul>
        );
    }
}
export default ChartGalleryComponent;