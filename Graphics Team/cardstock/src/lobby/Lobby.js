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

   render() {
      return (
         <div class="screen">
            <input type="text" placeholder="Enter Name" value={this.state.name}
                  onChange={this.handleName}></input>
            <div
               class="createPlayer"
               onClick={() => {this.createPlayer()}}>
            </div>
            <div>{this.displayList()}</div>
            <div class="ready"></div>
         </div>
      )
   }

   createPlayer = () => {
      console.log("create: " + this.state.name);
   }

   handleName = (event) => {
      this.setState({"name": event.target.value});
   }

   displayList = () => {
      this.state.playerList.map(function(player){
         let ready = (player.id == 1)?;
         return (
            <li>P{player.id}: {player.name} ({})</li>
         )
      });
   }

}

export default Lobby;
