import React from "react";
import "./stylesheets/settings.css";

class Settings extends React.Component {
   state = {
      ip: "localhost",
      ports: [
         { value: "8080" },
         { value: "8081" },
         { value: "8082" },
      ],
      left: 100,
      top: 100,
      ip_only: false,
   }

   constructor(props) {
      super(props);

      this.localStorage = window.localStorage;


       

      let ip = this.localStorage.getItem("cam_ip");
      if(ip !== null) {
         this.state.ip = ip;
      }
      let ports = this.localStorage.getItem("ports");
      if(ports !== null) {
         this.state.ports = JSON.parse(ports);
      }
      this.handleChecked = this.handleChecked.bind(this);

   }

   getStyles() {
      return {
         left: this.state.left + "px",
         top: this.state.top + "px"
      }
   }

   render() {
      return (
         <div id="settings" style={this.getStyles()}>
            <div class="header">
               <div onClick={this.handleExit}>
                  &times;
               </div>
            </div>
            {this.renderCamIp()}
            <br />
            Ip-only Mode:
            <input type="checkbox" onChange={ this.handleChecked }/>

            <br />
            Camera Ports:
            <div>
               {this.renderPorts()}
               <div className="button" onClick={() => this.addPort()}>Add Port</div>
            </div>
            <div className="footer">
               <div className="button" onClick={this.handleSave}>Save Settings</div>
               <div className="button">Reset to Defaults</div>
            </div>
         </div>
      );
   }

   renderCamIp() {
      if(!this.state.ip_only)
         return (
            <React.Fragment>
               Camera IP:
               <input
                  type="text"
                  value={this.state.ip}
                  onChange={this.handleIpChange}
               >
               </input>
            </ React.Fragment>
         );
   }

   renderPorts() {
      return this.state.ports.map((port, index) => (
         <div>
            {this.portLabel(index)}
            <input
               key={index}
               type="text "
               value={port.value}
               onChange={(e) => this.handlePortChange(index, e)}
               >
            </input>
            <div className="button remButt" onClick={() => this.removePort(index)}>
               -
            </div>
         </ div>
      ));
   }

   portLabel(index) {
      if(!this.state.ip_only)
         return "Port " + (index + 1) + ": ";
      return "IP " + (index + 1) + ": ";
   }


   addPort() {
      let newPorts = this.state.ports.slice(0); // make variable to access entire array
         newPorts.push({ value: 8080 }); // use push to ADD to end of array. not sure what to put inside push
      this.setState({ ports : newPorts }); // update Ports with the newPorts value
   }

   removePort(index) {
      let newPorts = this.state.ports.slice(0);
      if(index < newPorts.length && index >= 0)
         newPorts.splice(index, 1);
      this.setState({ ports: newPorts });
   }

   handleIpChange = (e) => {
      this.setState( {ip: e.target.value} );
   }

   handlePortChange = (index, e) => {
      let newPorts = this.state.ports.splice(0);
      newPorts[index].value = e.target.value;
      this.setState( {ports: newPorts});
   }

   handleChecked() {
      this.setState({ip_only: !this.state.ip_only});
   }

   handleSave = () => {
      try {
         this.props.onSave(this.state);

         this.localStorage.setItem("cam_ip", this.state.ip);
         this.localStorage.setItem("ports", JSON.stringify(this.state.ports));
      } catch (e) {

      }
   }

   handleExit = () => {
      console.log("Exit!")
      this.props.onExit();
   }


}

export default Settings;
