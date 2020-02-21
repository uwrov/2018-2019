import React from "react";
import Settings from "./Settings";
import MainCam from "./MainCam";

class GUI extends React.Component {
   state = {
      cam_ip: "localhost",
      cam_ports: [
         "8080"
      ],
      main_cam_index: 0,
      shownComponents: [
         "settings"
      ]
   }

   render() {
      return (
         <div>
            <MainCam ip={this.state.cam_ip + ":" +
                        this.state.cam_ports[this.state.main_cam_index]}/>
            {this.renderSettings()}
            {
               //<Widgets ip={this.state.cam_ip} cam_ports={this.state.cam_ports} />
            }

         </div>
      );

   }

   renderSettings() {
      if(this.state.shownComponents.indexOf("settings") !== -1)
         return (
            <Settings onSave={this.handleSettings}/>
         );
   }

   handleSettings = (state) => {
      this.setState( {cam_ip: state.ip} );
   }



}

export default GUI;
