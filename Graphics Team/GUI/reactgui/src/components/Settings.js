import React from "react";
import "./stylesheets/settings.css";

class Settings extends React.Component {
   state = {
      ip: "localhost",
      ports: [
         { value: "8080" },


      ],
      left: 100,
      top: 100,
   }

   constructor(props) {
      super(props);

      this.localStorage = window.localStorage;
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
            </div>
            Camera IP:
            <input
               type="text"
               value={this.state.ip}
               onChange={this.handleIpChange}
               />
            <br />
            Camera Ports:
            <div>
               {this.renderPorts()}
               <div className="button">Add Port</div>
            </div>
            <div className="footer">
               <div className="button" onClick={this.handleSave}>Save Settings</div>
               <div className="button">Reset to Defaults</div>
            </div>
         </div>
      );
   }

   renderPorts() {
      return this.state.ports.map((port) => {
         return (<div>
            Port:
            <input type="text " value={port.value}>
            </input>
            <div className="button">
               -
            </div>
         </div>
      )});
   }

   addPort() {

   }

   removePort() {

   }

   handleIpChange = (e) => {
      this.setState( {ip: e.target.value} );
   }

   handleSave = () => {
      try {
         this.props.onSave(this.state);
      } catch (e) {

      }
   }


}

export default Settings;
