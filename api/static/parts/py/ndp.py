#!/usr/bin/env python3
import os
import json
import parts.jaysDartClass as ndpDart
import parts.segFactory as segArr
import parts.scores as scoresArr

ndp_file = "ndp.json"

global data_ndp
data_ndp = {
			"ndp": {
				"dim": 300,
				"sb": 121,
				"sa": 121,
				"sc": 0,
				"dnit": 1,
				"dih": 3,
				"dn": [ 3 , 3 ],
				"loc": "ndpTemplate",
				"when": ""
			},

			"darts": [
				{
					"dnit": 1,
					"sb": 121,
					"sc": 0,
					"sa": 121,
					"sg": "DNT",
					"played": False,
					"dn": [3,3]
				},
				{
					"dnit": 2,
					"sb": 121,
					"sc": 0,
					"sa": 121,
					"sg": "DNT",
					"played": False,
					"dn": [ 3 ,3 ]
				},
				{
					"dnit": 3,
					"sb": 121,
					"sc": 0,
					"sa": 121,
					"sg": "DNT",
					"played": False,
					"dn": [ 3, 3 ]
				}
			]
		}

#################################################
#     	Get next dart preview info   			#
#################################################
def getndp():
	global data_ndp
	return data_ndp


def getDartInfo(dnit:int):
	global data_ndp
	dIdx = 0
	# first check if darts array exists
	if( dnit in [1,2,3] ):
		print("ndp.py getDartInfo dnit: ", dnit )
		dIdx = dnit-1
	elif( dnit == 0 ):
		print("ndp.py getDartInfo dnit == 0: ", dnit )
		dIdx = dnit
	else:
		print("ndp.py getDartInfo dnit in [123] else: ", dnit )

	try:
		print("ndp.py getNDPInfo dIdx =",dIdx,"returns:", str( data_ndp['darts'][dIdx] ) )

	finally:
		return data_ndp['darts'][dIdx]


