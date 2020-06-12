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
   }

   render() {
      return (
         <div>
            {
               displayGame();
               displayLobby();
            }
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
