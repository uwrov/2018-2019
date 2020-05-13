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
      return this.props.market.map(function(card) {
         return(
            <Draggable>
               <div className="card">
                  <h2>Company: {card.company}</h2>
                  <h3># of stocks: {card.stock}</h3>
                  <h3>Price: {card.price}</h3>
               </div>
            </Draggable>
         )
      });//list of draggable cards
   }
}

export default MarketCards;
