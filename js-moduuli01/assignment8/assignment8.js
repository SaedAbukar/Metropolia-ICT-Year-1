'use strict';

const startYear = parseInt(prompt('Enter the starting year:'));
const endYear = parseInt(prompt('Enter the end year:'));

const leapYearsList = document.getElementById('leapYear');

for (let i = startYear; i <= endYear; i += 4) {
  if ((i % 4 === 0 && i % 100 !== 0) || (i % 400 === 0)) {
    const listItem = document.createElement('li');
    listItem.textContent = i;
    leapYearsList.appendChild(listItem);
  }
}

// document.body.appendChild(leapYearsList);
