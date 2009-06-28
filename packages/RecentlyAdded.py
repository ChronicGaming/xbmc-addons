import xbmc
from xbmcgui import Window
from urllib import quote_plus
import re
import sys


class Main:
    # grab the home window
    WINDOW = Window( 10000 )

    def _clear_properties( self ):
        # we enumerate thru and clear individual properties in case other scripts set window properties
        for count in range( self.LIMIT ):
            # movies
            self.WINDOW.clearProperty( "LatestMovie.%d.Title" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestMovie.%d.Year" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestMovie.%d.RunningTime" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestMovie.%d.PlayedTime" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestMovie.%d.Path" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestMovie.%d.Fanart" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestMovie.%d.Thumb" % ( count + 1, ) )
            # tv shows
            self.WINDOW.clearProperty( "LatestEpisode.%d.ShowTitle" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestEpisode.%d.EpisodeTitle" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestEpisode.%d.EpisodeNo" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestEpisode.%d.PlayedTime" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestEpisode.%d.Path" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestEpisode.%d.Fanart" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestEpisode.%d.Thumb" % ( count + 1, ) )
            # music
            self.WINDOW.clearProperty( "LatestSong.%d.Title" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestSong.%d.Year" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestSong.%d.Artist" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestSong.%d.Album" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestSong.%d.Path" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestSong.%d.Fanart" % ( count + 1, ) )
            self.WINDOW.clearProperty( "LatestSong.%d.Thumb" % ( count + 1, ) )

    def _normalize_path( self, path ):
        # we need to strip stack:// and return only the first path
        if ( path.startswith( "stack://" ) ):
            path = path[ 8 : ].split( " , " )[ 0 ]
        # strip username/password
        return re.sub( "//.+?@", "//", path )

    def _parse_argv( self ):
        try:
            # parse sys.argv for params
            params = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
        except:
            # no params passed
            params = {}
        # set the 
        self.LIMIT = int( params.get( "limit", "5" ) )
        self.RECENT = not params.get( "partial", "" ) == "True"
        self.ALBUMS = params.get( "albums", "" ) == "True"
        self.UNPLAYED = params.get( "unplayed", "" ) == "True"

    def __init__( self ):
        # parse argv for any preferences
        self._parse_argv()
        # clear properties
        self._clear_properties()
        # format our records start and end
        xbmc.executehttpapi( "SetResponseFormat(OpenRecord,%s)" % ( "<record>", ) )
        xbmc.executehttpapi( "SetResponseFormat(CloseRecord,%s)" % ( "</record>", ) )
        # fetch movie info
        self._fetch_movie_info()
        # fetch tvshow info
        self._fetch_tvshow_info()
        # fetch music info
        self._fetch_music_info()

    def _fetch_movie_info( self ):
        # set our unplayed query
        unplayed = ( "", "where playCount isnull ", )[ self.UNPLAYED ]
        # sql statement
        if ( self.RECENT ):
            # recently added
            sql_movies = "select * from movieview %sorder by idMovie desc limit %d" % ( unplayed, self.LIMIT, )
        else:
            # movies not finished
            sql_movies = "select movieview.*, bookmark.timeInSeconds from movieview join bookmark on (movieview.idFile = bookmark.idFile) %sorder by movieview.c00 limit %d" % ( unplayed, self.LIMIT, )
        # query the database
        movies_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_movies ), )
        # separate the records
        movies = re.findall( "<record>(.+?)</record>", movies_xml, re.DOTALL )
        # enumerate thru our records and set our properties
        for count, movie in enumerate( movies ):
            # separate individual fields
            fields = re.findall( "<field>(.*?)</field>", movie, re.DOTALL )
            # set title
            self.WINDOW.setProperty( "LatestMovie.%d.Title" % ( count + 1, ), fields[ 1 ] )
            # set year
            self.WINDOW.setProperty( "LatestMovie.%d.Year" % ( count + 1, ), fields[ 8 ] )
            # set running time
            self.WINDOW.setProperty( "LatestMovie.%d.RunningTime" % ( count + 1, ), fields[ 12 ] )
            # set played time (only valid for unfinished list)
            try:
                self.WINDOW.setProperty( "LatestMovie.%d.PlayedTime" % ( count + 1, ), fields[ 27 ] )
            except:
                self.WINDOW.clearProperty( "LatestMovie.%d.PlayedTime" % ( count + 1, ) )
            # set path
            self.WINDOW.setProperty( "LatestMovie.%d.Path" % ( count + 1, ), fields[ 24 ] + fields[ 23 ] )
            # set cached thumb name
            cache_name = xbmc.getCacheThumbName( self._normalize_path( fields[ 24 ] ) + fields[ 23 ] )
            # set fanart
            self.WINDOW.setProperty( "LatestMovie.%d.Fanart" % ( count + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( "Fanart", cache_name, ) )
            # set thumbnail
            self.WINDOW.setProperty( "LatestMovie.%d.Thumb" % ( count + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( cache_name[ 0 ], cache_name, ) )

    def _fetch_tvshow_info( self ):
        # set our unplayed query
        unplayed = ( "", "where playCount isnull ", )[ self.UNPLAYED ]
        # sql statement
        if ( self.RECENT ):
            # recently added
            sql_episodes = "select * from episodeview %sorder by idepisode desc limit %d" % ( unplayed, self.LIMIT, )
        else:
            # tv shows not finished
            sql_episodes = "select episodeview.*, bookmark.timeInSeconds from episodeview join bookmark on (episodeview.idFile = bookmark.idFile) %sorder by episodeview.strTitle limit %d" % ( unplayed, self.LIMIT, )
        # query the database
        episodes_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_episodes ), )
        # separate the records
        episodes = re.findall( "<record>(.+?)</record>", episodes_xml, re.DOTALL )
        # enumerate thru our records and set our properties
        for count, episode in enumerate( episodes ):
            # separate individual fields
            fields = re.findall( "<field>(.*?)</field>", episode, re.DOTALL )
            # set show title
            self.WINDOW.setProperty( "LatestEpisode.%d.ShowTitle" % ( count + 1, ), fields[ 27 ] )
            # set episode title
            self.WINDOW.setProperty( "LatestEpisode.%d.EpisodeTitle" % ( count + 1, ), fields[ 1 ] )
            # set season/episode
            self.WINDOW.setProperty( "LatestEpisode.%d.EpisodeNo" % ( count + 1, ), "s%02de%02d" % ( int( fields[ 13 ] ), int( fields[ 14 ] ), ) )
            # set played time (only valid for unfinished list)
            try:
                self.WINDOW.setProperty( "LatestEpisode.%d.PlayedTime" % ( count + 1, ), fields[ 31 ] )
            except:
                self.WINDOW.clearProperty( "LatestEpisode.%d.PlayedTime" % ( count + 1, ) )
            # set path
            self.WINDOW.setProperty( "LatestEpisode.%d.Path" % ( count + 1, ), fields[ 24 ] + fields[ 23 ] )
            # set cached thumb name
            cache_name = xbmc.getCacheThumbName( self._normalize_path( fields[ 24 ] ) + fields[ 23 ] )
            # set fanart
            self.WINDOW.setProperty( "LatestEpisode.%d.Fanart" % ( count + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( "Fanart", cache_name, ) )
            # set thumbnail
            self.WINDOW.setProperty( "LatestEpisode.%d.Thumb" % ( count + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( cache_name[ 0 ], cache_name, ) )

    def _fetch_music_info( self ):
        # sql statement
        if ( self.ALBUMS ):
            sql_music = "select idAlbum from albumview order by idAlbum desc limit %d" % ( self.LIMIT, )
            # query the database for recently added albums
            music_xml = xbmc.executehttpapi( "QueryMusicDatabase(%s)" % quote_plus( sql_music ), )
            # separate the records
            albums = re.findall( "<record>(.+?)</record>", music_xml, re.DOTALL )
            # set our unplayed query
            unplayed = ( "(idAlbum = %s)", "(idAlbum = %s and lastplayed isnull)", )[ self.UNPLAYED ]
            # sql statement
            sql_music = "select songview.* from songview where %s limit 1" % ( unplayed, )
            # clear our xml data
            music_xml = ""
            # enumerate thru albums and fetch info
            for album in albums:
                # query the database
                music_xml += xbmc.executehttpapi( "QueryMusicDatabase(%s)" % quote_plus( sql_music % ( album.replace( "<field>", "" ).replace( "</field>", "" ), ) ), )
        else:
            # set our unplayed query
            unplayed = ( "", "where lastplayed isnull ", )[ self.UNPLAYED ]
            # sql statement
            sql_music = "select songview.* from albumview join songview on (songview.idAlbum = albumview.idAlbum) %sorder by idSong desc limit %d" % ( unplayed, self.LIMIT, )
            # query the database
            music_xml = xbmc.executehttpapi( "QueryMusicDatabase(%s)" % quote_plus( sql_music ), )
        # separate the records
        items = re.findall( "<record>(.+?)</record>", music_xml, re.DOTALL )
        # enumerate thru our records and set our properties
        for count, item in enumerate( items ):
            # separate individual fields
            fields = re.findall( "<field>(.*?)</field>", item, re.DOTALL )
            # set title
            self.WINDOW.setProperty( "LatestSong.%d.Title" % ( count + 1, ), fields[ 3 ] )
            # set year
            self.WINDOW.setProperty( "LatestSong.%d.Year" % ( count + 1, ), fields[ 6 ] )
            # set artist
            self.WINDOW.setProperty( "LatestSong.%d.Artist" % ( count + 1, ), fields[ 24 ] )
            # set album
            self.WINDOW.setProperty( "LatestSong.%d.Album" % ( count + 1, ), fields[ 21 ] )
            # set path
            path = fields[ 22 ]
            # don't add song for albums list TODO: figure out how toplay albums
            ##if ( not self.ALBUMS ):
            path += fields[ 8 ]
            self.WINDOW.setProperty( "LatestSong.%d.Path" % ( count + 1, ), path )
            # set fanart
            cache_name = xbmc.getCacheThumbName( fields[ 24 ] )
            self.WINDOW.setProperty( "LatestSong.%d.Fanart" % ( count + 1, ), "special://profile/Thumbnails/Music/%s/%s" % ( "Fanart", cache_name, ) )
            # set thumbnail
            self.WINDOW.setProperty( "LatestSong.%d.Thumb" % ( count + 1, ), fields[ 27 ] )


if ( __name__ == "__main__" ):
    Main()
