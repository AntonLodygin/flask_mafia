const form = document.querySelector('.check-lobby-password-form');
const lobbyElement = document.querySelectorAll('.close-lobby');
const password_error = document.querySelector("#password-error");

lobbyElement.forEach((el) => {
    el.addEventListener('click', (e)=> {
        form.querySelector('[type=hidden]').value = el.dataset.lobbyid;
    })
})

form.querySelector("[type=submit]").addEventListener('click', (e) => {
    e.preventDefault();
    const id = parseInt(e.target.parentNode.querySelector('[type=hidden]').value);
    const password = e.target.parentNode.querySelector('[type=password]').value;

    let xhr = new XMLHttpRequest();
    xhr.open("POST", `http://127.0.0.1:1337/check_lobby_password/`);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify({ lobby_id: id, password: password }))
    xhr.onload = function () {
        if (xhr.status == 200) {
              if (xhr.response == 'ok') {
                  location.href = `http://127.0.0.1:1337/lobby/${parseInt(id)}`;
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
// })
