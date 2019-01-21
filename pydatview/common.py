import numpy as np
import os
import platform

# --------------------------------------------------------------------------------}
# --- ellude
# --------------------------------------------------------------------------------{
def common_start(*strings):
    """ Returns the longest common substring
        from the beginning of the `strings`
    """
    if len(strings)==1:
        strings=tuple(strings[0])
    def _iter():
        for z in zip(*strings):
            if z.count(z[0]) == len(z):  # check all elements in `z` are the same
                yield z[0]
            else:
                return
    return ''.join(_iter())

def common_end(*strings):
    if len(strings)==1:
        strings=strings[0]
    else:
        strings=list(strings)
    strings = [s[-1::-1] for s in strings]
    return common_start(strings)[-1::-1]


def ellude_common(strings):
    # Selecting only the strings that do not start with the safe '>' char
    S = [s for i,s in enumerate(strings) if ((len(s)>0) and (s[0]!= '>'))]
    if len(S)==1:
        ns=S[0].rfind('|')+1
        ne=0;
    else:
        ss = common_start(S)
        se = common_end(S)
        iu = ss[:-1].rfind('_')
        ip = ss[:-1].rfind('_')
        if iu > 0:
            if ip>0:
                if iu>ip:
                    ss=ss[:iu+1]
            else:
                ss=ss[:iu+1]

        iu = se[:-1].find('_')
        if iu > 0:
            se=se[iu:]
        iu = se[:-1].find('.')
        if iu > 0:
            se=se[iu:]
        ns=len(ss)     
        ne=len(se)     

    for i,s in enumerate(strings):
        if len(s)>0 and s[0]=='>':
            strings[i]=s[1:]
        else:
            s=s[ns:]
            if ne>0:
                s = s[:-ne]
            strings[i]=s.lstrip('_')
            if len(strings[i])==0:
                strings[i]='tab{}'.format(i)
    return strings


# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def getMonoFontAbs():
    import wx
    #return wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')
    if os.name=='nt':
        font=wx.Font(9, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
    elif os.name=='posix':
        font=wx.Font(10, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
    else:
        font=wx.Font(8, wx.TELETYPE, wx.NORMAL, wx.NORMAL, False)
    return font

def getMonoFont(widget):
    import wx
    font = widget.GetFont()
    font.SetFamily(wx.TELETYPE)
    if platform.system()=='Windows':
        pass
    elif platform.system()=='Linux':
        pass
    elif platform.system()=='Darwin':
        font.SetPointSize(font.GetPointSize()-1)
    else:
        pass
    return font



def getColumn(df,i):
    import wx
    if i == wx.NOT_FOUND or i == 0:
        x = np.array(range(df.shape[0]))
        c = None
        isString = False
        isDate   = False
    else:
        c = df.iloc[:, i-1]
        x = df.iloc[:, i-1].values
        isString = c.dtype == np.object and isinstance(c.values[0], str)
        if isString:
            x=x.astype(str)
        isDate   = np.issubdtype(c.dtype, np.datetime64)
        if isDate:
            x=x.astype('datetime64[s]')

    return x,isString,isDate,c



def no_unit(s):
    iu=s.rfind(' [')
    if iu>1:
        return s[:iu]
    else:
        return s

def unit(s):
    iu=s.rfind('[')
    if iu>1:
        return s[iu+1:].replace(']','')
    else:
        return ''

def inverse_unit(s):
    u=unit(s).strip()
    if u=='':
        return ''
    elif u=='-':
        return '-'
    elif len(u)==1:
        return '1/'+u;
    elif u=='m/s':
        return 's/m';
    elif u=='deg':
        return '1/deg';
    else:
        return '1/('+u+')'


# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def pretty_time(t):
    # fPrettyTime: returns a 6-characters string corresponding to the input time in seconds.
    #   fPrettyTime(612)=='10m12s'
    # AUTHOR: E. Branlard
    if(t<0):
        s='------';
    elif (t<1) :
        c=np.floor(t*100);
        s='{:2d}.{:02d}s'.format(0,int(c))
    elif(t<60) :
        s=np.floor(t);
        c=np.floor((t-s)*100);
        s='{:2d}.{:02d}s'.format(int(s),int(c))
    elif(t<3600) :
        m=np.floor(t/60);
        s=np.mod( np.floor(t), 60);
        s='{:2d}m{:02d}s'.format(int(m),int(s))
    elif(t<86400) :
        h=np.floor(t/3600);
        m=np.floor(( np.mod( np.floor(t) , 3600))/60);
        s='{:2d}h{:02d}m'.format(int(h),int(m))
    elif(t<8553600) : #below 3month
        d=np.floor(t/86400);
        h=np.floor( np.mod(np.floor(t), 86400)/3600);
        s='{:2d}d{:02d}h'.format(int(d),int(h))
    elif(t<31536000):
        m=t/(3600*24*30.5);
        s='{:4.1f}mo'.format(m)
        #s='+3mon.';
    else:
        y=t/(3600*24*365.25);
        s='{:.1f}y'.format(y)
    return s

def pretty_num(x):
    if abs(x)<1000 and abs(x)>1e-4:
        return "{:9.4f}".format(x)
    else:
        return '{:.3e}'.format(x)



# --------------------------------------------------------------------------------}
# --- Helper functions
# --------------------------------------------------------------------------------{
def YesNo(parent, question, caption = 'Yes or no?'):
    import wx
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result
def Info(parent, message, caption = 'Info'):
    import wx
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
def Warn(parent, message, caption = 'Warning!'):
    import wx
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()
def Error(parent, message, caption = 'Error!'):
    import wx
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()



# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def yMean(pd):
    if pd.yIsString or  pd.yIsDate:
        return None,'NA'
    else:
        v=np.nanmean(pd.y)
        s=pretty_num(v)
    return (v,s)

def yStd(pd):
    if pd.yIsString or  pd.yIsDate:
        return None,'NA'
    else:
        v=np.nanstd(pd.y)
        s=pretty_num(v)
    return (v,s)

def yMin(pd):
    if pd.yIsString:
        return pd.y[0],pd.y[0].strip()
    elif pd.yIsDate:
        return pd.y[0],'{}'.format(pd.y[0])
    else:
        v=np.nanmin(pd.y)
        s=pretty_num(v)
    return (v,s)

def yMax(pd):
    if pd.yIsString:
        return pd.y[-1],pd.y[-1].strip()
    elif pd.yIsDate:
        return pd.y[-1],'{}'.format(pd.y[-1])
    else:
        v=np.nanmax(pd.y)
        s=pretty_num(v)
    return (v,s)
