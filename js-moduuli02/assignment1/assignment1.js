const userNumbers = [];

for (let i = 0; i < 5; i++) {
  const userInput = parseInt(prompt(`Enter the ${i + 1}. number.`))
  userNumbers.push(userInput);
}

console.log("Numbers in reverse order: ")
for (let j = userNumbers.length - 1; j >= 0; j--) {
  console.log(userNumbers[j]);
}