'use strict';
const img = document.querySelector('#start-img');
const penaltyImg = document.querySelector('#penalty-img');


const O = "\u26BD";
const divpen1 = document.createElement('div');
const roundInfo = document.createElement('p');
const scoreInfo = document.createElement('p');
const attemptInfo = document.createElement('p');

const divpen2 = document.createElement('div');
const shotDirection = document.createElement('p');
const resultInfo = document.createElement('p');

const divpen3 = document.createElement('div');
const finalResult = document.createElement('p');

const gamesElement = document.querySelector('.stats-games-target');
const winsElement = document.querySelector('.stats-wins-target');
const penStartDiv = document.querySelector('#penalty-start');

const startButton = document.getElementById('start-button');
const p1 = document.querySelector('#p1');
const p2 = document.querySelector('#p2');



// divpen1.classList.add('penalty-info');
divpen1.classList.add('hide');
roundInfo.classList.add('round-info');
scoreInfo.classList.add('score-info');
attemptInfo.classList.add('attempt-info');

// divpen2.classList.add('penalty-info');
divpen2.classList.add('hide');
shotDirection.classList.add('shot-direction');
resultInfo.classList.add('result-info');

// divpen3.classList.add('penalty-info');
divpen3.classList.add('hide');
finalResult.classList.add('final-result');

divpen1.append(roundInfo, scoreInfo, attemptInfo);
divpen2.append(shotDirection, resultInfo);
divpen3.append(finalResult);

const section = document.querySelector('section');
const divcontainer = document.querySelector('.container');
const main = document.querySelector('main');

section.append(divpen1, divpen2, divpen3);
main.append(section);
divcontainer.append(main);
document.body.append(divcontainer);

const divpen4 = document.createElement('div');
const button1 = document.createElement('button');
const button2 = document.createElement('button');


button1.id = 'button1';
button2.id = 'button2';
button1.value = '1';
button2.value = '2';
button1.type = 'submit';
button2.type = 'submit';
button1.textContent = 'Shoot to the left';
button2.textContent = 'Shoot to the right';

console.log(button1.value)

divpen4.classList.add('button')
button1.classList.add('hide');
button2.classList.add('hide');
button1.classList.add('choice-button');
button2.classList.add('choice-button');

button1.setAttribute('data-selection', '1');
button2.setAttribute('data-selection', '2');

divpen4.append(button1, button2);
section.append(divpen4);
main.append(section);
divcontainer.append(main)
document.body.append(divcontainer);


roundInfo.innerHTML = 'Round: 0';
scoreInfo.innerHTML = 'Score: 0 - 0';
attemptInfo.innerHTML = 'Turn: -';
shotDirection.innerHTML = 'Shot direction: - , dive direction: -';
resultInfo.innerHTML = 'I might cheer you on...';
finalResult.innerHTML = 'The game will start when you pick your side!';



const selectionButtons = document.querySelectorAll('[data-selection]');
const SELECTIONS = [1, 2]

const stages = ['Group-Stage', 'Group-Stage', 'Group-Stage', 'Round of 16', 'Quarter-Finals', 'Semi-Finals', 'Final']
const TOTALGAMES = 7;
let gamesPlayed = 0;
let wins = 0;

if(gamesPlayed === TOTALGAMES) {
    penStartDiv.classList.add('hide');
    divpen1.classList.add('hide');
    divpen2.classList.add('hide');
    divpen3.classList.remove('hide')
    if (wins < 2 && gamesPlayed === 3) {
        penStartDiv.classList.add('hide');
        divpen1.classList.add('hide');
        divpen2.classList.add('hide');
        divpen3.classList.remove('hide');
        finalResult.innerText = `You lost 2 games out of 3. You didnt make it out the group stage... Better luck next time!`
    }
    if (wins > 3 && wins !== TOTALGAMES) {
        penStartDiv.classList.add('hide');
        divpen1.classList.add('hide');
        divpen2.classList.add('hide');
        divpen3.classList.remove('hide');
        finalResult.innerText = `You lost in the ${stages[wins + 1]} stage.. Valiant effort! Keep your head up!`
    }
    if (wins === 7) {
        penStartDiv.classList.add('hide');
        divpen1.classList.add('hide');
        divpen2.classList.add('hide');
        divpen3.classList.remove('hide');
        finalResult.innerText = `Congratulations! You are a World Champion!!`
    }
}



