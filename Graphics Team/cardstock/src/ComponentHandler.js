import React from 'react';
import Lobby from './lobby/Lobby.js';
import MainFrame from './components/MainFrame';

class ComponentHandler extends React.Component {
   state = {
      id: null,
      socket: null,
      gameStart: false
   }

   constructor(props) {
      super(props);

      this.state.socket = require('socket.io-client')('http://localhost:8080');

      let id = window.localStorage.getItem("id");
      if(id === null) {
         this.state.socket.emit("Generate ID");
      } else {
         this.state.id = id;
      }
      this.state.socket.on("connected", this.setID);
   }

   setID(id) {
      this.setState("id": id);
   }

   render() {
      return (
         <div>
            {this.displayGame()}
            {this.displayLobby()}
         </div>
      );
   }

   displayGame() {
      if(this.state.gameStart)
         return <MainFrame socket={this.state.socket} id={this.state.id}/>
   }

   displayLobby() {
      if(!this.state.gameStart)
         return <Lobby socket={this.state.socket} id={this.state.id} />;
   }
}

export default ComponentHandler;
