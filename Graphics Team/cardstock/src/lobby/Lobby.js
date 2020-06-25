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
      this.state.id = this.props.id;

      this.props.socket.on("Player Data", this.updatePlayerList);
   }

   componentDidMount() {
      this.props.socket.emit("Get Players");
      this.props.socket.emit("Create Player", {"id": this.state.id, "name": "andrew"});
   }

   render() {
      return (
         <div class="screen">
            <input type="text" placeholder="Enter Name" value={this.state.name}
                  onChange={this.handleName}></input>
            <div
               class="createPlayer"
               onClick={() => {this.createPlayer()}}>
            </div>
            <div>
               <p>List of Players:</p>
               <ul>{this.displayList()}</ul>
            </div>
            <div class="ready"></div>
         </div>
      )
   }

   updatePlayerList = (params) => {
      this.setState({ "playerList": params });
   }

   createPlayer = () => {
      console.log("create: " + this.state.name);
   }

   handleName = (event) => {
      this.setState({"name": event.target.value});
   }

   displayList = () => {
      let id = this.state.id;
      if(this.state.playerList.length !== 0) {
         return this.state.playerList.map(function(player, index){
            let ready = (player.ready === 1) ? "Ready" : "Not Ready";
            let highlight = (id === player.id) ? "This is You" : null;
            return (
               <li>P{index + 1}: {player.name} ({ready}) {highlight}</li>
            )
         });
      } else {
         return "No Players are Ready.";
      }
   }
}

export default Lobby;
