import React from 'react';
import './Lobby.css';
import Draggable from 'react-draggable';

class Lobby extends React.Component {
   state = {
      "id": 0,
      "name": "",
      "playerList": [
         {
            "id": 0,
            "name": "Chris",
            "ready": 1
         },
         {
            "id": 1,
            "name": "Andrew",
            "ready": 0
         }
      ]
   }
   constructor(props) {
      super(props);

      this.props.socket.on("Player List", this.updatePlayerList);

   }

   render() {
      return (
         <div>
            <input type="text" placeholder="Enter Name" value={this.state.name}
                  onChange={this.handleName} class="input"></input>
            <div
               class="createPlayer"
               onClick={() => {this.createPlayer()}}>
               <p>Create Players</p>
            </div>
            <div class="display">
               <p>List of Players:</p>
               <ul>{this.displayList()}</ul>
            </div>
            <div
               class="ready"
               onClick={() => {this.getReady()}}>
               <p>Ready</p>
            </div>
         </div>
      )
   }

   updatePlayerList = (params) => {

   }

   createPlayer = () => {
      console.log("create: " + this.state.name);
   }

   handleName = (event) => {
      this.setState({"name": event.target.value});
   }

   displayList = () => {
      let id = this.state.id;
      return this.state.playerList.map(function(player, index){
         let ready = (player.ready === 1) ? "Ready" : "Not Ready";
         let highlight = (id === player.id) ? "This is You" : null;
         return (
            <li>P{index + 1}: {player.name} ({ready}) {highlight}</li>
         )
      });
   }

   getReady = () => {
      // this function will be called when the ready button is pressed
   }

}

export default Lobby;
