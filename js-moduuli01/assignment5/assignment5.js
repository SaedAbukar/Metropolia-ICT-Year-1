'use strict';

const year = prompt(`Enter a year: `);
const yearInput = parseInt(year);

if ((yearInput % 4 === 0 && yearInput % 100 !== 0) || (yearInput % 400 === 0)) {
  let result = `The year ${year} is a leap year`;
  document.querySelector('#year').innerHTML = result;
}
else {
  let result = `The year ${year} is not a leap year`;
  document.querySelector('#year').innerHTML = result;
}