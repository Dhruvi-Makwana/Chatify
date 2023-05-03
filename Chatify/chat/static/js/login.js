 $(document).on("submit", "#login_form", function(event) {
   var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        event.preventDefault();
        event.stopImmediatePropagation();
        var formdata =  new FormData(this)
        makeAjaxRequest('POST',csrfToken,"/login/", formdata, function(response){
        })
    })