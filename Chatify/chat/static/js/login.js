function login(e) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    e.preventDefault();
    var formdata = new FormData($('#login_form')[0]);
    makeAjaxRequest('POST', csrfToken, "/api/login/", formdata, function(response) {
     window.location = '/chat/';
    })
}

