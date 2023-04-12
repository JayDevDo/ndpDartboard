#!/usr/bin/env python3
import parts.scores as scoresArr
from datetime import datetime

def strTimeStamp():
	return datetime.now().isoformat(timespec='seconds')

def ndpTemplate( sb:int=121):
	#print("ndpTemplate called with sb:\t", str(sb) )
	return	{	
				"ndp":{
						"dim":300,
						"sb": sb, 
						"sa": sb, 
						"sc": 0, 
						"dnit": 0, 
						"dih": 3, 
						"dn": [
							scoresArr.drtsNdd(sb), 
							scoresArr.drtsNdd(sb)
						],
						"loc": "ndpTemplate",
						"when": strTimeStamp()
				},
				"darts":[
						dartTemplate( dnit=1, sb=sb ),
						dartTemplate( dnit=2, sb=sb ),
						dartTemplate( dnit=3, sb=sb )
				]
			}

def dartTemplate( dnit:int(1), sb:int(121)):
	#print("ndpTemplate called with sb:\t", str(sb) ,"\tand dnit:\t", str(dnit) )

	if( sb != 121 ):
		return	{
					"dnit": max([ dnit , 1 ]) ,
					"sb": sb,
					"sc": 0,
					"sa": sb,
					"sg": "DNT",
					"played": False,
					"dn":[ scoresArr.drtsNdd(sb), scoresArr.drtsNdd(sb) ] 
		}

	else:

		return	{
					"dnit": max([ dnit , 1 ]) ,
					"sb": 121,
					"sc": 0,
					"sa": 121,
					"sg": "DNT",
					"played": False,
					"dn": [ 3, 3 ]
		}
