'use strict';
const CENTER = 0;
const LEFT = 1;
const RIGHT = 2;

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

divpen4.append(button1, button2);
section.append(divpen4);
main.append(section);
divcontainer.append(main)
document.body.append(divcontainer);



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

function penalties(team) {
    console.log("-----------------");
    console.log("|     _ o _     |");
    console.log("|       |       |");
    console.log("|      / \\      |");

    let numberRounds = 5;
    const team1 = 'Suomi';
    const team2 = team;
    let gameContinues = true;
    let team1Score = 0;
    let team2Score = 0;
    let team1Turn = 0;
    let team2Turn = 0;
    let currentTeam = team2;
    let rounds = 0;

    while (gameContinues) {
        if (Math.abs(team1Score - team2Score) > (numberRounds - rounds) && team1Turn === team2Turn) {
            gameContinues = false;
        } else {
            if (team1Turn === team2Turn) {
                rounds += 1;
                console.log(`KIERROS ${rounds}`);
                roundInfo.innerHTML = `Round: ${rounds}`;
            }
            console.log(`${team1} on tehnyt ${team1Score} maalia, ${team2} on tehnyt ${team2Score}.`);
            scoreInfo.innerHTML = `Score: ${team1} ${team1Score} - ${team2} ${team2Score}`
            if (currentTeam === team1) {
                currentTeam = team2;
                console.log(`Nyt on ${currentTeam} joukkueen vuoro!`);
                attemptInfo.innerHTML = `Turn: ${currentTeam}`
                team2Turn += 1;
            } else {
                currentTeam = team1;
                console.log(`Nyt on ${currentTeam} joukkueen vuoro`);
                attemptInfo.innerHTML = `Turn: ${currentTeam}`
                team1Turn += 1;
            }

            let kick;
            if (currentTeam === team1) {
                kick = parseInt(prompt("Kumpaan suuntaan haluat vetää? (1: vasemmalle/2: oikealle)\n"));
                // kick = 1;
            } else {
                kick = Math.floor(Math.random() * 2) + 1;
            }

            let diveDirection;
            if (currentTeam === team2) {
                diveDirection = parseInt(prompt("Minne maalivahti hyppää? (1: vasemmalle/2: oikealle)\n"));
                // diveDirection = 2;
            } else {
                diveDirection = dive();
            }

            if (goal(kick, diveDirection)) {
                console.log(`Veto: ${kick} Torjunta: ${diveDirection}`);
                console.log("Ja veto menee...");
                printBall(kick);
                console.log("Ja maalivahti menee...");
                printGoalkeeper(diveDirection);
                console.log(`${currentTeam} sai maalin!`);
                shotDirection.innerHTML = `Shot direction: ${kick}, Dive direction: ${diveDirection}`;
                resultInfo.innerHTML = `Goal! ${currentTeam} scored!`

                if (currentTeam === team1) {
                    team1Score += 1;
                } else {
                    team2Score += 1;
                }
            } else {
                console.log(`Veto: ${kick} Torjunta: ${diveDirection}`);
                console.log("Ja veto menee...");
                printBall(kick);
                console.log("Ja maalivahti menee...");
                printGoalkeeper(diveDirection);
                console.log("Ei maalia. Maalivahti torjui vedon!");
                shotDirection.innerHTML = `Shot direction: ${kick}, Dive direction: ${diveDirection}`;
                resultInfo.innerHTML = `No goal! The keeper saved the shot!`
            }

            if (rounds >= numberRounds && team1Score === team2Score && team1Turn === team2Turn) {
                console.log("Tasapeli! Siirrytään äkkikuolema -kierroksiin!");
                finalResult.innerHTML = `Draw! Now we move to sudden death rounds!`
                numberRounds++;
            }
        }
    }

    console.log(`${team1} yritykset: ${team1Turn}`);
    console.log(`${team2} yritykset: ${team2Turn}`);
    console.log(`Peli päättyi! ${team1} teki ${team1Score} ja ${team2} teki ${team2Score}`);
    finalResult.innerHTML = `Game over! The Score is ${team1} ${team1Score} - ${team2} ${team2Score}`;
    if (team1Score > team2Score) {
        return team1;
    } else if (team2Score > team1Score) {
        console.log(`Ottelun voittaja on ${team2}!`);
        return team2;
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
        p2.classList.remove('hide');

        // Start the penalty shootout when the button is clicked
        penalties('TeamB');
    });
});
