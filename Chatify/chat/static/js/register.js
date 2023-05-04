function register(e) {
        e.preventDefault();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var formdata = new FormData($('#register_form')[0]);
        makeAjaxRequest('POST', csrfToken, "/register/", formdata, function(response) {
        })
}

