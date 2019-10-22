/*
*	This is the main javascript file for the vase breaker project.
*/

let numVases = 0; //increases by one everytime a vase is clicked, and will accumulate
let time = 0; // increases by one every second until gameState is false
let gameState = true; // will become false when manager is present, and a vase is clicked
let managerPresence = false; // appears(and become true) every five seconds, and remains for two seconds
let vaseSpeed = 5; // takes five seconds to cross the screen
let lightsFlicker = false; //will be true a second before the managerPresence is true.
function vaseButton() {
	//when clicked, broken vase image(Google it)
	//it will not disappear. it will only stay on the conveyer
	// every time tshis function is triggered numVase++
	//hitBox = rectangle

}
function vaseMovement() {
	//position time  -> a displacement funtion with respect to time?

}
function scoreBoard() {
	//timePassed
	//score
}
function manager() {
  //managerPresence
	//lights flicker
}



(function() {
	"use strict";

	//
	//	Init will run when the web page loads.
	//

	window.addEventListener("load", init);

	/**
    *	Is to be called when the page loads. initiates all the event listener in the starting
    * 	screen
    */


  	function init() {

  	}


})();
