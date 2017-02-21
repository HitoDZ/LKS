function showError(container, errorMessage) {

    var msgElem = document.createElement('span');
    msgElem.className = "error-message";
    msgElem.innerHTML = errorMessage;
    container.appendChild(msgElem);

}

function resetError(container) {

    if (container.lastChild.className == "error-message") {

        container.removeChild(container.lastChild);

    }
}

function valid(form) {

    var validate = 1;
    var elems = form.elements;
    resetError(elems.login.parentNode);
    resetError(document.getElementById("log1"));

    if (!elems.login.value) {

        validate = 0;
        showError(elems.login.parentNode, '  enter the login ');

    }

    resetError(elems.password.parentNode);
    resetError(document.getElementById("log2"));

    if (!elems.password.value) {

        validate = 0;
        showError(elems.password.parentNode, '  enter the password');

    }

    if (validate) {

        check_log_pass(elems); //(elems.login.value,elems.password.value);

        //validate = 0;

        //showError(elems.login.parentNode,' The email you’ve entered doesn’t match any account. ');//Sign up for an account. //..

        //  validate = 0;

        //  showError(elems.password.parentNode,'   The password you’ve entered is incorrect.');// Forgot Password?

    }
}

function check_log_pass(elems) {

    console.log("check_log_pass");
    var xhr = new XMLHttpRequest();
    var newURL = "http://" + window.location.host + "/api/log_in"
    var metas = document.getElementsByTagName('meta');
    for (var i = 0; i < metas.length; i++) {

        if (metas[i].getAttribute("name") == "csrf-token") {
            var csrftoken = metas[i].getAttribute("content");
            break;

        }

    }

    xhr.open('POST', newURL);
    xhr.setRequestHeader("X-CSRFToken", csrftoken)

    var ch_login_pass = {

        login: elems.login.value,
        pass: elems.password.value,
        action: "ch_login_pass"

    }

    xhr.onreadystatechange = function(elems) {

        if (xhr.readyState == 4 && xhr.status == 200) {

            resetError(document.getElementById("log1"));
            resetError(document.getElementById("log2"));
            if (xhr.responseText == "uncorrect_log") {

                showError(document.getElementById("log1"), ' The email you’ve entered doesn’t match any account. '); //Sign up for an account.

            } else if (xhr.responseText == "uncorrect_pass") {

                showError(document.getElementById("log2"), '   The password you’ve entered is incorrect.'); // Forgot Password?

            } else if (xhr.responseText == "Ok") {

                document.getElementById("log_form").submit();

            }
        }
    };

    xhr.send(JSON.stringify(ch_login_pass));
}

/////////////////////////////////////////////////////judgment

function falert(form) {
    document.getElementById("form1").submit()
}

function ask(form) {
    var div = document.createElement('div');

    var metas = document.getElementsByTagName('meta');
    for (var i = 0; i < metas.length; i++) {

        if (metas[i].getAttribute("name") == "csrf-token") {
            var csrftoken = metas[i].getAttribute("content");
            break;

        }
    }

    div.className = "modal_box";
    div.innerHTML = "<form method='post' id='forma'>Are you sure?<br>" +
        "<input type='button' value='No' onclick=remove_modalBox()>&nbsp" +
        "<input type='button' value='Yes'onclick=falert(this.form)>" +
        "<input type='hidden' name='csrf' value=" + csrftoken + "></form>";
    document.body.appendChild(div)
}

function remove_modalBox() {
    document.body.removeChild(document.body.lastChild)
}

///////////////////////////////////////////Admin part _comands.html
function c_valid(form) {

    var validate = 1;
    var elems = form.elements;
    resetError(document.getElementById("comand1"));

    if (!elems.name.value) {

        validate = 0;
        showError(elems.name.parentNode, '  enter the name');

    }

    resetError(document.getElementById("comand2"));

    if (!elems.nomination.value) {

        validate = 0;
        showError(elems.nomination.parentNode, '  enter the nomination');

    }
    
    if (validate) {

        check_c_order(elems); //(elems.login.value,elems.password.value);


    }
}

function check_c_order(elems) {

    console.log("check_c_order");
    var xhr = new XMLHttpRequest();
    var newURL = "http://" + window.location.host + "/api/comands"
    var metas = document.getElementsByTagName('meta');
    for (var i = 0; i < metas.length; i++) {

        if (metas[i].getAttribute("name") == "csrf-token") {
            var csrftoken = metas[i].getAttribute("content");
            break;

        }

    }

    xhr.open('POST', newURL);
    xhr.setRequestHeader("X-CSRFToken", csrftoken)

    var ch_c_order = {

        name: elems.name.value,
        nomination: elems.nomination.value,
        C_order: elems.C_order.value,
        action: "ch_c_order"

    }

    xhr.onreadystatechange = function(elems) {

        if (xhr.readyState == 4 && xhr.status == 200) {

            resetError(document.getElementById("comand3"));

            if (xhr.responseText == "ErrorOrder") {

                showError(document.getElementById("comand3"), ' Vasya tam uje est takoy nomer. '); //Sign up for an account.

            } else if (xhr.responseText == "Ok") {

                document.getElementById("comand_form").submit();

            }
        }
    };

    xhr.send(JSON.stringify(ch_login_pass));
}
