import React from 'react';
import Lobby from './lobby/Lobby.js';
import MainFrame from './components/MainFrame';
import Results from './results/Results';
import "./ComponentHandler.css";
import Pop from './components/Pop';

class ComponentHandler extends React.Component {
   state = {
      id: null,
      socket: null,
      gameStart: true,
      showResults: false,
      pop: false,
      message: ""
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
      this.state.socket.on("Game State", this.checkState);
      this.state.socket.on("Pop Up", this.updatePop)
      this.state.socket.on("error", this.updatePop)
   }

   setID = (id) => {
      window.localStorage.setItem("id", id);
      this.setState( { "id": id } );
   }

   checkState = (data) => {
      this.setState( {gameStart: data.state, showResults: data.results} );
   }

   componentDidMount(){
      this.state.socket.emit("Update Request");
   }

   render() {
      return (
         <div className="componentWindow">
            {this.displayGame()}
            {this.displayLobby()}
            {this.displayResults()}
            {this.displayPop()}
         </div>
      );
   }

   displayGame() {
      if(this.state.gameStart && !this.state.showResults)
         return <MainFrame socket={this.state.socket} id={this.state.id}/>
   }

   displayLobby() {
      if(!this.state.gameStart)
         return <Lobby socket={this.state.socket} id={this.state.id} />;
   }

   displayResults() {
      if(this.state.showResults && this.state.gameStart)
         return <Results socket={this.state.socket} id={this.state.id} />;
   }

   displayPop() {
      if(this.state.pop)
         return <Pop socket={this.state.socket} id={this.state.id}
                  pop={this.resumePop} message={this.state.message}/>;
   }

   resumePop = () => {
      this.setState({pop: false});
      // this is supposed to change the pop field to make the pop up screen
      // disappear, but it is not doing that.
   }

   updatePop = (data) => {
      console.log(data);
      this.setState({pop: true, message: data.message})
   }
}

export default ComponentHandler;
