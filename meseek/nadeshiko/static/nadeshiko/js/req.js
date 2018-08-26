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
    console.log(quizzScore)
    var resultScore = document.createElement('h4');
    resultScore.appendChild(ScoreTitle);

    var gifV = ""
    switch (Number(quizzScore)) {
        case 100:
            gifV = "/static/nadeshiko/img/scores/SPEECHLESS.gif";
            break;
        case 90:
            gifV = "/static/nadeshiko/img/scores/AWESOME JOB.gif";
            break;
        case 80:
            gifV = "/static/nadeshiko/img/scores/AMAZING.gif";
            break;
        case 70:
            gifV = "/static/nadeshiko/img/scores/Alright.gif";
            break;
        case 60:
            gifV = "/static/nadeshiko/img/scores/Mouais.gif";
            break;
        case 50:
            gifV = "/static/nadeshiko/img/scores/Mehh.gif";
            break;
        default:
            gifV = "/static/nadeshiko/img/scores/Essaie encore.gif";
    }

    var resultGif = document.createElement('img');
    resultGif.setAttribute('style', "height: 300px");
    resultGif.setAttribute('src', gifV);
    var resultGifDiv = document.createElement('div')
    resultGifDiv.appendChild(resultGif)

    var tmp = gifV.split('/').pop();
    var phrase = tmp.split('.');
    phrase.pop();
    var CatchPhrase = document.createTextNode(phrase);
    var resultCatchPhrase = document.createElement('h4');
    resultCatchPhrase.appendChild(CatchPhrase);

    
    var ResultTitle = document.createTextNode("Vous avez terminé !!! Votre score est de: ");
    var resultTitle = document.createElement('h4');
    resultTitle.appendChild(ResultTitle);   

    var resultDivElt = document.createElement('div');
    resultDivElt.setAttribute('class', 'col-md-9 mx-auto text-center');
    resultDivElt.setAttribute('id', "result");
    resultDivElt.appendChild(resultTitle);
    resultDivElt.appendChild(resultScore);
    resultDivElt.appendChild(resultCatchPhrase);
    resultDivElt.appendChild(resultGifDiv);
    resultDivElt.appendChild(resetLink);

    return resultDivElt;

}


var wins = [
  "/static/nadeshiko/img/ryu/wins/SHOORYUUUKEN !!!.gif",
  "/static/nadeshiko/img/ryu/wins/TATSUMAKI !!!.gif",
  "/static/nadeshiko/img/ryu/wins/YEEAAH !!!.gif",
  "/static/nadeshiko/img/ryu/wins/HADOOOOKEN !!!.gif",
];

var loses = [
  "/static/nadeshiko/img/ryu/loses/Huuuuuhh.gif",
  "/static/nadeshiko/img/ryu/loses/Nooooooo.gif",
  "/static/nadeshiko/img/ryu/loses/Arrgggh.gif",
];

function animatesRyu () {
    var thumbsUp = document.createElement('i')
    thumbsUp.setAttribute('class', 'fa fa-thumbs-o-up')    

    var thumbsDown = document.createElement('i')
    thumbsDown.setAttribute('class', 'fa fa-thumbs-o-down')

    if (lastAnswer) {
        var winsLen = wins.length;
        var WIN = Math.floor(winsLen*Math.random());
        document.getElementById('ryu').src=wins[WIN];
        var gif = wins[WIN].split('/').pop();
        var phrase = gif.split('.');
        phrase.pop();
        document.getElementById('ryu_says').innerHTML=phrase + '&emsp;';
        document.getElementById('ryu_says').appendChild(thumbsUp);
    }
    else {
        var losesLen = loses.length;
        var LOSE = Math.floor(losesLen*Math.random());
        document.getElementById('ryu').src=loses[LOSE];
        var gif = loses[LOSE].split('/').pop();
        var phrase = gif.split('.');
        phrase.pop();
        document.getElementById('ryu_says').innerHTML=phrase + '&emsp;';
        document.getElementById('ryu_says').appendChild(thumbsDown);
      }
}


////////////////////////////////
// Backend interaction server //
////////////////////////////////
// Answer form sender

answer.addEventListener('keypress', function (e) {
    if (e.keyCode === 13 && answer.value !== null) {
        element = document.getElementById("questionDiv")
        quizzQuestion = element.innerHTML
        quizzAnswer = answer.value.toUpperCase()
        answer.value= '' // reinit field
        answerSent = {"jp": quizzQuestion, "fr": quizzAnswer}
        var MsgClient = {
            "index": quizzIndex,
            "answer": answerSent,
            };
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
                animatesRyu(lastAnswer)
            }
            else {
                var info = document.getElementById("info")
                animatesRyu(lastAnswer)
                document.getElementById("questionDiv").innerHTML = quizzQuestion
                document.getElementById("questionProgression").innerHTML = quizzProgression
            }          
        }
    })
};


