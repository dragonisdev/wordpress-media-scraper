# WordPress Media Scraper

A Python tool that scrapes all media content from WordPress pages, downloading videos, audio files, and images.

## Supported File Types

Video files:
- .mp4, .avi, .mov, .mkv, .webm

Audio files:
- .mp3, .wav, .flac, .m4a, .ogg

Image files:
- .png, .svg, .webp, .jpg, .jpeg

## Features

- Downloads videos using yt-dlp (converts to MP4)
- Scrapes direct media files from webpage HTML
- Extracts images from CSS background properties
- Automatically organizes files into video/, audio/, and image/ folders

## Dependencies

```bash
pip install yt-dlp requests beautifulsoup4
```

**Note:** yt-dlp requires FFmpeg for video processing and format conversion. Install FFmpeg on your system:
- Windows: Download from https://ffmpeg.org/ or use `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent for your distro

## Usage

1. Edit the `url` variable in the script to target your WordPress page
2. Run the script:
```bash
python scraper.py
```

The script will create three folders and download all found media files into the appropriate directories.

## How it works

- Uses yt-dlp to download embedded videos and convert them to MP4
- Parses HTML with BeautifulSoup to find direct media links
- Downloads files based on their extensions
- Handles both direct links and CSS background images