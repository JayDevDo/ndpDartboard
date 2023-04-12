#!/usr/bin/env python3

import wx
import wx.html2 as webview
import wx.grid
import wx.html

import math
import os
import time

baseUrl = "http://127.0.0.1:5123/input/"

class inputDaboFrame(wx.Frame):

	def __init__(self, *args, **kwds):

		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE

		wx.Frame.__init__(self, *args, **kwds)

		print("running on ", str(wx.PlatformInfo) )
		print("args kwds", str(kwds) )
		print("args kwds['title']", str(kwds['title']) )
		self.startArgs = kwds['title'].split("#")
		print("self.startArgs", str(self.startArgs) )

		# ViewModel variables
		self.darts = []
		self.ndp_sb = int(self.startArgs[0])
		self.ndp_sc = 0
		self.ndp_sa = ( self.ndp_sb - self.ndp_sc )
		self.activeDart = int(self.startArgs[1])
		self.dih = 3
		self.ndp_dnsb = 3
		self.ndp_dnsa = 3
		self.fin_alive = True # add algo later


		"""
		####################################################################################################################
		DABO 1
		####################################################################################################################
		"""
		# dabo1 will be stored in inputDaboSizer
		inputURL = baseUrl + "1"
		self.inputBoard = webview.WebView.New(self)
		self.inputBoard.LoadURL(inputURL)
		self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.inputTitleChangedEvt, self.inputBoard)

		self.__setProps()



	def afterClick( self, evt ):
		""" afterClick takes care of updating app views and reloading next dabo's """
		print("afterClick evt.GetString = ", evt.GetString() )
		# self.updateView("afterClick --> activeDart = 0")
		print("afterDart len(self.darts) = 0 !!")	


	# WebView events
	def inputTitleChangedEvt(self, evt):
		"""
			# the JavaScript function segmentClick has fired a post to the boardserver
			# the boardserver fired ndpUpdate updateDart procedure which dumps the new ndp object as json.
			# inputTitleChangedEvt is triggered by JavaScript function segmentClick changing the window title
			# after receiving post confirmation from boardserver.
		"""


		# print("inputTitleChangedEvt received event from", evt.GetString() )
		# print("inputTitleChangedEvt evt.GetString()[1]", evt.GetString()[1] )
		# evt.Skip()
		# evt.Veto()
		daboTtl = evt.GetString()

		# self.getNDPinfo()
		time.sleep(0.5)
		
		if( (len(daboTtl)>0) and (daboTtl[0] == "#") ):
			daboNr = int(evt.GetString()[1])
			if( daboNr == 1 ):
				self.afterClick(evt)
			elif( daboNr == 2 ):
				self.afterClick(evt)
			elif( daboNr == 3 ):
				self.afterClick(evt)
			else:
				print("inputTitleChangedEvt daboNr Else?? ", daboNr )

		else:
			print("inputTitleChangedEvt first load, dabo title =", daboTtl )


	def OnWebViewLoaded(self, evt):
		# The full document has loaded
		print("inputDaboFrame OnWebViewLoaded received event from", evt.GetURL() )
		evt.Skip()


	def __doLayout(self):
		"""  __doLayout organises sizers and other layout functions """
		# frm sizer for the entire frame (includes dabo1/2/3Sizers )
		inputDaboSizerMain = wx.BoxSizer(wx.VERTICAL)

		# dabo sizers include html preview and dabo info sizer
		inputDaboSizer = wx.BoxSizer(wx.HORIZONTAL)
		inputDaboSizer.Add( self.inputBoard, 	proportion=1, 	flag=wx.EXPAND,			border=0 )
		inputDaboSizerMain.Add(inputDaboSizer,1,wx.EXPAND | wx.ALIGN_LEFT,0)

		self.SetSizer( inputDaboSizerMain )
		self.Layout()
		
	
	def __setProps(self):
		self.SetTitle("Dart Nr "+ self.startArgs[1] )
		self.SetBackgroundColour("#000000")
		self.inputBoard.SetBackgroundColour("#000000")
		self.__doLayout()



class MyApp(wx.App):
	def OnInit(self):
		# self.frame = inputDaboFrame(None, wx.ID_ANY, "")
		# style=wx.DEFAULT_FRAME_STYLE wx.BORDER_NONE
		actDart = 1
		sb=121
		ttl = str(sb)+"#"+str(actDart)
		daboDim = 600
		self.frame = inputDaboFrame(None, wx.ID_ANY, title=ttl, pos=wx.DefaultPosition,size=([daboDim, daboDim]), style=wx.CAPTION | wx.BORDER_NONE )
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True


# end of class MyApp

if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()
