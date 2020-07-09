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
            <h3>Round number: {this.props.round}</h3>
            <ol className="players">
               {
                  this.getPlayersInfo(this.props.market)
               }
            </ol>
            <h4>Turn order:</h4>
            {this.renderCurrentTurn()}
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

         if(i === 0) {
            return (
               <li className="BIGBOY">
                  {player[0].name}'s net worth: {player[1]}
               </li>
            );
         } else {
            return (
               <li>{player[0].name}'s net worth: {player[1]}</li>
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
