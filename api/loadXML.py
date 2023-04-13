#!/usr/bin/env python3

# Public
import sys, os, json
import xml.etree.ElementTree as ET
from datetime import datetime

# Private
import scores as scrs

clrArr = [
	"#006400",  # 0: DarkGreen  same darts needed
	"#00ff00",  # lime          -1 darts needed
	"#ffab00",  # orange        +1 darts needed
	"#ff0000"   # red           bust !
]


xmlSourcePath 	= "static/parts/xml/"
xmlTemplName 	= "dartBoardSvgSource.xml"
inputFileName 	= xmlSourcePath + xmlTemplName 

# /home/newmate/Documents/DEV/PROJECTS/PYTHON/pyFPL/VERCEL/JaysSVGDartBoard/api/static/tmp
xmlOutputPath 	= "static/tmp/"
xmlOutputName 	= xmlOutputPath + "tmp_xml_bak.xml"


def ndpClrs(dnDiff):
	if( dnDiff == -1 ):
		return  clrArr[2]

	elif( dnDiff == 0 ):
		return  clrArr[0]

	elif( dnDiff == 1 ):
		return  clrArr[1]

	elif( dnDiff == 2 ):
		return  clrArr[3]

	else:
		return  clrArr[0]



def alive(scr):
	# scrDN = scrs.drtsNdd(scr) print(f"alive for {scr}? { ( scrDN <= dih ) } . dn={ scrDN } with {dih} darts in hand (dih)")
	return ( scrs.drtsNdd(scr) <= dih )



"""
	The sourcefile is an svg containing 8 groups:
	svg:[
			"background":[rect,circle],
			"JDDbSgmnts": [path-M01,path-D01,  etc ],
			"JDDbSgmntTxts": [text-M01,blank,blank,blank,blank,text-M18,blank, etc ],
			"legend_top_score": [ text-label, text-value(id-sb) ],
			"legend_bottom_dn": [ text-label, text-label, text-value(id=sbdn) ],
			"legend_bottom_dih": [ text-label, text-value(id=dih) ],
			"legend_colors_bg": [ rect, rect, rect, rect ],
			"legend_colors_txt": [ text, text + text, text,  text ]
		]
"""
def walksvg(dih:int,score:int):
	root = []
	# 	Calculate the darts needed of the score before dart (sbdn).
	sbdn =  scrs.drtsNdd(score)

	try:

		if os.path.exists( inputFileName ):

			tree = ET.parse( inputFileName )
			root = tree.getroot()

			for i,grp in enumerate(root):
				print(f"walksvg root[{i}] '{ root[i].attrib['id'] }' len { len(root[i]) } ")

			if( score > -1 ):

				for seg in root[1]:

					# 	Find the segVal of the element.
					# 	Calculate score after and darts needed after (sa, sadn).
					# 	Update/create scrAftr and sadn values.
					# 	Update score after darts needed (sadn).

					for el in seg.iter():

						attribEl = el.attrib

						if len( attribEl ) > 1:

							if( ("segVal" in attribEl.keys()) and ( int( attribEl['segMulti'] ) > 0 ) ) : 

								segvalue 	= int( attribEl['segVal'] )
								segsa 		= score - segvalue
								sadn 		= scrs.drtsNdd( segsa )
								dndiff 		= sbdn - sadn
								newcolor 	= ""

								if( segsa > 1):
									# score after > 1
									newcolor = ndpClrs( dndiff )

								elif( (segsa == 1) or ( segsa < 0) ):
									# score after == 1 or < 0 .
									# This is NOT a score that is valid --> BUST
									newcolor = clrArr[3] 

								elif( segsa == 0):
									# score after == 0
									if(int( attribEl['segMulti'] ) == 2):
										# This is a double that leaves zero --> WIN
										newcolor = "#cc33ff" # clrArr[1] 
									else:
										# This is NOT a double that leaves zero --> BUST
										newcolor = clrArr[3] 

								else:
									pass
									# print(f"segsa ELSE ??")

								attribEl['style'] = "fill:" + newcolor + ";"
								# print(f"element check: segVal={ segvalue}. Score After = { segsa } which is a { sadn } darter. alive: { alive(segsa) } dn difference = { dndiff }. New color = { newcolor } " )

							else:
								#print(f"no segval in attribEl")
								pass 

						else:
							# print(f" len( attribEl ) = 0 ")
							pass

				# Update the score before ,darts needed and darts in hand texts
				for tseg in root:
					for txtSeg in tseg.iter():
						txtAttrib = txtSeg.attrib
						if len( txtAttrib  ) > 1:
							if( ( "id" in txtAttrib.keys() ) and ( txtAttrib['id'] == "sb" ) ):
								txtSeg.text = str(score)
							elif( ( "id" in txtAttrib.keys() ) and ( txtAttrib['id'] == "dih" ) ):
								txtSeg.text = str(dih)
							elif( ( "id" in txtAttrib.keys() ) and ( txtAttrib['id'] == "sbdn" ) ):
								txtSeg.text = str(sbdn)

			else:
				print(f"walksvg- ndp called with negative SB ({ score }). returning a plain dartboard")

			tree.write( xmlOutputName )

		else:
			print(f"walksvg-{ inputFileName } does NOT exist !")

	except Exception as e:
		print(f"walksvg- createSourceBackUp - exception {e}" )

	finally:
		return xmlOutputName



def ndpsvg(dih:int,score:int):
	# Need to add dimensions. ["100px", "125","150px", "175px", "200px", "250px", "300px", "350px", "400px", "450px", "500px", "600px", "750px"]
	# dimensions are of the dartboard. A legend ribbon of 30px is added beneath the dartboard, making the total height of the svg +30px. 	
	flNm = walksvg(dih,score)

	# Read in the file
	file = open(flNm, "r")
	filedata = file.read()
	file.close()

	clean1 = filedata.replace("<ns0:svg xmlns:ns0=", "<svg xmlns=") 
	clean2 = clean1.replace("ns0:", "") 

	templateFiller = {'tekst': clean2 }
	# print(f"ndpsvg -> inputData { clean2 }" )
	return render_template( "dabo.html", data=templateFiller )

