import React from "react";
import Settings from "./Settings";
import MainCam from "./MainCam";
import NavBar from "./NavBar";


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

   buttons = [
      {
         text: "Settings",
         onClick: () => {this.showComponent("settings");}
      },
      {
         text: "Debugger",
         onClick: () => {this.showComponent("debugger");}
      }

   ]

   render() {
      return (
         <div>
            <MainCam ip={this.state.cam_ip + ":" +
                        this.state.cam_ports[this.state.main_cam_index]}/>
            {this.renderSettings()}
            {
               //<Widgets ip={this.state.cam_ip} cam_ports={this.state.cam_ports} />
            }

            <NavBar buttons={this.state.buttons}/>

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

   showComponent(name) {
      let visible = this.state.shownComponents.slice(0);
      if(visible.indexOf(name) === -1)
         visible.push(name);
      this.setState({ shownComponents: visible });
   }

   removeComponent(name) {
      let visible = this.state.shownComponents.slice(0);
      let index = visible.indexOf(name)
      if(index !== -1)
         visible.splice(index, 1);
      this.setState({ shownComponents: visible } );
   }

}

export default GUI;
