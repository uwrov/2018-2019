import React from "react";
import GameStat from "./GameStat";
import CurrPlayer from "./CurrPlayer";
import MarketCards from "./MarketCards";
import StockMarket from "./StockMarket";
import PlayerCards from "./PlayerCards";
import ActionButtons from "./ActionButtons";

class MainFrame extends React.Component {
   state = {
      index: 0,
      players: [
         { name: "test1", money: 13, stock_hand: [
               { company: "Goobletest1", amount: 3, price: 0 },
               { company: "Amazoomtest2", amount: 1, price: 0 },
            ]},
         { name: "test2", money: 9, stock_hand: [
               { company: "Macrosofttest3", amount: 3, price: 0 },
               { company: "Amazoomtest2", amount: 2, price: 0 },
               { company: "Amazoomtest2", amount: 1, price: 0 },
            ]},
         { name: "test3", money: 23, stock_hand: [
               { company: "Goobletest1", amount: 2, price: 0 },
            ]},
      ],
      stock_market: {
         "Goobletest1": 10,
         "Amazoomtest2": 15,
         "Macrosofttest3": 13,
      },
      turn: 3,
      current_market: [
         { company: "Goobletest1", amount: 3, price: 21 },
         { company: "Goobletest1", amount: 1, price: 10 },
         { company: "Amazoomtest2", amount: 2, price: 24 },
         { company: "Macrosofttest3", amount: 3, price: 28 },
         { company: "Amazoomtest2", amount: 1, price: 15 },
      ]
    }

    constructor(props) {
        super(props);
        this.myTurn = false;
        this.socket = this.props.socket;
        if(this.socket == null) {
           this.socket = require('socket.io-client')('http://localhost:8080');
        }
        this.socket.on('Game Turn', this.updateTurn);
        this.socket.on('Market Cards', this.updateMarketCards);
        this.socket.on('Stock Market', this.updateStockMarket);

        this.socket.on('Player Index', this.updatePlayerIndex);
        this.socket.on('Player List', this.updatePlayerData);

        this.socket.on('Connect', this.updateEverything);

    }

    componentDidMount(){
        this.socket.emit("Update Request");
    }

    updatePlayerIndex = (data) => {
        //set myTurn
        if (this.state.index == data) {
            this.myTurn = true;
        }
        else {
            this.myTurn = false;
        }
    }

    updateMarketCards = (data) => {
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
      for(let i = 0; i < data.length; i++) {
        if(data[i].id === this.props.id) {
           this.setState({"index": i});
        }
      }
      console.log(data);
    }

    updateEverything = (data) => {
        this.playerNumber = data;//set the player number
    }

    updateTurn = (data) => {
        this.setState({
           turn: data
        });
    }

   render() {
      return (
         <div>
            <MarketCards market={this.state.current_market} onBuy={this.buyStock}/>
            <GameStat
               turn={this.state.turn}
               players={this.state.players}
               market= {this.state.stock_market}/>
            <CurrPlayer info={this.state.players[this.state.index]}/>
            <StockMarket stock_price={this.state.stock_market}/>
            <PlayerCards playerCards={this.state.players[this.state.index].stock_hand}
                         onSell={this.sellStock}/>
            <ActionButtons onEndTurn={this.endTurn} />
         </div>
      );
   }

   buyStock = (index) => {
      console.log("Stock Bought");
      console.log("Bought: " + this.state.current_market[index]);
       this.socket.emit("Buy Card", {"id": this.props.id, "target": index });
   }

   sellStock = (index) => {
      console.log("Stock Sold");
      console.log("Sold: " + this.state.players[this.state.index].stock_hand[index]);
       this.socket.emit("Sell Card", {"id": this.props.id, "target": index });
   }

   //End Turn
    endTurn = () => {
       console.log("Turn Skipped");
        this.socket.emit("End Turn", { "id": this.props.id});//default for skip turn

   }

}

export default MainFrame;
