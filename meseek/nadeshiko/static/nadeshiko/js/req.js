////////////////////////////////////////////////////////////////
// DOM selectors declaration                                  //
////////////////////////////////////////////////////////////////
var main = document.getElementById("main");
var answer = document.getElementById("answerInput")
var info = document.getElementById("info")
var form = document.getElementById("theForm");
var quizzIndex = Number(DjangoQuizzIndex);
console.log(quizzIndex)

////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
// Main section

function createResultsDiv (quizzScore) {    

    var currentUrl = window.location.href
    var temp_list = currentUrl.split('/')
    temp_list.pop()
    var redirectURL = temp_list.join('/')
    var resetPhrase = document.createTextNode("Faire un autre quizz :)")
    var resetLink = document.createElement('a')
    resetLink.setAttribute('href', redirectURL)
    resetLink.appendChild(resetPhrase)

    var ScoreTitle = document.createTextNode(quizzScore);
    var resultScore = document.createElement('h4');
    resultScore.appendChild(ScoreTitle);

    var ResultTitle = document.createTextNode("Vous avez terminé !!! Votre score est de: ");
    var resultTitle = document.createElement('h4');
    resultTitle.appendChild(ResultTitle);   

    var resultDivElt = document.createElement('div');
    resultDivElt.setAttribute('class', 'col-md-9 mx-auto text-center');
    resultDivElt.setAttribute('id', "result");
    resultDivElt.appendChild(resultTitle);
    resultDivElt.appendChild(resultScore);
    resultDivElt.appendChild(resetLink);
    return resultDivElt;

}

function createAnimatedDiv () {
    if (lastAnswer) {
        var gif = document.createElement('img')
        gif.setAttribute('src', '/static/nadeshiko/img/ryu_reg.gif');
        gif.setAttribute('alt', 'ryu_ok');
        gif.setAttribute('style', 'height:200px');
    }
    else {
        var gif = document.createElement('img')
        gif.setAttribute('src', '/static/nadeshiko/img/ryu_kick.gif');
        gif.setAttribute('alt', 'ryu_nok');        
        gif.setAttribute('style', 'height:200px');
    }
    var animatedDiv = document.createElement('div')
    animatedDiv.setAttribute('class', 'col-md-3 mx-auto text-center');
    animatedDiv.setAttribute('id', "info");
    animatedDiv.appendChild(gif)
    return animatedDiv
}

////////////////////////////////
// Backend interaction server //
////////////////////////////////
// Answer form sender

answer.addEventListener('keypress', function (e) {
    if (e.keyCode === 13 && answer.value !== '') {
        element = document.getElementById("questionDiv")
        quizzQuestion = element.innerHTML
        quizzAnswer = answer.value.toUpperCase()
        answer.value= '' // reinit field
        answerSent = {"jp": quizzQuestion, "fr": quizzAnswer}
        var MsgClient = {
            "index": quizzIndex,
            "answer": answerSent,
            };
        console.log(MsgClient)
        ajaxSend(MsgClient);
        e.preventDefault()
    }
});


// Ajax post request call
function ajaxSend(MsgClient){
    console.log("i'm sending")
    $.ajax({
        "url": window.location.href,
        "type": "POST",
        "contentType": "application/json; #charset=utf-8", 
        "dataType": "json",
        "data": JSON.stringify(MsgClient),
        "success": function(MsgServer) {
            quizzQuestion = MsgServer.quizzQuestion
            quizzProgression = "Question: " + MsgServer.quizzIndex + "/" + MsgServer.quizzLength
            quizzIndex = MsgServer.quizzIndex
            quizzEnd = MsgServer.completion
            quizzScore = MsgServer.score
            lastAnswer = MsgServer.lastAnswer
            if (quizzEnd) {
                results = createResultsDiv(quizzScore)
                question = document.getElementById("question")
                main.replaceChild(results, question)

            }
            else {
                var info = document.getElementById("info")
                ryu = createAnimatedDiv(lastAnswer)
                main.replaceChild(ryu, info)
                document.getElementById("questionDiv").innerHTML = quizzQuestion
                document.getElementById("questionProgression").innerHTML = quizzProgression
            }          
        }
    })
};


