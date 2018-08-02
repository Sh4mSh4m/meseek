////////////////////////////////////////////////////////////////
// DOM selectors declaration                                  //
////////////////////////////////////////////////////////////////
var main = document.getElementById("main");
var form = document.getElementById("theForm");


////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////
var quizzIndex = 0
var question = ''
console.log('initiating page')
// Main section
function createQuizzDiv (questionItem) {
    // Answer div content with form creation
    var answerTextArea = document.createElement('input');
    answerTextArea.setAttribute('type', 'text');
    answerTextArea.setAttribute('id', 'answerInput');
    answerTextArea.setAttribute('class', 'form-control');
    answerTextArea.setAttribute('autofocus', 'true');
    answerTextArea.setAttribute('placeholder', 'Répondez ici');
    
    var answerFormClass = document.createElement('div');
    answerFormClass.setAttribute('class', 'form-group');

    var answerFormDiv = document.createElement('form');
    answerFormDiv.appendChild(answerFormClass);
    answerFormDiv.appendChild(answerTextArea);

    // Question div content
    var questionItemElt = document.createTextNode(questionItem);

    var quizzQuestionDivElt = document.createElement('div');
    quizzQuestionDivElt.setAttribute('class', 'col-md-6 mx-auto text-center');
    quizzQuestionDivElt.appendChild(questionItemElt);

    var quizzAnswerDivElt = document.createElement('div');
    quizzQuestionDivElt.setAttribute('id', 'questionDiv');
    quizzAnswerDivElt.setAttribute('class', 'col-md-6 mx-auto text-center');
    quizzAnswerDivElt.appendChild(answerFormDiv);

    var quizzRowElt = document.createElement('div');
    quizzRowElt.setAttribute('class', 'row');
    quizzRowElt.setAttribute('id', 'questionRow');
    quizzRowElt.appendChild(quizzQuestionDivElt);
    quizzRowElt.appendChild(quizzAnswerDivElt);

    var Title = document.createTextNode("A vous de jouer !");
    var quizzTitle = document.createElement('h4');
    quizzTitle.appendChild(Title)

    var quizzDivElt = document.createElement('div');
    quizzDivElt.setAttribute('class', 'col-md-9 mx-auto text-center');
    quizzDivElt.setAttribute('id', "question");
    quizzDivElt.appendChild(quizzTitle);
    quizzDivElt.appendChild(quizzRowElt);
    return quizzDivElt;
};

function createNewQuizzElt (questionItem) {
    var questionItemElt = document.createTextNode(questionItem);

    var quizzQuestionDivElt = document.createElement('div');
    quizzQuestionDivElt.setAttribute('id', 'questionDiv');
    quizzQuestionDivElt.setAttribute('class', 'col-md-6 mx-auto text-center');
    quizzQuestionDivElt.appendChild(questionItemElt);    
    return quizzQuestionDivElt
};

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
            quizzIndex = MsgServer.quizzIndex
            var configuration = document.getElementById("configuration");
            if (configuration !== null) {
                question = createQuizzDiv(quizzQuestion)
                main.replaceChild(question, configuration)
            }
            else {
                document.getElementById("questionDiv").innerHTML = quizzQuestion
            }          
        }
    })
};




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


//main.addEventListener('keypress', check)

//function check (e) {
//    if (e.target && e.target.id == "answerInput") {
//        var answerForm = document.getElementById("answerInput")
//        if (e.keyCode === 13 && answerForm.value !== '') {
//            quizzAnswer = answerForm.value.toUpperCase()
//            answer = {"jp": quizzQuestion, "fr": quizzAnswer}
//            var MsgClient = {
//                "index": quizzIndex,
//                "answer": answer,
//                "reinitRequest": false,
//                "settings": {
//                    "level": 1,
//                    "quizzLength": 10,
//                    }
//                };
//            ajaxSend(MsgClient);
//            }
//    }       e.preventDefault(); 
//};

