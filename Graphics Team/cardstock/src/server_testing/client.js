
const WebSocket = require('ws');
var url = "wss://localhost:4000";
var protocols = "protocolOne";
webSocket = new WebSocket(url, protocols);
//webSocket.send("hello, can you hear me");
webSocket.onopen = function (event) {
    webSocket.send("hello, can you hear me?");
};
webSocket.onmessage = function (event) {
    console.log("server recievved the message from the server");
    var state = JSON.parse(event)

}



