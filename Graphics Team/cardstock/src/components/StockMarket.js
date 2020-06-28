import React from 'react';
import './StockMarket.css';

class StockMarket extends React.Component {
   constructor(props) {
      super(props);

   }

   render() {
      return (
         <div className="stock_market">
            <ul>
               {this.renderStocks()}
            </ul>
         </div>
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
