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
            "net_worth": 100,
            "rank": 1
         },
         {
            "id": 1,
            "name": "Andrew",
            "net_worth": 75,
            "rank": 2
         },
         {
            "id": 2,
            "name": "Justin",
            "net_worth": 50,
            "rank": 3
         },
         {
            "id": 3,
            "name": "Alex",
            "net_worth": 25,
            "rank": 4
         }
      ]
   }

   constructor(props) {
      super(props);

      this.props.socket.on("End Results", this.updateResultsList);
   }

   componentDidMount() {
      this.props.socket.emit("Get Results");
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

   updateResultsList = (list) => {
      console.log(list);
      console.log("uwu");
      this.setState({ playerList: list });
   }

   rankPlayers(players) {
      let maxNet = 0;
      players.forEach(function(player) {
         if(player.net_worth > maxNet) {
            maxNet = player.net_worth;
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
                  height : (player.net_worth / maxNet) * 280 + "px",
                  // attempting to adjust the bar appearance depending on the rank of the player
                  //filter : "opacity(" + (1 - (player.rank - 1) / players.size) * 100 + "%)"
               }}></div>
               <div class="profile">
                  <p>{rank}: {player.name}</p>
                  <p>Net: {player.net_worth}</p>
               </div>
            </div>
         )
      });
   }

   restart = () => {
      // function to restart the game
      this.props.socket.emit("Reset Server");
   }

}

export default Results;
