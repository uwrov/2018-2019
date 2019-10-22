/*
*	This is the main javascript file that me, Andrew Jang, will be updating to help organize
*	everything on the page. It will also be an example for style guidelines that we will
*	practice for the entirety of programming the actual graphics ui. 
*
*	Hopefully everything is legible and if there are any questions you can come by me. 
*/

(function() {
	"use strict"; //important cause catches more bugs more often.


	/*
	*	Example comment:
	*
	*	(description of the function, try to keep everything that happens internally
	*	out of the description. A simple format will be what the method takes in, 
	*	what it does to it, or what it does in the whole scope of the program, and what 
	*	it returns)
	*
	*	@param (var name) any variables that are part of the parameters
	*	....
	*
	*	@return description of the value the method returns. 
	*
	*	@exception (type of exception) Any exceptions that will possibly be thrown. 
	*/

	/*
	*	Any variables that should be initialized should be at the beginning of the program. 
	*/

	//	Init will run when the web page loads. 
	//
	//	*******IMPORTANT FOR EVERYONE ELSE CREATING THEIR SEPARATE JAVASCRIPT FILES********
	//
	//	This is how everything should be initialized in your separate files(Adding event 
	//	listeners and etc.) First add a event listener to "load" and creating an init()
	//	function that starts at the load of the page. 
	window.addEventListener("load", init);

	/**
    *	Is to be called when the page loads. initiates all the event listener in the starting
    * 	screen
    */
  	function init() {
    	document.getElementById('demo-button').addEventListener('click', demoButtonClick);
  	}

  	/**
  	*	Is to be called when the demo button is clicked. Changes the color of the demo button
  	*	on the page.
  	*/
  	function demoButtonClick() {
  		console.log("Click!");
  		document.getElementById('demo-button').style.backgroundColor = getRandomColor();
  	}

  	/**
  	*	Returns a random hexadecimal that corolates to a random color. 
  	*
  	*	@return a random hexadecimal
  	*/
	function getRandomColor() {
		var letters = '0123456789ABCDEF';
		var color = '#';
		for (var i = 0; i < 6; i++) {
		    color += letters[Math.floor(Math.random() * 16)];
		}
		return color;
	}
})();