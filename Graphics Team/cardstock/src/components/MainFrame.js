import React from "react";
import GameStat from "./GameStat";
import CurrPlayer from "./CurrPlayer";
import MarketCards from "./MarketCards";
import StockMarket from "./StockMarket";
import PlayerCards from "./PlayerCards";
import ActionButtons from "./ActionButtons";

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

    buyCard(index) {
        this.socket.emit("Buy Card", { playerN: this.playerNumber, index: index });//buy a card
    }
    sellCard(index) {
        this.socket.emit("Sell Card", { playerN: this.playerNumber, index: index }); //sell a card
    }
    requestTurn() {
        this.socket.emit("Get Turn");//request the turn
    }
    constructor(props) {
        super(props);
        this.playerNumber = -1;
        this.myTurn = false;
        this.socket = require('socket.io-client')('http://localhost:8080');
        this.socket.on('Player Turn', this.updatePlayer);
        this.socket.on('Update Market Cards', this.updateStockCards);
        this.socket.on('Update Stock Market', this.updateStockMarket);
        this.socket.on('Update Current Player', this.updateCurrentPlayer);
        this.socket.on('UpdateEverything', this.updateEverything);
        this.socket.on('Connect', this.updateEverything);
        this.socket.on('buy outcome', this.buyOutcome);
        this.socket.on('sell outcome', this.sellOutcome);
    }
    sellOutcome = (data) => {
        if (data == 0) {
            console.log("sold, no errors!");
        } else if (data == 1) {
            console.log("error: index out of bounds!");
        } else {
            console.log("unknown error");
        }
    }
    buyOutcome = (data) => {
        if (data == 0) {
            console.log("bought a card, no errors!");
        } else if (data == 1) {
            console.log("error: index out of bounds!");
        } else if (data == 2) {
            console.log("nothing bought, no errors!");
        } else if (data == 3) {
            console.log("error: not your turn, cannot buy!");
        } else {
            console.log("unknown error");
        }

    }
    updatePlayer = (data) => {
        //set myTurn
        if (this.playerNumber == data) {
            this.myTurn = true;
        }
        else {
            this.myTurn = false;
        }
    }
    updateStockCards = (data) => {
    }
    updateStockMarket = (data) => {
    }
    updateCurrentPlayer = (data) => {
    }
    updateEverything = (data) => {
        this.playerNumber = data;//set the player number
    }
   render() {
      return (
         <div>
            <MarketCards market={this.state.current_market} onBuy={this.buyStock}/>
            <GameStat
               turn={this.state.turn}
               players={this.state.players}
               market= {this.state.stock_market}/>
            <CurrPlayer info={this.state.currentPlayer}/>
            <StockMarket stock_price={this.state.stock_market}/>
            <PlayerCards playerCards={this.state.currentPlayer.stock}/>
            <ActionButtons onSkipTurn={this.skipTurn} />
         </div>
      );
   }

   buyStock = (index) => {
      console.log("Stock Bought");
      console.log("Bought: " + this.state.current_market[index]);
   }

   //End Turn
   skipTurn = () => {


   }

}

export default MainFrame;
