import React from 'react';
import './StockMarket.css';
import Draggable from 'react-draggable';

class StockMarket extends React.Component {
   constructor(props) {
      super(props);

   }

   render() {
      return (
         <Draggable grid={[80, 80]}>
            <div className="stock_market">
               <ul>
                  {this.renderStocks()}
               </ul>
            </div>
         </Draggable>
      )
   }

   renderStocks = () => {
      let list = [];
      for(let key in this.props.stock_price) {
         let detail = (<li>{key}: ${this.props.stock_price[key]}</li>);
         list.push(detail);
      }
      return list
   }
}

export default StockMarket;
