import React, { Component } from 'react';
import ChartGalleryComponent from './chartGallery';
// import { Tab } from 'react-bootstrap';
interface tabProps{
    actionName:string,
    data: object[],
    recommendedGraphSpec: object[]
}
class TabComponent extends Component<tabProps,any> {
    constructor(props:any) {
        super(props);
    }
    render() {
        return (
            // <Tab eventKey={this.props.actionName} title={this.props.actionName}>
            //     {/* <ChartGalleryComponent data={this.props.data} graphSpec={this.props.recommendedGraphSpec}/> */}
            //     blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
            //     blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
            //     blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
            //     blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
            // </Tab>
            // <Tab eventKey={this.props.actionName} title={this.props.actionName}>
            //     Tab {this.props.actionName} content
            // </Tab>
            <ChartGalleryComponent data={this.props.data} graphSpec={this.props.recommendedGraphSpec}/> 
            // <Tab eventKey="home" title="Home">
            //     blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
            // </Tab>
        );
    }
}
export default TabComponent;