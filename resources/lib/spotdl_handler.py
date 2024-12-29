import xbmcgui
import xbmcvfs
import subprocess
import sys
import os

class SpotDLHandler:
    def __init__(self, settings):
        self.settings = settings
        self.download_path = settings.getSetting('download_path')
        self.audio_format = settings.getSetting('audio_format')
        self.audio_quality = settings.getSetting('audio_quality')
        
    def check_spotdl_installation(self):
        """Check if spotDL is installed"""
        try:
            import spotdl
            return True
        except ImportError:
            return False
            
    def install_spotdl(self):
        """Install spotDL using pip"""
        dialog = xbmcgui.Dialog()
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'spotdl'])
            return True
        except subprocess.CalledProcessError:
            dialog.notification('SpotDL', 'Failed to install spotDL', 
                              xbmcgui.NOTIFICATION_ERROR, 5000)
            return False
            
    def download(self, url):
        """Download music from Spotify URL"""
        if not self.check_spotdl_installation():
            if not self.install_spotdl():
                return False
                
        dialog = xbmcgui.Dialog()
        try:
            # Ensure download directory exists
            if not xbmcvfs.exists(self.download_path):
                xbmcvfs.mkdirs(self.download_path)
            
            # TODO: Implement actual download using spotDL
            # This is a placeholder for now
            dialog.notification('SpotDL', 'Starting download...', 
                              xbmcgui.NOTIFICATION_INFO, 2000)
            
            return True
            
        except Exception as e:
            dialog.notification('SpotDL', f'Download failed: {str(e)}', 
                              xbmcgui.NOTIFICATION_ERROR, 5000)
            return False