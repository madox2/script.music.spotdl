import xbmcaddon
import xbmcgui
import xbmcvfs
import xbmc
import sys
import os
import yaml

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')

# Add resources/lib to python path
sys.path.append(os.path.join(ADDON_PATH, 'resources', 'lib'))
from spotdl_handler import SpotDLHandler

def main():
    dialog = xbmcgui.Dialog()
    
    # Ask user if they want to download/sync
    if dialog.yesno('SpotDL', 'Download/synchronize playlists?'):
        # Initialize SpotDL handler
        handler = SpotDLHandler(ADDON)
        
        # Load and log config file content
        config_file = handler.config_file
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config_data = yaml.safe_load(f)
                    if not isinstance(config_data, dict) or 'directories' not in config_data:
                        raise ValueError("Config file must contain 'directories' key")
                    
                    directories = config_data['directories']
                    if not isinstance(directories, list):
                        raise ValueError("'directories' must be an array")
                    
                    parsed_dirs = []
                    for dir_entry in directories:
                        if not isinstance(dir_entry, dict) or 'name' not in dir_entry or 'query' not in dir_entry:
                            raise ValueError("Each directory entry must contain 'name' and 'query' keys")
                        parsed_dirs.append({
                            'name': dir_entry['name'],
                            'query': dir_entry['query']
                        })
                    
                    xbmc.log(f"SpotDL parsed directories:\n{parsed_dirs}", xbmc.LOGINFO)
                    handler.directories = parsed_dirs
                    
                    # Create directories in download folder
                    for dir_entry in parsed_dirs:
                        dir_path = os.path.join(handler.download_path, dir_entry['name'])
                        if not xbmcvfs.exists(dir_path):
                            xbmc.log(f"Creating directory: {dir_path}", xbmc.LOGINFO)
                            if not xbmcvfs.mkdirs(dir_path):
                                raise ValueError(f"Failed to create directory: {dir_path}")
                        else:
                            xbmc.log(f"Directory already exists: {dir_path}", xbmc.LOGINFO)
            except Exception as e:
                xbmc.log(f"SpotDL error reading config file: {str(e)}", xbmc.LOGERROR)
                dialog.notification('SpotDL', 'Error reading config file', 
                                  xbmcgui.NOTIFICATION_ERROR, 3000)
                return
        else:
            xbmc.log("SpotDL: No config file specified or file doesn't exist", xbmc.LOGWARNING)
            dialog.notification('SpotDL', 'No config file found', 
                              xbmcgui.NOTIFICATION_WARNING, 3000)
            return

if __name__ == '__main__':
    main()
