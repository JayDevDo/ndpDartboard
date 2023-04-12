import sys, os, json
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Flask, render_template, send_file, request, jsonify

xmlSourcePath 	= "static/parts/xml/"
xmlTemplName 	= "dartBoardSvgSource.xml"
inputFileName 	= xmlSourcePath + xmlTemplName 

# /home/newmate/Documents/DEV/PROJECTS/PYTHON/pyFPL/VERCEL/JaysSVGDartBoard/api/static/tmp
xmlOutputPath 	= "static/tmp/"
xmlOutputName 	= xmlOutputPath + "tmp_xml_bak.xml"


app = Flask(__name__)

@app.route('/')
def home():
	xmlVars = {
		'time:':  datetime.now().isoformat(timespec='seconds'),
		'xmlSourcePath': xmlSourcePath,
		'xmlTemplName': xmlTemplName,
		'inputFileName': inputFileName,
		'xmlOutputPath': xmlOutputPath,
		'xmlOutputName': xmlSourcePath,
		'json present': os.path.exists("static/json/scores.json")
	}
	respObj = {
		'homeReply': "Hi World if vercel allows this deployment. Cause they kept pushing old braches from their cache."
	}
	print(f"home called. What is home actually? { request }. and script vars: { jsonify(xmlVars) }")
	respObj['xmlVars']= xmlVars
	return respObj

@app.route('/about')
def about():
	return '<h1>ABOUT</h1><h2>test fase</h2><a src="http://ndpdartboard-jaydevdo.vercel.app/">see it work</a>'
