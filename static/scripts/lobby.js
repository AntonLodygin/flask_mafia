const lobbyId = parseInt(location.href.split("/").at(-1));
const socket = io();
let actionButtons = document.querySelectorAll("[type=button]");
let verdicts = document.querySelectorAll(p);
let cardFooters = document.querySelectorAll(".card-footer");
let lobbyId = parseInt(location.href.split("/").at(-1));
let userID;

socket.on("lobby full", function (data) {
    socket.emit("get roles");
});

socket.on("get roles successful", function (data) {
    for (let i = 0; i < 10; i++) {
        cardFooters[i].innerHTML = data["players_roles"][String(i)];
    }
    userId = data["user_id"];
    socket.emit("start game", {lobby_id: lobbyId})
});

socket.on("game", function (data) {
    let turn = data["turn"];
    document.querySelector("#player-turn");
    let playersLife = data["players_life"];
    let playersRoles = data["players_roles"];
    if (turn == playersRoles[userId] == "mafia" && playersLife[userId]) {
        for (let j = 0; j < 10; j++) {
//                    if (["civilian", "sheriff"].includes(playersRoles[j])) {
            if (j != userId) {
                actionButtons[j].classList.add("btn-danger");
                actionButtons[j].value = "Убить";
                actionButtons[j].hidden = false;
                actionButtons[j].addEventListener("click", function () {
                    socket.emit("kill", {player_id: j, lobby_id: lobbyId});
                    actionButtons.forEach((el) => {
                        el.hidden = true;
                        el.classList.remove("btn-danger");
                    });
                })
            };
        }
    }
    else if (turn == playersRoles[userId] == "don" && playersLife[userId]) {
        for (let j = 0; j < 10; j++) {
//                    if (["civilian", "sheriff"].includes(playersRoles[j])) {
            if (j != userId) {
                actionButtons[j].classList.add("btn-warning");
                actionButtons[j].value = "Проверить";
                actionButtons[j].hidden = false;
                actionButtons[j].addEventListener("click", function () {
                    socket.emit("check on sheriff", {player_id: j, lobby_id: lobbyId});
                    actionButtons.forEach((el) => {
                        el.hidden = true;
                        el.classList.remove("btn-warning");
                    });
                })
            };
        }
    }
    else if (turn == playersRoles[userId] == "sheriff" && playersLife[userId]) {
        for (let j = 0; j < 10; j++) {
            if (j != userId) {
                actionButtons[j].classList.add("btn-info");
                actionButtons[j].value = "Проверить";
                actionButtons[j].hidden = false;
                actionButtons[j].addEventListener("click", function () {
                    socket.emit("check on mafia", {player_id: j, lobby_id: lobbyId});
                    actionButtons.forEach((el) => {
                        el.hidden = true;
                        el.classList.remove("btn-info");
                    });
                })
            };
        }
    }

});

socket.on("check on sheriff successful", function (data) {
    verdicts[data["player_id"]].innerHTML = (data["is_sheriff"]) ? ("Этот шериф") : ("Это не шериф");
});

socket.on("check on mafia successful", function (data) {
    verdicts[data["player_id"]].innerHTML = (data["is_mafia"]) ? ("Это мафия") : ("Это не мафия");
});
