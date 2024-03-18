'use strict';
function concat(array) {
  let newList = '';
  for (let i = 0; i < array.length; i++) {
    newList += array[i];
  }
  return newList;
}
const list = ["Saed", "made", "this", "one"];
const result = concat(list);

const headOne = document.createElement('h1');
headOne.textContent = result;

document.body.appendChild(headOne);