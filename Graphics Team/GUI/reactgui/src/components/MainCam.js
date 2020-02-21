import React from "react";


class MainCam extends React.Component {

   render() {
      return (
         <img src={this.props.ip} alt= "Main Cam"/>
      );
   }

}

export default MainCam;
