#!/usr/bin/env python3

import os
import json
import parts.segFactory as segArr
import parts.scores as scoresArr

ndp_file = "../ndp.json"

segArray = segArr.segmentArray()
segInfo = []

def getSegInfo(segId):
	for d in segArray:
		if( d['segId'] == segId ):
			return d


def dumpNdp(ndpObj):
	wrNdp = open( ndp_file,"w+")
	wrNdp.write( json.dumps(ndpObj, indent=4) ) 
	wrNdp.close


def visitScore(dartArr):
	sc=0
	for d in dartArr:
		# print("ndpUpdate visitScore d:", d.keys() )
		if( d['sg'] == "DNT"):
			return sc
		else:
			sc += d['sc']

	return sc


def updateDart(dnit:int,segId):
	print("ndpUpdate->updateDart(dnit,segId):\t", dnit,"\t,segId:\t",segId )

	if dnit not in [1,2,3]:
		print("dnit MUST be 1,2 or 3")
		return False

	else:
		segInfo = getSegInfo(segId)
		# print("ndpUpdate-> getSegInfo(segId): ", segInfo , segInfo['segVal'])
		ndpAll = open(ndp_file, "r" )
		temp_ndp = json.load( ndpAll )
		ndpAll.close

	try:
		# dart nr 1 corresponds to arrayIndex 0 etc....
		dartIndex = dnit-1
		if(dartIndex < 0 ):
			print( "updateDart -> dartIndex < 0 !!" )

		else:
			# save some values of current dart
			ogseg =	segId
			ndsb = temp_ndp[1]['darts'][dartIndex]['sb']
			ogsc = segInfo['segVal']
			ogpld = True

			# set score and dn values for this and following dart(s)
			for dIdx in range(dartIndex,3):	
				d = temp_ndp[1]['darts'][dIdx]
				d['sg'] = ogseg
				temp_ndp[0]['ndp']['segs'][dIdx] = ogseg
				d['sb'] = ndsb
				d['sc'] = ogsc
				d['sa'] = ( d['sb'] - d['sc'] )
				d['played'] = ogpld
				d['dn'][0] = scoresArr.drtsNdd( ndsb )
				d['dn'][1] = scoresArr.drtsNdd( d['sa'])
				# change score values for next dart
				ogseg = "DNT"
				ndsb = d['sa']
				ogsc = 0
				ogpld = False

			# save 'ndp' info
			# temp_ndp[1]['ndp']['sb'] never changes
			# temp_ndp[1]['ndp']['dim'] never changes
			# temp_ndp[1]['ndp']['dn'][0] never changes
			temp_ndp[0]['ndp']['dnit'] = dnit
			temp_ndp[0]['ndp']['dih'] = (3-dnit)
			temp_ndp[0]['ndp']['sc'] = visitScore( temp_ndp[1]['darts'] )
			temp_ndp[0]['ndp']['sa'] = (temp_ndp[0]['ndp']['sb'] - temp_ndp[0]['ndp']['sc'])
			temp_ndp[0]['ndp']['dn'][1] = scoresArr.drtsNdd( temp_ndp[0]['ndp']['sa'])

			"""
			except Exception as e:
				print("ndpUpdate.py -> updateDart -> Exception:", e)
			"""
	finally:
		print("ndpUpdate.py -> dumping temp_ndp:\n", str(temp_ndp) )
		dumpNdp(temp_ndp)

