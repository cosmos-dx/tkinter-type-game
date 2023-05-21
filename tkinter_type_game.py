#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
    from reportlab.lib.pagesizes import landscape, portrait
    from reportlab.pdfgen import canvas
except :
    import os, sys
    pp = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, pp)
    ##from reportlab.lib.pagesizes import landscape, portrait
    ##from reportlab.pdfgen import canvas
    

try:
    # for Python2
    from Tkinter import *
    import ttk
    from ttk import Notebook, Combobox
    import tkFileDialog as FileDialog
    import tkColorChooser as FiCor
    import Queue as queue
    #import Tkinter as tk
    #tk = Tk()
except ImportError:
    # for Python3
    from tkinter import filedialog as FileDialog
    from tkinter import colorchooser as FiCor
    from tkinter import *
    from tkinter import ttk
    from tkinter.ttk import Notebook, Combobox
    import queue as queue
from collections import defaultdict, OrderedDict
from functools import partial
import json
import os
import time
from datetime import datetime
    
class Typtest(Frame):
    def __init__(self, parent, sptag, sizepos, **kw):
        Frame.__init__(self, parent)
        self.rscr = kw['rscr']
        self.sptag = sptag
        self.ftsz = 14 #### Font Size 
        sw= self.rscr['sw']
        sh= self.rscr['sh']
        try:
            self.master.iconbitmap(self.rscr['myiconpath']) ### Setting Icon
        except :
            print ("icon file not set, place .ico file and rename as 'myicon.ico' "
                   "\n inside ===>>> %s Directory"%self.rscr['mydirpath'] )
        if sizepos:
            wsw, wsh, xpos, ypos = sizepos
            self.sizepos1 = sizepos
            self.sizepos2 = self.SetFrameCenter(sw, sh)
        else:
            wsw, wsh, xpos, ypos = self.SetFrameCenter(sw, sh)
            self.sizepos1 = wsw, wsh, xpos, ypos
            self.sizepos2 = wsw, wsh, xpos, ypos
        ###self.master.geometry('%dx%d+%d+%d' % (wsw, wsh, xpos, ypos))
        self.master.title(self.sptag.upper())
        labelfontsize = ['Courier New', self.ftsz, 'normal'] ###self.rscr['font']['label']['font']
        self.lfont = labelfontsize
        bg = 'SystemButtonFace'
        self.lfnt_fg_bg = {'font': ['Courier New', self.ftsz, 'normal'], 'bg':bg, 'fg':'black'} ###self.rscr['font']['label']
        self.lfnt_fg_bgsm = {'font': ['Courier New', self.ftsz-2, 'normal'], 'bg':bg, 'fg':'black'}
        lb_fg_bg = {'font': ['Courier New', self.ftsz, 'bold'], 'bg': '#b0e0e6', 'fg': 'black',} ###self.rscr['font']['listbox']
        lbfgbg = {'font': ['Courier New', self.ftsz-2, 'bold'],'bg':bg, 'fg':'blue',} ###self.rscr['font']['listbox']
        lbfgbgsm = {'font': ['Courier New', self.ftsz-4, 'bold'],'bg':bg, 'fg':'blue',}
        self.ebg = '#b0e0e6'
        self.htcolor = 'light yellow'
        efnt_fg_bg = {'font': ['Courier New', self.ftsz, 'bold'], 'bd':3, 'bg':self.ebg, 'fg':'black', 'relief':'sunken'}
        self.efnt_fg_bg = efnt_fg_bg
        self.bfnt_fg_bg = {'font': ['Courier New', self.ftsz, 'bold'], 'bg':self.htcolor, 'fg':'blue', 'relief':'raised'}
        self.bfnt_fg_bgw = {'font': ['Courier New', self.ftsz, 'bold'], 'bg':'white','fg':'black', 'relief':'raised'}
        ### decorating label... by selecting font face; background color, foreground color
        headlabelkw = {'font': ['Comic Sans MS', sum([self.ftsz,6]), 'bold'], 'bg':'yellow', 'fg':'black'}
        self.levelbutton_bg = 'sky blue'
        self.levelbutton_bg_hc = 'yellow'  ### highlight colour bg
        userlabelkw = {'font': ['Comic Sans MS', self.ftsz, 'bold'], 'bg':self.levelbutton_bg, 'fg':'black','relief':'raised'}
        typtest_fg_bg = {'font': ['Courier New', sum([self.ftsz, 2]), 'bold'], 'bd':3, 'bg':self.ebg, 'fg':'black', 'relief':'sunken'}
        wrow = 0

        self.head = Label(self.master, text="WelCome to Typing Test Game !!",
                    justify='center', **headlabelkw)
        self.head.grid(row=wrow, column = 0, columnspan=10, sticky = 'nwes')
        
        wrow += 1
        self.top = Label(self.master, text="Login and Proceed !",
                    justify='center', **self.lfnt_fg_bg)
        
        self.top.grid(row=wrow, column=0,columnspan=10, sticky = 'nwes')
        wrow += 1

        self.ulstx = Label(self.master, text='Login ID:', **self.lfnt_fg_bg)
        self.ulstx.grid(row=wrow, column = 1, columnspan=2, sticky = 'e')
        self.ultx = Entry(self.master, **self.efnt_fg_bg)
        self.ultx.grid(row=wrow, column=3, columnspan=4, sticky = 'w')
        wrow += 1
        self.upstx = Label(self.master, text='User Password:', **self.lfnt_fg_bg)
        self.upstx.grid(row=wrow, column = 1, columnspan=2, sticky = 'e')
        self.uptx = Entry(self.master, show = '*', **self.efnt_fg_bg)
        self.uptx.grid(row=wrow, column = 3, columnspan=4, sticky = 'w')
        wrow += 1
        self.topscore = 0
        self.highscore_stx = Label(self.master, text='Highest Score :', **self.lfnt_fg_bg)
        self.highscore_stx.grid(row=wrow, column = 1, columnspan=8, sticky = 'w')
        self.highscore_stx['fg']='blue'
        self.highscore_stx['bg']='OliveDrab1'
        wrow += 2
        
        self.loginbtn_wrow = wrow ### will reuse later
        self.loginbtn = Button(self.master, text='Login',
                            command=self.OnLogin, **self.bfnt_fg_bg)
        self.loginbtn.grid(row=wrow, column=3, columnspan=4, sticky = 'we')
       
        self.registebtn_press = False ### will reuse later
        self.registebtn = Button(self.master, text='Register',
                            command=self.OnRegister, **self.bfnt_fg_bgw)
        self.registebtn.grid(row=wrow, column=9, columnspan=1, sticky = 'e')
        
        self.para = ''' ParqaGraph dfdhkh dhgkjdhfkjg  \n fgdgdfgdf \n dfgdfg '''

        self.stx = Text(self.master,  height=12,
                     **typtest_fg_bg)
        self.SetValue(self.stx, self.rscr['para'])
        txtll = {i:tx for i, tx in enumerate(self.rscr['para'].split('\n'))}
        
        self.GetPara()
        
        self.stxvbar = Scrollbar(self.master, orient='vertical', command=self.stx.yview)
        self.stx.config(yscrollcommand=self.stxvbar.set)
        self.stx['state']='disabled'
        self.stxhbar = Scrollbar(self.master, orient='horizontal', command=self.stx.xview)
        self.stx.config(xscrollcommand=self.stxhbar.set)
        self.txstop = False
        self.tx = CustomText(self.master, height=12, **typtest_fg_bg)
        self.txvbar = Scrollbar(self.master, orient='vertical', command=self.tx.yview)
        self.tx.config(yscrollcommand=self.txvbar.set)

        self.txhbar = Scrollbar(self.master, orient='horizontal', command=self.tx.xview)
        self.tx.config(xscrollcommand=self.txhbar.set)
        
        setrowfrom = 1
        self.ullb = [] ### Now we are taking Label widget in list ( list or dictionary )
        self.ulevelbtn = []
        self.ulevel = {} ### Now we are taking Label widget in list ( list or dictionary )
        levelcount = 1
        for tx in ['USER 1', 'USER 2', 'USER 3', 'USER 4', 'USER 5',]:## will not use enumerate; enumerate start from zero, and we need different method
            ### we will take width also for static gap between user name and user login Label
            lb = Label(self.master, width=40, text=tx, **userlabelkw)
            levelbtn = Button(self.master, width=20, text='Level %s '%levelcount, **userlabelkw)
            ### sticky for sticky labels on our left side; similarly column = 0 for left side
            lb.grid(row=setrowfrom, column=0, columnspan=1, sticky = 'w')
            ### Taking Padding with Label between loging Entry Widget and levelbtn Label Widget
            Label(self.master, width=15, ).grid(row=setrowfrom, column=8, columnspan=1, sticky = 'e') 
            levelbtn.grid(row=setrowfrom, column=9, columnspan=1, sticky = 'e') 
            self.ullb.append(lb) ### all label stored in list; we can reuse later; whenever required
            ### all button stored in dictionary; we can reuse later; whenever required
            ### take button widget as key and value as index; so we can catch which levelbtn button pressed
            ### this is actual programming technique; otherwise if you define seperate widget and seperate function
            ### you programme will become unnecessrily lengthy;
            ### take SHARP LOOK ... what is happening here....
            self.ulevel[levelbtn]=levelcount
            self.ulevelbtn.append(levelbtn) ### required list
            levelbtn.bind('<Button-1>', self.OnCommonLevelLoadButton) ### binding common function for all level button
            setrowfrom += 1
            levelcount += 1
        firstlevelbutton = self.ulevelbtn[0]
        firstlevelbutton['bg']=self.levelbutton_bg_hc
        firstlevelbutton['relief']='sunken'
        firstlevelbutton['bd']=3
        self.ultx.bind('<Key>', self.OnUseridKey) 
        self.uptx.bind('<Key>', self.OnUserpassKey)
        self.loginbtn.bind('<Key>', self.OnloginKey)
        
        self.tx.bind("<<TextModified>>", self.OnCustomText) ### Live event
        self.tx.bind('<Key>', self.OnEyKey)
        self.tx.tag_configure("red", foreground="red") ### configuring self.tx for charecter selection and show them red whenever you need

        #self.stx.grid(row=wrow, column = 1, sticky = 'wens')
        wrow += 1 ### for verical display by one row down
        #self.tx.grid(row=wrow, column = 1, sticky = 'wens')

        self.status = Label(self.master, text='', **self.lfnt_fg_bg)
        wrow += 1 ### for verical display by one row down
        self.status.grid(row=wrow, column = 1, columnspan=10, sticky = 'wens')

        wrow += 1 ### for verical display by one row down
        self.status1 = Label(self.master, text='', **self.lfnt_fg_bg)
        self.status1.grid(row=wrow, column = 1, columnspan=10, sticky = 'wens')
        self.status1['fg']='red'
        self.startbtn = Button(self.master, text='Start',
                            command=self.OnStart, **self.bfnt_fg_bg)
        self.startbtn.bind('<Key>', self.OnStartKey)
        
        self.closebtn = Button(self.master, text='Close',
                            command=self.OnClose, **self.bfnt_fg_bg)
        self.resetbtn = Button(self.master, text='Reset',
                            command=self.OnReset, **self.bfnt_fg_bg)
        self.bottpad = Label(self.master, text=' - ', **self.lfnt_fg_bg)
        self.timecount = '0'
        ### Taking 1 minutes i,e 60 seconds(from datetime)
        ### so we have to take value less than 60 seconds,
        ### after that Game Over After this value
        self.timemax = 59
        self.errorcount = 0
        self.scorecount = 0
        self.accuracycount = 0
        self.charslen = 0
       
        self.userid = None
        self.counter = 66600
        self.running = False
        self.the_time = ''
        self.myclock = Label(self.master, text='', **headlabelkw)
        wrow += 1 ### for verical display by one row down
       
        for r in range(30):
            self.master.rowconfigure(r, weight=1)
        for c in range(8):
            self.master.columnconfigure(c,weight=1)
        self.wrow = wrow
        ### check user password exist or not
        self.topscore_dict={}
        if not self.rscr['login'] :
            self.top['text']=' User Not Register Yet! \n Please Register \n and Proceed !!' 
            self.top['fg']='red'
            self.loginbtn['text']='Register'
            self.loginbtn['fg']='blue'
            self.loginbtn.grid(row=self.loginbtn_wrow, column=1, columnspan=4,)
            self.registebtn.grid_forget()
            self.highscore_stx['text']='Highest Score: N.A'
        else:
            for i, (k, v) in enumerate(self.rscr['login'].items()):
                try:
                    self.topscore_dict[v['sc']]=k ### will get userid as value and score as key
                except KeyError:
                    self.topscore_dict['0']='N.A' ### Not Avelable
                try:
                    self.ullb[i]['text']='[ %s ]: Highest Score:%s Accuracy:%s'%(k.title(), v['sc'], v['ac'])
                except IndexError: ### Actual user may exceed than user Label list ; so >>> sticking with self.ullb Labels Only  
                    pass
            self.topscore = max(self.topscore_dict.keys())
            hs_user = self.topscore_dict[self.topscore]
            self.highscore_stx['text']='Highest Score:%s [%s]'%(self.topscore, hs_user)
             
        self.ultx.focus()
    
    def GetPara(self):
        self.paradict = {}
        for i, v in enumerate(self.rscr['para'].split('\n')):
            subdict = {}
            for idx, txt in enumerate(v):
                subdict[idx]=txt 
            self.paradict[i]=subdict

    def RefreshButtons(self):
        for b in self.ulevel:
            b['bg']=self.levelbutton_bg
            b['relief']='raised'
            b['bd']=3
            
    def OnCommonLevelLoadButton(self, event):
        wdg = event.widget  ### event has widget attribute; which widget is calling this event; so widget = event.widget
        levelidx = self.ulevel[wdg]
        self.RefreshButtons()
        wdg['bg']=self.levelbutton_bg_hc
        wdg['relief']='sunken'
        wdg['bd']=1
        
        filepath = os.path.join(self.rscr['mydirpath'], '%s%s.txt'%(self.rscr['textfilename'],str(levelidx)))
        gettext = ''
        try:
            with open(filepath, 'r') as f:
                gettext = f.read()
            self.rscr['para'] = gettext
            self.stx['state']='normal'
            self.SetValue(self.stx, self.rscr['para']) ### disabled widget not allow set value; first make normal > set value > disabled
            self.stx['state']='disabled'
        except :
            self.top['text']='ReStart Again !! \nThis is First Time Login !!'
            self.top['fg']='red'
            self.closebtn['fg']='red'
        
    def SetFrameCenter(self, sw, sh):
        wsw = int(sw/1.6)  ### window Width
        wsh = sh-100   ### window Height reducing from buttom side
        xpos = (sw/2)-(wsw/2) ### Center On Screen
        ypos = 0 ####(sh/2)-(wsh/2)  ### Center On Screen
        return wsw, wsh, xpos, ypos
    
    def SetValue(self, wdg, value):
        wdg.delete(1.0, "end")
        wdg.insert("end", value)
    
    def Hide(self):
        self.head.grid_forget()
        for lb in self.ullb:
            lb.grid_forget()
        self.ulstx.grid_forget()
        self.ultx.grid_forget()
        self.upstx.grid_forget()
        self.uptx.grid_forget()
        self.loginbtn.grid_forget()
        self.registebtn.grid_forget()
        
    def Show(self):
        self.top.grid(row=0, column=1,columnspan=4,sticky = 'wens')
        self.top.configure(text='*** Maximum Time Limit 60 Seconds ***')
        stxcol = 1
        stxrow = 1
        stxrowspan = 2
        stxcolspan = 4
        txcol = 1
        txrow = 4
        txrowspan = 4
        txcolspan = 4
        self.myclock.grid(row=0, column = 8, columnspan=2, rowspan=1, sticky = 'news')
        self.stx.grid(row=1, column = stxcol, columnspan=4, rowspan=2, sticky = 'news')
        self.stxvbar.grid(row=1, column = stxcol-1, rowspan=stxrowspan, sticky='ens')
        self.stxhbar.grid(row=sum([stxrow,stxrowspan]), column = 1, columnspan=stxcolspan, rowspan=1, sticky='news')
        self.tx.grid(row=4, column = 1, columnspan=4, rowspan=4, sticky = 'news')
        self.txvbar.grid(row=txrow, column = txcol-1, rowspan=txrowspan, sticky='ens')
        self.txhbar.grid(row=sum([txrow,txrowspan]) , column = 1, columnspan=txcolspan, rowspan=1, sticky='news')
        self.status.grid(row=9, column = 1, columnspan=10, rowspan=1, sticky = 'news')
        self.closebtn.grid(row=10, column = 0, columnspan=2, rowspan=1, sticky = 's')
        self.startbtn.grid(row=10, column=3, columnspan=2, rowspan=1, sticky = 'news')
        self.resetbtn.grid(row=7, column = 8, columnspan=4, rowspan=1, sticky = 'ew')
        self.bottpad.grid(row=11, column = 0, columnspan=4, rowspan=1, )
        self.highscore_stx.grid(row=8, column = 8, columnspan=2, sticky = 'w')
        ###wsw, wsh, xpos, ypos = self.sizepos2
        pad = 70
        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth(), self.master.winfo_screenheight()-pad))
        self.tx['state']='disabled'
        self.startbtn.focus()
        
    def ClearFields(self):
        self.ultx.delete(0, "end")
        self.ultx.insert("end", '')
        self.uptx.delete(0, "end")
        self.uptx.insert("end", '')
        self.registebtn_press = True
        
    def Validate_Insert_Data(self, userid, userpass):
        validdate = True ### default
        self.status['text']=''
        self.status['fg']='black'  ### default background
        if userid.strip() == "":
            self.status['text']='UserID Cannot Leave Empty !'
            self.status['fg']='red'
            validdate = False
        if userpass.strip() == "":
            self.status['text']='Password Cannot Leave Empty !'
            self.status['fg']='red'
            validdate = False
        return validdate

    def WriteJson(self, userid, userpass, firsttime=True):
        validate = True
        jsondata = self.rscr['login']       
        filepath = self.rscr['jsonpath']
        if firsttime:
            jsondata[userid]={'p':userpass, 'err':'', 'sc':0, 'ac':0, 'at':0, 'other':''} ### at is attempt
            with open (filepath, 'w') as jsf:
                json.dump(jsondata, jsf)
        else:
            for k, v in jsondata.items():
                if  userid == k:
                    validate = False
                    break
            if validate:
                jsondata[userid]={'p':userpass, 'err':'', 'sc':0, 'ac':0, 'at':0, 'other':''} ### at is attempt
                with open (filepath, 'w') as jsf:
                    json.dump(jsondata, jsf)
                ### New Registration successfully Done
                self.registebtn.grid_forget()
                self.loginbtn.grid(row=self.loginbtn_wrow, column=3, columnspan=4, sticky='w')
            else:
                self.status['text']='User [%s] Already Register'%userid
                self.status['fg']='red'
            
    def ValidateUser(self, userid, userpass):
        validate = self.Validate_Insert_Data(userid, userpass)
        if not validate:
            validate = False
            return validate ### Terminate Functiion Here (Empty Fields)
        jsondata = self.rscr['login']
        if jsondata.get(userid): ### Matching user id with key:value
            vuserpass = jsondata.get(userid)
            ### vuserpass is now a dictionary {'p':userpass, 'err':'', 'sc':0, 'ac':0, 'at':0, 'other':''} ### at is attempt
            if vuserpass['p'] == userpass:
                self.status['text']='Hi %s !'%userid
                self.status['fg']='blue'
                validate = True
            else:
                self.status['text']='Sorry ! Wrong UserID or Password !'
                self.status['fg']='red'
                validate = False
        else:
            validate = False
            self.status['text']='Sorry ! Wrong UserID !'
            self.status['fg']='red'
        return validate

    def OnRegister(self, event=None):
        self.loginbtn.grid_forget()
        self.registebtn.grid(row=self.loginbtn_wrow, column=3, columnspan=4, sticky='w')
        self.top['text']='New User Registeration !!'
        self.top['fg']='blue'
        if self.registebtn_press:
            self.userid = self.ultx.get()
            userpass = self.uptx.get()
            validate = self.Validate_Insert_Data(self.userid, userpass)
            if validate:
                ### Only After Validation data will write
                self.WriteJson(self.userid, userpass, firsttime=False)
                self.OnSuccessWrite()
            else:
                ###return unchanged
                return False
        self.ClearFields()
       
    def OnSuccessWrite(self):
        self.loginbtn['text']=' Login '
        self.loginbtn['fg']='black'
        self.top['text']='Successfully Register !!\n Login Agian !!'
        self.top['fg']='blue'
        self.loginbtn.grid(row=self.loginbtn_wrow, column=3, columnspan=4, sticky='w')
                
    def OnLogin(self, event=None):
        self.userid = self.ultx.get()
        userpass = self.uptx.get()
        if self.loginbtn['text'].lower() == 'register': ### take text in lower; no matter what Button Label in Capital or Title
            ### otherwise string will not match (case senesitive)
            ### wite json data here
            validate = self.Validate_Insert_Data(self.userid, userpass)
            if validate:
                ### Only After Validation data will write
                self.WriteJson(self.userid, userpass)
                self.OnSuccessWrite()
            else:
                ###return unchanged
                return False
        else:
            if self.ValidateUser(self.userid, userpass):
                self.Hide()
                self.Show()
        
    def OnUseridKey(self, event=None):
        if event.keysym in ['Next','Tab','Return']:
            self.uptx.focus()

    def OnUserpassKey(self, event=None):
        if event.keysym in ['Next','Tab','Return']:
            self.loginbtn.focus()

    def OnloginKey(self, event=None):
        if event.keysym in ['Next','Tab','Return']:
            self.OnLogin()
            
    def OnEyKey(self, event=None):
        key = event.keysym
        if key == 'BackSpace':
            if self.errorcount > 0:
                self.errorcount -= 1
            
    def OnCustomText(self, event):
        if self.txstop:
            return
        if int(self.timecount) > self.timemax:
            self.status.configure(text="Game Over")
            self.SaveAfterGameOver()
            return
        try:
            text = event.widget.get("1.0", "end-1c")
             
            charslen = len(text)-1
            self.status.configure(text="%s chars" % charslen)
            wdgindex = event.widget.index("end-1c")
            (l, c) = map(int, wdgindex.split("."))
            line = l-1
            self.charslen = c-1
            if self.charslen == -1:
                self.charslen = 0
            text = text.split('\n')[line]
           
            #### here strip used only for when user press enter white space create 
            if self.paradict[line][self.charslen].strip() != text[self.charslen:c].strip(): 
                self.status.configure(text="%s chars" % self.charslen)
                self.status1.configure(text="%s Errors" % self.errorcount)
                mod1, mod2 = wdgindex.split('.')
                mod1_ = mod1 #sum([int(mod1), -1])
                mod2_ = sum([int(mod2), -1])
                mod21_ = sum([int(mod2), 1])
                wdgindex = '.'.join([str(mod1), str(mod2_)])
                wdgindex2 = '.'.join([str(mod1), str(mod21_)])
                #print wdgindex, wdgindex2
                #self.tx.tag_add("red", "1.2", "1.4")
                self.tx.tag_add("red", wdgindex, wdgindex2)
                self.errorcount += 1
        except KeyError:
            pass

    def SaveAfterGameOver(self):
        charslen = len(self.tx.get("1.0", "end-1c"))
        score = charslen - self.errorcount
        self.scorecount = score*100
        self.accuracycount = (score*100)/charslen
        
        jsondata = self.rscr['login']
        accuracypercent = ' '.join([str(self.accuracycount),'%'])
        jsondata[self.userid]['ac']=accuracypercent
        jsondata[self.userid]['sc']=self.scorecount
        jsondata[self.userid]['err']=self.errorcount
        filepath = self.rscr['jsonpath']
        with open (filepath, 'w') as jsf:
            json.dump(jsondata, jsf)
        self.status['text']= 'Score %s'%self.scorecount
        self.status1['text']='Score: %s| Accuracy: %s'%(self.scorecount, accuracypercent)
        
    def counter_label(self):
        def count():
            if self.running:			
                # To manage the initial delay.
                if self.counter==66600:
                    self.timecount = '0'
                    display="Starting..."
                else:
                    if int(self.timecount) >= self.timemax:
                        self.top.configure(text='*** Game Over ***')
                        self.top['fg'] = 'red'
                        self.tx['state']='disabled'
                        self.SaveAfterGameOver()
                        return
                    tt = datetime.fromtimestamp(self.counter)
                    #string = tt.strftime("%H:%M:%S")
                    self.timecount = tt.strftime("%S")
                    display=self.timecount                    
                    
                self.myclock['text']='%s - Seconds '%display # Or label.config(text=display)
                # self.myclock.after(arg1, arg2) delays by
                # first argument given in milliseconds
                # and then calls the function given as second argument.
                # Generally like here we need to call the
                # function in which it is present repeatedly.
                # Delays by 1000ms=1 seconds and call count again.
                self.myclock.after(1000, count)
                self.counter += 1
        # Triggering the start of the counter.
        count()

    def ResetTime(self):
        self.counter=66600
	# If rest is pressed after pressing stop.
        if self.running==False:	
	    #reset['state']='disabled'
            self.myclock['text']='0 - Seconds'
            # If reset is pressed while the stopwatch is running.
        else:			
            self.myclock['text']='Starting...'

    def OnStartKey(self, event):
        if event.keysym in ['Next','Tab','Return']:
            self.OnStart()
            
    def OnStart(self, event=None):
        self.CommonReset()
        self.running=True ### Time Start here
        self.counter_label()
        self.startbtn['state']='disabled'
        self.tx.focus()

    def CommonReset(self):
        self.txstop = True
        self.errorcount = 0
        self.the_time = ''
        self.myclock.config(text='')
        self.status.configure(text="")
        self.status1.configure(text="")
        self.SetValue(self.tx, '')
        self.txstop = False
        self.running = False
        self.myclock.config(text='')
        self.top.configure(text='*** Maximun Time Limit 60 Seconds ***')
        self.top['fg'] = 'black'
        self.tx['state']='normal'
        self.ResetTime()
        
    def OnReset(self, event=None):
        self.CommonReset()
        self.startbtn['state']='normal'
        self.tx['state']='disabled'
        self.startbtn.focus()
                          
    def OnClose(self, event=None):
        try:
            self.master.destroy()
        except Exception as err:
            pass
        

