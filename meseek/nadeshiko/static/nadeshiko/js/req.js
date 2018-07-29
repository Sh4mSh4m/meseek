////////////////////////////////////////////////////////////////
// DOM selectors declaration                                  //
////////////////////////////////////////////////////////////////
var configuration = document.getElementById("configuration");
var question = document.getElementById("question");
var main = document.getElementById("main");
var form = document.getElementById("theForm");


////////////////////////////////////////////////////////////////
// Functions that creates HTML elements to display in the log //
////////////////////////////////////////////////////////////////

// Main section
function createQuizzDiv (questionItem) {
    var QuestionItemElt = document.createTextNode(questionItem);
    var AnswerItemElt = document.createTextNode("AnswerForm");

    var quizzQuestionDivElt = document.createElement("div");
    quizzQuestionDivElt.setAttribute("class", "col-md-6 mx-auto text-center");
    quizzQuestionDivElt.appendChild(QuestionItemElt);

    var quizzAnswerDivElt = document.createElement("div");
    quizzAnswerDivElt.setAttribute("class", "col-md-6 mx-auto text-center");
    quizzAnswerDivElt.appendChild(AnswerItemElt);

    var quizzRowElt = document.createElement("div");
    quizzRowElt.setAttribute("class", "row");
    quizzRowElt.appendChild(quizzQuestionDivElt);
    quizzRowElt.appendChild(quizzAnswerDivElt);

    var Title = document.createTextNode("A vous de jouer !");
    var quizzTitle = document.createElement("h4");
    quizzTitle.appendChild(Title)

    var quizzDivElt = document.createElement("div");
    quizzDivElt.setAttribute("class", "col-md-9 mx-auto text-center");
    quizzDivElt.setAttribute("id", "question");
    quizzDivElt.appendChild(quizzTitle);
    quizzDivElt.appendChild(quizzRowElt);
    return quizzDivElt;
}

function ajaxSend(MsgClient){
    console.log("i'm in")
    $.ajax({
        "url": "http://127.0.0.1:8000/nadeshiko/quizz/",
        "type": "POST",
        "contentType": "application/json; #charset=utf-8", 
        "dataType": "json",
        "data": JSON.stringify(MsgClient),
        "success": function(MsgServer) {
            quizzQuestion = MsgServer.quizzQuestion
            quizzIndex = MsgServer.quizzIndex
            question = createQuizzDiv(quizzQuestion)
            if (quizzIndex !== 0) {
                main.replaceChild(question, configuration)
            }
            else {
              console.log("not done yet")
            }            
        }
    })
};




form.addEventListener("submit", function (e) {
    e.preventDefault();
    var MsgClient = {
        "answer": "Caca",
        "reinitRequest": false,
        "settings": {
            "level": 1,
            "quizzLength": 10,
            }
        };
    console.log('sending shit')
    ajaxSend(MsgClient);
});

configuration.addEventListener('keypress', function(e) {
    if (e.keyCode === 13) {
        var MsgClient = {
            "answer": Caca,
            "reinitRequest": false,
            "settings": {
                "level": 1,
                "quizzLength": 10,
                }
            };
        ajaxSend(MsgClient);
        }        e.preventDefault();   
});
