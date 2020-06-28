import React from "react";
import "./PlayerCards.css";
import Draggable from 'react-draggable';

class PlayerCards extends React.Component {

   //
   // Properties to be handling:
   // this.props.onSkipTurn:
   //
   render() {
      return (
         <div className="playerCards">
            {this.displayPlayerCards()}
         </div>
      );
   }

   displayPlayerCards = () => {
      if(this.props.playerCards instanceof Array) {

         return this.props.playerCards.map((card, index) => {
            return (
               <Draggable bounds="parent">
                  <div className="playerCard">
                     <h2>Company: {card.company}</h2>
                     <h3># of stocks: {card.amount}</h3>
                     <div className="sellButton"
                     onClick={() => {this.handleSell(index)}}>
                        Sell!
                     </div>
                  </div>
               </Draggable>
            );
         });
      }
      return;
   }

   handleSell = (index) => {
      this.props.onSell(index);
   }
}

export default PlayerCards;
