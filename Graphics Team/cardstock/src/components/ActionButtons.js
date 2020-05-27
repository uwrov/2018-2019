import React from "react";
import "./ActionButtons.css";

class ActionButtons extends React.Component {

   //
   // Properties to be handling:
   // this.props.onSkipTurn:
   //
   render() {
      return (
         <div className="actionbuttons">
            <div className="skipButton" onClick={this.handleSkip}>
               End turn!
            </div>
         </div>
      );
   }

   handleSkip = () => {
      if(this.props.onSkipTurn instanceof Function) {
         this.props.onSkipTurn();
      } else {
         console.log("Error: no function was supplied!");
      }
   }
}

export default ActionButtons;
