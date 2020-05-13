import React from "react";
import GameStat from "./GameStat";
import CurrPlayer from "./CurrPlayer";
import MarketCards from "./MarketCards";

class MainFrame extends React.Component {
   state = {
      currentPlayer: {
         name: "Bob",
         money: 13,
         stock: [
            { company: "Gooble", stock: 3, price: 0 },
            { company: "Amazoom", stock: 1, price: 0 },
         ]
      },
      players: [
         { name: "Bob", money: 13, stock: [
               { company: "Gooble", stock: 3, price: 0 },
               { company: "Amazoom", stock: 1, price: 0 },
            ]},
         { name: "Dad", money: 9, stock: [
               { company: "Macrosoft", stock: 3, price: 0 },
               { company: "Amazoom", stock: 2, price: 0 },
               { company: "Amazoom", stock: 1, price: 0 },
            ]},
         { name: "Chris", money: 23, stock: [
               { company: "Gooble", stock: 2, price: 0 },
            ]},
      ],
      stock_market: {
         "Gooble": 10,
         "Amazoom": 15,
         "Macrosoft": 13,
      },
      turn: 3,
      current_market: [
         { company: "Gooble", stock: 3, price: 21 },
         { company: "Gooble", stock: 1, price: 10 },
         { company: "Amazoom", stock: 2, price: 24 },
         { company: "Macrosoft", stock: 3, price: 28 },
         { company: "Amazoom", stock: 1, price: 15 },
      ]
   }
    constructor(props) {
        super(props);
        var playerID;
        this.socket = require('socket.io-client')('http://localhost:8080');
        socket.on('Player Turn', this.updatePlayer);
        socket.on('Update Market Cards', this.updateStockCards);
        socket.on('Update Stock Market', this.updateStockMarket);
        socket.on('Update Current Player', this.updateCurrentPlayer);
        socket.on('UpdateEverything', this.updateEverything);
        socket.on('Connect', this.updateEverything);
    }
    
    updatePlayer = (data) => {
    }
    updateStockCards = (data) => {
    }
    updateStockMarket = (data) => {
    }
    updateCurrentPlayer = (data) => {
    }
    updateEverything = (data) => {
        this.playerID = data.playerID;//set the player id
    }
   render() {
      return (
         <div>
            <MarketCards market={this.state.current_market}/>
            <GameStat
               turn={this.state.turn}
               players={this.state.players}
               market= {this.state.stock_market}/>
            <CurrPlayer info={this.state.currentPlayer}/>
         </div>
      );
   }
}

export default MainFrame;
