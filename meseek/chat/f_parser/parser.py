#! /usr/bin/env python

def arraySentencesCleaner(arraySentences):
    return [sentence.strip() for sentence in arraySentences if sentence != '']

def msgParser(rawInput):
    """
    Input is a string and returns a dict:
    - 'sentences' key: list of sentences
    - 'questions' key: list of questions
    """
    sentences = []
    questions = []
    sentences.append(rawInput.lower())
    punctuation = parserDictionnary['punctuation']
    for p in punctuation:
        if p is not "?":
            for sentence in sentences:
                if p in sentence:
                    #replace the sentence with array of parsed sentence
                    sentences.remove(sentence)
                    sentences.extend(sentence.split(p))
        #only questions remaining
        else:
            for sentence in sentences:
                if p in sentence:
                    sentences.remove(sentence)
                    results = sentence.split(p)
                    len_results = len(results)
                    for k in (range(len_results-1)):
                        questions.append(results[k])
                    sentences.append(results[-1])
    sentences = arraySentencesCleaner(sentences)
    questions = arraySentencesCleaner(questions)
    parsedBatch = {'sentences': sentences, 'questions': questions}
    return parsedBatch
