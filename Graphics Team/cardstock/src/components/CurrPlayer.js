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
                  {
                     this.stockInfo(this.props.info.stock)
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
   stockInfo(stocks) {
      return stocks.map(function(stock) {
         // Maybe include the value of the stocks as well.
         // In order to do this, I must give access to the
         // market field.
         return <li># of {stock.company} Stock: {stock.stock}</li>
      });
   }

}
export default CurrPlayer;
