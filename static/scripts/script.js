
const form = document.querySelector('.check-lobby-password-form');
// console.log(forms)
// forms.forEach((form) => {

const lobbyElement = document.querySelectorAll('.close-lobby');

lobbyElement.forEach((el)=>{
  // console.log(this)
  el.addEventListener('click', (e)=> {
    // console.log(el)
      form.querySelector('[type=hidden]').value = el.dataset.lobbyid;
  })
})
form.querySelector("[type=submit]").addEventListener('click', (e) => {
  e.preventDefault();
  console.log(e.target, e.target.parentNode)
  const id = parseInt(e.target.parentNode.querySelector('[type=hidden]').value);
  const password = e.target.parentNode.querySelector('[type=password]').value;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", `http://127.0.0.1:1212/check_lobby_password/`);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.send(JSON.stringify({ lobby_id: id, password: password }))
  xhr.onload = function () {
    if (xhr.status == 200) {
      if (xhr.response == 'ok') {
        location.href = `http://127.0.0.1:1212/lobby/${parseInt(id)}`;
      } else {
      console.log("wrong")
      }
      

    } else {
      console.log('not 200')
    }
  };
})
// })
