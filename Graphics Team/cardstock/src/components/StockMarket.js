import React from 'react';
import './StockMarket.css';

class StockMarket extends React.Component {
   state = {
      image_src: null
   }

   constructor(props) {
      super(props);

      this.props.socket.on("Stock Graph", (image) => {
         this.setImage(image);
      })
   }

   setImage = (image) => {
      let typed_array = new Uint8Array(image.image);
      const data = typed_array.reduce((acc, i) => acc += String.fromCharCode.apply(null, [i]), '');
      //const string_char = String.fromCharCode.apply(null, typed_array);
      let imageurl = "data:image/png;base64, " + data;
      this.setState({ image_src: imageurl });
   }

   componentDidMount = () => {
      this.props.socket.emit("Get Stock Graph");
   }

   render() {
      return (
         <div className="stock_market">
            <img src={this.state.image_src} alt="Stock Graph"/>
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
