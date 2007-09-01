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

chset = [10, 11, 12, 13, 14, 15,
         16, 26, 28, 29, 30, 31,
         32, 33, 43, 44, 45, 46, 47,
         57, 58, 59, 60, 61, 62, 63,
         65, 66, 67, 68, 69, 70, 71, 72, 73,
         81, 82, 83, 84, 85, 86, 87, 88, 89,
         98, 99, 100, 101, 102, 103, 104, 105,
         123,
         129, 130, 131, 132, 133, 134, 135, 136, 137,
         145, 146, 147, 148, 149, 150, 151, 152, 153,
         162, 163, 164, 165, 166, 167, 168, 169,
         176, 177, 178, 179, 180, 181, 182, 183, 184, 185]
         
ch = { 65 : 'a',
       66 : 'b',
       67 : 'c',
       68 : 'd',
       69 : 'e',
       70 : 'f',
       71 : 'g',
       72 : 'h',
       73 : 'i',
       81 : 'j',
       82 : 'k',
       83 : 'l',
       84 : 'm',
       85 : 'n',
       86 : 'o',
       87 : 'p',
       88 : 'q',
       89 : 'r',
       98 : 's',
       99 : 't',
      100 : 'u',
      101 : 'v',
      102 : 'w',
      103 : 'x',
      104 : 'y',
      105 : 'z',
      129 : 'A',
      130 : 'B',
      131 : 'C',
      132 : 'D',
      133 : 'E',
      134 : 'F',
      135 : 'G',
      136 : 'H',
      137 : 'I',
      145 : 'J',
      146 : 'K',
      147 : 'L',
      148 : 'M',
      149 : 'N',
      150 : 'O',
      151 : 'P',
      152 : 'Q',
      153 : 'R',
      162 : 'S',
      163 : 'T',
      164 : 'U',
      165 : 'V',
      166 : 'W',
      167 : 'X',
      168 : 'Y',
      169 : 'Z',
      176 : '0',
      177 : '1',
      178 : '2',
      179 : '3',
      180 : '4',
      181 : '5',
      182 : '6',
      183 : '7',
      184 : '8',
      185 : '9'}
         

class VirtualList(wx.ListCtrl):
    def __init__(self, parent, id=-1):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_VIRTUAL)

        self.setData([])

        self.InsertColumn(0, "ICFP")
        self.InsertColumn(1, "int")
        self.InsertColumn(2, "ascii")

    def setData(self, data):
        self.m_data = data
        self.SetItemCount(len(self.m_data))

    def OnGetItemText(self, item, col):
        return self.m_data[item][col]

def nat(dna, ix):
    try:
        dnastr = dna[ix]
        if (dnastr == 'P'):
            return 0, ix+1
        elif (dnastr == 'I') or (dnastr == 'F'):
            n, tmp = nat(dna, ix+1)
            return 2 * n, tmp
        elif (dnastr == 'C'):
            n, tmp = nat(dna, ix+1)
            return 2 * n + 1, tmp
    except IndexError:
        raise dna2rna_ref.NoMoreData

class DNADebuggerGui(wx.Frame):
    def __init__(self):
        self.m_dna = dnareflist.DNAList() 
        wx.Frame.__init__(self, None, -1, TITLE_HEADER, size=(1024,768))
        
        # Art provider.
        self.m_art = wx.ArtProvider()

        self.m_vsplitter = wx.SplitterWindow(self, -1)
        self.m_red = wx.TextCtrl(self.m_vsplitter, -1, style=wx.TE_MULTILINE|wx.TE_DONTWRAP)            
        self.m_blue = VirtualList(self.m_vsplitter, -1)
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
        dnalen = len(self.m_dna)
        
        ix = bpos+slen
        data = []
        try:
            while ix < dnalen:
                oldix = ix
                n, ix = nat(self.m_dna, ix)
                data.append((''.join(self.m_dna[oldix:min(ix,dnalen)]), str(n), ch.get(n, '')))
        except dna2rna_ref.NoMoreData:
            data.append((''.join(self.m_dna[oldix:min(ix,dnalen)]), "", ""))
            pass
        self.m_blue.setData(data)

if __name__ == '__main__':
    import psyco
    psyco.full()
    app = wx.App(False)
    gui = DNADebuggerGui()
    gui.Center()
    app.MainLoop()
