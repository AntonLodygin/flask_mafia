const lobbyId = parseInt(location.href.split("/").at(-1));
let actionButtons = document.querySelectorAll("[type=button]");
let verdicts = document.querySelectorAll("p");
let cardFooters = document.querySelectorAll(".card-footer");
let userID;

socket.on("lobby full", function () {
    alert("lobby full");
    socket.emit("get roles", {lobby_id: lobbyId});
});

socket.on("get roles successful", function (data) {
    roles = data["players_roles"];
    userId = data["user_id"];
    cardFooters = document.querySelectorAll(".card-footer");
    for (let i = 0; i < 10; i++) {
        if (["civilian", "sheriff"].includes(roles[String(userId)])) {
            cardFooters[i].innerHTML = "";
        }
        else if (["don", "mafia"].includes(roles[String(userId)]) && ["don", "mafia"].includes(roles[String(i)])) {
            cardFooters[i].innerHTML = roles[String(i)];
        }
    }
    socket.emit("start_game", {lobby_id: lobbyId})
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
                    socket.emit("check_on_sheriff", {player_id: j, lobby_id: lobbyId});
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
                    socket.emit("check_on_mafia", {player_id: j, lobby_id: lobbyId});
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

socket.on("player joined", function (data) {
    console.log("player joined");
    let card = document.createElement("div");
    card.classList.add("card");
    let cardHeader = document.createElement("div");
    cardHeader.classList.add("card-header");
    let cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    cardBody.innerHTML = data["user_login"];
    let cardFooter = document.createElement("div");
    cardFooter.classList.add("card-footer");
    card.append(cardHeader);
    card.append(cardBody);
    card.append(cardFooter);

    let actionDiv = document.createElement("div");
    actionDiv.id = action;
    actionDiv.classList.add("d-flex");
    actionDiv.classList.add("justify-content-center");
    actionDiv.classList.add("mt-1");
    let btn = document.createElement("input");
    btn.classList.add("btn");
    btn.classList.add("btn-sm");
    btn.type = "button";
    btn.hidden = true;
    let p = document.createElement("p");
    actionDiv.append(btn);
    actionDiv.append(p);

    let col = document.createElement("div");
    col.classList.add("col");
    col.append(card);
    col.append(actionDiv);

    alert("add");
    document.querySelector(".row").append(col);
});