class CustomText(Text):
    try:
        import Tkinter as tk
    except ImportError:
        import tkinter as tk
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
       
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result    

def LoadTxtData(runpath, mydir, filepath, filename):
    level1 = '''q w e r t y u i o p \na s d f g h j k l\n z x c v b n m \n
qwert yuiop\n asdfg hjkl;' \n zxcvb nm,./'''
    level2 = '''hello Hello, and And, welcome Welcome, \ntyping Typing, game Game, speed Speed \n
hello Hello, and And, welcome Welcome, \ntyping Typing, game Game, speed Speed \n
hello Hello, and And, welcome Welcome, \ntyping Typing, game Game, speed Speed \n
hello Hello, and And, welcome Welcome, \ntyping Typing, game Game, speed Speed '''
    level3 = '''hello and welcome typing game speed test\n hello and welcome typing game speed test \n
Hello And welcome Typing Game Speed Test\n Hello And welcome Typing Game Speed Test\n
And now I'm Going to Win This Typing Game. '''
    level4 = '''It was a thursday, but it felt like a  monday to hari prasad\n 
and hari loved mondays he thrived at work he dismissed the \n
old cliche of dreading monday mornings and refused to engage \n
in water cooler complaints about the grind and empty conversations \n
that included the familiar parry how was your weekend ? \n 
too short. yes, hari liked his work and was unashamed'''
    level5 = '''It was a Thursday, but it felt like a  Monday to John. \n
And John loved Mondays. He thrived at work. He dismissed the \n
old cliché of dreading Monday mornings and refused to engage \n
in water-cooler complaints about “the grind” and empty \n
conversations that included the familiar parry \n
“How was your weekend?” “Too short!”. Yes, John liked his \n
work and was unashamed. I should probably get another latte. I’ve \n
just been sitting here with this empty cup. But then I’ll start to \n
get jittery. I’ll get a decaf. No, that’s stupid, it feels stupid \n
to pay for a decaf. I can’t justify that. John was always impatient \n
on the weekends; he missed the formal structure of the business week. \n 
When he was younger he used to stay late after school on Fridays and \n
come in early on Mondays, a pattern his mother referred to with equal \n
parts admiration and disdain as “studying overtime.” Jesus, \n
I’ve written another loser. '''
    if os.path.exists(filepath):
        text = ""
        with open(filepath, 'r') as f:
            textlist = list(f.read().split('\n'))
        maxline = 100   #### you can change values according to your requirment
        indexlen = 70   #### you can change values according to your requirment; but this always less than maxline
        ### do some mathematics here; because line given in .txt file may large than your widget size,
        ### Although extra large line would adjust inside your widget; but their is always scope for 'customization'
        ### so, due to customization aspect this mathematics done
        for txt in textlist:
            feedlinelen = len(txt)
            if feedlinelen > maxline:
                ### extra lage line above our parameter i,e maxline
                ### append as new line by '\n' index by indexlen, this is called slicing
                txt = '\n'.join([txt[:indexlen], txt[indexlen:indexlen*2], txt[indexlen*2:indexlen*3],])
            text += '%s\n'%txt.strip()
        
    else:
        ### giving and setting default text here;
        ### you can copy paste any text into tfpath = './gettypetext.txt' .txt file
        ### which will create if not find in this running script path
        
        ### Creating file because it is not found at required path as we want
        mydirpath = os.path.join(runpath, mydir)
        if not os.path.exists(mydirpath):
            os.mkdir(mydirpath)
            if os.path.exists(filepath):
                print (filepath, ' line no 504 ')
        else: 
            #### Directory Path Exists but File not Found
            
            myfilepath = os.path.join(runpath, mydir)
            textlist = ['empty for zero index',level1,level2,level3,level4,level5,]
            for i in range(1, 6): ### here, we do not want index from zero, we want index from 1, so using range(1, 6); default from zero  
                levelmyfilepath = os.path.join(myfilepath, '%s%s.txt'%(filename, str(i)))
                text = textlist[i]
                with open(levelmyfilepath, 'w') as f:
                    f.write(text)
    return level1

