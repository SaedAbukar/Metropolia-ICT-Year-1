'use strict';
const name = prompt(`Enter your name: `);
const classNum = Math.floor(Math.random() * 4) + 1;

let house;

if (classNum === 1) {
  house = 'Gryffindor';
}
else if (classNum === 2) {
  house = 'Slytherin';
}
else if (classNum === 3) {
  house = 'Hufflepuff';
}
else {
  house = 'Ravenclaw';
}

const result = `${name}, you are ${house}.`
document.querySelector('#house').innerHTML = result

// const options = ['G', 'S', 'H', 'R']
// const random = Math.floor(Math.random() * options.length)
//
// console.log(random)
//
// console.log(options[random])