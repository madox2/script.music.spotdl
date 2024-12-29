# SpotDL Kodi Addon

A Kodi addon that integrates spotDL functionality to download music from Spotify. This addon allows you to download tracks, albums, and playlists directly from Spotify to your Kodi media center.

## Features

- Download tracks, albums, and playlists from Spotify
- Configurable download directory
- Multiple audio format support (mp3, flac, wav, m4a)
- Adjustable audio quality settings
- Automatic metadata tagging
- Album artwork download

## Requirements

- Kodi 19 (Matrix) or higher
- Python 3.8+
- Internet connection

## Development Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/script.music.spotdl.git
cd script.music.spotdl
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a symlink to your Kodi addons directory:
```bash
# Linux/macOS
ln -s "$(pwd)" ~/.kodi/addons/script.music.spotdl

# Windows (PowerShell, run as Administrator)
New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Kodi\addons\script.music.spotdl" -Target "$(pwd)"
```

## Installation for Users

1. Download the latest release zip file
2. In Kodi, go to Add-ons > Install from zip file
3. Select the downloaded zip file
4. The addon will be installed and available in your Programs section

## Usage

1. Launch the addon from Programs section in Kodi
2. Enter a Spotify URL (track, album, or playlist)
3. Configure settings as needed:
   - Download Directory
   - Audio Format (mp3, flac, wav, m4a)
   - Audio Quality
4. Start downloading

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License

## Acknowledgments

- [spotDL](https://github.com/spotDL/spotify-downloader) - The core downloading functionality
- [Kodi Team](https://kodi.tv/) - For the amazing media center