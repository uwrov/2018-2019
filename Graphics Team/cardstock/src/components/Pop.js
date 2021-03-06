import React from 'react';
import './Pop.css';

class Pop extends React.Component {
   state = {
      message: "This is a popup!"
      //change message if: error when buying card, last turn
   }

   constructor(props) {
      super(props);
      this.state.message = props.message;
   }

   render() {
      return (
         <div>
            <div class="box">
               <h1 class="message">{this.state.message}</h1>
               <div
                  class="resume"
                  onClick={() => {this.resume()}}>
                  resume
               </div>
            </div>
         </div>
      )
   }

   resume = () => {
      this.props.pop();
   }
}

export default Pop;