def LoadJsonData(runpath, mydir, filepath):
    jsondata = {} #### json file are dictionary type structures
    ### jsondata default data is remain empty
    if os.path.exists(filepath):
        ### if found load json data here
        with open(filepath, 'r') as jsf: 
            jsondata = json.load(jsf)
            #### load jsondata filled by user
    else:
        ### not found at required path, lets create empty jason file data
        ### because jsondata is give as default so no need to load jason here
        ### jsondata is available by default
        with open(filepath, 'w') as jsf:
            json.dump(jsondata, jsf)
    return jsondata

def main():
    
    root = Tk()
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    rscr = {} #### Empty Dictionary you can modify if you want
    ### or
    rscr['sw']=sw
    rscr['sh']=sh
    sizepos = [700, 300, 200, 0]
    runpath = (os.path.dirname(os.path.realpath(__file__)))
    mydir = 'mygame'
    myiconpath = os.path.join(runpath,mydir,'myicon.ico')
   
    tfpath = os.path.join(runpath,mydir,'level1.txt')  ###'./%s/gettypetext.txt'%mydir #### file text path in this runnung file path only
    jsonfilepath = os.path.join(runpath,mydir,'userlogin.json')  ###'./%s/userlogin.json'%mydir ### json file path in this runnung file path only
    ### Making Logic inside Function; for neat and clear reading...
    textfilename = 'level'
    rscr['para']=LoadTxtData(runpath, mydir, tfpath, textfilename)
    rscr['myiconpath']=myiconpath
    rscr['runpath']=runpath
    rscr['mydir']=mydir
    rscr['textfilename']=textfilename
    mydirpath = os.path.join(runpath,mydir)
    rscr['mydirpath']=mydirpath
    rscr['txtpath']=tfpath
    ### Making Logic inside Function; for neat and clear reading...
    rscr['login']=LoadJsonData(runpath, mydir, jsonfilepath)
    rscr['jsonpath']=jsonfilepath
    #root.iconphoto(False, tk.PhotoImage(file=myiconpath))
    app = Typtest(root, 'Typing Test', sizepos, rscr=rscr)
    root.mainloop()


if __name__ == '__main__':
    main()

