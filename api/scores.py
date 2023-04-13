#!/usr/bin/env python3
import json
import os

global scoresArray 
scoresArray = []

def getScoresArr():
	tmpscores = []

	if os.path.exists("static/json/scores.json"):

		scrFile = open("static/json/scores.json")
		tmpscores = json.loads( scrFile.read() )
		scrFile.close()


	return tmpscores



if(len(scoresArray)<1):
	scoresArray = getScoresArr()



#
# dn returns darts needed for a score
def drtsNdd(scr:int):
	return scoresArray[scr]['DARTSNEEDED'] 

#
# vstsNdd returns visit profile for a score
def vstsNdd(scr:int):
	return scoresArray[scr]['VISITSNEEDED'] 

#
# isdbl returns ISDOUBLE for a score
def isDbl(scr:int):
	return scoresArray[scr]['ISDOUBLE'] 


#
# fn returns isfinish for a score
def isFnsh(scr:int):
	return scoresArray[scr]['ISFINISH'] 

