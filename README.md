# SpotDL (Spotify) Kodi Addon

A Kodi plugin that uses [spotdl](https://github.com/spotDL/spotify-downloader) library to download music from Spotify. Download songs, playlists, and entire artist discographies directly through Kodi.

Made with [OpenHands](https://github.com/All-Hands-AI/OpenHands).

## Installation
1. Download the latest release zip file from the [Releases](https://github.com/madox2/script.music.spotdl/releases) page
2. In Kodi, go to Add-ons > Install from zip file
3. Navigate to the downloaded zip file and select it
4. The plugin will install automatically

## Configuration
1. Go to Add-ons > My Add-ons > Music Add-ons > SpotDL
2. Select Configure
3. Set your preferred download location:
```
Download Path: /path/to/your/music
Config file (.yaml): /path/to/your/playlists.yaml
```

Config example:

```yaml
playlists:
  - name: "My Favorite Songs"
    queries:
      - "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID"
      - "https://open.spotify.com/track/YOUR_TRACK_ID"
  - name: "Rock Collection"
    queries:
      - "https://open.spotify.com/album/YOUR_ALBUM_ID"
```

## Requirements
- Kodi 19 or higher
- Internet connection
- Sufficient storage space for downloads

## Development

### Creating a New Release

To create a new release:

1. Update the version number in `addon.xml`
2. Create and push a new tag:
   ```bash
   git tag v1.0.0  # Use appropriate version number
   git push origin v1.0.0
