import xbmcgui
import xbmcvfs
import xbmc
import subprocess
import sys
import os

INDEFINITE_TIME = 1000 * 60 * 60 # hour is big enough

class SpotDLHandler:
    def __init__(self, settings):
        self.settings = settings
        self.download_path = settings.getSetting('download_path')
        self.config_file = settings.getSetting('config_file')
        self.spotdl_url = settings.getSetting('spotdl_url')
        self.directories = []
        binary_name = os.path.basename(self.spotdl_url)
        temp_dir = xbmcvfs.translatePath('special://temp')
        self.binary_path = os.path.join(temp_dir, binary_name)

        xbmc.log(f"SpotDL temp directory: {temp_dir}", xbmc.LOGINFO)
        xbmc.log(f"SpotDL binary path: {self.binary_path}", xbmc.LOGINFO)
        
        # Debug log the paths
        xbmc.log(f"SpotDL download path: {self.download_path}", xbmc.LOGINFO)
        xbmc.log(f"SpotDL config file: {self.config_file}", xbmc.LOGINFO)
        xbmc.log(f"SpotDL binary URL: {self.spotdl_url}", xbmc.LOGINFO)

    def install_spotdl(self):
        dialog = xbmcgui.Dialog()
        # Get the binary name from the URL
        binary_path = self.binary_path

        # Download the binary if it doesn't exist
        if not os.path.exists(binary_path):
            xbmc.log(f"Downloading SpotDL binary from {self.spotdl_url}", xbmc.LOGINFO)
            import requests
            try:
                dialog.notification('SpotDL', 'Downloading SpotDL binary...', 
                                  xbmcgui.NOTIFICATION_INFO, INDEFINITE_TIME)
                
                response = requests.get(self.spotdl_url)
                response.raise_for_status()
                
                with open(binary_path, 'wb') as f:
                    f.write(response.content)
                os.chmod(binary_path, 0o755)  # Make executable
                xbmc.log(f"Successfully downloaded and made executable: {binary_path}", xbmc.LOGINFO)
                
                # Download ffmpeg if enabled in settings
                if self.settings.getSettingBool('install_ffmpeg'):
                    dialog.notification('SpotDL', 'Downloading ffmpeg...', 
                                      xbmcgui.NOTIFICATION_INFO, INDEFINITE_TIME)
                    try:
                        result = subprocess.run([binary_path, '--download-ffmpeg'],
                                             check=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             text=True,
                                             encoding='utf-8',
                                             errors='replace')
                        if result.stdout:
                            xbmc.log(f"FFmpeg download stdout:\n{result.stdout}", xbmc.LOGINFO)
                        if result.stderr:
                            xbmc.log(f"FFmpeg download stderr:\n{result.stderr}", xbmc.LOGINFO)
                        xbmc.log("Successfully downloaded ffmpeg", xbmc.LOGINFO)
                        dialog.notification('SpotDL', 'FFmpeg successfully downloaded', 
                                          xbmcgui.NOTIFICATION_INFO, 2000)
                    except subprocess.CalledProcessError as e:
                        error_msg = f"Failed to download ffmpeg: {str(e)}"
                        if e.stdout:
                            xbmc.log(f"FFmpeg download stdout:\n{e.stdout}", xbmc.LOGERROR)
                        if e.stderr:
                            xbmc.log(f"FFmpeg download stderr:\n{e.stderr}", xbmc.LOGERROR)
                        raise ValueError(error_msg)
                else:
                    xbmc.log("FFmpeg installation skipped (disabled in settings)", xbmc.LOGINFO)

                dialog.notification('SpotDL', 'Setup completed successfully', 
                                  xbmcgui.NOTIFICATION_INFO, 2000)
            except requests.exceptions.RequestException as e:
                error_msg = f"Failed to download SpotDL binary: {str(e)}"
                xbmc.log(error_msg, xbmc.LOGERROR)
                if os.path.exists(binary_path):
                    os.remove(binary_path)
                raise ValueError(error_msg)

        # Verify binary exists and is executable
        if not os.path.exists(binary_path):
            raise ValueError(f"SpotDL binary not found at: {binary_path}")
        if not os.access(binary_path, os.X_OK):
            raise ValueError(f"SpotDL binary is not executable: {binary_path}")

    def download(self):
        dialog = xbmcgui.Dialog()
        try:
            # Verify download path is set
            if not self.download_path:
                raise ValueError("Download path is not set in settings")
            xbmc.log(f"Using download path: {self.download_path}", xbmc.LOGINFO)
            
            # Verify we have directories to process
            if not self.directories:
                raise ValueError("No directories configured in config file")

            self.install_spotdl()

            total_dirs = len(self.directories)
            # Initialize counters for the summary
            total_downloaded = 0
            total_skipped = 0
            total_failed = 0
            
            for index, dir_entry in enumerate(self.directories, 1):
                dir_path = os.path.join(self.download_path, dir_entry['name'])
                queries = dir_entry['queries']
                total_queries = len(queries)
                
                xbmc.log(f"SpotDL: Processing directory {dir_path} with {total_queries} queries", xbmc.LOGINFO)
                
                # Change to the directory for all queries
                os.chdir(dir_path)
                
                for query_index, query in enumerate(queries, 1):
                    xbmc.log(f"SpotDL: Starting query {query_index}/{total_queries}: {query}", xbmc.LOGINFO)
                    dialog.notification('SpotDL', 
                                     f'Downloading {index}/{total_dirs}: {dir_entry["name"]}', 
                                     xbmcgui.NOTIFICATION_INFO, INDEFINITE_TIME)
                    
                    try:
                        result = subprocess.run([self.binary_path, 'download', query], 
                                         check=True, 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE,
                                         text=True,
                                         encoding='utf-8',
                                         errors='replace')
                        # Log stdout if there's any output
                        if result.stdout:
                            stdout = result.stdout.encode('utf-8', 'replace').decode('utf-8')
                            xbmc.log(f"SpotDL stdout for {query}:\n{stdout}", xbmc.LOGINFO)
                            # Count results
                            total_downloaded += stdout.count("Downloaded")
                            total_skipped += stdout.count("Skipping")
                            total_failed += stdout.count("Failed")
                        # Log stderr if there's any output (might contain progress info)
                        if result.stderr:
                            xbmc.log(f"SpotDL stderr for {query}:\n{result.stderr}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGINFO)
                            
                        xbmc.log(f"SpotDL: Finished query {query_index}/{total_queries}", xbmc.LOGINFO)
                    except subprocess.CalledProcessError as e:
                        # Log both stdout and stderr in case of error
                        if e.stdout:
                            xbmc.log(f"SpotDL stdout for {query}:\n{e.stdout}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGERROR)
                        if e.stderr:
                            xbmc.log(f"SpotDL stderr for {query}:\n{e.stderr}".encode('utf-8', 'replace').decode('utf-8'), xbmc.LOGERROR)
                        dialog.notification('SpotDL', f'Error in query {query_index}/{total_queries}', 
                                         xbmcgui.NOTIFICATION_ERROR, 3000)
                        continue
                
                xbmc.log(f"SpotDL: Finished all queries in {dir_path}", xbmc.LOGINFO)
            
            # Log the final summary
            summary = f"(d: {total_downloaded}, s: {total_skipped}, f: {total_failed})"
            xbmc.log(f"SpotDL download summary: {summary}", xbmc.LOGINFO)
            
            # Show summary notification
            dialog.notification('SpotDL', f'Download completed {summary}', 
                              xbmcgui.NOTIFICATION_INFO, 5000)
            return True
            
        except Exception as e:
            xbmc.log(f"SpotDL error: {str(e)}", xbmc.LOGERROR)
            dialog.notification('SpotDL', f'Download failed: {str(e)}', 
                              xbmcgui.NOTIFICATION_ERROR, 5000)
            return False
