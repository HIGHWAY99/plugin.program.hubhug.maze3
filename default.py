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
	ArtWork={}; visuals={}; button={}; Mistakes=0; NoOfMoves=0; tagUp="UP"; tagLeft="LEFT"; tagRight="RIGHT"; tagDown="DOWN"; 
	countA=0; countB=0; LineLength=0; ImFacing='down'; cSplit='\n||\n'; 
	MazeFont='font10'; MazeFont2='font14'; cUser='$'; cEnd='E'; cStart='S'; cWall='#'; cPath=' '; 
	csMap='O'; cMonster='R'; cKey='K'; cDoor='D'; cLife='L'; cToStart='s'; cMyLove='Y'; cSuperLife='l'; 
	cMonster0='0'; cMonster1='1'; cMonster2='2'; cMonster3='3'; cMonster4='4'; cMonster5='5'; cMonster6='6'; cMonster7='7'; cMonster8='8'; cMonster9='9'; 
	cPortalFA='A'; cPortalTA='a'; cPortalFP='P'; cPortalTP='p'; cPortalFO='O'; cPortalTO='o'; cPortalFQ='Q'; cPortalTQ='q'; cPortalFU='U'; cPortalTU='u'; cPortalFJ='J'; cPortalTJ='j'; 
	DistanceLeft=30; DistanceUp=15; ## Text Map - View Distance.
	StatsMsg='Level: %s   Life: %s   Keys: %s   ' #Battle Wins: %s   Battle Losses: %s   '
	#self.HoroTxt2.setText(self.StatsMsg % (str(self.gameLevel),str(self.gameLifes),str(self.gameKeys),str(self.gameMonstersKilled),str(self.gameMonstersLostTo)) ); 
	MazeVisL=430; MazeVisT=20; WH=60; #*2; 
	VisGridSizeH=5; ## # | # (Number / 2) - 1 = VisGridSizeH # Number of positions down.   # ##
	VisGridSizeV=9; ## # - # (Number / 2) - 1 = VisGridSizeV # Number of positions across. # ##
	##
	gameLevel=0; gameLifes=1; gameKeys=0; gameMonstersKilled=0; gameMonstersLostTo=0; gameMyLove=0; 
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
		#self.setupArtWork(); 
		##
		self.Fanart=(xbmc.translatePath(Config.fanart)); self.b1=artp("black1"); self.current=0; self.content=[]; self.scr={}; self.scr['L']=0; self.scr['T']=0; self.scr['W']=1280; self.scr['H']=720; 
		##
		self.MazeVisW=self.WH; self.MazeVisH=self.WH; 
		self.MazeVisL=self.scr['W']-10-(self.MazeVisW*((self.VisGridSizeV*2)+1))
		
		self.AniTime=' time=2000 '; self.AniEnd=' end=80 '; 
		#note("HUB-HUG Movement Series","Please wait.  Preparing screen.  Load Time may vary from device to device.",delay=10000); 
		
		self.IntroScreen(); 
		self.LoadGridFile(); 
		self.makePageItems(); 
	def IntroScreen(self):
		if tfalse(SettingG("select-puzzle"))==False:
			msg ="Hello Player.     Welcome to \n"
			msg+=((cFL(Config.name2,'red')).replace('[CR]','').replace('\n','').replace('HUB-HUG','').replace('XBMCHUB',''))+'\n\n'
			msg+="While at the ball with my Sweet Heart, a bunch of thugs bulged in.  They took my Sweet Heart!\n"
			msg+="If the folks find out, I'll never live it down.  No time to grab my gear, I might get caught by the folks.  \n"
			splash.do_My_TextSplash(msg,artj('text_splash01'),8,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=70); 
			#
			msg="Yes, yes!  \nTime to rush in head strong and RESCUE MY SWEET HEART!  "
			msg+="If I don't act FAST, they'll surely send a ransom letter.  If they find out this happened... embarrassment... and they'll cancel the wedding!  No, no, no.  Never, never, never!  Let's go save my SWEET HEART!\n"
			splash.do_My_TextSplash(msg,artj('text_splash01'),8,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=70); 
	def setupArtWork(self):
		self.ArtWork['Wall']='f_purple'; 
		self.ArtWork['Path']='blank1'; 
		self.ArtWork['Door']='door01'; 
		self.ArtWork['Key']='key01'; 
		self.ArtWork['Life']='life03'; 
		self.ArtWork['SuperLife']='life02'; 
		self.ArtWork['MonsterR']='monster0R'; 
		self.ArtWork['Monster0']='monster00'; 
		self.ArtWork['Monster1']='monster01'; 
		self.ArtWork['Monster2']='monster02'; 
		self.ArtWork['Monster3']='monster03'; 
		self.ArtWork['Monster4']='monster04'; 
		self.ArtWork['Monster5']='monster05'; 
		self.ArtWork['Monster6']='monster06'; 
		self.ArtWork['Monster7']='monster07'; 
		self.ArtWork['Monster8']='monster08'; 
		self.ArtWork['Monster9']='monster09'; 
		self.ArtWork['ToStart']='start02'; 
		self.ArtWork['Start']='start01'; 
		self.ArtWork['Exit']='home-favourites-FO_red'; 
		self.ArtWork['Portal1']='pegan01'; 
		self.ArtWork['Portal2']='pegan02'; 
		self.ArtWork['Portal3']='pegan03'; 
		self.ArtWork['Portal4']='pegan04'; 
		self.ArtWork['Portal5']='pegan05'; 
		self.ArtWork['Portal6']='pegan06'; 
		self.ArtWork['FoundMyLove']='found01'; 
		
		## ### ## Non-Graphics.
		## ### Sounds
		self.ArtWork['SFX_FoundMyLove']='kiss_1992'; 
		
		## ### Text
		self.ArtWork['TXT_FoundMyLove_Name']="Sweet Heart"
		
		##
	def LoadMapData(self):
				tData=self.getMapData(1); 
				if (len(tData) > 0) and (not tData=='...'):
					tData=eval(tData); 
					zz=['Wall','Door','Key','Life','SuperLife','Path','Start','ToStart','Exit','Portal1','Portal2','Portal3','Portal4','Portal5','Portal6']
					for z in zz:
						try: self.ArtWork[z]=tData[z.lower()]
						except: pass
					zz=['FoundMyLove']
					for z in zz:
						try: self.ArtWork['SFX_'+z]=tData['sfx_'+z.lower()]
						except: pass
					try: self.ArtWork['Path']=tData['floor']
					except: pass
					try: self.ArtWork['TXT_FoundMyLove_Name']=tData['txt_foundmylove_name']
					except: pass
					zz=['R','0','1','2','3','4','5','6','7','8','9']
					for z in zz:
						try: self.ArtWork['Monster'+z]=tData['monster'+z] #.lower()]
						except: pass
					
	def LoadGridFile(self):
		self.gameMyLove=0; self.setupArtWork(); 
		self.PuzzlePath=xbmc.translatePath(os.path.join(Config.path,'puzzles')); 
		self.PuzzleFiles=os.listdir(self.PuzzlePath); debob(self.PuzzleFiles); 
		zz=self.PuzzleFiles; 
		for z in zz:
			if '.bak' in z: self.PuzzleFiles.remove(z)
		PuF=self.PuzzleFiles[random.randint(0,len(self.PuzzleFiles)-1)]; 
		self.PuzzleFile=xbmc.translatePath(os.path.join(self.PuzzlePath,PuF)); 
		if tfalse(SettingG("select-puzzle"))==True:
			dialog=xbmcgui.Dialog()
			fn=str(dialog.browse(1,'Select Puzzle','files','.txt|.dungeon|.level|.map',False,False,self.PuzzleFile,False))
			try:
				if (fn==False) or (len(fn)==0): self.close; return
				if len(fn) > 1: deb('fn',fn); self.PuzzleFile=fn; 
			except: pass
		#self.PuzzleFile=xbmc.translatePath(os.path.join(self.PuzzlePath,PuF)); 
		deb('Random File Chosen',self.PuzzleFile); self.PuzzleFileHolder=Common._OpenFile(self.PuzzleFile); deb('Length of Grid File',str(len(self.PuzzleFileHolder))); 
		self.PuzzleFileHolder=self.PuzzleFileHolder.strip().replace('\a','\n').replace('\r','\n').replace('\n\n','\n').strip()
		self.PuzzleFileHolder_OverAll=''+self.PuzzleFileHolder
		if self.cSplit in self.PuzzleFileHolder:
			try: self.PuzzleFileHolder=self.PuzzleFileHolder.split(self.cSplit)[0].strip()
			except: pass
		self.PuzzleFileHolder=self.PuzzleFileHolder
		self.PuzzleFileHolder_Original=''+self.PuzzleFileHolder
		self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cStart,self.cUser,1)
		self.LineLength=len(self.PuzzleFileHolder.split('\n')[0]);
		## ### ## 
		if self.cSplit in self.PuzzleFileHolder_OverAll:
			try:
				self.LoadMapData(); 
			except: pass
		
		
		
		
		
		
		
		
		## ### ## 
		#if self.LineLength > 60: self.csMap='.'; 
		#else: self.csMap='O'; 
		self.gameLevel=self.gameLevel+1; 
		#self.PrepareMaze(self.PuzzleFileHolder)
		##
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
		#self.cMonster='R'; self.cKey='K'; self.cDoor='D'; self.cLife='L'; 
	def getMapData(self,n):
			try: 
				t=self.PuzzleFileHolder_OverAll.split(self.cSplit)[int(n)].strip()
				if t=='...': return ''
				return t
			except: return ''
	def PrepareMaze(self,t):
		tblack='bbbbb'; c=tblack; yT=t.split('\n'); 
		try: CurPos=t.index(self.cUser); 
		except: CurPos=0; 
		zCurPos=t[0:(t.index(self.cUser)+1)]
		if '\n' in zCurPos: zCurPos=zCurPos.split('\n')[-1]
		yCurPos=zCurPos.index(self.cUser)+1; 
		## 
		lCurPos=len(t.split(self.cUser)[0].split('\n')); 
		DistanceLeft=self.DistanceLeft; DistanceUp=self.DistanceUp; i=0;
		t=''; #debob(str(yCurPos)+','+str(lCurPos)); 
		for yt2 in yT: 
			if   ((i+DistanceUp+1) < lCurPos): pass
			elif ((i-DistanceUp+1) > lCurPos) and (i > ((DistanceUp*2)+1)): pass
			else:
				if yCurPos < (DistanceLeft): 
					try: t+=yt2[0:(((DistanceLeft*2)))]+'\n'; 
					except: 
						try: t+=yt2[0:yCurPos+DistanceLeft]+'\n'; 
						except: t+=yt2+'\n'; 
				else: 
					try: t+=yt2[yCurPos-DistanceLeft:yCurPos+DistanceLeft]+'\n'; 
					except: 
						try: t+=yt2[yCurPos-DistanceLeft:len(yt2)]+'\n'; 
						except: t+=yt2+'\n'; 
			i+=1; 
		## 
		t=t.replace(self.cWall,cFLL(self.cWall,'bbbbbbbbbbbb')); 
		t=t.replace(self.cPath,cFLL(self.cWall,c)); 
		zz=[self.cPortalTA,self.cPortalTO,self.cPortalTU,self.cPortalFA,self.cPortalFP,self.cPortalTP,self.cPortalFO,self.cPortalFQ,self.cPortalTQ,self.cPortalFU,self.cPortalFJ,self.cPortalTJ,self.cToStart]; 
		for z in zz: t=t.replace(z, cFLL(self.cWall,c) )
		##
		if (tfalse(SettingG("show-items"))==True): 
			c='bbbb'
			t=t.replace(self.cLife, cFLL(self.cWall,'bbbbbbbbb') ) 
			t=t.replace(self.cSuperLife, cFLL(self.cWall,'bbbbbbbbb') ) 
			t=t.replace(self.cMonster, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster0, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster1, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster2, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster3, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster4, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster5, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster6, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster7, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster8, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cMonster9, cFLL(self.cWall,'bbbbbbb') ) 
			t=t.replace(self.cDoor, cFLL(self.cWall,'bbbb') ) 
			t=t.replace(self.cKey, cFLL(self.cWall,'bbbbbb') ) 
		else:
			c=tblack
			t=t.replace(self.cLife, cFLL(self.cWall,c) ) 
			t=t.replace(self.cSuperLife, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster0, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster1, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster2, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster3, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster4, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster5, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster6, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster7, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster8, cFLL(self.cWall,c) ) 
			t=t.replace(self.cMonster9, cFLL(self.cWall,c) ) 
			t=t.replace(self.cDoor, cFLL(self.cWall,c) ) 
			t=t.replace(self.cKey, cFLL(self.cWall,c) ) 
		##
		
		t=t.replace(self.cMyLove, cFLL(self.cWall,tblack) )
		t=t.replace(self.cUser, cFLL(self.cWall,'bbb') )
		if (tfalse(SettingG("show-items"))==True): t=t.replace(self.cEnd, cFLL(self.cWall,'bb') ) 
		else: t=t.replace(self.cEnd, cFLL(self.cWall,'tblack') ) 
		t=t.replace(self.cStart, cFLL(self.cWall,'bbbbbbbb') ) 
		t=cFL(t,'mediumpurple'); 
		t=t.replace('[color_','[COLOR ').replace('[/color]','[/COLOR]'); t=t.replace('[ccccc_','[COLOR ').replace('[/ccccc]','[/COLOR]'); 
		t=t.replace(' bbbbb]',' black]'); t=t.replace(' bbbb]',' grey]'); 
		t=t.replace(' bbbbbb]',' yellow]'); t=t.replace(' bbbbbbb]',' coral]'); 
		t=t.replace(' bbbbbbbb]',' green]'); t=t.replace(' bbb]',' lightblue]'); 
		t=t.replace(' bb]',' red]'); t=t.replace(' bbbbbbbbb]',' maroon]'); t=t.replace(' bbbbbbbbbbbb]',' mediumpurple]'); 
		
		t=t.replace(self.cWall,self.csMap)
		
		self.PuzzleFileHolder_Publish=t
		#debob(self.PuzzleFileHolder_Publish); 
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
		zz=["XBMCHUB","Your","HUB-HUG"]; w=1000; h=50; l=15; t=700; t=575; 
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
						,'AncientHero':			'hero00'
						,'BlueShades1':			'hero01'
						,'BlueShades2':			'hero02'
						,'GreyHuman':				'hero03'
						,'BlackEyedHero':		'hero04'
						,'GreenHero':				'hero05'
						,'NerdHero':				'hero06'
						,'BanditHero':			'hero07'
						,'XBMCHero':				'hero08'
						,'AndroidHero':			'hero09'
						,'Girl1':					'girl01'
						,'Girl2':					'girl02'
						,'GirlNLove':			'girl03'
						,'HoodedGirl':			'girl04'
						#,'':				''
					}[SettingG("img-player")]
				except: return 'f_seagreen'
	def checkData(self,Pos,zV=0,zH=0):
		defaultMissing=self.ArtWork['Wall']; #'floor03' #'f_purple'; #'ThumbShadow'; 
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
			if   P==self.cWall: return defaultMissing #'floor02' #'f_purple'
			elif P==self.cEnd: return self.ArtWork['Exit'] #'home-favourites-FO_red'
			elif P==self.cStart: return self.ArtWork['Start'] #'start01' #'home-power-FO_green'
			elif P==self.cToStart: return self.ArtWork['ToStart'] #'start02' #'home-power-FO_green'
			elif P==self.cPath: return self.ArtWork['Path'] #'blank1' #'black1' #'f_black2'
			elif P in [self.cPortalFA,self.cPortalTA]: return self.ArtWork['Portal1'] #'pegan01'
			elif P in [self.cPortalFP,self.cPortalTP]: return self.ArtWork['Portal2'] #'pegan02'
			elif P in [self.cPortalFO,self.cPortalTO]: return self.ArtWork['Portal3'] #'pegan03'
			elif P in [self.cPortalFQ,self.cPortalTQ]: return self.ArtWork['Portal4'] #'pegan04'
			elif P in [self.cPortalFU,self.cPortalTU]: return self.ArtWork['Portal5'] #'pegan05'
			elif P in [self.cPortalFJ,self.cPortalTJ]: return self.ArtWork['Portal6'] #'pegan06'
			#elif P in [self.cPortalFA,self.cPortalFP,self.cPortalFO,self.cPortalFQ,self.cPortalFU,self.cPortalFJ]: return 'pegan02' #'portal01'
			#elif P in [self.cPortalTA,self.cPortalTP,self.cPortalTO,self.cPortalTQ,self.cPortalTU,self.cPortalTJ]: return 'pegan02' #'portal02'
			elif P==self.cUser: 
				try:
					return {
						'SeaGreen':					'SeaGreen'
						,'AncientHero':			'hero00'
						,'BlueShades1':			'hero01'
						,'BlueShades2':			'hero02'
						,'GreyHuman':				'hero03'
						,'BlackEyedHero':		'hero04'
						,'GreenHero':				'hero05'
						,'NerdHero':				'hero06'
						,'BanditHero':			'hero07'
						,'XBMCHero':				'hero08'
						,'AndroidHero':			'hero09'
						,'Girl1':						'girl01'
						,'Girl2':						'girl02'
						,'GirlNLove':				'girl03'
						,'HoodedGirl':			'girl04'
						#,'':				''
					}[SettingG("img-player")]
				except: return 'f_seagreen'
			elif P==self.cMyLove: 
				try:
					return {
						'SeaGreen':					'SeaGreen'
						,'AncientHero':			'girl04' #hero00'
						,'BlueShades1':			'girl03' #hero01'
						,'BlueShades2':			'girl01' #hero02'
						,'GreyHuman':				'girl02' #hero03'
						,'BlackEyedHero':		'girl01' #hero04'
						,'GreenHero':				'girl02' #hero05'
						,'NerdHero':				'girl01' #hero06'
						,'BanditHero':			'girl02' #hero07'
						,'XBMCHero':				'hero09' #hero08'
						,'AndroidHero':			'hero08' #hero09'
						,'Girl1':						'hero04' #girl01'
						,'Girl2':						'hero01' #girl02'
						,'GirlNLove':				'hero06' #girl03'
						,'HoodedGirl':			'hero00' #girl04'
						#,'':				''
					}[SettingG("img-player")]
				except: return 'f_seagreen'
			elif P==self.cMonster: 
				if (y==True) or (Si==True): return self.ArtWork['MonsterR'] #'monster0R'
				else: return self.ArtWork['Path']
			elif P==self.cMonster0: 
				if (y==True) or (Si==True): return self.ArtWork['Monster0'] #'monster00'
				else: return self.ArtWork['Path']
			elif P==self.cMonster1: 
				if (y==True) or (Si==True): return self.ArtWork['Monster1'] #'monster01'
				else: return self.ArtWork['Path']
			elif P==self.cMonster2: 
				if (y==True) or (Si==True): return self.ArtWork['Monster2'] #'monster02'
				else: return self.ArtWork['Path']
			elif P==self.cMonster3: 
				if (y==True) or (Si==True): return self.ArtWork['Monster3'] #'monster03'
				else: return self.ArtWork['Path']
			elif P==self.cMonster4: 
				if (y==True) or (Si==True): return self.ArtWork['Monster4'] #'monster04'
				else: return self.ArtWork['Path']
			elif P==self.cMonster5: 
				if (y==True) or (Si==True): return self.ArtWork['Monster5'] #'monster05'
				else: return self.ArtWork['Path']
			elif P==self.cMonster6: 
				if (y==True) or (Si==True): return self.ArtWork['Monster6'] #'monster06'
				else: return self.ArtWork['Path']
			elif P==self.cMonster7: 
				if (y==True) or (Si==True): return self.ArtWork['Monster7'] #'monster07'
				else: return self.ArtWork['Path']
			elif P==self.cMonster8: 
				if (y==True) or (Si==True): return self.ArtWork['Monster8'] #'monster08'
				else: return self.ArtWork['Path']
			elif P==self.cMonster9: 
				if (y==True) or (Si==True): return self.ArtWork['Monster9'] #'monster09'
				else: return self.ArtWork['Path']
			elif P==self.cKey: 
				if (y==True) or (Si==True): return self.ArtWork['Key'] #'key01'
				else: return self.ArtWork['Path']
			elif P==self.cDoor: 
				if (y==True) or (Si==True): return self.ArtWork['Door'] #'door01'
				else: return self.ArtWork['Path']
			elif P==self.cLife: 
				if (y==True) or (Si==True): return self.ArtWork['Life'] #'life03'
				else: return self.ArtWork['Path']
			elif P==self.cSuperLife: 
				if (y==True) or (Si==True): return self.ArtWork['SuperLife'] #'life02'
				else: return self.ArtWork['Path']
			else: return defaultMissing
		except: return defaultMissing
	def displayVisualItems(self,NewPos):
		i=0; i2=self.VisGridSizeH; zzH=[]; 
		for i3 in range((0-i2),i2+1): zzH.append((i,i3)); i+=1; 
		i=0; i2=self.VisGridSizeV; zzV=[]; 
		for i3 in range((0-i2),i2+1): zzV.append((i,i3)); i+=1; 
		for (zL,zH) in zzH:
			for (zC,zV) in zzV:
				Pos=NewPos+((self.LineLength+1)*zH)+zV
				self.displayVisualItem('L'+str(zL)+'C'+str(zC)+'F',self.ArtWork['Path']); 
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
				elif (P in [self.cLife,self.cSuperLife,self.cKey,self.cMyLove]): self.visuals[iTag].setVisible(True)
				elif (P in [self.cMonster,self.cMonster0,self.cMonster1,self.cMonster2,self.cMonster3,self.cMonster4,self.cMonster5,self.cMonster6,self.cMonster7,self.cMonster8,self.cMonster9]): self.visuals[iTag].setVisible(True)
				elif (P in [self.cPortalFA,self.cPortalTA,self.cPortalFP,self.cPortalTP,self.cPortalFO,self.cPortalTO,self.cPortalFQ,self.cPortalTQ,self.cPortalFU,self.cPortalTU,self.cPortalFJ,self.cPortalTJ,self.cToStart]): self.visuals[iTag].setVisible(True)
				elif (P==self.cDoor): 
					if self.gameKeys > 0: self.visuals[iTag].setVisible(True)
					else: self.visuals[iTag].setVisible(False)
				else: self.visuals[iTag].setVisible(False)
			except: self.visuals[iTag].setVisible(False)
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
		#self.LineLength
		#return
	def makeVisualItem(self,Type,iTag,l,t,w,h,visImg='black1',visImgB='blank1'):
		visImg=artp(visImg); visImgB=artp(visImgB); visImgF=artp(self.ArtWork['Path']); 
		#debob([Type,iTag,l,t,w,h,visImg]); 
		if Type.upper()=='B':
			self.visuals[iTag+'F']=xbmcgui.ControlImage(l,t,w,h,visImgF,aspectRatio=0); self.addControl(self.visuals[iTag+'F']); 
			self.visuals[iTag+'F'].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
			self.visuals[iTag]=xbmcgui.ControlImage(l,t,w,h,visImg,aspectRatio=0); self.addControl(self.visuals[iTag]); 
			self.visuals[iTag].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
			self.visuals[iTag+'B']=xbmcgui.ControlButton(l,t,w,h,"",textColor="0xFF000000",focusedColor="0xFF00BFFF",alignment=2,focusTexture=visImgB,noFocusTexture=visImgB); self.addControl(self.visuals[iTag+'B']); 
			self.visuals[iTag+'B'].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		elif Type.upper()=='I':
			self.visuals[iTag+'F']=xbmcgui.ControlImage(l,t,w,h,visImgF,aspectRatio=0); self.addControl(self.visuals[iTag+'F']); 
			self.visuals[iTag+'F'].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
			self.visuals[iTag]=xbmcgui.ControlImage(l,t,w,h,visImg,aspectRatio=0); self.addControl(self.visuals[iTag]); 
			self.visuals[iTag].setAnimations([('WindowOpen','effect=fade delay=4000 time=2000 start=0')]); 
		else: return
	def makeVisualItems(self):
		initVis=self.ArtWork['Path']; w=self.MazeVisW; h=self.MazeVisH; l=self.MazeVisL; t=self.MazeVisT; 
		self.makeVisualItem("I","BG",l,t,w*((self.VisGridSizeV*2)+1),h*((self.VisGridSizeH*2)+1),visImg='black1')
		#i=0; i2=self.VisGridSizeH; 
		#for i3 in range((0-i2),i2+1): zzH.append((i,i3)); i+=1; 
		#i=0; i2=self.VisGridSizeV; 
		#for i3 in range((0-i2),i2+1): zzV.append((i,i3)); i+=1; 
		## ((self.VisGridSizeV*2)+1))
		for hN in range(0,((self.VisGridSizeH*2)+1)):
			for wN in range(0,((self.VisGridSizeV*2)+1)):
				if   (hN==(self.VisGridSizeH-1)) and (wN==(self.VisGridSizeV)):
					iORb="B"; self.tagUp   ="L"+str(hN)+"C"+str(wN)+'B'; visImgB=   'move_up01'; 
				elif (hN==(self.VisGridSizeH)) and (wN==(self.VisGridSizeV-1)):
					iORb="B"; self.tagLeft ="L"+str(hN)+"C"+str(wN)+'B'; visImgB= 'move_left01'; 
				elif (hN==(self.VisGridSizeH)) and (wN==(self.VisGridSizeV+1)):
					iORb="B"; self.tagRight="L"+str(hN)+"C"+str(wN)+'B'; visImgB='move_right01'; 
				elif (hN==(self.VisGridSizeH+1)) and (wN==(self.VisGridSizeV)):
					iORb="B"; self.tagDown ="L"+str(hN)+"C"+str(wN)+'B'; visImgB= 'move_down01'; 
				else: iORb="I"; visImgB='blank1'; 
				self.makeVisualItem(iORb,"L"+str(hN)+"C"+str(wN),l+(w*wN),t+(h*hN),w,h,visImg=initVis,visImgB=visImgB); 
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
	## ### ############################################################ ### ## 
	def MoveTo_MyLove(self,action,F,CurPos,NewPos):
			MoveValid=False; SH_Title=self.ArtWork['TXT_FoundMyLove_Name']; SH_Msg="You've finally come!"; SH_Requirements="Required: 4 Keys, 10 Life"; 
			if(self.gameKeys > (4-1)):
				if (self.gameLifes > (10+1)):
					SFX(self.ArtWork['SFX_FoundMyLove']); self.gameKeys-=4; self.gameLifes-=10; self.gameMyLove+=1; MoveValid=True; deb('Found','Key'); self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
					splash.do_My_Splash(artp(self.ArtWork['FoundMyLove']),3,True,(self.scr['W'])/4,(self.scr['H'])/4,(self.scr['W'])/2,(self.scr['H'])/2); 
					SH_line2="You undo the chains (4 keys)"; SH_line3="You heal them (10 Life)"; 
				else: MoveValid=False; SH_line2="Please Heal me!"; SH_line3=SH_Requirements; 
			else: MoveValid=False; SH_line2="Hurry, unchain me!"; SH_line3=SH_Requirements; 
			popOK(msg=SH_Msg,title=SH_Title,line2=SH_line2,line3=SH_line3); 
			return MoveValid
	def MoveTo_Life(self,action,F,CurPos,NewPos):
			SFX('heartbeat1'); self.gameLifes=self.gameLifes+1; deb('Found','Extra Life'); 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			return True
	def MoveTo_SuperLife(self,action,F,CurPos,NewPos,PlusLife=5):
			SFX('heartbeat1'); self.gameLifes=self.gameLifes+PlusLife; deb('Found','SUPER Extra Life'); 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			return True
	def MoveTo_Key(self,action,F,CurPos,NewPos):
			SFX('gasp_x'); self.gameKeys=self.gameKeys+1; deb('Found','Key'); 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			return True
	def MoveTo_Door(self,action,F,CurPos,NewPos):
			MoveValid=False; 
			if self.gameKeys > 0:
				SFX('door2'); self.gameKeys=self.gameKeys-1; deb('Found','Door'); MoveValid=True; 
				self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
				if self.gameKeys==0: popOK(msg="That was my last key.",title="",line2="I need to find more: "+cFL("keys",'red'),line3=""); 
			else: MoveValid=False; 
			return MoveValid
	def MoveTo_Monster(self,action,F,CurPos,NewPos):
			MoveValid=False; 
			#elif self.PuzzleFileHolder[NewPos] in [self.cMonster,self.cMonster0,self.cMonster1,self.cMonster2,self.cMonster3,self.cMonster4,self.cMonster5,self.cMonster6,self.cMonster7,self.cMonster8,self.cMonster9]: 
			self.gameLifes=self.gameLifes-1; deb('Found Monster',str(self.PuzzleFileHolder[NewPos])); 
			if self.gameLifes > 0: SFX('hit_with_frying_pan_y'); splash.do_My_Splash(artp('dead_halo_smiley'),1,True,(self.scr['W']-(256*2))/2,(self.scr['H']-(256*2))/2,(256*2),(256*2)); 
			#self.gameMonstersLostTo=self.gameMonstersLostTo+1; #self.gameMonstersKilled=self.gameMonstersKilled+1; 
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cPath,self.PuzzleFileHolder); 
			if self.gameLifes==1: popOK(msg="I'm down to my last life.",title="",line2="I need to find more: "+cFL("extra life",'red'),line3=""); 
			MoveValid=True; 
			return MoveValid
	def MoveTo_MonsterBattle(self,action,F,CurPos,NewPos):
			MoveValid=False; 
			
			return MoveValid
	## ### ############################################################ ### ## 
	def isEmptyPath(self,Pos):
		try:
			if self.PuzzleFileHolder[Pos] in [self.cPath]: return True
			else: return False
		except: return False
	def isMonster(self,Pos):
		try:
			if self.PuzzleFileHolder[Pos] in [self.cMonster,self.cMonster0,self.cMonster1,self.cMonster2,self.cMonster3,self.cMonster4,self.cMonster5,self.cMonster6,self.cMonster7,self.cMonster8,self.cMonster9]: return True
			else: return False
		except: return False
	def MoveMent_AdjustMonsterPlacement(self,action,F,CurPos,NewPos):
			## Mobs to the Right of the User.
			zz=[[1,1,0,''],
					[1,2,1,self.cPath],
					[1,3,2,self.cPath+self.cPath],
					[1,4,3,self.cPath+self.cPath+self.cPath],
					[1,5,4,self.cPath+self.cPath+self.cPath+self.cPath],
					]
			for (i,n,nn,e) in zz:
				if self.isMonster((NewPos+i)+n)==True:
					if self.PuzzleFileHolder[(NewPos+i):(NewPos+i)+nn]==e:
						self.PuzzleFileHolder=self.replacePos((NewPos+i)+nn,self.PuzzleFileHolder[(NewPos+i)+n],self.PuzzleFileHolder); 
						self.PuzzleFileHolder=self.replacePos((NewPos+i)+n,self.cPath,self.PuzzleFileHolder); 
			## Mobs to the Right of the User.
			zz=[[0-1,0-1,0-0,''],
					[0-1,0-2,0-1,self.cPath],
					[0-1,0-3,0-2,self.cPath+self.cPath],
					[0-1,0-4,0-3,self.cPath+self.cPath+self.cPath],
					[0-1,0-5,0-4,self.cPath+self.cPath+self.cPath+self.cPath],
					]
			for (i,n,nn,e) in zz:
				if self.isMonster((NewPos+i)+n)==True:
					if self.PuzzleFileHolder[(NewPos+i)+nn:(NewPos+i)]==e:
						self.PuzzleFileHolder=self.replacePos((NewPos+i)+nn,self.PuzzleFileHolder[(NewPos+i)+n],self.PuzzleFileHolder); 
						self.PuzzleFileHolder=self.replacePos((NewPos+i)+n,self.cPath,self.PuzzleFileHolder); 
			## Mobs Above of the User.
			i=1; n=2; nn=1; e=''+self.cPath
			if self.isMonster((NewPos-((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*1))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			i=1; n=3; nn=2; e=''+self.cPath+self.cPath
			if self.isMonster((NewPos-((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*1))]+self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*nn))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			i=1; n=4; nn=3; e=''+self.cPath+self.cPath+self.cPath
			if self.isMonster((NewPos-((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*1))]+self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*nn))]+self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*(nn-1)))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			i=1; n=5; nn=4; e=''+self.cPath+self.cPath+self.cPath+self.cPath
			if self.isMonster((NewPos-((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*1))]+self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*nn))]+self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*(nn-1)))]+self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*(nn-2)))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos-((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos-((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			
			## Mobs Below of the User.
			i=1; n=2; nn=1; e=''+self.cPath
			if self.isMonster((NewPos+((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*1))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			i=1; n=3; nn=2; e=''+self.cPath+self.cPath
			if self.isMonster((NewPos+((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*1))]+self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*nn))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			i=1; n=4; nn=3; e=''+self.cPath+self.cPath+self.cPath
			if self.isMonster((NewPos+((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*1))]+self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*nn))]+self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*(nn-1)))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			i=1; n=5; nn=4; e=''+self.cPath+self.cPath+self.cPath+self.cPath
			if self.isMonster((NewPos+((self.LineLength+1)*n)))==True:
				if self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*1))]+self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*nn))]+self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*(nn-1)))]+self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*(nn-2)))]==e:
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*nn)),self.PuzzleFileHolder[(NewPos+((self.LineLength+1)*n))],self.PuzzleFileHolder); 
					self.PuzzleFileHolder=self.replacePos((NewPos+((self.LineLength+1)*n)),self.cPath,self.PuzzleFileHolder); 
			
			
			
			### ### ## 
	## ### ############################################################ ### ## 
	def DoFight(self,action,F):
		MoveValid=False; 
		try: CurPos=self.PuzzleFileHolder.index(self.cUser); 
		except: return #deb('unable to grab CurPos',str(action)); 
		## ### ## Direction We're Moving.
		if   action==Config.ACTION_MOVE_LEFT:  NewPos=CurPos-1; self.ImFacing='left'; 
		elif action==Config.ACTION_MOVE_RIGHT: NewPos=CurPos+1; self.ImFacing='right'; 
		elif action==Config.ACTION_MOVE_UP:    NewPos=CurPos-(self.LineLength+1); self.ImFacing='up'; 
		elif action==Config.ACTION_MOVE_DOWN:  NewPos=CurPos+(self.LineLength+1); self.ImFacing='down'; 
		else: return #deb('unhandled action',str(action)); 
 		## ### ## What's @ the new position.
		if NewPos > len(self.PuzzleFileHolder): MoveValid=False; 					 ## Outside of MAP. New Position is before the start of the map.
		elif NewPos < 0: MoveValid=False; 																 ## Outside of MAP. New Position is after the end of the map.
		elif self.PuzzleFileHolder[NewPos]==self.cWall: 	MoveValid=False; ## Walls
		elif self.PuzzleFileHolder[NewPos]=='\n': 				MoveValid=False; ## Line Wrap
		elif self.PuzzleFileHolder[NewPos]==self.cPath:  	MoveValid=True;  ## Empty Space / Path
		elif self.PuzzleFileHolder[NewPos]==self.cEnd: 	 	MoveValid=True;  ## Exit / End / Stairs
		elif self.PuzzleFileHolder[NewPos]==self.cStart: 	MoveValid=True;  ## Start Location. Acts as a path and jump-to point.
		elif self.PuzzleFileHolder[NewPos]==self.cKey: 		MoveValid=self.MoveTo_Key(action,F,CurPos,NewPos)
		elif self.PuzzleFileHolder[NewPos]==self.cMyLove: MoveValid=self.MoveTo_MyLove(action,F,CurPos,NewPos)
		elif self.PuzzleFileHolder[NewPos] in [self.cMonster,self.cMonster0,self.cMonster1,self.cMonster2,self.cMonster3,self.cMonster4,self.cMonster5,self.cMonster6,self.cMonster7,self.cMonster8,self.cMonster9]: 
			MoveValid=self.MoveTo_Monster(action,F,CurPos,NewPos)
		elif self.PuzzleFileHolder[NewPos]==self.cDoor: 	MoveValid=self.MoveTo_Door(action,F,CurPos,NewPos)
		elif self.PuzzleFileHolder[NewPos]==self.cLife: 	MoveValid=self.MoveTo_Life(action,F,CurPos,NewPos)
		elif self.PuzzleFileHolder[NewPos]==self.cSuperLife: 	MoveValid=self.MoveTo_SuperLife(action,F,CurPos,NewPos)
		elif self.PuzzleFileHolder[NewPos]==self.cPortalFA: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalTA)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalTA); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalTA: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalFA)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalFA); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalFP: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalTP)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalTP); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalTP: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalFP)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalFP); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalFO: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalTO)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalTO); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalTO: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalFO)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalFO); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalFQ: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalTQ)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalTQ); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalTQ: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalFQ)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalFQ); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalFU: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalTU)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalTU); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalTU: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalFU)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalFU); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalFJ: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalTJ)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalTJ); 
		elif self.PuzzleFileHolder[NewPos]==self.cPortalTJ: self.JumpAvatar(self.PuzzleFileHolder.index(self.cPortalFJ)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cPortalFJ); 
		elif self.PuzzleFileHolder[NewPos]==self.cToStart: self.JumpAvatar(self.PuzzleFileHolder.index(self.cStart)); MoveValid=True; NewPos=self.PuzzleFileHolder.index(self.cStart); 
		else: MoveValid=False; ## New Position is invalid. 
		#debob('NewPos character "'+self.PuzzleFileHolder[NewPos]+'"'); 
 		## ### ## Prepare data for output.
		if MoveValid==True: #debob('valid move from '+str(CurPos)+' to '+str(NewPos))
			## ### ## ### ## Selecting Currect Object for Previous Location (CurPos).
			if self.PuzzleFileHolder_Original[CurPos]==self.cStart: self.replaceUSER(self.cStart)
			elif self.PuzzleFileHolder_Original[CurPos]==self.cEnd: self.replaceUSER(self.cEnd)
			elif self.PuzzleFileHolder_Original[CurPos] in [self.cPortalFA,self.cPortalFP,self.cPortalFO,self.cPortalFQ,self.cPortalFU,self.cPortalFJ,self.cPortalTA,self.cPortalTP,self.cPortalTO,self.cPortalTQ,self.cPortalTU,self.cPortalTJ,self.cToStart]: self.replaceUSER(self.PuzzleFileHolder_Original[CurPos])
			else: self.replaceUSER(self.cPath)
			## ### ## ### ## Placing User @ the New Location (NewPos).
			self.PuzzleFileHolder=self.replacePos(NewPos,self.cUser,self.PuzzleFileHolder) #self.PuzzleFileHolder=self.PuzzleFileHolder[0:NewPos]+self.cUser+self.PuzzleFileHolder[NewPos+1:len(self.PuzzleFileHolder)]; 
			## ### ## ### ## Code for Monster Movement.
			self.MoveMent_AdjustMonsterPlacement(action,F,CurPos,NewPos)
			## ### ## ### ## Checking Status of User and The Game.
			if self.gameLifes < 1: self.GameOver(); ## You're D-E-A-D!
			elif self.PuzzleFileHolder_Original[NewPos]==self.cEnd: self.VictoryDance(); ## You've found the exit. #elif self.PuzzleFileHolder_Original[NewPos]==self.cMyLove: self.FinalVictoryDance(); 
			## ### ## ### ## Output Display Coding.
			if (tfalse(SettingG("show-map"))==True) and (tfalse(SettingG("show-maplocation"))==True): self.PrepareMaze(self.PuzzleFileHolder); ## Display for the Text Map.
			NewPos=self.PuzzleFileHolder.index(self.cUser); 
			self.displayVisualItems(NewPos); 
		#self.cUser='@'; self.cEnd='E'; self.cStart='S'; self.cWall='#'; self.cPath=' '; 
	def JumpAvatar(self,NewPos):
		#self.PuzzleFileHolder.index(self.cPortalFJ)
		return
	def replaceUSER(self,n):
		try: self.PuzzleFileHolder=self.PuzzleFileHolder.replace(self.cUser,n,1)
		except: pass
	def replacePos(self,Pos,n,t):
		try: return t[0:Pos]+n+t[Pos+1:len(t)]
		except: return t
		
	def VictoryDance(self):
		try:
				if self.gameMyLove > 0: self.FinalVictoryDance(); return
				deb("game won",str(self.gameMyLove)); 
				SFX('fanfare_x'); 
				##splash.do_My_Splash(self.iDuckShot3,1); 
				splash.do_My_Splash(artp('nextlevel02'),3,True,(self.scr['W']-580)/2,(self.scr['H']-135)/2,580,135); 
				#splash.do_My_Splash(artj('corn-maze-exit'),3,True,(self.scr['W']-500)/2,(self.scr['H']-333)/2,500,333); 
				##splash.do_My_Splash(artj('corn-maze-exit'),2,True,10,150,self.scr['W']-200,self.scr['H']-150); 
				self.LoadGridFile(); 
				xbmc.sleep(20); 
				NewPos=self.PuzzleFileHolder.index(self.cUser); 
				self.displayVisualItems(NewPos); 
				#self.CloseWindow1st(); #DoA("Back"); 
		except: pass
	def FinalVictoryDance(self):
		try:
				deb("game won #2",str(self.gameMyLove)); 
				SFX('fanfare2'); 
				splash.do_My_Splash(artj('congrats02'),5,True,(self.scr['W'])/4,(self.scr['H'])/4,(self.scr['W'])/2,(self.scr['H'])/2); 
				xbmc.sleep(20); 
				self.CloseWindow1st(); #DoA("Back"); 
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
