/*
*
*/

(function() {
	"use strict";

	window.addEventListener("load", init);

	/**
    *	Is to be called when the page loads. initiates all the event listener in the starting
    * 	screen
    */
  	function init() {
		document.getElementById("add").addEventListener("click", add);
		document.getElementById("subtract").addEventListener("click", subtract);
  	}

	function add() {
		let a = document.getElementById("num_a").value;
		let b = document.getElementById("num_b").value;
		a = parseFloat(a);
		b = parseFloat(b);
		document.getElementById("ans").innerText = a + b;

	}

	function subtract() {
		let a = document.getElementById("num_a").value;
		let b = document.getElementById("num_b").value;
		a = parseFloat(a);
		b = parseFloat(b);
		document.getElementById("ans").innerText = a - b;
	}
})();
