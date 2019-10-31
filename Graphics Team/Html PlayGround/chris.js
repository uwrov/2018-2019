/*
*
*/

(function() {
	"use strict";


	let balance = 100;


	window.addEventListener("load", init);

	/**
    *	Is to be called when the page loads. initiates all the event listener in the starting
    * 	screen
    */
  	function init() {
		document.getElementById("add").addEventListener("click", add);
		document.getElementById("subtract").addEventListener("click", subtract);
		document.getElementById("heads").addEventListener("click", coinFlip);
		document.getElementById("tails").addEventListener("click", coinFlip);
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

	function getBet() {
		return document.getElementById("bet-input").value;
	}

	function coinFlip() {
		console.log("Click!");
		let bet = getBet();
		if(bet == null || bet > balance) {
			cantBet();
		} else {
			let guess = this.value;
			let num = Math.floor(Math.random() * 2);
			//heads = 1
			//tails = 0
			let result;
			if(num == 0) {
				result = "tails";
			} else if(num == 1) {
				result = "heads";
			}

			let win = result == guess;
			if(win) {
				balance += parseInt(bet);
				document.getElementById("coin-results").innerText = "You win!";
			} else {
				balance -= parseInt(bet);
				document.getElementById("coin-results").innerText = "You lose!";
			}
			updateBalance();
			document.getElementById("coin-results").innerText += " Flip was " + result +
												", Your guess was " + guess + "!";

		}
	}

	function cantBet() {
		document.getElementById("coin-results").innerText = "You don't have enough money!";
	}

	function updateBalance() {
		document.getElementById("balance").innerText = balance;
	}

})();
