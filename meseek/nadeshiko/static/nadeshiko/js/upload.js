var text = document.getElementById("upload")
var level = document.getElementById('level')
var currentUrl = window.location.href
var temp_list = currentUrl.split('/')
temp_list.pop()
temp_list.pop()
var redirectURL = temp_list.join('/') + "/loading/"

text.addEventListener('keypress', function (e) {
    if (e.keyCode === 13 && text.value !== '') {
        levelEntered = level.value
        textEntered = text.value
        var MsgClient = {
            "level": levelEntered,
            "text": textEntered,
            };
        ajaxSend(MsgClient);
        e.preventDefault()
    }
});


// Ajax post request call
function ajaxSend(MsgClient){
    console.log("i'm sending")
    $.ajax({
        "url": redirectURL,
        "type": "POST",
        "contentType": "application/json; #charset=utf-8", 
        "dataType": "json",
        "data": JSON.stringify(MsgClient),
        "success": function(MsgServer) {
            console.log("OK RECEIVED")
            }          
    })
};
