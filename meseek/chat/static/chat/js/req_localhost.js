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
    var data = {
        dialogContent : data
    }
    ajaxPost("http://localhost:5000/dialog", data, function (text) {
      var listData= JSON.parse(text)
      msg = listData.interaction
      response = listData.response
      console.log(response)
      keyWord = listData.keyWord
      complement = listData.complement
      botMsg = displayLogMessage("bot", msg, response, complement);
      dialogDisplay.insertAdjacentElement("afterbegin", botMsg);
      imgRickBaseElt = createImgRickBase()
      setTimeout(function () {
          var imgRickThinkingElt = document.getElementById('rick')
          nav.replaceChild(imgRickBaseElt, imgRickThinkingElt)
          dialogDisplay.removeChild(botThinkingMsg)
        }, 500)
    }, true);
};

////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
function createImgRickBase () {
    var imgRickBaseElt = document.createElement("img")
    imgRickBaseElt.setAttribute("id", "rick");
    imgRickBaseElt.setAttribute("class", "img-circle img-responsive");
    imgRickBaseElt.setAttribute("src", "../static/img/rick_base.jpeg");
    imgRickBaseElt.setAttribute("alt", "rick_base");
    return imgRickBaseElt
}

function createImgRickThinking () {
    var imgRickThinkingElt = document.createElement("img")
    imgRickThinkingElt.setAttribute("id", "rick");
    imgRickThinkingElt.setAttribute("class", "img-circle img-responsive");
    imgRickThinkingElt.setAttribute("src", "../static/img/rick_thinking.jpeg");
    imgRickThinkingElt.setAttribute("alt", "rick_thinking");
    return imgRickThinkingElt
}

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
}

function createComplementElt (complement) {
    var complementElt = document.createElement("span");
    complementElt.setAttribute("class", "response");
    complementElt.textContent = complement;
    return complementElt
}

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

function displayLogMessage (source, text, response, complement) {
    var msgElt = createDivElt(source);
    var msgAvatarElt = createAvatarElt(source)
    if (response !== '') {
        var msgInputElt = createParagraphElt(text + "Ooouu Eeee j'ai trouvé ! ")
        msgInputElt.appendChild(createMapsElt(response))
        msgInputElt.appendChild(createComplementElt(complement))
    }
    else if (source === 'bot' && text === '' && response === '' && complement === '') {
        var msgInputElt = createParagraphElt("Désolé je n'ai pas tout compris ! ")
    }
    else if (source === 'bot' && response === '') {
        console.log("perdu")
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

function checkInput (data) {
    if (typeof data === 'string') {
        return true;
    }
    else {
        return false;
    }
};

function sendUsrInput (data) {
    dialogInput.value = null;
    userMsg = displayLogMessage('user', data, '', '');
    botThinkingMsg = displayLogMessage('botThinking', "MEEESEEKKK AND DESTROY", '', '');
    dialogDisplay.insertAdjacentElement('afterbegin', userMsg);
    dialogDisplay.insertAdjacentElement('afterbegin', botThinkingMsg);
    imgRickThinkingElt = createImgRickThinking()
    var imgRickBaseElt = document.getElementById('rick')
    nav.replaceChild(imgRickThinkingElt, imgRickBaseElt);
    dialogSend(data);
}

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