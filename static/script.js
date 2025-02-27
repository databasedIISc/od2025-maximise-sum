const boardLength = 14

let numbers = [];
let playerChoice = 1;
let leftIndex = 0, rightIndex = boardLength - 1;
let playerScores = {1: 0, 2: 0};
let currentPlayer = 1;
let waiting = false;

async function startGame(player) {
    playerChoice = player;
    leftIndex = 0;
    rightIndex = boardLength - 1;
    playerScores = {1: 0, 2: 0};
    currentPlayer = 1;
    waiting = false;
    document.getElementById("result").innerHTML = "";
    document.getElementById("box-container").innerHTML = "";
    document.getElementById("confetti-container").style.display = "none";
    document.querySelector('body').style.background = "#f4f4f4";

    document.querySelector('.buttons').style.display = 'none';

    let response = await fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player: player, boardLength: boardLength })
    });

    let data = await response.json();
    numbers = data.numbers;
    displayBoxes();

    if (playerChoice === 2) {
        setTimeout(computerMove, 1000);
        
        // techincally, based on the existing organisation,
        // we should do this in the backend
        let os = 0, es = 0;
        for (i = 0; i < numbers.length; i++) {
            if ((i+1) % 2 == 0) es += numbers[i];
            else os += numbers[i]; }
        addComputerMsg("Since I am going first, I can use the <b>odd-even "+
        "strategy</b>. I see that the sum of the odd-indexed numbers is <b>" + os + "</b> while " +
        "that of the even-indexed ones is <b>" + es + "</b>. So, I will try to pick the "+
        (os > es ? "odd" : "even") + "-indexed numbers.");
    }
}

function displayBoxes() {
    let container = document.getElementById('box-container');
    container.innerHTML = '';

    numbers.forEach((num, index) => {
        let box = document.createElement('div');
        box.classList.add('box');
        box.textContent = num;
        box.dataset.index = index;

        if (index === leftIndex || index === rightIndex) {
            box.addEventListener('click', () => handlePlayerMove(index));
        }

        container.appendChild(box);
    });

    updateScoreDisplay();
}

async function handlePlayerMove(index) {
    if (waiting || (index !== leftIndex && index !== rightIndex)) return;

    let selectedBox = document.querySelector(`.box[data-index='${index}']`);
    selectedBox.classList.add('disabled');

    playerScores[currentPlayer] += numbers[index];

    if (index === leftIndex) leftIndex++;
    else rightIndex--;

    updateClickableBoxes();
    updateScoreDisplay();
    addPlayerMsg("I pick " + numbers[index] + ".");

    currentPlayer = 3 - currentPlayer;
    waiting = true;

    if (leftIndex <= rightIndex) {
        setTimeout(computerMove, 1000);
    } else {
        showFinalResult();
    }
}

function updateClickableBoxes() {
    let boxes = document.querySelectorAll('.box');
    boxes.forEach((box, index) => {
        if (index === leftIndex || index === rightIndex) {
            box.style.opacity = '1';
            box.addEventListener('click', () => handlePlayerMove(index));
        } else {
            box.style.opacity = '1';
            box.removeEventListener('click', handlePlayerMove);
        }
    });
}

function showConfetti() {
    let confettiContainer = document.getElementById("confetti-container");
    confettiContainer.innerHTML = ""; // Clear previous confetti
    confettiContainer.style.display = "block";

    for (let i = 0; i < 100; i++) { // Generate 100 confetti pieces
        let confetti = document.createElement("div");
        confetti.classList.add("confetti");
        confetti.style.left = `${Math.random() * 100}vw`; // Random horizontal position
        confetti.style.animationDuration = `${Math.random() * 2 + 1}s`; // Random fall speed
        confetti.style.backgroundColor = getRandomColor(); // Random color

        confettiContainer.appendChild(confetti);
    }

    setTimeout(() => {
        confettiContainer.style.display = "none"; // Hide after some time
    }, 3000);
}

function getRandomColor() {
    let colors = ["gold", "red", "blue", "green", "purple", "pink", "orange"];
    return colors[Math.floor(Math.random() * colors.length)];
}

async function computerMove() {
    let response = await fetch('/computer-move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            player: playerChoice,
            numbers: numbers.slice(leftIndex, rightIndex + 1)
        })
    });

    let data = await response.json();
    let move = data.choice;
    let moveIndex = numbers.indexOf(move);

    let selectedBox = document.querySelector(`.box[data-index='${moveIndex}']`);
    selectedBox.classList.add('disabled');

    playerScores[currentPlayer] += move;

    if (moveIndex === leftIndex) leftIndex++;
    else rightIndex--;

    updateClickableBoxes();
    updateScoreDisplay();
    addComputerMsg(data.explanation);

    currentPlayer = 3 - currentPlayer;
    waiting = false;

    if (leftIndex > rightIndex) {
        showFinalResult();
    }
}

function updateScoreDisplay() {
    document.getElementById('result').innerHTML = `
        <h3>Scores</h3>
        <p>Player 1: ${playerScores[1]}</p>
        <p>Player 2: ${playerScores[2]}</p>
    `;
}

function showFinalResult() {
    let winnerText = playerScores[1] > playerScores[2] ? "Player 1 Wins!" :
                    playerScores[2] > playerScores[1] ? "Player 2 Wins!" :
                    "It's a Tie!";
    
    document.getElementById('box-container').innerHTML = "";
    document.getElementById('result').innerHTML = `
        <h2>Game Over</h2>
        <p>Player 1 Score: ${playerScores[1]}</p>
        <p>Player 2 Score: ${playerScores[2]}</p>
        <h2>${winnerText}</h2>
    `;

    if (playerScores[playerChoice] > playerScores[3 - playerChoice]) {
        showConfetti();
    } else {
        document.body.style.background = "#333";
        document.getElementById("result").style.color = "white";
    }
}

function addComputerMsg(msg) {
    let txt = "<div class=\"emsg cmsg\">" + msg + "</div>";
    console.log(txt);
    let e = document.getElementById("explainc");
    e.insertAdjacentHTML('beforeend', txt);
    e.lastElementChild.scrollIntoView();
}

function addPlayerMsg(msg) {
    let txt = "<div class=\"emsg ymsg\">" + msg + "</div>";
    console.log(txt);
    let e = document.getElementById("explainc");
    e.insertAdjacentHTML('beforeend', txt);
    e.lastElementChild.scrollIntoView();
}

function toggleExplanation() {
    let x = document.getElementById("explain");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
