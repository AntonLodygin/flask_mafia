const form = document.querySelector('.check-lobby-password-form');
const closeLobbies = document.querySelectorAll('.close-lobby');
const openLobbies = document.querySelectorAll('.open-lobby');
const password_error = document.querySelector("#password-error");


openLobbies.forEach((el) => {
    el.addEventListener('click', (e) => {
        location.href = `http://127.0.0.1:1234/lobby/${parseInt(el.dataset.lobbyid)}`;
        socket.on('connect', function() {
            socket.emit('user_join', {room: el.dataset.lobbyid});
        });
    })
})

closeLobbies.forEach((el) => {
    el.addEventListener('click', (e)=> {
        form.querySelector('[type=password]').value = "";
        password_error.hidden = true;
        form.querySelector('[type=hidden]').value = el.dataset.lobbyid;
    })
})

form.querySelector("[type=submit]").addEventListener('click', (e) => {
    e.preventDefault();
    const lobby_id = parseInt(e.target.parentNode.querySelector('[type=hidden]').value);
    const password = e.target.parentNode.querySelector('[type=password]').value;

    let xhr = new XMLHttpRequest();
    xhr.open("POST", `http://127.0.0.1:1234/check_lobby_password/`);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify({ lobby_id: lobby_id, password: password }))
    xhr.onload = function () {
        if (xhr.status == 200) {
            if (xhr.response == 'ok') {
                location.href = `http://127.0.0.1:1234/lobby/${parseInt(lobby_id)}`;
                socket.on('connect', function() {
                    console.log(socket.connected);
                    socket.emit('user_join', {room: lobby_id});
                    });
            }
            else {
                password_error.hidden = false;
            }
        }
        else {
            console.log('not 200');
        }
    };
})
