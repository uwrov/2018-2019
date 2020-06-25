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

      this.state.socket = require('socket.io-client')('http://localhost:4000');

      let id = window.localStorage.getItem("id");
      if(id === null) {
         this.state.socket.emit("Generate ID");
      } else {
         id = parseInt(id);
         this.state.socket.emit("Previous ID", id);
      }
      this.state.socket.on("ID Confirm", this.setID);
   }

   setID = (id) => {
      window.localStorage.setItem("id", id);
      console.log("id: " + id);
      this.setState( { "id": id } );
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
