import React from 'react';
import "./stylesheets/minicam.css"

class MiniCam extends React.Component {

    render() {
      let altText = "This is cam #: " + this.cam_Num;
      return(
        <div id="minicam">
          {this.renderMiniCams()}
        </div>
        // <img id="minicam" src={this.img_URL} alt={altText}> </img>;
      )
    }

    renderMiniCams() {
      return this.props.ports.map((port, index) => {
        if(index !== this.props.mainIndex) {
          return <img id="miniCam" src={"http://" + this.props.ip + ":" + port} alt="MiniCam" />
        }
        return null;
      });
    }

}

export default MiniCam;
