import React from 'react';
import "./minicam.css"

class MiniCam extends React.Component {

  constructor() {
    super();
    this.img_URL = "10.19.";
    this.cam_Num = 2;

  }


    render() {
      let altText = "This is cam #: " + this.cam_Num;
      return(
        <img id="minicam" src={this.img_URL} alt={altText}> </img>;
      )
    }

}

export default MiniCam;
