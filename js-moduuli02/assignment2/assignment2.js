const numOfParti = parseInt(prompt(`Enter the number of participants`));
const namesList = [];
const orderList = document.createElement('ol');

for (let i = 1; i <= numOfParti; i ++) {
  const names = prompt(`Enter the name of ${i}. participant.`);
  namesList.push(names);
  const listItem = document.createElement('li');
  listItem.textContent = names;
  orderList.appendChild(listItem);
}

document.body.appendChild(orderList);
