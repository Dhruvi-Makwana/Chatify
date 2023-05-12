function login(e) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    e.preventDefault();
    var formdata = new FormData($('#login_form')[0]);
    makeAjaxRequest('POST', csrfToken, "/login/", formdata, function (response) { window.location.href = "/chat/" })
}

