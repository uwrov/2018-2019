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

socket.emit("Get Stock Market", {Target = 0, Player});

console.log("init");