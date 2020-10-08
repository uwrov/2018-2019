import React from 'react';
import './GameStat.css';

class GameStat extends React.Component {
   state = {
      current_turn: null
   };
   // I feel like I can make a field to keep track of
   // the ranking of richest players, and then display
   // them at the top...
   render() {
      return (
         <div className="GameStat">
            <div className="board">
               <h4 style={{color : "white"}}>Round number: {this.props.round}</h4>
               <dl className="players">
                  {
                     this.getPlayersInfo(this.props.market)
                  }
               </dl>
            </div>
            <div className="turn">
               <h4 style={{color : "white"}}>Turn order:</h4>
               {this.renderCurrentTurn()}
            </div>
         </div>

      );
   }

   getPlayersInfo(market) {
      // I'm directly editing the players array. I shouldn't
      let players = this.props.players;
      // maybe just iterate
      let sorter = [];
      for(let i = 0; i < players.length; i++) {
         let player = players[i];
         let netWorth = player.money;
         for(let i = 0; i < player["stock_hand"].length; i++) {
            let stock = player["stock_hand"][i];
            netWorth += stock.amount * market[stock.company];
         }
         let tup = [player, netWorth];
         sorter.push(tup);
      }
      sorter.sort((a, b) => (a[1] > b[1]) ? 1 : -1);
      sorter.reverse();
      return sorter.map(function(player, i) {
         let order = "th";
         if(i === 0) {
            return (
               <dt className="BIGBOY">
                  {"1st: " + player[0].name}'s NW - {player[1]}
               </dt>
            );
         } else {
            if ((i + 1) % 10 === 2) {
               order = "nd";
            } else if ((i + 1) % 10 === 3) {
               order = "rd";
            }
            return (
               <dt>{(i + 1) + order + ": " + player[0].name}'s NW - {player[1]}</dt>
            )
         }
      });
   }

   renderCurrentTurn = () => {
      let turn = this.props.turn_index
      return this.props.players.map(function(player, i) {
            let playerClass = "waitingPlayerBox"
            if(i === turn) {
               playerClass = "currentPlayerBox"
            }
            return (
               <div className={"playerBox " + playerClass}>
                  <span>{player.name}</span>
               </div>
            )
         }
      )
   }

}
export default GameStat;
