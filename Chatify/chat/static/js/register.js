$(document).on("submit", "#register_form", function(event) {
        console.log("hii")
        event.preventDefault();
        event.stopImmediatePropagation();
        var formdata =  new FormData(this)
        makeAjaxRequest('POST',csrfToken,"/register/", formdata, function(response){
        console.log("register")
        })
    })