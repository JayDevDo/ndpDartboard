import sys, os, json
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Flask, render_template, send_file, request, jsonify

import loadXML as ndpsvg
import scores as scrs

xmlSP 	= "static/parts/xml/"
xmlTN 	= "dartBoardSvgSource.xml"
xmlIFN 	= xmlSP + xmlTN 

# /home/newmate/Documents/DEV/PROJECTS/PYTHON/pyFPL/VERCEL/JaysSVGDartBoard/api/static/tmp
xmlOP 	= "static/tmp/"
xmlON 	= xmlOP + "tmp_xml_bak.xml"

app = Flask(__name__)


@app.route('/')
def home():
	xmlVars = {
		'time:': datetime.now().isoformat(timespec='seconds'),
		'xmlSP': xmlSP,
		'xmlTN': xmlTN,
		'xmlIFN': xmlIFN,
		'xmlOP': xmlOP,
		'xmlON': xmlON,
		'json available': os.path.exists("static/json/scores.json"),
		'loadXML active': ndpsvg.ndpClrs(2),
		'vstsNdd': scrs.vstsNdd(39)
	}

	respObj = { 'homeReply': "Hi World ! (if vercel allows this deployment.)" }

	print(f"home called. What is home actually?. and script vars: { json.dumps(xmlVars) }" )
	respObj['xmlVars']= xmlVars

	return respObj



@app.route('/ndp')
def ndp():
	nm = ndpsvg.walksvg(3,152)
	# return walksvg()
	return send_file( nm )



@app.route('/ndp/<int:dih>/<int:score>', methods=['GET'])
def svgDartBoard(dih:int,score:int):
	# Need to add dimensions. ["100px", "125","150px", "175px", "200px", "250px", "300px", "350px", "400px", "450px", "500px", "600px", "750px"]
	# dimensions are of the dartboard. A legend ribbon of 30px is added beneath the dartboard, making the total height of the svg +30px. 	
	flNm = ndpsvg.walksvg(dih,score)

	# Read in the file
	file = open(flNm, "r")
	filedata = file.read()
	file.close()

	clean1 = filedata.replace("<ns0:svg xmlns:ns0=", "<svg xmlns=") 
	clean2 = clean1.replace("ns0:", "") 

	templateFiller = {'tekst': clean2 }
	# print(f"ndpsvg -> inputData { clean2 }" )
	return render_template( "dabo.html", data=templateFiller )
