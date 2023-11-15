'use strict';
const question = confirm("Should I calculate the square root?");
let result

if (question) {
  const number = parseInt(prompt(`Enter a number: `));
  if (number < 0) {
  result = "The square root of a negative number is not defined";
  document.querySelector('#squareRoot').innerHTML = result;
} else {
  const squareRoot = Math.sqrt(number);
  result = `The square root of the number ${number} is ${squareRoot}`;
  document.querySelector('#squareRoot').innerHTML = result;
}}
else {
  result = "The square root is not calculated.";
  document.querySelector('#squareRoot').innerHTML = result;
}
