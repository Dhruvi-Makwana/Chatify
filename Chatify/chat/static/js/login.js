var csrfToken = null

function csrfFunc(token) {
    csrfToken = token
}
 $(document).on("submit", "#login_form", function(event) {
        console.log("hii")
        event.preventDefault();
        event.stopImmediatePropagation();
        var formdata =  new FormData(this)
        makeAjaxRequest('POST',csrfToken,"/login/", formdata, function(response){

        })
    })