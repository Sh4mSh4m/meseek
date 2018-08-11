////////////////////////////////////////////////////////////////
// DOM selectors declaration                                  //
////////////////////////////////////////////////////////////////
var main = document.getElementById("main");
var answer = document.getElementById("answerInput")
var form = document.getElementById("theForm");
var quizzIndex = Number(DjangoQuizzIndex);
console.log(quizzIndex)

////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
// Main section

function createResultsDiv (quizzScore) {    

    var resetPhrase = document.createTextNode("Faire un autre quizz :)")
    var resetLink = document.createElement('a')
    resetLink.setAttribute('href', "http://127.0.0.1:8000/nadeshiko/quizz/")
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
            console.log(MsgServer)
            quizzQuestion = MsgServer.quizzQuestion
            quizzProgression = "Question: " + MsgServer.quizzIndex + "/" + MsgServer.quizzLength
            quizzIndex = MsgServer.quizzIndex
            quizzEnd = MsgServer.completion
            quizzScore = MsgServer.score
            if (quizzEnd) {
                results = createResultsDiv(quizzScore)
                question = document.getElementById("question")
                main.replaceChild(results, question)

            }
            else {
                document.getElementById("questionDiv").innerHTML = quizzQuestion
                document.getElementById("questionProgression").innerHTML = quizzProgression
            }          
        }
    })
};


