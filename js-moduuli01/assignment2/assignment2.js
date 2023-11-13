'use strict';
const name = prompt(`Enter your name: `);
// console.log(`Hello ${name}!`);
document.querySelector('#greet').innerHTML = `Hello ${name}!`