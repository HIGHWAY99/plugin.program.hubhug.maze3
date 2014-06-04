# ###  - By TheHighway ### #
# ########################################################## #

import xbmc,xbmcgui,urllib,urllib2,os,sys,logging,array,re,time,datetime,random,string,StringIO,xbmcplugin,xbmcaddon
from config import Config as Config
import common as Common
from common import *
import common
import splash_highway as splash

def DoA(a): xbmc.executebuiltin("Action(%s)" % a)
def SFX(n,e='.wav'):
	if len(n)==0: return
	snd=art(n,e)
	try: xbmc.playSFX(snd,False)
	except: 
		try: xbmc.playSFX(snd)
		except: pass

class MyWindow(xbmcgui.Window):
	visuals={}; button={}; Mistakes=0; NoOfMoves=0; tagUp="UP"; tagLeft="LEFT"; tagRight="RIGHT"; tagDown="DOWN"; 
	countA=0; countB=0; LineLength=0; 
	MazeFont='font10'; MazeFont2='font14'; cUser='$'; cEnd='E'; cStart='S'; cWall='#'; cPath=' '; 
	cMonster='R'; cKey='K'; cDoor='D'; cLife='L'; 
	cMonster0='0'; cMonster1='1'; cMonster2='2'; cMonster3='3'; cMonster4='4'; cMonster5='5'; cMonster6='6'; cMonster7='7'; cMonster8='8'; cMonster9='9'; 
	StatsMsg='Level: %s   Life: %s   Keys: %s   ' #Battle Wins: %s   Battle Losses: %s   '
	#self.HoroTxt2.setText(self.StatsMsg % (str(self.gameLevel),str(self.gameLifes),str(self.gameKeys),str(self.gameMonstersKilled),str(self.gameMonstersLostTo)) ); 
	MazeVisL=430; MazeVisT=20; WH=60; #*2; 
	VisGridSizeH=5; ## # | # (Number / 2) - 1 = VisGridSizeH # Number of positions down.   # ##
	VisGridSizeV=9; ## # - # (Number / 2) - 1 = VisGridSizeV # Number of positions across. # ##
	##
	gameLevel=0; gameLifes=1; gameKeys=0; gameMonstersKilled=0; gameMonstersLostTo=0; 
	##
	tWinner='winner'; GridButton={}; GridButtonUD={}; GridButtonUDC={}; GridButtonUDN={}; 
	Hands=[1,2,3];
	PuzzleGridA=''; PuzzleGridB=''; PuzzleWordList=''; PuzzleFileHolder=''; 
	def __init__(self):
		vsW=SettingG("viz-scale-width"); vsH=SettingG("viz-scale-height"); 
		try: self.VisGridSizeV=(int(vsW)-1)/2
		except: pass
		try: self.VisGridSizeH=(int(vsH)-1)/2
		except: pass
		##
		self.Fanart=(xbmc.translatePath(Config.fanart)); self.b1=artp("black1"); self.current=0; self.content=[]; self.scr={}; self.scr['L']=0; self.scr['T']=0; self.scr['W']=1280; self.scr['H']=720; 
		##
		self.MazeVisW=self.WH; self.MazeVisH=self.WH; 
		self.MazeVisL=self.scr['W']-10-(self.MazeVisW*((self.VisGridSizeV*2)+1))
		
		self.AniTime=' time=2000 '; self.AniEnd=' end=80 '; 
		#note("HUB-HUG Movement Series","Please wait.  Preparing screen.  Load Time may vary from device to device.",delay=10000); 
		self.LoadGridFile(); 
		self.makePageItems(); 
	def LoadGridFile(self):
		self.PuzzlePath=xbmc.translatePath(os.path.join(Config.path,'puzzles')); 
		self.PuzzleFiles=os.listdir(self.PuzzlePath); debob(self.PuzzleFiles); 
		zz=self.PuzzleFiles; 
		for z in zz:
			if '.bak' in z: self.PuzzleFiles.remove(z)
		PuF=self.PuzzleFiles[random.randint(0,len(self.PuzzleFiles)-1)]; 
		self.PuzzleFile=xbmc.translatePath(os.path.join(self.PuzzlePath,PuF)); 
		if tfalse(SettingG("select-puzzle"))==True:
			dialog=xbmcgui.Dialog()
			fn=str(dialog.browse(1,'Select Puzzle','files','.txt|.puzzle|.puz',False,False,self.PuzzleFile,False))
			try:
				if (fn==False) or (len(fn)==0): self.close; return
				if len(fn) > 1: deb('fn',fn); self.PuzzleFile=fn; 
			except: pass
		#self.PuzzleFile=xbmc.translatePath(os.path.join(self.PuzzlePath,PuF)); 
		deb('Random File Chosen',self.PuzzleFile); self.PuzzleFileHolder=Common._OpenFile(self.PuzzleFile); deb('Length of Grid File',str(len(self.PuzzleFileHolder))); 
		self.PuzzleFileHolder=self.PuzzleFileHolder.strip().replace('\a','\n').replace('\r','\n').replace('\n\n','\n').strip()
		self.PuzzleFileHolder_Original=''+self.PuzzleFileHolder
		self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cStart,self.cUser,1)
		self.LineLength=len(self.PuzzleFileHolder.split('\n')[0]);
		self.gameLevel=self.gameLevel+1; 
		#self.PrepareMaze(self.PuzzleFileHolder)
		##
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
		#self.cMonster='R'; self.cKey='K'; self.cDoor='D'; self.cLife='L'; 
	def PrepareMaze(self,t):
		t=t.replace(self.cPath,cFLL(self.cWall,'black'))
		#t=t.replace(self.cPath,cFLL(self.cWall,'black'))
		##
		if (tfalse(SettingG("show-items"))==True): 
			c='grey' #'black'
			t=t.replace(self.cLife, cFLL(self.cLife,'maroon') ) 
			t=t.replace(self.cMonster, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster0, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster1, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster2, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster3, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster4, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster5, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster6, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster7, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster8, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cMonster9, cFLL(self.cMonster,'coral') ) 
			t=t.replace(self.cDoor, cFLL(self.cDoor,'grey') ) 
			t=t.replace(self.cKey, cFLL(self.cKey,'yellow') ) 
		else:
			c='black'
			t=t.replace(self.cLife, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster0, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster1, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster2, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster3, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster4, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster5, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster6, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster7, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster8, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cMonster9, cFLL(self.cWall,'c') ) 
			t=t.replace(self.cDoor, cFLL(self.cWall,c) ) 
			t=t.replace(self.cKey, cFLL(self.cWall,c) ) 
		##
		t=t.replace(self.cUser, cFLL(self.cUser,'lightblue') )
		t=t.replace(self.cEnd, cFLL(self.cEnd,'red') ) 
		t=t.replace(self.cStart, cFLL(self.cStart,'green') ) 
		t=cFL(t,'mediumpurple')
		t=t.replace('[color ','[COLOR ').replace('[/color]','[/COLOR]')
		self.PuzzleFileHolder_Publish=t
		self.HoroTxt.setText(self.PuzzleFileHolder_Publish)
		self.HoroTxt2.setText(self.StatsMsg % (str(self.gameLevel),str(self.gameLifes),str(self.gameKeys)) ); 
		#self.HoroTxt2.setText(self.StatsMsg % (str(self.gameLevel),str(self.gameLifes),str(self.gameKeys),str(self.gameMonstersKilled),str(self.gameMonstersLostTo)) ); 
	def makePageItems(self):
		focus=artp("button-focus_lightblue"); nofocus=artp("button-focus_seagreen"); self.background=self.Fanart; #self.background=artj("backdrop_temp"); 
		## ### ## Background
		self.BG=xbmcgui.ControlImage(self.scr['L'],self.scr['T'],self.scr['W'],self.scr['H'],self.background,aspectRatio=0); self.addControl(self.BG)
		self.BG.setAnimations([('WindowOpen','effect=fade '+self.AniTime+' start=0')])
		## ### ##
		l=95; t=20; #l=195; t=20; 
		l=100; 
		#w=self.scr['W']-l-30; h=self.scr['H']-(t*2)-100-36; 
		w=self.scr['W']-(l*2); h=self.scr['H']-(t*2); 
		w=self.scr['W']-(l+t-10); 
		self.HoroTxtBG=xbmcgui.ControlButton(l,t,w,h,"",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=self.b1,noFocusTexture=self.b1); 
		self.HoroTxt=xbmcgui.ControlTextBox(l+10,t+2,w-20,h-4,font=self.MazeFont,textColor="0xFFFFFFFF"); 
		zz=[self.HoroTxtBG,self.HoroTxt]
		for z in zz: self.addControl(z); #z.setAnimations([('WindowOpen','effect=fade delay=2000 time=2000 start=0 end=80')]); 
		self.HoroTxtBG.setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0 end=90')]); 
		self.HoroTxt.setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		#self.HoroTxt.setText("blah..........."); 
		l=100; t=self.scr['H']-40; w=self.scr['W']-(l*2); h=40; 
		self.HoroTxt2BG=xbmcgui.ControlButton(l,t,w,h,"",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=self.b1,noFocusTexture=self.b1); 
		self.HoroTxt2=xbmcgui.ControlTextBox(l+10,t+2,w-20,h-4,font=self.MazeFont2,textColor="0xFFFFFFFF"); 
		zz=[self.HoroTxt2BG,self.HoroTxt2]
		for z in zz: self.addControl(z); #z.setAnimations([('WindowOpen','effect=fade delay=2000 time=2000 start=0 end=80')]); 
		self.HoroTxt2BG.setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0 end=90')]); 
		self.HoroTxt2.setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		
		## ### ## Addon Title
		zz=["XBMCHUB","Your","HUB-HUG"]; w=1000; h=50; l=15; t=700; t=560; 
		self.LabTitleText=Config.name2; #self.LabTitleText=Config.name; 
		self.LabTitle=xbmcgui.ControlLabel(l,t,w,h,'','font30','0xFFFF0000',angle=90); self.addControl(self.LabTitle)
		for z in zz:
			if z+" " in self.LabTitleText: self.LabTitleText=self.LabTitleText.replace(z+" ","[COLOR deepskyblue][B][I]"+z+"[/I][/B][/COLOR]  [CR]")
		if "Highway" in self.LabTitleText: self.LabTitleText=self.LabTitleText.replace("Highway","[COLOR tan]Highway[/COLOR]")
		self.LabTitle.setAnimations([('WindowOpen','effect=slide delay=1000 time=1000 start=-100')]); self.LabTitle.setLabel(self.LabTitleText); 
		## ### ## Exit
		w=135; h=32; l=20; t=70; t=170; 
		self.button[0]=xbmcgui.ControlButton(l,t,w,h,"Exit",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.button[0])
		zz=[self.button[0]] #,self.button[1],self.button[2]]
		for z in zz: z.setAnimations([('WindowOpen','effect=rotate delay=0 time=1 center='+str(l)+','+str(t)+' end=90')])
		## ### ## Movements
		#self.button[0].controlRight(self.GridButton[0]); self.button[0].controlDown(self.GridButton[0]); 
		#zz=[self.HoroTxtBG,self.HoroTxt]; bZ=self.button[0]; 
		#for z in zz: z.controlUp(bZ); z.controlLeft(bZ); z.controlRight(bZ); z.controlDown(bZ); 
		## ### ## Focus
		#self.setFocus(self.button[0])
		self.setFocus(self.HoroTxtBG); 
		## ### ## 
		self.makeVisualItems(); 
		if (tfalse(SettingG("show-map"))==True): self.PrepareMaze(self.PuzzleFileHolder); 
		self.displayVisualItems(self.PuzzleFileHolder.index(self.cUser)); 
		## ### ## 
	def displayVisualItem(self,iTag,visImg='f_black2'):
		visImg=artp(visImg); 
		#try: 
		self.visuals[iTag].setImage(visImg,True);
		#except: 
		#	try: self.visuals[iTag].setImage(visImg,True);
		#	except: pass
		
	def getHeroAvatar(self):
				try:
					return {
						'SeaGreen':					'SeaGreen'
						,'BlueShades1':			'hero01'
						,'BlueShades2':			'hero02'
						,'GreyHuman':				'hero03'
						#,'':				''
					}[SettingG("img-player")]
				except: return 'f_seagreen'
	def checkData(self,Pos,zV=0,zH=0):
		defaultMissing='f_purple'; #'ThumbShadow'; 
		if Pos < 0: return defaultMissing
		if Pos > len(self.PuzzleFileHolder): return defaultMissing
		try:
			P=self.PuzzleFileHolder[Pos]; 
			CurPos=self.PuzzleFileHolder.index(self.cUser)
			if not P==self.cWall:
				#MidPosOfLine=(CurPos+(zH*self.LineLength+1))
				#ShouldBePos=(CurPos+(zH*self.LineLength+1))+zV
				if (zV < 0):
						try: segMent=self.PuzzleFileHolder[Pos:Pos-(zV)]
						except: segMent=""
						if ('\n' in segMent): return defaultMissing #deb('Before Avatar',str(Pos)+'  '+str(zH)+'  '+str(zV)); deb(str(Pos)+' to '+str(MidPosOfLine)+' for '+str(len(segMent)),'"'+str(segMent)+'"'); deb('Location',str(Pos)+'  '+str(zH)+'  '+str(zV)); 
				if (zV > 0):
						try: segMent=self.PuzzleFileHolder[Pos-(zV):Pos]
						except: segMent=""
						if ('\n' in segMent): return defaultMissing #deb('After  Avatar',str(Pos)+'  '+str(zH)+'  '+str(zV)); deb(str(MidPosOfLine)+' to '+str(Pos)+' for '+str(len(segMent)),'"'+str(segMent)+'"'); deb('Location',str(Pos)+'  '+str(zH)+'  '+str(zV)); 
			if   Pos==(CurPos-(self.LineLength+1)): y=True
			elif Pos==(CurPos-(1)): y=True
			elif Pos==(CurPos+(1)): y=True
			elif Pos==(CurPos+(self.LineLength+1)): y=True
			else: y=False
			#deb(str(Pos),P); 
			Si=tfalse(SettingG("show-items")); 
			if   P==self.cWall: return 'f_purple'
			elif P==self.cEnd: return 'home-favourites-FO_red'
			elif P==self.cStart: return 'home-power-FO_green'
			elif P==self.cPath: return 'f_black2'
			elif P==self.cUser: 
				try:
					return {
						'SeaGreen':					'SeaGreen'
						,'BlueShades1':			'hero01'
						,'BlueShades2':			'hero02'
						,'GreyHuman':				'hero03'
						#,'':				''
					}[SettingG("img-player")]
				except: return 'f_seagreen'
			elif P==self.cMonster: 
				if (y==True) or (Si==True): return 'monster0R'
				else: return 'f_black2'
			elif P==self.cMonster0: 
				if (y==True) or (Si==True): return 'monster00'
				else: return 'f_black2'
			elif P==self.cMonster1: 
				if (y==True) or (Si==True): return 'monster01'
				else: return 'f_black2'
			elif P==self.cMonster2: 
				if (y==True) or (Si==True): return 'monster02'
				else: return 'f_black2'
			elif P==self.cMonster3: 
				if (y==True) or (Si==True): return 'monster03'
				else: return 'f_black2'
			elif P==self.cMonster4: 
				if (y==True) or (Si==True): return 'monster04'
				else: return 'f_black2'
			elif P==self.cMonster5: 
				if (y==True) or (Si==True): return 'monster05'
				else: return 'f_black2'
			elif P==self.cMonster6: 
				if (y==True) or (Si==True): return 'monster06'
				else: return 'f_black2'
			elif P==self.cMonster7: 
				if (y==True) or (Si==True): return 'monster07'
				else: return 'f_black2'
			elif P==self.cMonster8: 
				if (y==True) or (Si==True): return 'monster08'
				else: return 'f_black2'
			elif P==self.cMonster9: 
				if (y==True) or (Si==True): return 'monster09'
				else: return 'f_black2'
			elif P==self.cKey: 
				if (y==True) or (Si==True): return 'key01'
				else: return 'f_black2'
			elif P==self.cDoor: 
				if (y==True) or (Si==True): return 'door01'
				else: return 'f_black2'
			elif P==self.cLife: 
				if (y==True) or (Si==True): return 'life01'
				else: return 'f_black2'
			else: return defaultMissing
		except: return defaultMissing
		#if (tfalse(SettingG("show-items"))==True): 
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
		#self.cMonster='R'; self.cKey='K'; self.cDoor='D'; self.cLife='L'; 
	def displayVisualItems(self,NewPos):
		i=0; i2=self.VisGridSizeH; zzH=[]
		for i3 in range((0-i2),i2+1): zzH.append((i,i3)); i+=1; 
		i=0; i2=self.VisGridSizeV; zzV=[]
		for i3 in range((0-i2),i2+1): zzV.append((i,i3)); i+=1; 
		for (zL,zH) in zzH:
			for (zC,zV) in zzV:
				Pos=NewPos+((self.LineLength+1)*zH)+zV
				self.displayVisualItem('L'+str(zL)+'C'+str(zC),self.checkData( Pos,zV,zH )); 
		zz=[[self.tagUp,( NewPos-((self.LineLength+1)*1) )],[self.tagLeft,( NewPos-1 )],[self.tagRight,( NewPos+1 )],[self.tagDown,( NewPos+((self.LineLength+1)*1) )]]
		#debob(zz); 
		for iTag,Pos in zz:
			try:
				P=self.PuzzleFileHolder[Pos]; 
				if   (P==self.cPath): self.visuals[iTag].setVisible(True)
				elif (P==self.cEnd): self.visuals[iTag].setVisible(True)
				elif (P==self.cStart): self.visuals[iTag].setVisible(True)
				elif (P==self.cPath): self.visuals[iTag].setVisible(True)
				elif (P==self.cWall): self.visuals[iTag].setVisible(False)
				elif (P in [self.cLife,self.cKey]): self.visuals[iTag].setVisible(True)
				elif (P in [self.cMonster,self.cMonster0,self.cMonster1,self.cMonster2,self.cMonster3,self.cMonster4,self.cMonster5,self.cMonster6,self.cMonster7,self.cMonster8,self.cMonster9]): self.visuals[iTag].setVisible(True)
				elif (P==self.cDoor): 
					if self.gameKeys > 0: self.visuals[iTag].setVisible(True)
					else: self.visuals[iTag].setVisible(False)
				else: self.visuals[iTag].setVisible(False)
			except: self.visuals[iTag].setVisible(False)
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
		#self.LineLength
		#return
	def makeVisualItem(self,Type,iTag,l,t,w,h,visImg='f_black2'):
		visImg=artp(visImg); visImgB=artp('OverlayWatched_orange'); 
		#debob([Type,iTag,l,t,w,h,visImg]); 
		if Type.upper()=='B':
			self.visuals[iTag]=xbmcgui.ControlImage(l,t,w,h,visImg,aspectRatio=0); 
			self.addControl(self.visuals[iTag])
			self.visuals[iTag+'B']=xbmcgui.ControlButton(l,t,w,h,"",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=visImgB,noFocusTexture=visImgB); 
			self.addControl(self.visuals[iTag+'B'])
			self.visuals[iTag].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
			self.visuals[iTag+'B'].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		elif Type.upper()=='I':
			self.visuals[iTag]=xbmcgui.ControlImage(l,t,w,h,visImg,aspectRatio=0); 
			self.addControl(self.visuals[iTag])
			self.visuals[iTag].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		else: return
	def makeVisualItems(self):
		initVis='f_black2'; w=self.MazeVisW; h=self.MazeVisH; l=self.MazeVisL; t=self.MazeVisT; 
		self.makeVisualItem("I","BG",l,t,w*((self.VisGridSizeV*2)+1),h*((self.VisGridSizeH*2)+1),visImg='black1')
		#i=0; i2=self.VisGridSizeH; 
		#for i3 in range((0-i2),i2+1): zzH.append((i,i3)); i+=1; 
		#i=0; i2=self.VisGridSizeV; 
		#for i3 in range((0-i2),i2+1): zzV.append((i,i3)); i+=1; 
		## ((self.VisGridSizeV*2)+1))
		for hN in range(0,((self.VisGridSizeH*2)+1)):
			for wN in range(0,((self.VisGridSizeV*2)+1)):
				if   (hN==(self.VisGridSizeH-1)) and (wN==(self.VisGridSizeV)):
					iORb="B"; self.tagUp="L"+str(hN)+"C"+str(wN)+'B'; 
				elif (hN==(self.VisGridSizeH)) and (wN==(self.VisGridSizeV-1)):
					iORb="B"; self.tagLeft="L"+str(hN)+"C"+str(wN)+'B'; 
				elif (hN==(self.VisGridSizeH)) and (wN==(self.VisGridSizeV+1)):
					iORb="B"; self.tagRight="L"+str(hN)+"C"+str(wN)+'B'; 
				elif (hN==(self.VisGridSizeH+1)) and (wN==(self.VisGridSizeV)):
					iORb="B"; self.tagDown="L"+str(hN)+"C"+str(wN)+'B'; 
				else: iORb="I"
				self.makeVisualItem(iORb,"L"+str(hN)+"C"+str(wN),l+(w*wN),t+(h*hN),w,h,visImg=initVis); 
		debob([self.tagUp,self.tagLeft,self.tagRight,self.tagDown]); 
		##
	def onAction(self,action):
		try: F=self.getFocus()
		except: F=False
		if   action == Config.ACTION_PREVIOUS_MENU: self.CloseWindow1st()
		elif action == Config.ACTION_NAV_BACK: self.CloseWindow1st()
		else:
		#elif (F==self.HoroTxtBG) or (F==self.HoroTxtBG):
			#try: 
				self.DoFight(action,F)
			#except: pass
	def onControl(self,control):
		if   control==self.button[0]: self.CloseWindow1st()
		#elif (F==self.HoroTxtBG) or (F==self.HoroTxtBG):
		else:
			try:
				if self.visuals[self.tagUp]==control: self.onAction(Config.ACTION_MOVE_UP)
				if self.visuals[self.tagLeft]==control:self.onAction(Config.ACTION_MOVE_LEFT)
				if self.visuals[self.tagRight]==control:self.onAction(Config.ACTION_MOVE_RIGHT)
				if self.visuals[self.tagDown]==control:self.onAction(Config.ACTION_MOVE_DOWN)
			except: pass
		##
	def DoFight(self,action,F):
		#self.LineLength
		MoveValid=False; 
		try: CurPos=self.PuzzleFileHolder.index(self.cUser); 
		except:
			#deb('unable to grab CurPos',str(action)); 
			return
		if   action==Config.ACTION_MOVE_LEFT:  NewPos=CurPos-1
		elif action==Config.ACTION_MOVE_RIGHT: NewPos=CurPos+1
		elif action==Config.ACTION_MOVE_UP:    NewPos=CurPos-(self.LineLength+1)
		elif action==Config.ACTION_MOVE_DOWN:  NewPos=CurPos+(self.LineLength+1)
		else: 
			#deb('unhandled action',str(action)); 
			return
		#debob('\n'+self.PuzzleFileHolder); 
		if NewPos > len(self.PuzzleFileHolder): MoveValid=False; 
		elif NewPos < 0: MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]==self.cWall: MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]=='\n': 			MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]==self.cPath:  MoveValid=True; 
		elif self.PuzzleFileHolder[NewPos]==self.cEnd: 	 MoveValid=True; 
		elif self.PuzzleFileHolder[NewPos]==self.cStart: MoveValid=True; 
		#
		#self.HoroTxt2.setText(self.StatsMsg % (str(self.gameLevel),str(self.gameLifes),str(self.gameKeys),str(self.gameMonstersKilled),str(self.gameMonstersLostTo)) ); 
		#elif self.PuzzleFileHolder[NewPos]==self.cMonster: 
		elif self.PuzzleFileHolder[NewPos] in [self.cMonster,self.cMonster0,self.cMonster1,self.cMonster2,self.cMonster3,self.cMonster4,self.cMonster5,self.cMonster6,self.cMonster7,self.cMonster8,self.cMonster9]: 
			self.gameLifes=self.gameLifes-1; deb('Found Monster',str(self.PuzzleFileHolder[NewPos])); 
			if self.gameLifes > 0: SFX('hit_with_frying_pan_y'); splash.do_My_Splash(artp('dead_halo_smiley'),1,True,(self.scr['W']-(256*2))/2,(self.scr['H']-(256*2))/2,(256*2),(256*2)); 
			#self.gameMonstersLostTo=self.gameMonstersLostTo+1; #self.gameMonstersKilled=self.gameMonstersKilled+1; 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			MoveValid=True; 
		elif self.PuzzleFileHolder[NewPos]==self.cKey: 
			SFX('gasp_x'); 
			self.gameKeys=self.gameKeys+1; deb('Found','Key'); 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			MoveValid=True; 
		elif self.PuzzleFileHolder[NewPos]==self.cDoor: 
			if self.gameKeys > 0:
				SFX('door2'); 
				self.gameKeys=self.gameKeys-1; deb('Found','Door'); 
				self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
				MoveValid=True; 
			else: MoveValid=False; 
		elif self.PuzzleFileHolder[NewPos]==self.cLife: 
			SFX('heartbeat1'); 
			self.gameLifes=self.gameLifes+1; deb('Found','Extra Life'); 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			MoveValid=True; 
		#
		else: MoveValid=False; 
		#debob('NewPos character "'+self.PuzzleFileHolder[NewPos]+'"'); 
		if MoveValid==True:
			#debob('valid move from '+str(CurPos)+' to '+str(NewPos))
			if self.PuzzleFileHolder_Original[CurPos]==self.cStart: 
				    self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,self.cStart,1)
			if self.PuzzleFileHolder_Original[CurPos]==self.cEnd: 
				    self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,self.cEnd,1)
			else: self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,self.cPath,1)
			#if self.PuzzleFileHolder[NewPos]==self.cPath:  
			#	self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cPath,self.cUser,1)
			#elif self.PuzzleFileHolder[NewPos]==self.cEnd: 	 
			#	self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cEnd,self.cUser,1)
			#elif self.PuzzleFileHolder[NewPos]==self.cStart: 
			#	self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cStart,self.cUser,1)
			#self.PuzzleFileHolder=
			#self.PuzzleFileHolder[NewPos:1]=self.cUser
			#self.PuzzleFileHolder[NewPos]=self.cUser
			self.PuzzleFileHolder=self.PuzzleFileHolder[0:NewPos]+self.cUser+self.PuzzleFileHolder[NewPos+1:len(self.PuzzleFileHolder)]; 
			if self.gameLifes < 1: self.GameOver(); 
			elif self.PuzzleFileHolder_Original[NewPos]==self.cEnd: self.VictoryDance(); 
			if (tfalse(SettingG("show-map"))==True) and (tfalse(SettingG("show-maplocation"))==True): self.PrepareMaze(self.PuzzleFileHolder); 
			NewPos=self.PuzzleFileHolder.index(self.cUser); 
			self.displayVisualItems(NewPos); 
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
	def replacePos(self,Pos,n,t):
		try: return t[0:Pos]+n+t[Pos+1:len(t)]
		except: return t
		
	def VictoryDance(self):
		try:
				debob("game won"); 
				SFX('fanfare_x'); 
				#splash.do_My_Splash(self.iDuckShot3,1); 
				splash.do_My_Splash(artj('corn-maze-exit'),3,True,(self.scr['W']-500)/2,(self.scr['H']-333)/2,500,333); 
				#splash.do_My_Splash(artj('corn-maze-exit'),2,True,10,150,self.scr['W']-200,self.scr['H']-150); 
				self.LoadGridFile(); 
				xbmc.sleep(20); 
				NewPos=self.PuzzleFileHolder.index(self.cUser); 
				self.displayVisualItems(NewPos); 
				#self.CloseWindow1st(); #DoA("Back"); 
		except: pass
	def GameOver(self):
		try:
				debob("game lost"); 
				SFX('exit_cue_y'); 
				#splash.do_My_Splash(self.iDuckShot3,1); 
				splash.do_My_Splash(artj('youaredead_icon_icon921'),3,True,(self.scr['W']-(256*2))/2,(self.scr['H']-(256*2))/2,(256*2),(256*2)); 
				#splash.do_My_Splash(artj('corn-maze-exit'),2,True,10,150,self.scr['W']-200,self.scr['H']-150); 
				self.CloseWindow1st(); #DoA("Back"); 
		except: pass
	def CloseWindow1st(self):
		#try: zz=[self.CtrlList,self.RepoThumbnail,self.RepoFanart2,self.RepoFanart,self.LabCurrentRepo,self.LabTitle,self.button[0],self.TVS,self.TVSBGB,self.BGB]
		#except: zz=[]
		#for z in zz:
		#	try: self.removeControl(z); del z
		#	except: pass
		self.close()
## ################################################## ##
## ################################################## ##
## Start of program
TempWindow=MyWindow(); TempWindow.doModal(); del TempWindow
## ################################################## ##
## ################################################## ##
