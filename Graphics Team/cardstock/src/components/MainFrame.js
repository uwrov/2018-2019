import React from "react";
import GameStat from "./GameStat";
import CurrPlayer from "./CurrPlayer";
import MarketCards from "./MarketCards";
import StockMarket from "./StockMarket";
import PlayerCards from "./PlayerCards";
import ActionButtons from "./ActionButtons";

class MainFrame extends React.Component {
   state = {
      currentPlayer: 0,
      players: [
         { name: "test1", money: 13, stock: [
               { company: "Goobletest1", stock: 3, price: 0 },
               { company: "Amazoomtest2", stock: 1, price: 0 },
            ]},
         { name: "test2", money: 9, stock: [
               { company: "Macrosofttest3", stock: 3, price: 0 },
               { company: "Amazoomtest2", stock: 2, price: 0 },
               { company: "Amazoomtest2", stock: 1, price: 0 },
            ]},
         { name: "test3", money: 23, stock: [
               { company: "Goobletest1", stock: 2, price: 0 },
            ]},
      ],
      stock_market: {
         "Goobletest1": 10,
         "Amazoomtest2": 15,
         "Macrosofttest3": 13,
      },
      turn: 3,
      current_market: [
         { company: "Goobletest1", stock: 3, price: 21 },
         { company: "Goobletest1", stock: 1, price: 10 },
         { company: "Amazoomtest2", stock: 2, price: 24 },
         { company: "Macrosofttest3", stock: 3, price: 28 },
         { company: "Amazoomtest2", stock: 1, price: 15 },
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
        this.socket.on('Update Market Cards', this.updateMarketCards);
        this.socket.on('Update Stock Market', this.updateStockMarket);

        this.socket.on('Player Index', this.updatePlayerIndex);
        this.socket.on('Update Market Cards', this.updateStockCards);
        this.socket.on('Update Stock Market', this.updateStockMarket);
        this.socket.on('Update Players', this.updatePlayerData);

        this.socket.on('Connect', this.updateEverything);
        this.socket.on('Buy Outcome', this.buyOutcome);
        this.socket.on('Sell Outcome', this.sellOutcome);
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
        if (data === 0) {
            console.log("bought a card, no errors!");
        } else if (data === 1) {
            console.log("error: index out of bounds!");
        } else if (data === 2) {
            console.log("nothing bought, no errors!");
        } else if (data === 3) {
            console.log("error: not your turn, cannot buy!");
        } else {
            console.log("unknown error");
        }

    }

    updatePlayerIndex = (data) => {
        //set myTurn
        if (this.state.currentPlayer == data) {
            this.myTurn = true;
        }
        else {
            this.myTurn = false;
        }
    }

    updateStockCards = (data) => {
      this.setState({
         current_market: data
      });
    }

    updateStockMarket = (data) => {
      this.setState({
         stock_market: data
      });
    }

    updatePlayerData = (data) => {
      this.setState({
         players: data
      });
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
            <CurrPlayer info={this.state.players[this.state.currentPlayer]}/>
            <StockMarket stock_price={this.state.stock_market}/>
            <PlayerCards playerCards={this.state.players[this.state.currentPlayer].stock}
                         onSell={this.sellStock}/>
            <ActionButtons onSkipTurn={this.skipTurn} />
         </div>
      );
   }

   buyStock = (index) => {
      console.log("Stock Bought");
      console.log("Bought: " + this.state.current_market[index]);
       this.socket.emit("buy card", {"playerN": this.state.currentPlayer, "index": index });
   }

   sellStock = (index) => {
      console.log("Stock Sold");
      console.log("Sold: " + this.state.players[this.state.currentPlayer].stock[index]);
       this.socket.emit("sell card", {"playerN": this.state.currentPlayer, "index": index });
   }

   //End Turn
    skipTurn = () => {
       console.log("Turn Skipped");
        this.socket.emit("buy card", { "playerN": this.playerNumber, "index": -1 });//default for skip turn

   }

}

export default MainFrame;
