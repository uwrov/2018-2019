import React from 'react';
import './CurrPlayer.css';

class CurrPlayer extends React.Component {
   render() {
      return (
         <div className="currPlayer">
            <h3>Current Player Info: </h3>
            <div>
               {
                  this.getPlayers(this.props.info)
               }
            </div>
         </div>
      );
   }

   getPlayers(info) {
      return (
         <div>
            <p>Name: {info.name}</p>
            <p>Money: {info.money}</p>
         </div>
      );
   }

}
export default CurrPlayer;
