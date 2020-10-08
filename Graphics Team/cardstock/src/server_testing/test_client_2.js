var socket = require('socket.io-client')('http://localhost:4000');

let playerIndexCopy = null;
let playerListCopy = [];
let stockMarketCopy = [];
let marketCardsCopy = [];
let playerIdCopy = null;


socket.on('connect', function(){
   socket.emit("Get Stock Graph");
});

socket.on('Market Cards', function(market_cards){
   console.log("market cards")
   console.log(market_cards)
   marketCardsCopy = market_cards
});

socket.on('Player Index', function(player_index){
   playerIndexCopy = player_index
});

socket.on('Stock Market', function(stock_market){
   console.log("stock market ")
   console.log(stock_market)
   stockMarketCopy = stock_market
});

socket.on('Player List', function(player_list){
   console.log("player list ");
   console.log(JSON.stringify(player_list));
   playerListCopy = player_list;
   console.log("playerListCopy = " + JSON.stringify(playerListCopy));
});

socket.on('connected', function(player_id_generator){
   playerIdCopy = player_id_generator
});

socket.on('error', function(error){
   console.log("error: " + error.message);
});

socket.on('Stock Graph', function(image){
   console.log(image.image.toString("ascii"));
});

// socket.emit("Get Market");
// socket.emit("Get Players");
// socket.emit("Get Player Index");
// socket.emit("Get Stock Market");
// socket.emit("Create Player", { "id": 1, "name":"Real Justin"});



// setTimeout(function() {
//    console.log(playerListCopy[0]);
//    socket.emit("Buy Card", { "player": playerListCopy[0], "target":0});
// }, 1000);
//
// console.log(JSON.stringify(playerListCopy[0]));
//
// // setTimeout(function() {
// //    console.log(playerListCopy[0]);
// //    socket.emit("Buy Card", { "player": playerListCopy[0], "target":0});
// // }, 1000);
//
// console.log(JSON.stringify(playerListCopy[0]));
//
// setTimeout(function() {
//    console.log(playerListCopy[0]);
//    socket.emit("Sell Card", { "player": playerListCopy[0], "target":0});
// }, 1000);
//
// console.log(JSON.stringify(playerListCopy[0]));
