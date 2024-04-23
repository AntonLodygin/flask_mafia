const players = document.querySelector(".row").querySelectorAll(".col").length;
const playersCount = document.querySelector("#players-count").value;
const lobbyId = location.href.split("/").at(-1);
//const socket = io();
//socket.on("connect", function () {
//    socket.emit('user_join', {room: lobbyId});
//    })


if (players == playersCount) {
    console.log("lobby full");
    let xhr = new XMLHttpRequest();
    xhr.open("POST", `http://127.0.0.1:1338/distribution_roles/`);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify({lobby_id: lobbyId}));
    xhr.onload = function () {
        if (xhr.status == 200) {
            let response = JSON.parse(xhr.response)
            let userId = response["user_id"]
            console.log("response successful");
            let cardFooters = document.querySelectorAll(".card-footer");
            let actionButtons = document.querySelectorAll("input");
            let playersLife = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1, "9": 1}
            for (let i = 0; i < players; i++) {
                cardFooters[i].innerHTML = response[String(i)];
            }
            if (cardFooters[userId].innerHTML == "mafia" && playersLife[userId]) {
//            if (["mafia", "don", "sheriff"].includes(cardFooters[userId].innerHTML) && playersLife[userId]) {
                for (let j = 0; j < players; j++) {
                    console.log(cardFooters[j].innerHTML);
//                    if (["civilian", "sheriff"].includes(cardFooters[j].innerHTML)) {
                    if (j != userId) {
                        actionButtons[j].classList.add("btn-danger");
                        actionButtons[j].value = "убить";
                        actionButtons[j].hidden = false;
                        actionButtons[j].addEventListener("click", function () {
                            let xhr = new XMLHttpRequest();
                            xhr.open("POST", `http://127.0.0.1:1338/kill/`);
                            xhr.setRequestHeader("Content-type", "application/json");
                            xhr.send(JSON.stringify({player_id: j, lobby_id: lobbyId}));
                            xhr.onload = function () {
                                if (xhr.status == 200) {
                                    console.log("kill successful");
                                    actionButtons.forEach((el) => el.hidden = true);
                                    playersLife[String(J)] = 0;

                                }
                                else {
                                    console.log("kill, not 200");
                                }
                            }
                        });
                    }
                }
            }
        }
        else {
            console.log('not 200');
        }
    };
}