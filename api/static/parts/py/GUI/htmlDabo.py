#!/usr/bin/env python3

import wx
import wx.html2 as webview
import wx.grid
import wx.html

import math
import os
import time

import jaysDartClass as ndpDart
import scores as scoresArr
import ndp as ndp
import inputBoard as ipboard

baseUrl = "http://127.0.0.1:5123/dabo/"
 # src/html/dabo.html

class MyFrame(wx.Frame):

	def __init__(self, *args, **kwds):

		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE

		wx.Frame.__init__(self, *args, **kwds)

		print("running on ", str(wx.PlatformInfo) )

		# ViewModel variables
		self.wdwW = 1200 
		self.wdwH = 900

		self.darts = []

		self.ndp_sb = 121
		self.ndp_sc = self.visitScore()
		self.ndp_sa = ( self.ndp_sb - self.ndp_sc )
		self.activeDart = 1
		self.dih = 3
		self.ndp_dnsb = scoresArr.drtsNdd( self.ndp_sb )
		self.ndp_dnsa = scoresArr.drtsNdd( self.ndp_sa )
		self.fin_alive = True # add algo later

		# View Display
		"""
		###		DABO 0 		###
		"""
		self.dabo0DIH 			= wx.StaticText(self, wx.ID_ANY, "0 DIH")
		self.dabo0FinAlive 		= wx.CheckBox(self, wx.ID_ANY) # wx.StaticText(self, wx.ID_ANY, " SA dn")
		self.dabo0AD 			= wx.StaticText(self, wx.ID_ANY, "0 AD")
		self.dabo0SB 			= wx.StaticText(self, wx.ID_ANY, "0 SB ")
		self.dabo0SBDN 			= wx.StaticText(self, wx.ID_ANY, "0 SB (dn)")
		self.dabo0SG 			= wx.StaticText(self, wx.ID_ANY, "0 Seg ")
		self.dabo0SC 			= wx.StaticText(self, wx.ID_ANY, "0 SC")
		self.dabo0SA 			= wx.StaticText(self, wx.ID_ANY, "0 SA")
		self.dabo0SADN 			= wx.StaticText(self, wx.ID_ANY, "0 SA (dn)")

		# labels:
		self.dabo0DIH_lbl 		= wx.StaticText(self, wx.ID_ANY, "DIH")
		self.dabo0FinAlive_lbl 	= wx.StaticText(self, wx.ID_ANY, "Alive")
		self.dabo0AD_lbl 		= wx.StaticText(self, wx.ID_ANY, "Active Dart")
		self.dabo0SB_lbl 		= wx.StaticText(self, wx.ID_ANY, "Score Before")
		self.dabo0SBDN_lbl 		= wx.StaticText(self, wx.ID_ANY, "Score Before (dn)")
		self.dabo0SG_lbl 		= wx.StaticText(self, wx.ID_ANY, "Segment hit")
		self.dabo0SC_lbl 		= wx.StaticText(self, wx.ID_ANY, "Visit Score ")
		self.dabo0SA_lbl 		= wx.StaticText(self, wx.ID_ANY, "Score After")
		self.dabo0SADN_lbl 		= wx.StaticText(self, wx.ID_ANY, "Score After (dn)")


		"""
		####################################################################################################################
		INPUT DARTBOARD
		####################################################################################################################
		"""
		self.daboInputW = int(self.wdwW/2)
		self.daboInputH = int((self.wdwW/2)*1.15)

		self.inputTitle = str(self.ndp_sb)+"#"+str(self.activeDart)
		self.daboInput 	= 	ipboard.inputDaboFrame(
								self, 
								wx.ID_ANY, 
								title=self.inputTitle, 
								pos=wx.DefaultPosition,
								size=( [self.daboInputW , self.daboInputH]), 
								style=wx.CAPTION | wx.BORDER_NONE 
							)


		"""
		####################################################################################################################
		DABO 1
		####################################################################################################################
		"""
		# dabo1 will be stored in dabo1Sizer
		dabo1Url = baseUrl + "/1/"
		self.dabo1 = webview.WebView.New(self)
		self.dabo1.LoadURL(dabo1Url)
		self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.daboTitleChangedEvt, self.dabo1)

		# dabo1Info * will be stored in dabo1InfoSizer
		self.dabo1InfoSB 		= wx.StaticText(self, wx.ID_ANY, " SB ")
		self.dabo1InfoSBDN 		= wx.StaticText(self, wx.ID_ANY, " SB dn")
		self.dabo1InfoSG 		= wx.StaticText(self, wx.ID_ANY, " Seg ")
		self.dabo1InfoSC 		= wx.StaticText(self, wx.ID_ANY, " Score ")
		self.dabo1InfoSA 		= wx.StaticText(self, wx.ID_ANY, " SA ")
		self.dabo1InfoSADN 		= wx.StaticText(self, wx.ID_ANY, " SA dn")

		"""
		####################################################################################################################
		DABO 2
		####################################################################################################################
		"""
		# dabo2 will be stored in dabo1Sizer
		dabo2Url = baseUrl + "/2/"
		self.dabo2 = webview.WebView.New(self)
		self.dabo2.LoadURL(dabo2Url)
		self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.daboTitleChangedEvt, self.dabo2)

		# dabo2Info * will be stored in dabo2InfoSizer
		self.dabo2InfoSB 		= wx.StaticText(self, wx.ID_ANY, " SB ")
		self.dabo2InfoSBDN 		= wx.StaticText(self, wx.ID_ANY, " SB dn")
		self.dabo2InfoSG 		= wx.StaticText(self, wx.ID_ANY, " Seg ")
		self.dabo2InfoSC 		= wx.StaticText(self, wx.ID_ANY, " Score ")
		self.dabo2InfoSA 		= wx.StaticText(self, wx.ID_ANY, " SA ")
		self.dabo2InfoSADN 		= wx.StaticText(self, wx.ID_ANY, " SA dn")

		"""
		####################################################################################################################
		DABO 3
		####################################################################################################################
		"""
		# dabo3 will be stored in dabo1Sizer
		dabo3Url = baseUrl + "/3/"
		self.dabo3 = webview.WebView.New(self)
		self.dabo3.LoadURL(dabo3Url)
		self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.daboTitleChangedEvt, self.dabo3)
		
		# dabo3Info * will be stored in dabo3InfoSizer
		self.dabo3InfoSB 		= wx.StaticText(self, wx.ID_ANY, " SB ")
		self.dabo3InfoSBDN 		= wx.StaticText(self, wx.ID_ANY, " SB dn")
		self.dabo3InfoSG 		= wx.StaticText(self, wx.ID_ANY, " Seg ")
		self.dabo3InfoSC 		= wx.StaticText(self, wx.ID_ANY, " Score ")
		self.dabo3InfoSA 		= wx.StaticText(self, wx.ID_ANY, " SA ")
		self.dabo3InfoSADN 		= wx.StaticText(self, wx.ID_ANY, " SA dn")

		wx.CallLater(500, self.getNDPinfo )
		self.__setProps()


	def getDart( self, dnit ):
		"""  getDart returns self.darts[dnit-1] """	
		if( (len(self.darts)==3) and (dnit in [1,2,3]) ):
			print("getDart ", dnit, "returning ", self.darts[ dnit - 1 ] )
			return self.darts[dnit-1]
		else:
			print( "getDart found no darts in self.darts[]. Loading from ndp.json" )
			self.getNDPinfo()


	def getNDPinfo(self):
		""" getNDPinfo: gets the current data from ndp.json and updates ndp_info """
		try:
			jsonNDPAll 	= dict(ndp.getndp())
			jsonNDP 	= jsonNDPAll['ndp']
			jsonDarts 	= jsonNDPAll['darts']
			print("getNDPinfo -jsonNDP:\t", str(jsonNDP) )

			self.clearVisit("getNDPinfo --> before adding from ndp")

			for d in jsonDarts:
				print("appending d:", str(d) )
				self.darts.append( d )

			jsonDartCount = self.dartCounter("getNDPinfo -> jsonDartCount after append ")

			if( jsonDartCount[0] == 4 ):
				print("jsonDartCount[0] == 4 ")
				self.ndp_sb = self.darts[2]['sa']

			elif( jsonDartCount[0] == 3 ):
				print("jsonDartCount[0] == 3 ")
				self.ndp_sb = self.darts[2]['sa']

			elif( jsonDartCount[0] == 2 ):
				print("jsonDartCount[0] == 2 ")
				self.ndp_sb = self.darts[2]['sb']

			elif( jsonDartCount[0] == 1 ):
				print("jsonDartCount[0] == 1 ")
				self.ndp_sb = self.darts[1]['sb']

			elif( jsonDartCount[0] < 1 ):
				print("jsonDartCount[0] < 1 ")
				self.ndp_sb = self.darts[0]['sb']

			else:
				print("No darts thrown (yet)")

		finally:
			self.updateView("getNDPinfo finished")
			# print("getNDPinfo finished" )


	def isActiveBoard(self):
		print("isActiveBoard: ", str(self.activeDart) )
		boards = [ self.dabo1, self.dabo2, self.dabo3 ]
		for i in range(0,3):
			if(i==self.activeDart):
				print("Board ", str(i)," is active")
				boards[i].SetBackgroundColour(wx.Colour("#DADADA"))
				# boards[i].Enabled(False)


	def dartCounter(self, whosCalling):
		""" dartCounter: returns a tuple with darts played out of items in self.darts """
		played = 0
		for d in self.darts:
			if( d['played'] ):
				played+=1

		print("dartCounter called by ", whosCalling , " returns:\t", str( [played, len(self.darts)] ) )
		self.activeDart = min( [ 3 , ( played+1 ) ] )
		self.dih = 4 - self.activeDart
		return (played, len(self.darts))


	def visitScore(self):
		sc = 0
		for d in self.darts:
			if(d['sg'] == "DNT"):
				# Dart Not Thrown = 0
				sc += 0
			else:
				sc += int(d['sc'])

		print("htmlDabo.py visitScore sc=", str(sc) )
		return sc


	def clearVisit(self, whosCalling):
		""" clearVisit: empties self.darts for the moment"""
		print("ClearVisit, emptying self.darts on request by:", whosCalling )
		self.darts = []


	def updateView(self, caller):
		# self.dabo0DIH.SetLabel(str(self.dih))
		curSeg = self.getDart(self.activeDart)
		print("updateView activeDart:\t", caller, "\t" , str(self.activeDart) , "\tcurSeg:", str(curSeg) )
		self.dabo0FinAlive.SetValue(self.fin_alive)
		self.dabo0AD.SetLabel(str(self.activeDart))
		self.dabo0SBDN.SetLabel(str(self.ndp_dnsb))
		self.dabo0SADN.SetLabel(str(self.ndp_dnsa))
		self.dabo0DIH.SetLabel(str(self.dih))
		if( curSeg ):
			self.dabo0SG.SetLabel( curSeg['sg'] )
			self.dabo0SB.SetLabel( str(curSeg['sb']) )
			self.dabo0SC.SetLabel( str(curSeg['sc']) )
			self.dabo0SA.SetLabel( str(curSeg['sa']) )
		else:
			self.dabo0SG.SetLabel( "DNT"	)
			self.dabo0SB.SetLabel( "121"	)
			self.dabo0SC.SetLabel( "000"	)
			self.dabo0SA.SetLabel( "121"	)

		self.isActiveBoard()

	def afterDart1( self, evt ):
		""" afterDart1 takes care of updating app views and reloading next dabo's """
		print("afterDart1 evt.GetString = ", evt.GetString() )

		if( len( self.darts ) > 0 ):
			self.ndp_sb = self.darts[ 0 ]['sb']
			self.ndp_sc = self.darts[ 0 ]['sc']
			self.ndp_sa = self.darts[ 0 ]['sa']
			self.ndp_dnsb = scoresArr.drtsNdd( self.ndp_sb )
			self.ndp_dnsa = scoresArr.drtsNdd( self.ndp_sa )
			self.fin_alive = True
			self.activeDart = 2

			self.dabo1InfoSB.SetLabel( str( self.darts[ 0 ]['sb'] ) )
			self.dabo1InfoSA.SetLabel( str( self.darts[ 0 ]['sa'] ) )
			self.dabo1InfoSG.SetLabel( str( self.darts[ 0 ]['sg'] ) )
			self.dabo1InfoSC.SetLabel( str( self.darts[ 0 ]['sc'] ) )
			self.dabo1InfoSBDN.SetLabel( str( self.darts[ 0 ]['dn'][0] ) )
			self.dabo1InfoSADN.SetLabel( str( self.darts[ 0 ]['dn'][1] ) )

			self.dabo2.LoadURL(baseUrl+"2/")
			self.dabo3.LoadURL(baseUrl+"3/")
			self.updateView("afterDart1")

		else:
			print("afterDart len(self.darts) = 0 !!")	


	def afterDart2( self, evt ):
		""" afterDart1 takes care of updating app views and reloading next dabo's """
		print("afterDart2 evt.GetString = ", evt.GetString() )

		if( len( self.darts ) > 1 ):
			self.ndp_sb = self.darts[ 1 ]['sb']
			self.ndp_sc = self.darts[ 1 ]['sc']
			self.ndp_sa = self.darts[ 1 ]['sa']
			self.ndp_dnsb = scoresArr.drtsNdd( self.ndp_sb )
			self.ndp_dnsa = scoresArr.drtsNdd( self.ndp_sa )
			self.fin_alive = True
			self.activeDart = 3

			self.dabo2InfoSB.SetLabel( str( self.darts[ 1 ]['sb'] ) )
			self.dabo2InfoSA.SetLabel( str( self.darts[ 1 ]['sa'] ) )
			self.dabo2InfoSG.SetLabel( str( self.darts[ 1 ]['sg'] ) )
			self.dabo2InfoSC.SetLabel( str( self.darts[ 1 ]['sc'] ) )
			self.dabo2InfoSBDN.SetLabel( str( self.darts[ 1 ]['dn'][0] ) )
			self.dabo2InfoSADN.SetLabel( str( self.darts[ 1 ]['dn'][1] ) )

			self.dabo3.LoadURL(baseUrl+"3/")
			self.updateView("afterDart2")

		else:
			print("afterDart len(self.darts) = 0 !!")	


	def afterDart3( self, evt ):
		""" afterDart3 takes care of updating app views and reloading next dabo's """
		print("afterDart3 evt.GetString = ", evt.GetString() )

		if( len( self.darts ) > 2 ):
			self.ndp_sb = self.darts[ 2 ]['sb']
			self.ndp_sc = self.darts[ 2 ]['sc']
			self.ndp_sa = self.darts[ 2 ]['sa']
			self.ndp_dnsb = scoresArr.drtsNdd( self.ndp_sb )
			self.ndp_dnsa = scoresArr.drtsNdd( self.ndp_sa )
			self.fin_alive = True
			self.activeDart = 4

			self.dabo3InfoSB.SetLabel( str( self.darts[ 2 ]['sb'] ) )
			self.dabo3InfoSA.SetLabel( str( self.darts[ 2 ]['sa'] ) )
			self.dabo3InfoSG.SetLabel( str( self.darts[ 2 ]['sg'] ) )
			self.dabo3InfoSC.SetLabel( str( self.darts[ 2 ]['sc'] ) )
			self.dabo3InfoSBDN.SetLabel( str( self.darts[ 2 ]['dn'][0] ) )
			self.dabo3InfoSADN.SetLabel( str( self.darts[ 2 ]['dn'][1] ) )

			self.updateView("afterDart3 --> activeDart = 0")

		else:
			print("afterDart len(self.darts) = 0 !!")	


	# WebView events
	def daboTitleChangedEvt(self, evt):
		"""
			# the JavaScript function segmentClick has fired a post to the boardserver
			# the boardserver fired ndpUpdate updateDart procedure which dumps the new ndp object as json.
			# daboTitleChangedEvt is triggered by JavaScript function segmentClick changing the window title
			# after receiving post confirmation from boardserver.
		"""


		# print("daboTitleChangedEvt received event from", evt.GetString() )
		# print("daboTitleChangedEvt evt.GetString()[1]", evt.GetString()[1] )
		# evt.Skip()
		# evt.Veto()
		daboTtl = evt.GetString()

		self.getNDPinfo()
		time.sleep(0.5)
		
		if( (len(daboTtl)>0) and (daboTtl[0] == "#") ):
			daboNr = int(evt.GetString()[1])
			if( daboNr == 1 ):
				self.afterDart1(evt)
			elif( daboNr == 2 ):
				self.afterDart2(evt)
			elif( daboNr == 3 ):
				self.afterDart3(evt)
			else:
				print("daboTitleChangedEvt daboNr Else?? ", daboNr )

		else:
			print("daboTitleChangedEvt first load, dabo title =", daboTtl )


	def OnWebViewLoaded(self, evt):
		# The full document has loaded
		print("OnWebViewLoaded received event from", evt.GetURL() )
		evt.Skip()


	def __doLayout(self):
		"""  __doLayout organises sizers and other layout functions """
		# WdwSizer for the main window (includes scores details frame, daboInput frame and frmSizer )
		wdwSizer = wx.BoxSizer(wx.HORIZONTAL)
		# frm sizer for the entire frame (includes dabo1/2/3Sizers )
		frmSizer = wx.BoxSizer(wx.VERTICAL)

		# scores sizer for the entirescores detail frame (includes dabo1/2/3Sizers )
		scrsSizer = wx.GridSizer( 9, 3, 1, 1 )
		scrsSizer.AddMany([
			( (10,20),0,0 ),
			( (10,20),0,0 ),
			( (10,20),0,0 ),

			( self.dabo0AD_lbl, 	0,	0, 0 ),
			( self.dabo0DIH_lbl, 	0,	0, 0 ),
			( self.dabo0FinAlive_lbl,0,	0, 0 ),

			( self.dabo0AD, 		0,	0, 0 ),
			( self.dabo0DIH, 		0,	0, 0 ),
			( self.dabo0FinAlive, 	0,	0, 0 ),

			( self.dabo0SBDN_lbl, 	0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),
			( (20,50),0,0 ),
			( self.dabo0SB_lbl, 	0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),

			( self.dabo0SBDN, 		0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),
			( (20,50),0,0 ),
			( self.dabo0SB, 		0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),

			( self.dabo0SG_lbl, 	0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),
			( (20,50),0,0 ),
			( self.dabo0SC_lbl, 	0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),

			( self.dabo0SG, 		0, 	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),
			( (20,50),0,0 ),
			( self.dabo0SC, 		0, 	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),

			( self.dabo0SADN_lbl, 	0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),
			( (20,50),0,0 ),
			( self.dabo0SA_lbl, 	0,	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),

			( self.dabo0SADN, 		0, 	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),
			( (20,50),0,0 ),
			( self.dabo0SA, 		0, 	wx.ALIGN_TOP | wx.ALIGN_CENTRE, 0 ),

		])	


		# daboInputSizer
		daboInputSizer = wx.BoxSizer(wx.VERTICAL)
		daboInputSizer.Add( self.daboInput, 	proportion=1, 	flag=wx.EXPAND,			border=0 )


		# dabo sizers include html preview and dabo info sizer
		dabo1Sizer = wx.BoxSizer(wx.HORIZONTAL)
		dabo1InfoSizer = wx.GridSizer( 6, 2, 1, 1)
		dabo2Sizer = wx.BoxSizer(wx.HORIZONTAL)
		dabo2InfoSizer = wx.GridSizer( 6, 2, 1, 1)
		dabo3Sizer = wx.BoxSizer(wx.HORIZONTAL)
		dabo3InfoSizer = wx.GridSizer( 6, 2, 1, 1)

		# dabo1InfoSizer includes infoSB, infoSA, infoSeg (atm)
		dabo1InfoSizer.AddMany([
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo1InfoSB,	1,	wx.ALIGN_RIGHT,	1),
			(self.dabo1InfoSBDN,1,	wx.ALIGN_RIGHT,	1),
			(self.dabo1InfoSG,	1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo1InfoSC,	1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo1InfoSA,	1,	wx.ALIGN_RIGHT,	1),
			(self.dabo1InfoSADN,1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			((40, 30), 0, wx.ALIGN_RIGHT,1)
		])

		dabo2InfoSizer.AddMany([
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo2InfoSB,	1,	wx.ALIGN_RIGHT,	1),
			(self.dabo2InfoSBDN,1,	wx.ALIGN_RIGHT,	1),
			(self.dabo2InfoSG,	1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo2InfoSC,	1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo2InfoSA,	1,	wx.ALIGN_RIGHT,	1),
			(self.dabo2InfoSADN,1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			((40, 30), 0, wx.ALIGN_RIGHT,1)
		])

		dabo3InfoSizer.AddMany([
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo3InfoSB,	1,	wx.ALIGN_RIGHT,	1),
			(self.dabo3InfoSBDN,1,	wx.ALIGN_RIGHT,	1),
			(self.dabo3InfoSG,	1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo3InfoSC,	1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			(self.dabo3InfoSA,	1,	wx.ALIGN_RIGHT,	1),
			(self.dabo3InfoSADN,1,	wx.ALIGN_RIGHT,	1),
			((40, 30), 0, wx.ALIGN_RIGHT,1),
			((40, 30), 0, wx.ALIGN_RIGHT,1)
		])

		dabo1Sizer.Add( self.dabo1, 	proportion=1, 	flag=wx.EXPAND,			border=0 )
		dabo1Sizer.Add( dabo1InfoSizer, proportion=1, 	flag=wx.ALIGN_RIGHT, 	border=1 )

		dabo2Sizer.Add( self.dabo2,		proportion=1,	flag=wx.EXPAND,			border=0 )
		dabo2Sizer.Add( dabo2InfoSizer, proportion=1, 	flag=wx.ALIGN_RIGHT, 	border=1 )

		dabo3Sizer.Add( self.dabo3,		proportion=1,	flag=wx.EXPAND,			border=0 )
		dabo3Sizer.Add( dabo3InfoSizer, proportion=1, 	flag=wx.ALIGN_RIGHT, 	border=1 )

		frmSizer.Add(dabo1Sizer,1,wx.EXPAND | wx.ALIGN_LEFT,0)
		frmSizer.Add(dabo2Sizer,1,wx.EXPAND | wx.ALIGN_LEFT,0)
		frmSizer.Add(dabo3Sizer,1,wx.EXPAND | wx.ALIGN_LEFT,0)

		wdwSizer.Add( scrsSizer,		1, wx.EXPAND | wx.ALIGN_LEFT, 2 )
		wdwSizer.Add( daboInputSizer,	4, wx.EXPAND | wx.ALIGN_CENTRE, 2)
		wdwSizer.Add( frmSizer, 		2, wx.EXPAND | wx.ALIGN_RIGHT, 2 )

		self.SetSizer( wdwSizer )
		self.Layout()
		
	
	def __setProps(self):
		self.SetSize((self.wdwW, self.wdwH))
		self.SetTitle("py NDP GUI II")
		self.SetBackgroundColour("#000000")
		self.daboInput.SetBackgroundColour("#ff0000")
		self.dabo1.SetBackgroundColour("#000000")
		self.dabo2.SetBackgroundColour("#000000")
		self.dabo3.SetBackgroundColour("#000000")

		self.dabo0SB.SetFont( 	wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0SBDN.SetFont( wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0SG.SetFont( 	wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0SC.SetFont( 	wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0SA.SetFont( 	wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0SADN.SetFont( wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0AD.SetFont( 	wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo0DIH.SetFont( 	wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.dabo1InfoSB.SetFont( 	wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo1InfoSBDN.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo1InfoSG.SetFont( 	wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo1InfoSC.SetFont( 	wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo1InfoSA.SetFont( 	wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo1InfoSADN.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.dabo2InfoSB.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo2InfoSBDN.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo2InfoSG.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo2InfoSC.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo2InfoSA.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo2InfoSADN.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.dabo3InfoSB.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo3InfoSBDN.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo3InfoSG.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo3InfoSC.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo3InfoSA.SetFont(   wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.dabo3InfoSADN.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.__doLayout()





class MyApp(wx.App):
	def OnInit(self):
		self.frame = MyFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True


	def runServer(usePort):
		# make a thread that runs dabo-server
		pass


# end of class MyApp

if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()

"""
	let JDDbSgmntArc    =   d3.arc()
								.innerRadius(   function(data){ return (JDDbR * data.SegInRad);})
								.outerRadius(   function(data){ return ((JDDbR * 0.995) * data.SegOutRad);})
								.startAngle(    function(data){ return (data.SegSA * (Math.PI/180)); }) 
								.endAngle(      function(data){ return (data.SegEA * (Math.PI/180)); }) 
							;

"""