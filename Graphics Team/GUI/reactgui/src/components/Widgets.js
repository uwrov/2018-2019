import React from "react";
import MiniCam from './MiniCam';
import './stylesheets/widgets.css';

class Widgets extends React.Component {

   render() {
      return (
      <MiniCam camPorts={this.props.camPorts} ip={this.props.ip}/>
      );
   }

}
export default Widgets;
