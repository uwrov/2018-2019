import React from "react";
import "./stylesheets/maincam.css";


class MainCam extends React.Component {

   render() {
      return (
         <img id="maincam" src={"http://" + this.props.ip} alt= "Main Cam"/>
      );
   }

}

export default MainCam;
