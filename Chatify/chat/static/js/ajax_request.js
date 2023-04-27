var csrfToken = null

function csrfFunc(token) {
    csrfToken = token
}
function makeAjaxRequest(methodType, csrfToken, url, data, callback)
{
    $.ajax({
        method: methodType,
        headers: {
            'X-CSRFToken': csrfToken
        },
        url: url,
        data: data,
        contentType: false,
        success: function(data) {
            if (callback) {
                callback(data)
            }
        },
        error: function(data) {
           console.log(data)
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

 $(document).on("submit", "#register_form", function(event) {
        console.log("hii")
        event.preventDefault();
        event.stopImmediatePropagation();
        var formdata =  new FormData(this)
        makeAjaxRequest('POST',csrfToken,"/register/", formdata, function(response){
        console.log("register")
        })
    })

 $(document).on("submit", "#login_form", function(event) {
        console.log("hii")
        event.preventDefault();
        event.stopImmediatePropagation();
        var formdata =  new FormData(this)
        makeAjaxRequest('POST',csrfToken,"/login/", formdata, function(response){
            window.location = '/login/';
        })
    })