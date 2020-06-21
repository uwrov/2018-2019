var socket = require('socket.io-client')('http://localhost:4000');
/**
socket.on('connect', function(){
   console.log("connected!");
   setTimeout(() => {socket.emit('message', 'Hello there!')}, 1000);
});
socket.on('message', function(data){
   console.log("data: " + data.hello);
   setTimeout(() => {
      socket.emit('message', {'message':'Hello there!'})
   }, 1000);
});
socket.on('disconnect', function(){
   console.log("disconnected");
});
socket.on('requestPlayerTurn', function () {
    console.log("requested players turn");
    socket.emit('getPlayersTurn');
});
socket.on('getPlayerTurn', function (data) {

})
*/

let playerIndexCopy = null;
let playerListCopy = [];
let stockMarketCopy = [];
let marketCardsCopy = [];
let playerIdCopy = null;


socket.on('Market Cards', function(market_cards){
   console.log(market_cards)
   marketCardsCopy = market_cards
});

socket.on('Player Data', function(player_list){
   console.log(player_list)
   playerListCopy = player_list
});

socket.on('Player Index', function(player_index){
   console.log(player_index)
   playerIndexCopy = player_index
});

socket.on('Stock Market', function(stock_market){
   console.log(stock_market)
   stockMarketCopy = stock_market
});

socket.on('Player List', function(player_list){
   console.log(player_list)
   playerListCopy = player_list
});

socket.on('connected', function(player_id_generator){
   console.log(player_id_generator)
   playerIdCopy = player_id_generator
});

socket.emit("Get Market");
socket.emit("Get Players");
socket.emit("Get Player Index");
socket.emit("Get Stock Market");
socket.emit("Create Player", { "id": 1, "name":"Real Justin"});
socket.emit("connect");

// socket.on(function(data){
//
// });
//
// socket.emit("Sell Card");

// console.log("init");
