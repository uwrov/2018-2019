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
         },
         {
            "id": 2,
            "name": "Justin",
            "ready": 0
         },
         {
            "id": 3,
            "name": "Alex",
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
         <div>
            <input type="text" placeholder="Enter Name" value={this.state.name}
                  onChange={this.handleName} class="input"></input>
            <div
               class="createPlayer"
               onClick={() => {this.createPlayer()}}>
               Create Players
            </div>
            <div class="display">{this.displayList()}</div>
            <div
               class="ready"
               onClick={() => {this.getReady()}}>
               Ready
            </div>
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
      return this.state.playerList.map(function(player, index){
         let highlight = (id === player.id) ? "This is You" : null;
         /*
         return (
            <li>P{index + 1}: {player.name} ({ready}) {highlight}</li>
         )
         */
         let color = (player.ready === 1) ? ({backgroundColor : '#98FB98'}) : ({backgroundColor : '#FA8072'});
         return(
            <div style={color}>
               <h4>P{index + 1}</h4>
               <h4>{player.name}</h4>
               <h5>{highlight}</h5>
            </div>
         );
      });
   }

   getReady = () => {
      // this function will be called when the ready button is pressed
   }

}

export default Lobby;
