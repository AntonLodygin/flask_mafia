const players = document.querySelector(".row").querySelectorAll(".col").length
const playersCount = document.querySelector("#players-count").value
const lobbyId = location.href.split("/").at(-1)

console.log(location.href.split("/").at(-1))

if (players == playersCount) {
    console.log("lobby full");
    let xhr = new XMLHttpRequest();
    xhr.open("POST", `http://127.0.0.1:1338/distribution_roles/`);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify({ lobby_id: lobbyId }));
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log(JSON.parse(xhr.response)["status"]);
            let response = JSON.parse(xhr.response)
            if (response["status"] == 'ok') {
                console.log("response successful");
                let cardFooters = document.querySelectorAll(".card-footer")
                for (let i = 0; i < players; i++) {
                    cardFooters[i].innerHTML = response[String(i)];
                }
            }
            else {
                console.log("not ok");
                password_error.hidden = false;
            }
        }
        else {
            console.log('not 200');
        }
    };
}