let numberRounds = 5;
const team1 = 'Suomi';
const team2 = 's';
let gameContinues = true;
let team1Score = 0;
let team2Score = 0;
let team1Turn = 0;
let team2Turn = 0;
let currentTeam = team2;
let rounds = 0;

function resetPenaltyGame () {
    setTimeout(function () {
        gameContinues = true;
        team1Score = 0;
        team2Score = 0;
        team1Turn = 0;
        team2Turn = 0;
        currentTeam = team2;
        rounds = 0;
        roundInfo.innerHTML = 'Round: 0';
        scoreInfo.innerHTML = 'Score: 0 - 0';
        attemptInfo.innerHTML = 'Turn: -';
        shotDirection.innerHTML = 'Shot direction: - , dive direction: -';
        resultInfo.innerHTML = 'I might cheer you on...';
        finalResult.innerHTML = 'The game will start when you pick your side!';

        penStartDiv.classList.add('hide');
        startButton.classList.add('hide');
        divpen1.classList.add('hide');
        divpen1.classList.remove('penalty-info');
        divpen2.classList.add('hide');
        divpen2.classList.remove('penalty-info');
        divpen3.classList.add('hide');
        divpen3.classList.remove('penalty-info');
        button1.classList.add('hide');
        button2.classList.add('hide');
        p1.classList.remove('hide');
        img.src = "../img/Suomen-MM-kisa-peli.jpg";
        // p2.classList.add('hide');
                }, 5000);}



selectionButtons.forEach(selectionButton => {
    selectionButton.addEventListener('click', e => {
        if (!gameContinues) {
            resetPenaltyGame();
            return; // Stop processing clicks if the game is over
        }
        if (Math.abs(team1Score - team2Score) > (numberRounds - rounds) && team1Turn === team2Turn) {
            gameContinues = false;
            console.log(`${team1} yritykset: ${team1Turn}`);
            console.log(`${team2} yritykset: ${team2Turn}`);
            console.log(`Peli päättyi! ${team1} teki ${team1Score} ja ${team2} teki ${team2Score}`);
            finalResult.innerHTML = `Game over! The Score is ${team1} ${team1Score} - ${team2} ${team2Score}.`;
            resetPenaltyGame();
            if (team1Score > team2Score) {
                gamesPlayed++;
                gamesElement.innerText = `${gamesPlayed}`;
                wins++;
                winsElement.innerText = `${wins}`
                finalResult.innerHTML = ` You won the game against ${team2}! Final score: ${team1Score} - ${team2Score}. This window will close soon. Continue your search for opponents!`
                resetPenaltyGame();
                return team1;
            } else if (team2Score > team1Score) {
                gamesPlayed++;
                gamesElement.innerText = `${gamesPlayed}`;
                finalResult.innerHTML = ` You lost the game against ${team2}... Final score: ${team1Score} - ${team2Score}. This window will close soon. Continue your search for opponents!`
                resetPenaltyGame();
                return team2;
            }
        }

        const selectionName = parseInt(selectionButton.dataset.selection);
        const selection = SELECTIONS.find(selection => selection === selectionName);
        makeSelection(selectionName)
        if (team1Turn === team2Turn) {
            rounds += 1;
            console.log(`KIERROS ${rounds}`);
            roundInfo.innerHTML = `Round: ${rounds}`;
        }
        console.log(`${team1} on tehnyt ${team1Score} maalia, ${team2} on tehnyt ${team2Score}.`);
        // scoreInfo.innerHTML = `Score: ${team1} ${team1Score} - ${team2} ${team2Score}`
        if (currentTeam === team1) {
            currentTeam = team2;
            button1.textContent = 'Shoot to the left';
            button2.textContent = 'Shoot to the right';
            console.log(`Nyt on ${currentTeam} joukkueen vuoro!`);
            attemptInfo.innerHTML = `Turn: ${team1}`
            team2Turn += 1;
        } else {
            currentTeam = team1;
            button1.textContent = 'Dive to the left';
            button2.textContent = 'Dive to the right';
            console.log(`Nyt on ${currentTeam} joukkueen vuoro`);
            attemptInfo.innerHTML = `Turn: ${team2}`
            team1Turn += 1;
        }

        let kick;
        if (currentTeam === team1) {
            // kick = parseInt(prompt("Kumpaan suuntaan haluat vetää? (1: vasemmalle/2: oikealle)\n"));
            kick = selection;
        } else {
            kick = Math.floor(Math.random() * 2) + 1;
        }

        let diveDirection;
        if (currentTeam === team2) {
            // diveDirection = parseInt(prompt("Minne maalivahti hyppää? (1: vasemmalle/2: oikealle)\n"));
            diveDirection = selection;
        } else {
            diveDirection = dive();
        }

        if (goal(kick, diveDirection)) {
            if (currentTeam === team1) {
                img.src = '../img/penalty-goal.gif'
                resultInfo.innerHTML = `Yes!! You scored a goal! The keeper had no chance!`
                finalResult.innerHTML = `Now It's time to save the penalty shot! Choose where do you want to dive!`
                team1Score += 1;
            } else {
                img.src = '../img/penalty-allowed.gif'
                resultInfo.innerHTML = `The opposition scored. You almost had it!`
                finalResult.innerHTML = `Now it's time to pay them back! Choose where do you want to shoot!`
                team2Score += 1;
            }
            console.log(`Veto: ${kick} Torjunta: ${diveDirection}`);
            console.log("Ja veto menee...");
            printBall(kick);
            console.log("Ja maalivahti menee...");
            printGoalkeeper(diveDirection);
            console.log(`${currentTeam} sai maalin!`);
            shotDirection.innerHTML = `Shot direction: ${kick}, Dive direction: ${diveDirection}`;
            scoreInfo.innerHTML = `Score: ${team1} ${team1Score} - ${team2} ${team2Score}`

            // if (currentTeam === team1) {
            //     team1Score += 1;
            // } else {
            //     team2Score += 1;
            // }
        } else {
            if (currentTeam === team1) {
                img.src = '../img/penalty-miss.gif'
                resultInfo.innerHTML = `Oh no! No goal! You missed the shot! Maybe next one!`
                finalResult.innerHTML = `Get yourself together. We got a game to win. Choose where do you want to dive!`
            } else {
                img.src = '../img/penalty-save.gif'
                resultInfo.innerHTML = `Yes! No goal! You saved the shot! Way to go!`
                finalResult.innerHTML = `That's more like it!! Now it's time to score! Choose where do you want to shoot!`
            }
            console.log(`Veto: ${kick} Torjunta: ${diveDirection}`);
            console.log("Ja veto menee...");
            printBall(kick);
            console.log("Ja maalivahti menee...");
            printGoalkeeper(diveDirection);
            console.log("Ei maalia. Maalivahti torjui vedon!");
            shotDirection.innerHTML = `Shot direction: ${kick}, Dive direction: ${diveDirection}`;
            scoreInfo.innerHTML = `Score: ${team1} ${team1Score} - ${team2} ${team2Score}`
        }
        if (rounds >= numberRounds && team1Score === team2Score && team1Turn === team2Turn) {
            console.log("Tasapeli! Siirrytään äkkikuolema -kierroksiin!");
            finalResult.innerHTML = `Draw! Now we move to sudden death rounds!`
            numberRounds++;
        }
    })
})

