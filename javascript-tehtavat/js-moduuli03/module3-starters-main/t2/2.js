const ul = document.getElementById('target');
const items = ['First item', 'Second item', 'Third item'];
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.innerHTML = items[i];
  ul.appendChild(li);
}

const secondLi= document.getElementsByTagName('li')[1];
secondLi.classList.add('my-list');