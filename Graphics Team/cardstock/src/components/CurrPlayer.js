import React from 'react';
import './CurrPlayer.css';
import Draggable from 'react-draggable';

class CurrPlayer extends React.Component {
   render() {
      return (
         <Draggable grid={[80, 80]}>
            <div className="currPlayer">
               <h2>Current Player Info: </h2>
               <div>
                  {
                     this.getPlayers(this.props.info)
                  }
               </div>
            </div>
         </Draggable>
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
