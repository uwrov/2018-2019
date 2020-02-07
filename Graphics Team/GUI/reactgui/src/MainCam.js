import React from 'react';
import "./maincam.css"

class MainCam extends React.Component {
   constructor() {
      super();
      this.img_URL = "http://10.18.207.212:8080/video";
      this.cam_Num = 1;
   }

   render() {
      let altText = "This is cam #: " + this.cam_Num;
      return <img id="maincam" src={this.img_URL} alt={altText}></img>;
   }
}

export default MainCam;
