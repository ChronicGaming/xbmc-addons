
__scriptname__ = "NBA.com Videos"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/NBA.com%20Videos"
__date__ = '2009-04-01'
__version__ = "r878"

HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8'
import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback

def showRoot():
		li=xbmcgui.ListItem("Teams")
		u=sys.argv[0]+"?mode=5"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/video_whatsnew.txt"
		li3=xbmcgui.ListItem("What's New")
		u3=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
		url2="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_topplays.txt"
		li4=xbmcgui.ListItem("Top Plays")
		u4=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url2)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u4,li4,True)
		# li5=xbmcgui.ListItem("TNT OverTime")
		# u5=sys.argv[0]+"?mode=6"
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u5,li5,True)
		url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_nbatv.txt"
		li3=xbmcgui.ListItem("NBA TV")
		u3=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
		url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_tntovertime.txt"
		li3=xbmcgui.ListItem("TNT OverTime")
		u3=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)

def showTeams():
		li=xbmcgui.ListItem("Team Highlights")
		u=sys.argv[0]+"?mode=1"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li2=xbmcgui.ListItem("Team Originals")
		u2=sys.argv[0]+"?mode=4"
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u2,li2,True)

# def showTNT():
		# url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_tntovertime_topfiveofinside.txt"
		# li=xbmcgui.ListItem("Top 5 of Inside the NBA: #1")
		# u=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		# url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_tntovertime_reggiesmailbag.txt"
		# li=xbmcgui.ListItem("Reggie's Mailbag")
		# u=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		# url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_tntovertime_soundoff.txt"
		# li=xbmcgui.ListItem("TNT Soundoff")
		# u=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		# url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_tntovertime_insidethenba.txt"
		# li=xbmcgui.ListItem("Inside the NBA")
		# u=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		# url="http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/channels/video_channel_tntovertime_insiderreport.txt"
		# li=xbmcgui.ListItem("Insider Report with David Aldridge")
		# u=sys.argv[0]+"?mode=2&url="+urllib.quote_plus(url)
		# xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		
def showCategories():
		nba=['bos', 'njn', 'nyk', 'phi', 'tor', 'chi', 'cle', 'det', 'ind', 'mil', 'atl', 'cha', 'mia', 'orl', 'was', 'dal', 'hou', 'mem', 'noh', 'sas', 'den', 'min', 'por', 'okc', 'uth', 'gsw', 'lac', 'lal', 'pho', 'sac']
		teams=['Boston Celtics', 'New Jersey Nets', 'New York Knicks', 'Philadelphia 76ers', 'Toronto Raptors', 'Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks', 'Atlanta Hawks', 'Charlotte Bobcats', 'Miami Heat', 'Orlando Magic', 'Washington Wizards', 'Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Hornets', 'San Antonio Spurs','Denver Nuggets', 'Minnesota Timberwolves', 'Portland Trail Blazers', 'Oklahoma City Thunder', 'Utah Jazz', 'Golden State Warriors', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings' ]         
		x=0
		url="http://www.nba.com/rss/"
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('"http://www.nba.com/media/(.+?).gif"')
		match=p.findall(a)
		for thumb in match:
			url = 'http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/teams/video_nba_'+nba[x].upper()+'_tab1_page1.txt'
			name=teams[x]
			if (nba[x] == 'noh'):
				nba[x] = 'nor'
			thumb = 'http://assets.espn.go.com/i/teamlogos/nba/lrg/trans/'+nba[x]+'.gif'
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showCategories2():
		nba=['bos', 'njn', 'nyk', 'phi', 'tor', 'chi', 'cle', 'det', 'ind', 'mil', 'atl', 'cha', 'mia', 'orl', 'was', 'dal', 'hou', 'mem', 'noh', 'sas', 'den', 'min', 'por', 'okc', 'uth', 'gsw', 'lac', 'lal', 'pho', 'sac']
		teams=['Boston Celtics', 'New Jersey Nets', 'New York Knicks', 'Philadelphia 76ers', 'Toronto Raptors', 'Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks', 'Atlanta Hawks', 'Charlotte Bobcats', 'Miami Heat', 'Orlando Magic', 'Washington Wizards', 'Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Hornets', 'San Antonio Spurs','Denver Nuggets', 'Minnesota Timberwolves', 'Portland Trail Blazers', 'Oklahoma City Thunder', 'Utah Jazz', 'Golden State Warriors', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings' ]         
		x=0
		url="http://www.nba.com/rss/"
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('"http://www.nba.com/media/(.+?).gif"')
		match=p.findall(a)
		for thumb in match:
			url = 'http://www.nba.com/.element/ssi/auto/1.0/aps/video/videoplayer/teams/video_nba_'+nba[x].upper()+'_tab2_page1.txt'
			name=teams[x]
			if (nba[x] == 'noh'):
				nba[x] = 'nor'
			thumb = 'http://assets.espn.go.com/i/teamlogos/nba/lrg/trans/'+nba[x]+'.gif'
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
			x=x+1

def showList(url,page):
		thisurl=url
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<div class="nbaVideoImageWrapper"><img src="(.+?)"><span class="nbaSpanOverlay"></span></div></a><a href="javascript:changePlaylist(''(.+?)'');" class="nbaVideoGridContentHeader">(.+?)</a><div class="nbaVideoGridTextBlock">(.+?)</div>')
		URLS=p.findall(a)
		x=0
		for thumb, url, url2, name, info in URLS:
			print url
			name = str(int(x+1))+'. '+name
			url=url.replace('(','')
			url=url.replace(')','')
			remove = "'"
			url=url.replace(remove,'')
			url=url.replace('/video/','')
			url=url.replace('.json','')
			url = 'http://nba.cdn.turner.com/nba/big/' + url + '_nba_576x324.flv'
			print url
			print "+"
			li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
			li.setInfo( type="Video", infoLabels={ "Title": name+' - '+info } )
			u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
			x=x+1
			
def playVideo(url, name):
	def Download(url,dest):
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading','',url)
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
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name + '.flv'))
			Download(url,flv_file)
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select('What do you want to do?', ['Download & Play', 'Stream', 'Exit'])
		if (ret == 0):
			flv_file = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('download_Path'), name + '.flv'))
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

if mode==None:
	showRoot()
elif mode==1:
	showCategories()
elif mode==2:
	showList(url,page)
elif mode==3:
	playVideo(url, name)
elif mode==4:
	showCategories2()
elif mode==5:
	showTeams()
# elif mode==6:
	# showTNT()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
