import React from "react";
import MiniCam from './MiniCam';
import './stylesheets/widgets.css';

class Widgets extends React.Component {

   render() {
      return (
         <div id="widgets">
            <MiniCam
              ports={this.props.camPorts} 
              ip={this.props.ip}
              mainIndex={this.props.mainIndex}/>
         </div>
      );
   }

}
export default Widgets;
