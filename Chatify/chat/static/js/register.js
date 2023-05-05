function register(e) {
        e.preventDefault();
        console.log("Ajax call")
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var formdata = new FormData($('#register_form')[0]);
        makeAjaxRequest('POST', csrfToken, "http://127.0.0.1:8000/api/register/", formdata, function (response) {
        })
}

