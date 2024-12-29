import xbmcgui
import xbmcvfs
import xbmc
import subprocess
import sys
import os

class SpotDLHandler:
    def __init__(self, settings):
        self.settings = settings
        self.download_path = settings.getSetting('download_path')
        self.config_file = settings.getSetting('config_file')
        self.directories = []
        
        # Debug log the paths
        xbmc.log(f"SpotDL download path: {self.download_path}", xbmc.LOGINFO)
        xbmc.log(f"SpotDL config file: {self.config_file}", xbmc.LOGINFO)
        
    def download(self):
        # It is assumed and intended that spotdl is already installed on the system
                
        dialog = xbmcgui.Dialog()
        try:
            for dir_entry in self.directories:
                dir_path = os.path.join(self.download_path, dir_entry['name'])
                query = dir_entry['query']
                
                xbmc.log(f"SpotDL: Starting download in {dir_path} with query: {query}", xbmc.LOGINFO)
                dialog.notification('SpotDL', f'Downloading to {dir_entry["name"]}...', 
                                  xbmcgui.NOTIFICATION_INFO, 2000)
                
                # Change to the directory and run spotdl
                os.chdir(dir_path)
                try:
                    result = subprocess.run(['/home/m/Desktop/spotdl-4.2.10-linux', 'download', query], 
                                 check=True, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True,
                                 encoding='utf-8',
                                 errors='replace')
                    # Log stdout if there's any output
                    if result.stdout:
                        xbmc.log(f"SpotDL stdout in {dir_path}:\n{result.stdout}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGINFO)
                    # Log stderr if there's any output (might contain progress info)
                    if result.stderr:
                        xbmc.log(f"SpotDL stderr in {dir_path}:\n{result.stderr}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGINFO)
                except subprocess.CalledProcessError as e:
                    # Log both stdout and stderr in case of error
                    if e.stdout:
                        xbmc.log(f"SpotDL stdout in {dir_path}:\n{e.stdout}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGERROR)
                    if e.stderr:
                        xbmc.log(f"SpotDL stderr in {dir_path}:\n{e.stderr}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGERROR)
                    dialog.notification('SpotDL', f'Error in {dir_entry["name"]}', 
                                      xbmcgui.NOTIFICATION_ERROR, 3000)
                    continue
                
                xbmc.log(f"SpotDL: Finished download in {dir_path}", xbmc.LOGINFO)
            
            return True
            
        except Exception as e:
            xbmc.log(f"SpotDL error: {str(e)}", xbmc.LOGERROR)
            dialog.notification('SpotDL', f'Download failed: {str(e)}', 
                              xbmcgui.NOTIFICATION_ERROR, 5000)
            return False
