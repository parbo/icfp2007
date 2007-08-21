import wx
import wx.lib.scrolledpanel as scrolled
import dna2rna_ref
import dnareflist
        
# Tool/menu IDs        
ID_OPEN_FILE  = 102

# Code dialog button IDs
#ID_DLG_SAVE_CMD         = 1003

# Editor title
TITLE_HEADER = 'DNA debugger'

class DNADebuggerGui(wx.Frame):
    def __init__(self):
        self.m_dna = dnareflist.DNAList() 
        wx.Frame.__init__(self, None, -1, TITLE_HEADER, size=(1024,768))
        
        # Art provider.
        self.m_art = wx.ArtProvider()

        self.m_vsplitter = wx.SplitterWindow(self, -1)
        self.m_red = wx.TextCtrl(self.m_vsplitter, -1, style=wx.TE_MULTILINE|wx.TE_DONTWRAP)            
        self.m_blue = wx.TextCtrl(self.m_vsplitter, -1, style=wx.TE_MULTILINE|wx.TE_DONTWRAP)            
        self.m_vsplitter.SplitVertically(self.m_red, self.m_blue, 100)
        
        menubar = wx.MenuBar()

        file = wx.Menu()

        openitem = file.Append(-1, '&Open DNA\tCtrl+O', 'Open DNA File')
        
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        
        self.m_toolBar = self.CreateToolBar(0, -1)
        self.m_toolBar.SetToolSeparation(50)
        stepitem = self.m_toolBar.AddLabelTool(-1, '', self.m_art.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR), shortHelp = 'Single step', longHelp = 'Single step in RNA commands')
        self.m_toolBar.Realize()
        
        self.CreateStatusBar()
        self.GetStatusBar().SetFieldsCount(3)
        self.GetStatusBar().SetStatusWidths([64, 150, -1])

        # Bind events            
        self.Bind(wx.EVT_MENU, self.OnOpenFile, openitem)
        self.Bind(wx.EVT_TOOL, self.OnStep, stepitem)
             
        self.Show()
            
    def OnOpenFile(self, event):
        dlg = wx.FileDialog(self, 'Open DNA file', wildcard = 'DNA files (*.dna)|*.dna', style = wx.OPEN | wx.FILE_MUST_EXIST | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            dlg2 = wx.FileDialog(self, 'Open DNA prefix file', wildcard = 'DNA files (*.dna)|*.dna', style = wx.OPEN | wx.FILE_MUST_EXIST | wx.CHANGE_DIR)
            prefixfilename = ""
            prefix = ""
            if dlg2.ShowModal() == wx.ID_OK:
                 prefixfilename = dlg2.GetPath()
                 prefixfile = file(prefixfilename, 'r')
                 prefix = prefixfile.read()
                 prefixfile.close()
            self.SetTitle(TITLE_HEADER + filename + prefixfilename)
            dnafile = file(filename, 'r')
            dnastr = prefix + dnafile.read()
            self.m_dna = dnareflist.DNAList()
            self.m_dna.insertfront([dnareflist.DNARef(0, len(dnastr), list(dnastr))])
            self.m_rna = []
            dnafile.close()
            self.Update()
            dlg2.Destroy()
        dlg.Destroy()
    
    def OnStep(self, event):
        try:
            p = dna2rna_ref.pattern(self.m_dna, self.m_rna)
            t = dna2rna_ref.template(self.m_dna, self.m_rna)
            dna2rna_ref.matchreplace(self.m_dna, p, t)
        except dna2rna_ref.NoMoreData:
            pass
            
        self.Update()
        
    def Update(self):
        sstr = "IFPICFPPCFIPP" 
        slen = len(sstr)
        bpos = self.m_dna.find(sstr, 0) 
        print bpos
        dnalen = len(self.m_dna)
        print dnalen
        self.m_blue.SetValue(''.join(self.m_dna[bpos+slen:dnalen]))

if __name__ == '__main__':
    import psyco
    psyco.full()
    app = wx.App(False)
    gui = DNADebuggerGui()
    gui.Center()
    app.MainLoop()
