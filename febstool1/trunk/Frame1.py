#Boa:Frame:Frame1

import sys
from flickrapi import FlickrAPI

import wx

# Autenticazione
flickrAPIKey = "ea9b8730af07cd76f6dc4fde27744b74"  # API key
flickrSecret = "45dfeeb5abec1ff9"                  # shared "secret"

# crea una istanza di FlickrAPI 
fapi = FlickrAPI(flickrAPIKey, flickrSecret)

# ottieni un token valido
if sys.platform == 'win32':
    token = fapi.getToken(browser="C:\\Progra~1\\Intern~1\\iexplore.exe", perms="write")
else:
    token = fapi.getToken(browser="firefox", perms="write")
rsp = fapi.auth_checkToken(api_key=flickrAPIKey, auth_token=token)
fapi.noExitTestFailure(rsp)
user_id = rsp.auth[0].user[0]['nsid']

#################sux

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1CHOICE1, wxID_FRAME1CHOICE2, wxID_FRAME1INTESTAZIONE, 
 wxID_FRAME1OKBUTTON, wxID_FRAME1STATUSBAR1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class Frame1(wx.Frame):
    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(number=0, text=u'')

        parent.SetStatusWidths([-1])

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(527, 490), size=wx.Size(341, 185),
              style=wx.DEFAULT_FRAME_STYLE, title=u'febs microtool #1')
        self.SetClientSize(wx.Size(341, 185))

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.intestazione = wx.StaticText(id=wxID_FRAME1INTESTAZIONE,
              label=u'This is a very simple tool. Insert the set and the pool ID down here and push the button.',
              name=u'intestazione', parent=self, pos=wx.Point(16, 8),
              size=wx.Size(304, 40), style=0)
        self.intestazione.SetExtraStyle(0)
        self.intestazione.Bind(wx.EVT_HELP, self.OnStaticText1Help,
              id=wxID_FRAME1INTESTAZIONE)

        self.okButton = wx.Button(id=wxID_FRAME1OKBUTTON, label=u'Push me!',
              name=u'okButton', parent=self, pos=wx.Point(232, 80),
              size=wx.Size(85, 30), style=0)
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOkButtonButton,
              id=wxID_FRAME1OKBUTTON)

        self.choice1 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE1,
              name='choice1', parent=self, pos=wx.Point(32, 56),
              size=wx.Size(136, 35), style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE2,
              name='choice2', parent=self, pos=wx.Point(32, 112),
              size=wx.Size(136, 35), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
	self.PopulateLists()

    def OnStaticText1Help(self, event):
        event.Skip()

    def OnOkButtonButton(self, event):
	# grabba tutte le foto con l'id specificato
	self.statusBar1.SetStatusText(number=0, text='getting photos for set ' + self.dictSet[self.choice1.GetString(self.choice1.GetSelection())] )
	self.statusBar1.Refresh()
	self.statusBar1.Update()
	rsp = fapi.photosets_getPhotos(api_key=flickrAPIKey,photoset_id=self.dictSet[self.choice1.GetString(self.choice1.GetSelection())] )
	self.statusBar1.SetStatusText(number=0, text='getting photos for set ' + self.dictSet[self.choice1.GetString(self.choice1.GetSelection())] + ': ' + str(fapi.noExitTestFailure(rsp)))
	self.statusBar1.Refresh()
	self.statusBar1.Update()

	#self.statusBar1.SetStatusText(number=0, text='MEGA ANAL')
	#self.statusBar1.Refresh()
	#self.statusBar1.Update()
	
	#posta quelle pubbliche nel gruppo
	for a in rsp.photoset[0].photo:
		rsp = fapi.photos_getPerms(api_key=flickrAPIKey,photo_id=a['id'],auth_token=token)
		if ( rsp.perms[0].attrib['ispublic'] ):
			rsp = fapi.groups_pools_add(api_key=flickrAPIKey,photo_id=a['id'],auth_token=token,group_id=self.dictGroup[self.choice2.GetString(self.choice2.GetSelection())] )
			self.statusBar1.SetStatusText(number=0, text='posting ' + a['id'] + '... ' + str(fapi.noExitTestFailure(rsp)) )
			self.statusBar1.Refresh()
			self.statusBar1.Update()
	self.statusBar1.SetStatusText(number=0, text=u'Finished.')
        event.Skip()
	
    def PopulateLists(self):
	self.dictSet={}
        rsp = fapi.photosets_getList(api_key=flickrAPIKey, user_id=user_id)
        self.statusBar1.SetStatusText(number=0, text='downloading list of sets:' + str(fapi.noExitTestFailure(rsp)))
        self.statusBar1.Refresh()
        self.statusBar1.Update()
        for set in rsp.photosets[0].photoset:	
              self.choice1.Append(set.title[0].elementText)
	      self.dictSet[set.title[0].elementText]=set['id']
    
	self.dictGroup={}
        rsp = fapi.groups_pools_getGroups(api_key=flickrAPIKey, user_id=user_id, auth_token=token)
        self.statusBar1.SetStatusText(number=0, text='downloading list of groups:' + str(fapi.noExitTestFailure(rsp)))
        self.statusBar1.Refresh()
        self.statusBar1.Update()
        for group in rsp.groups[0].group:	
              self.choice2.Append(group['name'])
	      self.dictGroup[group['name']]=group['id']
    
    def OnTextCtrlPoolIdSetFocus(self, event):
	#self.textCtrlPoolId.SetValue(u'')
        event.Skip()

    def OnTextCtrlSetIdSetFocus(self, event):
	#self.textCtrlSetId.SetValue(u'')
        event.Skip()
