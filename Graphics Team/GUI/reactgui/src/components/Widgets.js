import React from "react";
import MiniCam from './MiniCam';
import './stylesheets/widgets.css';

class Widgets extends React.Component {

   render() {
      return (
         <div id="widgets">
            <MiniCam camPorts={this.props.camPorts} ip={this.props.ip}/>
         </div>
      );
   }

}
export default Widgets;
