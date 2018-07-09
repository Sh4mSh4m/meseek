#! /usr/bin/env python
import json
import codecs
import requests

def getJsonApiWiki(keyWord):
    """
    Input string
    Returns string from JSON api
    """
    rawJson = requests.get(urlBuilder(keyWord))
    # returns a list of 4 items, the last 3 are lists
    jsonData = rawJson.json()
    title = jsonData[0]
    relatedTopics = jsonData[1]
    summaries = jsonData[2]
    relatedlinks = jsonData[3]
    if not len(summaries) == 0:
        return summaries[0]
    else:
        return ''

def urlBuilder(keyWord):
    """
    Input list of words
    return the url to request
    """
    urlApiWiki = "https://fr.wikipedia.org/w/api.php?"
    urlApiWikiAction= "action=opensearch&format=json&search="
    urlApiWikiCall = urlApiWiki + urlApiWikiAction + keyWord
    return urlApiWikiCall