function makeSelection(selection) {
    console.log(selection)
}

function dive() {
    const number = Math.floor(Math.random() * 2) + 1;
    return number;
}

function goal(kickDirection, diveDirection) {
    return kickDirection !== diveDirection;
}

function printBall(ball) {
    if (ball === 1) {
        console.log("------------------");
        console.log(`| ${O}             |`);
        console.log("|                |");
        console.log("|                |");
    }

    if (ball === 2) {
        console.log("------------------");
        console.log(`|             ${O} |`);
        console.log("|                |");
        console.log("|                |");
    }
}

function printGoalkeeper(goalkeeper) {
    if (goalkeeper === 1) {
        console.log("-----------------");
        console.log("| _ o|          |");
        console.log("|    \\          |");
        console.log("|     \\\\\        |");
    }

    if (goalkeeper === 2) {
        console.log("-----------------");
        console.log("|          |o _ |");
        console.log("|          /    |");
        console.log("|        //     |");
    }
}
document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('start-button');

    startButton.addEventListener('click', function () {
        const button1 = document.querySelector('#button1');
        const button2 = document.querySelector('#button2');
        const p1 = document.querySelector('#p1');
        const p2 = document.querySelector('#p2');
        startButton.classList.add('hide');
        divpen1.classList.remove('hide');
        divpen1.classList.add('penalty-info');
        divpen2.classList.remove('hide');
        divpen2.classList.add('penalty-info');
        divpen3.classList.remove('hide');
        divpen3.classList.add('penalty-info');
        button1.classList.remove('hide');
        button2.classList.remove('hide');
        p1.classList.add('hide');
        // p2.classList.remove('hide');
    });
});



