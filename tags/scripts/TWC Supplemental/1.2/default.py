"""
    This script displays radars and forecasts from www.weather.com
"""

#main imports
import sys
import os

# Script constants
__scriptname__ = "TWC Supplemental"
__author__ = "Nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/TWC%20Supplemental"
__credits__ = "Team XBMC"
__version__ = "1.2"
__svn_revision__ = 0

# Start the main gui
if ( __name__ == "__main__" ):
    import resources.lib.gui as gui
    ui = gui.GUI( "script-twc-main.xml", os.getcwd(), "Default" )
    ui.doModal()
    del ui
    sys.modules.clear()