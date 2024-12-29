import xbmcaddon
import xbmcgui
import xbmcvfs
import sys
import os

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')

# Add resources/lib to python path
sys.path.append(os.path.join(ADDON_PATH, 'resources', 'lib'))
from spotdl_handler import SpotDLHandler

def main():
    dialog = xbmcgui.Dialog()
    dialog.ok('SpotDL', 'Welcome to SpotDL Music Downloader!')
    
    # Initialize SpotDL handler
    handler = SpotDLHandler(ADDON)
    
    # Get Spotify URL from user
    spotify_url = dialog.input('Enter Spotify URL (track/album/playlist):')
    
    if spotify_url:
        # Check if the URL is a valid Spotify URL
        if 'spotify.com' not in spotify_url:
            dialog.notification('SpotDL', 'Invalid Spotify URL', 
                              xbmcgui.NOTIFICATION_ERROR, 3000)
            return
            
        # Start download process
        if handler.download(spotify_url):
            dialog.notification('SpotDL', 'Download started successfully', 
                              xbmcgui.NOTIFICATION_INFO, 3000)
        else:
            dialog.notification('SpotDL', 'Download failed', 
                              xbmcgui.NOTIFICATION_ERROR, 3000)
    else:
        dialog.notification('SpotDL', 'No URL provided', 
                          xbmcgui.NOTIFICATION_WARNING, 3000)

if __name__ == '__main__':
    main()