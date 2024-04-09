let xhr = new XMLHttpRequest();
xhr.open("POST", "http://127.0.0.1:1212/check_lobby_password");
xhr.send(JSON.stringify({lobby_id: document.getElementById("hidden_id").val, password: document.getElementById("hidden_id").val}))
xhr.onload = function() {
  if (xhr.status == 200) { // анализируем HTTP-статус ответа, если статус не 200, то произошла ошибка
    alert(`Ошибка ${xhr.status}: ${xhr.statusText}`); // Например, 404: Not Found
  } else { // если всё прошло гладко, выводим результат
    alert(`Готово, получили ${xhr.response.length} байт`); // response -- это ответ сервера
  }
};