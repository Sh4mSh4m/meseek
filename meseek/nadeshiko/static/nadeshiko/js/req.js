////////////////////////////////////////////////////////////////
// DOM selectors declaration                                  //
////////////////////////////////////////////////////////////////
var main = document.getElementById("main");
var form = document.getElementById("theForm");
var quizzIndex = 0

////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
// Main section
function createQuizzDiv (questionItem, questionProgression) {
    // Answer div content with form creation
    var answerTextArea = document.createElement('input');
    answerTextArea.setAttribute('type', 'text');
    answerTextArea.setAttribute('id', 'answerInput');
    answerTextArea.setAttribute('size', '20');
    answerTextArea.setAttribute('autofocus', 'true');
    answerTextArea.setAttribute('placeholder', 'Répondez ici');
    
    var answerFormClass = document.createElement('div');
    answerFormClass.setAttribute('class', 'form-group');

    var answerFormDiv = document.createElement('form');
    answerFormDiv.appendChild(answerFormClass);
    answerFormDiv.appendChild(answerTextArea);

    var quizzAnswerDivElt = document.createElement('div');
    quizzAnswerDivElt.setAttribute('class', 'col-md-6 mx-auto text-center');
    quizzAnswerDivElt.appendChild(answerFormDiv);
    // Quizz div content
        // Question item
    var questionItemElt = document.createTextNode(questionItem);
    var questionTitle = document.createElement('h4');
    questionTitle.setAttribute('id', 'questionDiv');
    questionTitle.appendChild(questionItemElt);
        // Question progression content
    var questionProgressionElt = document.createTextNode(questionProgression);
    var questionProgressionDiv = document.createElement('div');
    questionProgressionDiv.setAttribute('id', 'questionProgression');
    questionProgressionDiv.appendChild(questionProgressionElt)
        // Question Div
    var quizzQuestionDivElt = document.createElement('div');
    quizzQuestionDivElt.setAttribute('class', 'col-md-6 mx-auto text-center');
    quizzQuestionDivElt.appendChild(questionProgressionDiv);
    quizzQuestionDivElt.appendChild(questionTitle);

        // Quizz row
    var quizzRowElt = document.createElement('div');
    quizzRowElt.setAttribute('class', 'row');
    quizzRowElt.setAttribute('id', 'questionRow');
    quizzRowElt.appendChild(quizzQuestionDivElt);
    quizzRowElt.appendChild(quizzAnswerDivElt);
        // Quizz title
    var Title = document.createTextNode("A vous de jouer !");
    var quizzTitle = document.createElement('h4');
    quizzTitle.appendChild(Title);
    // Quizz div
    var quizzDivElt = document.createElement('div');
    quizzDivElt.setAttribute('class', 'col-md-9 mx-auto text-center');
    quizzDivElt.setAttribute('id', "question");
    quizzDivElt.appendChild(quizzTitle);
    quizzDivElt.appendChild(quizzRowElt);
    return quizzDivElt;
};

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


// Ajax post request call
function ajaxSend(MsgClient){
    console.log("i'm in")
    $.ajax({
        "url": "http://127.0.0.1:8000/nadeshiko/quizz/",
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
            var configuration = document.getElementById("configuration");
            if (configuration !== null) {
                question = createQuizzDiv(quizzQuestion, quizzProgression)
                main.replaceChild(question, configuration)
            }
            if (quizzEnd && configuration === null) {
                results = createResultsDiv(quizzScore)
                quesiton = document.getElementById("question")
                main.replaceChild(results, question)

            }
            else {
                document.getElementById("questionDiv").innerHTML = quizzQuestion
                document.getElementById("questionProgression").innerHTML = quizzProgression
            }          
        }
    })
};


// Quizz initiator
form.addEventListener("submit", function (e) {
    e.preventDefault();
    var MsgClient = {
        "index": quizzIndex,
        "answer": {},
        "reinitRequest": false,
        "settings": {
            "level": 1,
            "quizzLength": 10,
            }
        };
    ajaxSend(MsgClient);
});


// Answer form sender
main.addEventListener('keypress', function (e) {
    var answerForm = document.getElementById("answerInput")
    if (e.keyCode === 13 && answerForm.value !== '') {
        quizzAnswer = answerForm.value.toUpperCase()
        answerForm.value = ''
        answer = {"jp": quizzQuestion, "fr": quizzAnswer}
        var MsgClient = {
            "index": quizzIndex,
            "answer": answer,
            "reinitRequest": false,
            "settings": {
                "level": 1,
                "quizzLength": 10,
                }
            };
        ajaxSend(MsgClient);
    }
    else {
        answerForm.value += String.fromCharCode(e.keyCode)
    }
    e.preventDefault(); 
});
