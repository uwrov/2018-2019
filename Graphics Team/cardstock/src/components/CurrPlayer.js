import React from 'react';
import './CurrPlayer.css';

class CurrPlayer extends React.Component {
   render() {
      return (
         <div className="currPlayer">
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
            <span>Name: {info.name}</span>
            <span>Money: {info.money}</span>
         </div>
      );
   }

}
export default CurrPlayer;
