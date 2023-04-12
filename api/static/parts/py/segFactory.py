#!/usr/bin/env python3

segmentBase	=	[  "S",     "T",    "B",    "D",    "M" ]
multis		=	[   1,      3,      1,      2,      0   ]
segTexts	=	[ "Small single","Treble","Big single","Double","Missed"]
numberBase	=	[ 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20 ]
segRadPerc	=	[ 0.1200, 0.4900, 0.5900, 0.8100, 0.8900, 0.9999 ]
colors		=	[
					[ "#CBCBCB", "#000000"], # Small:      white / black
					[ "#00FF00", "#FF0000"], # Triples:    green / red
					[ "#CBCBCB", "#000000"], # Big:        white / black
					[ "#00FF00", "#FF0000"], # Doubles:    green / red
					[ "#585858", "#585858"], # Missed:     always same color
					[ "#00FF00", "#FF0000"]  # Bull:       green / red (not actually used )
				]

def colorpicker(nrIdx,segIdx):
	if ( (nrIdx%2) == 1 ):
		return colors[segIdx][1]
	else:
		return colors[segIdx][0]

def radAngles(nrIdx,segIdx):
	if( nrIdx == 0 ):
		retObj = { 
			"SA": 9, 
			"EA": 27, 
			"IR": segRadPerc[segIdx], 
			"OR": segRadPerc[segIdx+1]
		}

	elif( nrIdx == 19 ):
		retObj = { 
			"SA": 351, 
			"EA": 369, 
			"IR": segRadPerc[segIdx], 
			"OR": segRadPerc[segIdx+1]
		}

	else: 
		retObj = { 
			"SA": ( ( nrIdx * 18 ) + 9 ) , 
			"EA":( ( nrIdx * 18 ) + 27 ), 
			"IR": segRadPerc[segIdx], 
			"OR": segRadPerc[segIdx+1]  
		}

	return retObj;

def nrToStr(n):
	if( len(str(n))<2 ):
		return str("0"+str(n))
	else:
		return str(n)

def segmentArray():
	segArr = []
	nrIdx  = 0

	for nr in numberBase: 
		"""  console.log(nr, "creating segments for", numberBase[nr] ) """
		# print("nrIdx\t", str(nrIdx), "\nnr:\t", str(nr), "\tcreating segments for\t", numberBase[nrIdx] ) 
		segIdx = 0
		for seg in segmentBase:
			#print( "nrIdx:", str(nrIdx), "nr", str(nr), "segIdx:",  str(segIdx), "seg:", str(seg) )
			curRadAng       =   radAngles(nrIdx, segIdx)
			curseg          =   {
									'segId'        :   seg + nrToStr( numberBase[nrIdx] ),
									'segGrp'       :   str(nr),
									'segMulti'     :   multis[segIdx],
									'segVal'       :   multis[segIdx] * numberBase[nrIdx],
									'segSA'        :   curRadAng['SA'],
									'segEA'        :   curRadAng['EA'],
									'segInRad'     :   curRadAng['IR'],
									'segOutRad'    :   curRadAng['OR'],
									'segColor'     :   colorpicker(nrIdx,segIdx),
									'dbOrder'      :   str(nrIdx + 1) + str(segIdx + 1) ,
									'segTxt'       :   str(segTexts[segIdx]) + " " + str(numberBase[nrIdx]) ,
									'segPath'      :   ""
								}
			segArr.append( curseg )
			segIdx+=1
		
		# print("end of segmentBase-loop", str(segIdx), "\tseg\t", seg )
		nrIdx+=1

	# print("end of numberBase-loop", str(nrIdx), "\tnr\t", nr )
	""" adding bulls. In the end adding them as fixed objects shortens and speeds up the code """
	segArr.append({ 'segId': "SBL",'segGrp': "25",'segMulti': 1,'segVal': 25,'segSA': 0,'segEA': 360,'segInRad': 0.0500, 	'segOutRad': 0.1200,'segColor': "#00FF00",'dbOrder': 251,'segTxt': "Single Bull",'segPath': "" })
	segArr.append({ 'segId': "DBL",'segGrp': "25",'segMulti': 2,'segVal': 50,'segSA': 0,'segEA': 360,'segInRad': 0,		'segOutRad': 0.0500,'segColor': "#FF0000",'dbOrder': 252,'segTxt': "Double Bull",'segPath': "" })

	# print(str(segArr))
	return segArr