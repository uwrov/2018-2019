import React from "react";

class Settings extends React.Component {
   state = {
      ip: "localhost",
      ports: [
         { value: "8080" }
      ],
      left: 100,
      top: 100,
   }

   constructor(props) {
      super(props);

      this.localStorage = window.localStorage;

   }

   render() {
      return (
         <div>
            Camera IP:
            <input
               type="text"
               value={this.state.ip}
               onChange={this.handleIpChange}
               />
            Camera Ports:
            <div>
               {this.renderPorts()}
               <div>Add Port</div>
            </div>
            <div onClick={this.handleSave}>Save Settings</div>
            <div>Reset to Defaults</div>
         </div>
      );
   }

   renderPorts() {

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
