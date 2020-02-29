import React from 'react';
import "./stylesheets/minicam.css"

class MiniCam extends React.Component {

  state = {
    ip: "",
    ports: [],
  }

  constructor(props) {
    super(props);
    this.state.ip = this.props.ip;
    this.state.ports = this.props.camPorts;

  }


    render() {
      let altText = "This is cam #: " + this.cam_Num;
      return(
        <div id="minicam">
          {this.state.ports.map(port => (<img src={this.state.ip + ":" + port} alt="MiniCam" />))}
        </div>
        // <img id="minicam" src={this.img_URL} alt={altText}> </img>;
      )
    }

}

export default MiniCam;
