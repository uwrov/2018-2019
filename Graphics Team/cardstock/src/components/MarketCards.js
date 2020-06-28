import React from "react";
import Draggable from 'react-draggable';
import "./MarketCards.css";

class MarketCards extends React.Component {

   render() {
      return (
         <div className="cardMarket">
            {this.renderCards()}
         </div>
      );
   }

   renderCards = () => {
      return this.props.market.map((card, index) => {
         return(
            <Draggable bounds="parent">
               <div className="card">
                  <h3>Company: {card.company}</h3>
                  <p># of stocks: {card.stock}</p>
                  <p>Price: {card.price}</p>
                  <div className="buy" onClick={() => {this.handleBuy(index)}}>
                     BUY
                  </div>
               </div>
            </Draggable>
         )
      });//list of draggable cards
   }

   handleBuy = (index) => {
      // increment the # of stock by 1?
      //this.props.buy;
      if(this.props.onBuy instanceof Function) {
         this.props.onBuy(index);
      } else {
         console.log("Error: no function was supplied!");
      }
   }
}

export default MarketCards;
