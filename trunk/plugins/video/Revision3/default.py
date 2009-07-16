
__scriptname__ = "Revision3"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Revision3"
__date__ = '15-07-2009'
__version__ = "1.0"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback

def showCategoriesA():
		quality=xbmcplugin.getSetting('quality')
		quality=xbmc.getLocalizedString(30000+5+int(quality))
		url='http://revision3.com/shows/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<ul id="shows">(.+?)<div id="footer" class="clear">', re.DOTALL)
		match=p.findall(a)
		o=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>')
		data=o.findall(match[0])
		q=re.compile('class="thumbnail"><img src="(.+?)" /></a>')
		thumb=q.findall(match[0])
		x=0
		for url, name in data:
			url='http://revision3.com' + url + '/feed/' + quality
			li=xbmcgui.ListItem(name, iconImage=thumb[x], thumbnailImage=thumb[x])
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showListA(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<item>(.+?)<title>(.+?)</title>', re.DOTALL)
		o=re.compile('<enclosure url="(.+?)"')
		q=re.compile('<media:thumbnail url="(.+?)"')
		r=re.compile('<guid isPermaLink="false">(.+?)</guid>')
		time=r.findall(a)
		match=p.findall(a)
		URLS=o.findall(a)
		thumbs=q.findall(a)
		x=0
		for title in match:
			name = match[x][1]
			date=time[x]
			date=date.rsplit('/', 2)
			date=date[1]
			date=date.lstrip('0')
			name='Episode '+date+' - '+name
			name = str(int(x+1))+'. '+name
			url=URLS[x]
			print url
			thumb=thumbs[x]
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
			
def playVideoA(url, name):
	date=url
	date=date.replace('/tzdaily','')
	date=date.rsplit('/')
	name=date[10]
	def Download(url,dest):
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading','',name)
			urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
	def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
			try:
					percent = min((numblocks*blocksize*100)/filesize, 100)
					dp.update(percent)
			except:
					percent = 100
					dp.update(percent)
			if dp.iscanceled():
					dp.close()
	flv_file = None
	stream = 'false'
	if (xbmcplugin.getSetting('download') == 'true'):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
			Download(url,flv_file)
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
		if (ret == 0):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
			Download(url,flv_file)
		elif (ret == 1):
			stream = 'true'
		else:
			pass
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'false'):
		stream = 'true'
	if xbmcplugin.getSetting("dvdplayer") == "true":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
	else:
		player_type = xbmc.PLAYER_CORE_MPLAYER
	if (flv_file != None and os.path.isfile(flv_file)):
		xbmc.Player(player_type).play(str(flv_file))
	elif (stream == 'true'):
		xbmc.Player(player_type).play(str(url))
	xbmc.sleep(200)

def showCategories():
		url='http://revision3.com/shows/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<ul id="shows">(.+?)<div id="footer" class="clear">', re.DOTALL)
		match=p.findall(a)
		o=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>')
		data=o.findall(match[0])
		q=re.compile('class="thumbnail"><img src="(.+?)" /></a>')
		thumb=q.findall(match[0])
		x=0
		for url, name in data:
			url='http://revision3.com' + url
			li=xbmcgui.ListItem(name, iconImage=thumb[x], thumbnailImage=thumb[x])
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def newShow(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile(': <a href="(.+?)">(.+?)</a></h1>')
		data=p.findall(a)
		q=re.compile('<img src="(.+?)" width="300"')
		thumbs=q.findall(a)
		x=0
		for url, name in data:
			url='http://revision3.com'+url
			thumb=thumbs[x]
			name = str(int(x+1))+'. '+name
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			
def showList(url):
		newShow(url)
		url=url+'/episodes'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5')
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<!-- <span class="label">Page: </span> -->(.+?)<!-- <span class="label">Page: </span> -->', re.DOTALL)
		match=p.findall(a)
		o=re.compile('<a class="thumbnail" href="(.+?)"><img class="thumbnail" src="(.+?)"')
		data=o.findall(match[0])
		q=re.compile('Episode (.+?)<br />  (.+?)</a></p>')
		data2=q.findall(match[0])
		x=1
		y=0
		for url, thumb in data:
			url='http://revision3.com'+url
			print url
			name = 'Episode ' + data2[y][0] + ': ' + data2[y][1]
			name = str(int(x))+'. '+name
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name } )
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			#uncomment below to limit the amount of eps per show to 25
			# if (x == 24):
				# break
			x=x+1
			y=y+1

def showList2(url):
	quality=xbmcplugin.getSetting('quality')
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5')
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	p=re.compile('<div id="episode-sidebar-download">(.+?)<div id="episode-sidebar-subscribe"', re.DOTALL)
	n=re.compile('<a href="(.+?)">')
	match1=p.findall(a)
	match=n.findall(match1[0])
	if len(match) == 8:
		quality=int(quality)+1
	else:
		quality=int(quality)
	url=match[quality]
	date=url
	date=date.replace('/tzdaily','')
	date=date.rsplit('/')
	name=date[10]
	def Download(url,dest):
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading','',name)
			urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
	def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
			try:
					percent = min((numblocks*blocksize*100)/filesize, 100)
					dp.update(percent)
			except:
					percent = 100
					dp.update(percent)
			if dp.iscanceled():
					dp.close()
	flv_file = None
	stream = 'false'
	if (xbmcplugin.getSetting('download') == 'true'):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
			Download(url,flv_file)
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
		if (ret == 0):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name))
			Download(url,flv_file)
		elif (ret == 1):
			stream = 'true'
		else:
			pass
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'false'):
		stream = 'true'
	if xbmcplugin.getSetting("dvdplayer") == "true":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
	else:
		player_type = xbmc.PLAYER_CORE_MPLAYER
	if (flv_file != None and os.path.isfile(flv_file)):
		xbmc.Player(player_type).play(str(flv_file))
	elif (stream == 'true'):
		xbmc.Player(player_type).play(str(url))
	xbmc.sleep(200)

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
		
if mode==None and xbmcplugin.getSetting("episodes") == "false":
	showCategoriesA()
elif mode==1 and xbmcplugin.getSetting("episodes") == "false":
	showListA(url)
elif mode==2 and xbmcplugin.getSetting("episodes") == "false":
	playVideoA(url, name)
if mode==None and xbmcplugin.getSetting("episodes") == "true":
	showCategories()
elif mode==1 and xbmcplugin.getSetting("episodes") == "true":
	showList(url)
elif mode==2 and xbmcplugin.getSetting("episodes") == "true":
	showList2(url)

xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
