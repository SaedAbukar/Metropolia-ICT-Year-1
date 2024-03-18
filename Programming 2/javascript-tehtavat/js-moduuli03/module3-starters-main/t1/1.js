const ul = document.getElementById('target');
const items = ['First item', 'Second item', 'Third item'];
for (let i = 0; i < items.length; i++) {
  let li = document.createElement('li');
  li.innerHTML = items[i];
  ul.append(li);
}
ul.classList.add('my-list');
