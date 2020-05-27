import React from 'react';
import './GameStat.css';
import Draggable from 'react-draggable';

class GameStat extends React.Component {
   // I feel like I can make a field to keep track of
   // the ranking of richest players, and then display
   // them at the top...
   render() {
      return (
         <Draggable grid={[80, 80]}>
            <div className="GameStat">
               <h2>Turn number: {this.props.turn}</h2>
               <ol className="players">
                  {
                     this.getPlayersInfo(this.props.market)
                  }
               </ol>
            </div>
         </Draggable>
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
         for(let i = 0; i < player.stock.length; i++) {
            let stock = player.stock[i];
            netWorth += stock.stock * market[stock.company];
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


}
export default GameStat;
