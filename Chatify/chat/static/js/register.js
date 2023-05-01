
 $(document).on("submit", "#register_form", function(event) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        event.preventDefault();
        event.stopImmediatePropagation();
        var formdata =  new FormData(this)
        makeAjaxRequest('POST',csrfToken,"/register/", formdata, function(response){
        window.location = '/login/';
        })
    })