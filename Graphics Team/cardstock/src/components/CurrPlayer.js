import React from 'react';
import './CurrPlayer.css';

class CurrPlayer extends React.Component {

   render() {
      return (
         <div id="currPlayer">
            <h2>Current Player Info: </h2>
            <p>
               {
                  this.getPlayers(this.props.info)
               }
               {
                  this.stockInfo(this.props.info.stock)
               }
            </p>
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
