'use strict';
const ul = document.getElementById('target');
const names = ['John', 'Paul', 'Jones'];

for (let i = 0; i < names.length; i++) {
  const li = document.createElement('li');
  li.innerHTML = names[i];
  ul.appendChild(li);
}
