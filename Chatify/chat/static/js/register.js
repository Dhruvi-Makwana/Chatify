function register(e) {
        e.preventDefault();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var formdata = new FormData($('#register_form')[0]);
        makeAjaxRequest('POST', csrfToken, "/api/register/", formdata, function (response) {
             console.log(response)
             const errors = JSON.stringify(response.errors);
       
                // Update the text content of the small tags based on the error messages
        document.getElementById('email').innerHTML = errors.email[0].string;
        document.getElementById('phonenumber').innerHTML = errors.mobile_number[0].string;
        document.getElementById('password').innerHTML = errors.password[0].string;
        
        })
}

