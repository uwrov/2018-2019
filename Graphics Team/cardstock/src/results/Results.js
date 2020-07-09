import React from 'react';
import './Results.css';
import Draggable from 'react-draggable';

class Results extends React.Component {
   state = {
      "index": null,
      "name": "",
      "playerList": [
         {
            "id": 0,
            "name": "Chris",
            "ready": 1,
            "netWorth": 100,
            "rank": 1
         },
         {
            "id": 1,
            "name": "Andrew",
            "ready": 0,
            "netWorth": 75,
            "rank": 2
         },
         {
            "id": 2,
            "name": "Justin",
            "ready": 0,
            "netWorth": 50,
            "rank": 3
         },
         {
            "id": 3,
            "name": "Alex",
            "ready": 0,
            "netWorth": 25,
            "rank": 4
         }
      ]
   }

   constructor(props) {
      super(props);

      this.props.socket.on("Player List", this.updatePlayerList);
   }

   componentDidMount() {
      this.props.socket.emit("Get Players");
   }

   render() {
      return (
         <div>
            <div class="ranking">
               <div class="ranks">
                  {this.rankPlayers(this.state.playerList)}
               </div>
            </div>
            <div
               class="button"
               onClick={() => {this.restart()}}>
               Play Again!
            </div>
         </div>
      )
   }

   rankPlayers(players) {
      let maxNet = 0;
      players.forEach(function(player) {
         if(player.netWorth > maxNet) {
            maxNet = player.netWorth;
         }
      });
      return players.map(function(player) {
         let rank = "";
         if(player.rank % 10 === 1) {
            rank = player.rank + "st";
         } else if (player.rank % 10 === 2) {
            rank = player.rank + "nd";
         } else if (player.rank % 10 === 3) {
            rank = player.rank + "rd";
         } else {
            rank = player.rank + "th";
         }
         let message = (player.rank === 1) ? "(/ ^-^)/" : null;
         return(
            <div class="stats">
               <p class="winner">{message}</p>
               <div class="bar" style={{
                  height : (player.netWorth / maxNet) * 280 + "px",
                  // attempting to adjust the bar appearance depending on the rank of the player
                  //filter : "opacity(" + (1 - (player.rank - 1) / players.size) * 100 + "%)"
               }}></div>
               <div class="profile">
                  <p>{rank}: {player.name}</p>
                  <p>NW: {player.netWorth}</p>
               </div>
            </div>
         )
      });
   }

   restart = () => {
      // function to restart the game
   }

}

export default Results;
