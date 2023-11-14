const numberOfCandidates = parseInt(prompt('Enter the number of candidatess:'));
const candidates = [];

for (let i = 1; i <= numberOfCandidates; i++) {
  const nameOfCandidate = prompt(`Name for candidate ${i}`);
  let candidate = {
    name: nameOfCandidate,
    votes: 0
  };
  candidates.push(candidate);
}

const numberOfVoters = parseInt(prompt('Enter the number of voters'));
for (let j = 1; j <= numberOfVoters; j++) {
  const vote = prompt(`Voter ${j}. Enter the name of the candidate:`);
  const foundCandidate = candidates.find(candidate => candidate.name === vote);
  if (foundCandidate) {
    foundCandidate.votes ++;
  }
}

candidates.sort((a, b) => b.votes - a.votes);

console.log(`The winner is ${candidates[0].name} with ${candidates[0].votes} votes.`);
console.log('results:')
for (let z = 0; z < candidates.length; z++) {
  console.log(`${candidates[z].name}: ${candidates[z].votes} votes\n`)
}


