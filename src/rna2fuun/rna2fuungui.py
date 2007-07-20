import wx
import wx.lib.scrolledpanel as scrolled
import rna2fuun
        
# Tool/menu IDs        
ID_OPEN_FILE            = 102

# Code dialog button IDs
#ID_DLG_SAVE_CMD         = 1003

# Editor title
TITLE_HEADER = 'RNA 2 Fuun - '

def PILToImage(pilImage):
     if (pilImage.mode != 'RGB'):
         pilImage = pilImage.convert('RGB')
     imageData = pilImage.tostring('raw', 'RGB')
     img = wx.EmptyImage(pilImage.size[0], pilImage.size[1])
     img.SetData(imageData)
     return img

def PILToBitmap(image):
     return wx.BitmapFromImage(PILToImage(image))

class RNAListCtrl(wx.ListCtrl):
    def __init__(self, parent, main):
        self.main = main
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL)
        
    def OnGetItemText(self, item, column):
        if column == 0:
            return self.main.m_rna[item]
        else:
            return self.main.m_commands[item]
    
    def OnGetItemImage(self, item):
        return -1
    
    def OnGetItemAttr(self, item):
        return None

class RNA2FuunGui(wx.Frame):
    def __init__(self):

        self.m_r2f = rna2fuun.rna2fuun()
        self.m_rna = []
        self.m_row = 0

        wx.Frame.__init__(self, None, -1, TITLE_HEADER, size=(1024,768))
        
        # Art provider.
        self.m_art = wx.ArtProvider()

        self.m_vsplitter = wx.SplitterWindow(self, -1)
        self.m_hsplitter = wx.SplitterWindow(self.m_vsplitter, -1)    
        self.m_rightpanel = scrolled.ScrolledPanel(self.m_vsplitter, -1, size=(140, 300), style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)            
        self.m_rnalist = RNAListCtrl(self.m_hsplitter, self)
        self.m_rnalist.InsertColumn(0, "RNA")
        self.m_rnalist.InsertColumn(1, "Translation")
        self.m_image = wx.StaticBitmap(self.m_rightpanel, -1, size=(600,600))            
        self.m_data = wx.TextCtrl(self.m_hsplitter, -1, style=wx.TE_MULTILINE|wx.TE_DONTWRAP)            
        self.m_vsplitter.SplitVertically(self.m_hsplitter, self.m_rightpanel, 100)
        self.m_hsplitter.SplitHorizontally(self.m_rnalist, self.m_data)
        self.m_leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.m_leftSizer.Add(self.m_rnalist, 0, wx.EXPAND)
        self.m_leftSizer.Add(self.m_data, 1, wx.EXPAND)
        self.m_hsplitter.SetSizer(self.m_leftSizer)
        self.m_hsplitter.SetAutoLayout(1)
        self.m_rightpanel.SetAutoLayout(1)
        self.m_rightpanel.SetupScrolling()
        
        
        menubar = wx.MenuBar()

        file = wx.Menu()

        openitem = file.Append(-1, '&Open\tCtrl+O', 'Open RNA File')
        
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        
        self.m_toolBar = self.CreateToolBar(0, -1)
        self.m_toolBar.SetToolSeparation(50)
        stepitem = self.m_toolBar.AddLabelTool(-1, '', self.m_art.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR), shortHelp = 'New file', longHelp = 'Step')
        self.m_toolBar.Realize()
        
        self.CreateStatusBar()
        self.GetStatusBar().SetFieldsCount(3)
        self.GetStatusBar().SetStatusWidths([64, 150, -1])

        # Bind events            
        self.Bind(wx.EVT_MENU, self.OnOpenFile, openitem)
        self.Bind(wx.EVT_TOOL, self.OnStep, stepitem)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnRClick, self.m_rnalist)
             
        self.Show()
            
    def OnOpenFile(self, event):
        dlg = wx.FileDialog(self, 'Open file', wildcard = 'RNA files (*.rna)|*.rna', style = wx.OPEN | wx.FILE_MUST_EXIST | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.m_filename = dlg.GetPath()
            self.SetTitle(TITLE_HEADER + self.m_filename)
            # TODO
            self.m_rna = rna2fuun.read(self.m_filename)
            self.m_commands = []
            for r in self.m_rna:
                if r in rna2fuun.commands:
                    self.m_commands.append(rna2fuun.commands[r])
                else:
                    self.m_commands.append("Unknown")
                
            self.m_rnalist.DeleteAllItems()
            self.m_rnalist.SetItemCount(len(self.m_commands))
            self.m_buildgen = self.m_r2f.buildgenerator(self.m_rna)
            self.m_row=0
            self.Update()
        dlg.Destroy()
        return
    
    def OnStep(self, event):
        self.m_buildgen.next()
        self.m_row += 1
        self.Update()
        
    def OnRClick(self, event):
        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, -1, "Run to here")
        menu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnRunToHere, item)
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        print "vzxvcvczxc"
        self.PopupMenu(menu)
        menu.Destroy()

    def OnRunToHere(self, event):
        item = self.m_rnalist.GetNextItem(-1,
                                     wx.LIST_NEXT_ALL,
                                     wx.LIST_STATE_SELECTED)
        if item == -1:
            return
        
        while self.m_row < item:
            self.m_buildgen.next()
            self.m_row += 1
        self.Update()
        
    def OnNext(self, event):
        self.m_buildgen.next()
        self.m_row += 1
        self.Update()
        
    def Update(self):
        self.m_rnalist.EnsureVisible(self.m_row)
        self.m_rnalist.SetItemState(self.m_row, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
        self.m_data.SetValue("position: %(position)s\ndir: %(dir)s\nbucket: %(bucket)s"%self.m_r2f.__dict__)
        try:
            self.m_image.SetBitmap(PILToBitmap(self.m_r2f.bitmaps[0][0]))
        except:
            pass
        

if __name__ == '__main__':
    app = wx.App(False)
    gui = RNA2FuunGui()
    gui.Center()
    app.MainLoop()