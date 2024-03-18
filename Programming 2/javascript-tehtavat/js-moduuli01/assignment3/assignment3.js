'use strict';
const num1 = prompt(`Enter the first number: `);
const num2 = prompt(`Enter the second number: `);
const num3 = prompt(`Enter the third number: `);

const intNum1 = parseInt(num1);
const intNum2 = parseInt(num2);
const intNum3 = parseInt(num3);

const sum = intNum1 + intNum2 + intNum3;
const product = intNum1 * intNum2 * intNum3;
const average = sum / 3;

const resultSum = `Sum: ${sum}`;
const resultPro = `Product: ${product}`;
const resultAvg = `Average: ${average}`;

document.querySelector('#sum').innerHTML = resultSum;
document.querySelector('#product').innerHTML = resultPro;
document.querySelector('#average').innerHTML = resultAvg;
