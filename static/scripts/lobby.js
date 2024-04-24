const players = document.querySelector(".row").querySelectorAll(".col").length;
const playersCount = document.querySelector("#players-count").value;
const lobbyId = parseInt(location.href.split("/").at(-1));
const socket = io();
let actionButtons = document.querySelectorAll("input");
let playersLife;
let playerRole;
let hod;

if (players == playersCount) {
    console.log("lobby full");
    let xhr = new XMLHttpRequest();
    xhr.open("POST", `http://127.0.0.1:1234/distribution_roles/`);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify({lobby_id: lobbyId}));
    xhr.onload = function () {
        if (xhr.status == 200) {
            let response = JSON.parse(xhr.response);
            let userId = response["user_id"];
            console.log("response successful");
            let cardFooters = document.querySelectorAll(".card-footer");
            actionButtons = document.querySelectorAll("input");
            let localPlayersLife = localStorage.getItem("playersLife");
            console.log(localPlayersLife);
            if (localPlayersLife) {
                playersLife = JSON.parse(localPlayersLife);
            }
            else {
                playersLife = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1, "9": 1}
            }
            let localHod = localStorage.getItem("hod");
            if (localHod) {
                hod = localHod;
            }
            else {
                hod = 0;
            }
            playerRole = response[userId];
            console.log(playerRole);
            localStorage.setItem("playersLife", JSON.stringify(playersLife));
            localStorage.setItem("hod", hod);



            for (let i = 0; i < players; i++) {
                cardFooters[i].innerHTML = response[String(i)];
            }
//            if (cardFooters[userId].innerHTML == "mafia" && playersLife[userId]) {
            if (hod % 3 == 0 && ["mafia", "don", "sheriff", "civilian"].includes(cardFooters[userId].innerHTML) && playersLife[userId]) {
                for (let j = 0; j < players; j++) {
//                    if (["civilian", "sheriff"].includes(cardFooters[j].innerHTML)) {
                    if (j != userId && playersLife[j]) {
                        actionButtons[j].classList.add("btn-danger");
                        actionButtons[j].value = "убить";
                        actionButtons[j].hidden = false;
                        actionButtons[j].addEventListener("click", function () {
                            socket.emit("kill", {player_id: j, lobby_id: lobbyId});
                        })
                    };
                }
            }
            else if (hod % 3 == 1 && ["mafia", "don", "sheriff", "civilian"].includes(cardFooters[userId].innerHTML) && playersLife[userId]) {
                for (let j = 0; j < players; j++) {
                    if (j != userId && playersLife[j]) {
                        actionButtons[j].classList.add("btn-info");
                        actionButtons[j].value = "проверить";
                        actionButtons[j].hidden = false;
                        actionButtons[j].addEventListener("click", function () {
                            socket.emit("kill", {player_id: j, lobby_id: lobbyId});
                        })
                    };
                }
            }
        }
        else {
            console.log('not 200');
        }
    };
}
socket.on("kill successful", function (data) {
    console.log("kill successful");
    actionButtons.forEach((el) => {
        el.hidden = true; 
        el.classList.remove("btn-danger");
    });
    playersLife[String(data["player_id"])] = 0;
    localStorage.setItem("playersLife", JSON.stringify(playersLife));
    hod++;
    localStorage.setItem("hod", hod);
    document.querySelector("#player-move").innerHTML = hod;
    console.log(playersLife);
});
