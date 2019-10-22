/*
*	This is the main javascript file for the vase breaker project.
*/

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
    	document.getElementById('demo-button').addEventListener('click', demoButtonClick);
  	}

  
})();