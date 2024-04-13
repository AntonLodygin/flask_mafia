const elem = document.querySelector("#open");
const password_div = document.querySelector("#password-div");
const password = document.querySelector("#password");
elem.onchange = function() {
    if (elem.checked) {
        password_div.hidden = true;
        password.required = false;
        password.setAttribute("minlength", "0");
    }
    else {
        password_div.hidden = false;
        password.required = true;
        password.setAttribute("minlength", "4");
    };
};