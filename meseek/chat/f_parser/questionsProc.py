#! /usr/bin/env python
import json
import codecs

parserDictionnary = json.load(codecs.open("chat/f_parser/parserDictionnary.json",
                                          "r", "utf-8-sig"))

def stripStopWords(phrases):
    """
    Input is list
    Eliminates all the stop words from the phrases
    Returns a list of lists
    """
    cleanWordArrays = []
    for phrase in phrases:
        if len(phrase) is not 0:
            words = phrase.split()
            result = ([word for word in words if word not in 
                       parserDictionnary['stopWords']])
            if len(result) is not 0:
                cleanWordArrays.append(result)
    return cleanWordArrays


def questionsProc(lstQuestions, msgResponse):
    """
    Inputs lists of strings and dictionnary
    Builds the json response by appending strings to json entry
    Depending on the type of questions, it may retrieve key words to
    request APIs
    Returns the dictionnary updated
    """
    wordArrays = stripStopWords(lstQuestions)
    for wordArray in wordArrays:
        for locationAnchor in parserDictionnary['locationAnchor']:
            if locationAnchor in wordArray:
                index = wordArray.index(locationAnchor)
                for i in range(index+1, len(wordArray)):
                    msgResponse['keyWord'] += wordArray[i] + " "
    return msgResponse
    