
__scriptname__ = "Justin.tv"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Justin.tv"
__date__ = '2009-06-10'
__version__ = "r1046"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib2 import Request, urlopen, URLError, HTTPError
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10'
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')

def showCategories():
	if xbmcplugin.getSetting('language') == '0':
		idd = 'en'
		mode = '0'
	elif xbmcplugin.getSetting('language') == '1':
		idd = 'ar'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '2':
		idd = 'bg'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '3':
		idd = 'ca'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '4':
		idd = 'de'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '5':
		idd = 'el'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '6':
		idd = 'es'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '7':
		idd = 'fr'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '8':
		idd = 'hi'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '9':
		idd = 'hu'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '10':
		idd = 'id'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '11':
		idd = 'is'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '12':
		idd = 'it'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '13':
		idd = 'iw'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '14':
		idd = 'ja'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '15':
		idd = 'ko'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '16':
		idd = 'lt'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '17':
		idd = 'nl'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '18':
		idd = 'no'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '19':
		idd = 'pl'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '20':
		idd = 'pt'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '21':
		idd = 'ro'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '22':
		idd = 'ru'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '23':
		idd = 'sr'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '24':
		idd = 'tl'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '25':
		idd = 'tr'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '26':
		idd = 'uk'
		mode = '1'
	elif xbmcplugin.getSetting('language') == '27':
		idd = 'zh-TW'
		mode = '1'
	url='http://www.justin.tv/directory?order=hot&lang='+idd
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<div id="category_chooser">(.+?)<div class="section">', re.DOTALL).findall(a)
	cat=re.compile('<a href="(.+?)" class="category_link">(.+?)</a>').findall(match[0])
	#all=re.compile('<span class=\'not_linked\'>All</span> \n            (.+?)\n').findall(match[0])
	name = 'All '#+all[0]
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	for url,name in cat:
		url='http://www.justin.tv' + url
		li=xbmcgui.ListItem(name)
		u=sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('(Search)')
	u=sys.argv[0]+"?mode=3"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('(User Search)')
	u=sys.argv[0]+"?mode=5"
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showSubCategories(url, name):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<div id="subcategory_chooser">(.+?)<div id="category_chooser">', re.DOTALL).findall(a)
	cat=re.compile('<a href="(.+?)" class="category_link">(.+?)</a>').findall(match[0])
	name = 'All '
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	for url,name in cat:
		url='http://www.justin.tv' + url
		li=xbmcgui.ListItem(name)
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def showLinks(url, name):
	thisurl=url
	req = urllib2.Request(url+'&page='+str(int(page)))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	match=re.compile('<div class="grid_item_container"(.+?)<div id="pagelinks">', re.DOTALL).findall(a)
	if len(match) == 0:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Justin.tv', 'Error: No live streams available.')
		showCategories()
		return
	cat=re.compile('<h3 class="title"(.+?)<a href="(.+?)">(.*?)</a>', re.DOTALL).findall(match[0])
	data=re.compile('<a href="(.+?)"><img alt="" class="li_pic_125o i125x94 lateload" src1="(.+?)"').findall(a)
	stat1=re.compile('<em>Viewers</em>:&nbsp;<span>(.+?)</span><br />').findall(match[0])
	stat2=re.compile('<em>Views</em>:&nbsp;<span>(.+?)</span><br />').findall(match[0])
	stat3=re.compile('</a></h3>\n(.*?)</div>', re.DOTALL).findall(match[0])
	x=0
	for url,thumb in data:
		name=str(int(x+1)+(36*(page-1)))+'. '+cat[x][2]+': '+cleanStat(stat3[x])+' - Viewers: '+stat1[x]+' - Views: '+stat2[x]
		url=url.replace('/','')
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(data) >= 36:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def cleanStat(name):
    remove=[('\n',''),('                            ',''),('<p>',''),('</p>',''),('                    ','')]
    for trash, crap in remove:
        name=name.replace(trash,crap)
    return name
		
def runKeyboard():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Search")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	url = 'http://www.justin.tv/search?q='+newStr+'&commit=Search'
	runSearch(url)
		
def runSearch(url):
	thisurl=url
	req = urllib2.Request(url+'&page='+str(int(page)))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	title=re.compile('<a href="(.+?)" class="bold_results">(.+?)</a>\n            \n        </h3>').findall(a)
	thumbs=re.compile('class="li_pic_125o i125x94 lateload" src1="(.+?)" src').findall(a)
	info=re.compile('<p class="description bold_results">\n            (.*?)\n        </p>\n\n        <div class="stats">', re.DOTALL).findall(a)
	x=0
	for url, name in title:
		thumb=thumbs[x]
		name=str(int(x+1)+(10*(page-1)))+'. '+name+' - '+info[x]
		url=url.replace('/','')
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1
	if len(title) >= 10:	
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def runKeyboard2():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Enter the exact user name")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	li=xbmcgui.ListItem(newStr)
	u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(newStr)+"&url="+urllib.quote_plus(newStr)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			
def playVideo(url, name):
	vid='http://usher.justin.tv/find/live_user_' + url + '.xml'
	try:
		req = urllib2.Request(vid)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
	except HTTPError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Justin.tv', 'Error: Invalid user or not a live feed.')
		return
	a=f.read()
	f.close()
	data=re.compile('<play>(.+?)</play><connect>(.+?)</connect>').findall(a)
	playpath = data[0][0]
	rtmp_url = data[0][1]
	swf='http://www.justin.tv/meta/'+url+'.xml'
	req = urllib2.Request(swf)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data2=re.compile('SWFObject\(\'(.+?)\',').findall(a)
	data3=re.compile('<title>(.*?)</title>').findall(a)
	data4=re.compile('<status>(.*?)</status>').findall(a)
	referer = 'http://www.justin.tv/'
	SWFPlayer = data2[0] + '?referer=' + referer + '&userAgent=' + HEADER
	if len(data4) == 0:
		item = xbmcgui.ListItem(data3[0])
	else:
		item = xbmcgui.ListItem(data3[0]+': '+data4[0])
	item.setProperty("SWFPlayer", SWFPlayer)
	item.setProperty("PlayPath", playpath)
	item.setProperty("PageURL", referer)
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmp_url, item)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

params=get_params()
mode=None
name=None
url=None
page=1
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        page=int(params["page"])
except:
        pass

if mode==None:
	showCategories()
elif mode==0:
	showSubCategories(url, name)
elif mode==1:
	showLinks(url, name)
elif mode==2:
	playVideo(url, name)
elif mode==3:
	runKeyboard()
elif mode==4:
	runSearch(url)
elif mode==5:
	runKeyboard2()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	