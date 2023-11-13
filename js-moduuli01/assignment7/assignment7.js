'use strict';
const diceRolls = parseInt(prompt(`Enter the number of dice rolls: `));
let result

if (!isNaN(diceRolls) && diceRolls > 0) {
  let sum = 0;

  for (let i = 0; i < diceRolls; i++) {
    const diceThrows = Math.floor(Math.random() * 6) + 1;
    sum += diceThrows;
  }

    result = `The sum of the results of dice rolls is ${sum}.`;
    document.querySelector('#diceRolls').innerHTML = result;
}
else {
  result = 'Please enter a valid number of dice rolls.';
  document.querySelector('#diceRolls').innerHTML = result;
}


