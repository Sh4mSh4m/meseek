
////////////////////////////////////////////////////////////////
// DOM selecotrs declaration                                  //
////////////////////////////////////////////////////////////////
var form = document.querySelector("form");
var dialogInput = document.getElementById("dialogInput");
var dialogDisplay = document.getElementById("dialogDisplay");
var nav = document.querySelector("nav");

////////////////////////////////////////////////////////////////
// Post function sending user input and recovering server     //
// Calling back function to handle response                   //
////////////////////////////////////////////////////////////////
function dialogSend(data){
    //Json sent to the django server
    // Later on, might include user ID for instance
    // id recovered in the form as hidden parameter
    var data2send = {
        rawInput : data,
        userId : 10
    }
    //#charset=utf-8
    $.ajax({
        "url": "http://shamnorobotto.live/chat/",
        "type": "POST",
        "contentType": "application/json; #charset=utf-8", 
        "dataType": "json",
        "data": JSON.stringify(data2send),
        "success": function(text) {
            msg = text.interaction
            response = text.response
            keyWord = text.keyWord
            complement = text.complement
            list = text.list
            botMsg = displayLogMessage("bot", msg, response, complement, list);
            dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
            //imgRickBaseElt = createImgRickBase()
            setTimeout(function () {
                //var imgRickThinkingElt = document.getElementById('rick')
                //nav.replaceChild(imgRickBaseElt, imgRickThinkingElt)
                dialogDisplay.removeChild(botThinkingMsg)
            })
        }
    })
};



////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
function createImgRickBase () {
    var imgRickBaseElt = document.createElement("img")
    imgRickBaseElt.setAttribute("id", "rick");
    imgRickBaseElt.setAttribute("class", "img-circle img-responsive");
    imgRickBaseElt.setAttribute("src", "");
    imgRickBaseElt.setAttribute("alt", "rick_base");
    return imgRickBaseElt
};

function createImgRickThinking () {
    var imgRickThinkingElt = document.createElement("img")
    imgRickThinkingElt.setAttribute("id", "rick");
    imgRickThinkingElt.setAttribute("class", "img-circle img-responsive");
    imgRickThinkingElt.setAttribute("src", "");
    imgRickThinkingElt.setAttribute("alt", "rick_thinking");
    return imgRickThinkingElt
};

function createTimeStampElt () {
    var date = new Date ()
    var hour = date.getHours()
    var min = date.getMinutes()
    var spanElt = document.createElement("span")
    spanElt.setAttribute("class", "time");
    spanElt.textContent = hour + ":" + min
    return spanElt
};

function createParagraphElt (text) {
    var paragrapheElt = document.createElement("p");
    paragrapheElt.setAttribute("class", "wordwrap");
    paragrapheElt.textContent = text;
    return paragrapheElt
};

function createListElt (listContent) {
    var listElt = document.createElement("div");
    listElt.setAttribute("class", "console");
    array = listContent.split("\r\n")
    for (var i = 0; i < array.length; i++) {
        // Create the list item:
        var item = document.createElement("div");
        // Set its contents:
        item.appendChild(document.createTextNode(array[i]));
        // Add it to the list:
        listElt.appendChild(item);
    }
    return listElt;
};

function createMapsElt (response) {
    var mapsElt = document.createElement("iframe")
    mapsElt.setAttribute("class", "maps");
    srcBase = "https://www.google.com/maps/embed/v1/"
    srcSearch = "place?q=" + keyWord
    srcKey = "&key=AIzaSyAXHQGvaSlCZfPPratuxXQP-pZZqYPnI8w"
    src = srcBase + srcSearch + srcKey
    mapsElt.setAttribute('src', src)
    mapsElt.setAttribute('allowFullScreen', '')
    return mapsElt
};

function createComplementElt (complement) {
    var complementElt = document.createElement("span");
    complementElt.setAttribute("class", "response");
    complementElt.textContent = complement;
    return complementElt
};

function createAvatarElt (source) {
    var avatarElt = document.createElement("div");
    avatarElt.setAttribute("class", "avatar");
    avatarElt.setAttribute("id", source);
    return avatarElt
};

function createDivElt (source) {
    var divElt = document.createElement("div");
    divElt.setAttribute("class", source);
    return divElt
};


///////////////////////////////
// Displays server response  //
///////////////////////////////


function displayLogMessage (source, text, response, complement, list) {
    var msgElt = createDivElt(source);
    var msgAvatarElt = createAvatarElt(source)
    if (response !== '') {
        var msgInputElt = createParagraphElt(text + "Ooouu Eeee j'ai trouvé ! ")
        msgInputElt.appendChild(createMapsElt(response))
        msgInputElt.appendChild(createComplementElt(complement))
    }
    else if (source === 'bot' && text === '' && response === '' && complement === '' && list === '') {
        var msgInputElt = createParagraphElt("Désolé je n'ai pas tout compris ! ")
    }
    else if (source === 'bot' && list !== '') {
        var msgInputElt = createParagraphElt(text)
        msgInputElt.appendChild(createListElt(list))
    }
    else if (source === 'bot' && response === '') {
        var msgInputElt = createParagraphElt(text + complement)
    }
    else {
        var msgInputElt = createParagraphElt(text)
    }
    var msgInputTimeElt = createTimeStampElt()
    msgElt.appendChild(msgAvatarElt);
    msgElt.appendChild(msgInputElt);
    msgInputElt.appendChild(msgInputTimeElt)
    return msgElt;
};

//////////////////////////////////////////
// input control and sending functions  //
//                                      //
//////////////////////////////////////////

function checkInput (data) {
    if (typeof data === 'string') {
        return true;
    }
    else {
        return false;
    }
};

function sendUsrInput (data) {
    //refreshes the dialogInput form
    dialogInput.value = null;
    userMsg = displayLogMessage('user', data, '', '');
    botThinkingMsg = displayLogMessage('botThinking', "MEEESEEKKK AND DESTROY", '', '');
    dialogDisplay.insertAdjacentElement('afterbegin', userMsg);
    dialogDisplay.insertAdjacentElement('afterbegin', botThinkingMsg);
    imgRickThinkingElt = createImgRickThinking()
    //var imgRickBaseElt = document.getElementById('rick')
    //nav.replaceChild(imgRickThinkingElt, imgRickBaseElt);
    dialogSend(data);
};

////////////////////////////////////////////////////////////////
// Event listeners to submit user input upon clicking submit  //
// button                                                     //
////////////////////////////////////////////////////////////////


form.addEventListener("submit", function (e) {
    e.preventDefault();
    data = dialogInput.value;
    if (checkInput(data)) {
        sendUsrInput(data);
    }
    else {
        botMsg = displayLogMessage("bot", "HHooouuu eeee, wrong input mate");
        dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
    }
});

dialogInput.addEventListener('keypress', function(e) {
    if (e.keyCode === 13) { 
        data = dialogInput.value;
        if (checkInput(data)) {
            sendUsrInput(data);
        }
        else {
            botMsg = displayLogMessage("bot", "HHooouuu eeee, wrong input mate");
            dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
        }        e.preventDefault();
    }
});


// eventlistener for confirmation window