import yt_dlp
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# Create directories for the media types you want to scrape
for folder in ["video", "audio", "image"]:
    os.makedirs(folder, exist_ok=True)

# the wordpress site url you want to scrape
url = "https://dnbacademy.net/jon-tho-producer-bundle/"



def scrape_media(page_url):
    """Scrape images, audio, and video files from webpage"""
    try:
        response = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        urls = set()

        # Extract URLs from elements
        elements = soup.find_all(['img', 'source', 'picture', 'a', 'audio', 'video'])
        for element in elements:
            for attr in ['src', 'href', 'srcset', 'data-src', 'data-srcset']:
                if element.get(attr):
                    if 'srcset' in attr:
                        urls.update(u.strip().split()[0] for u in element[attr].split(','))
                    else:
                        urls.add(element[attr])

        # Extract CSS background images
        for element in soup.find_all(style=True):
            css_urls = re.findall(r'url\(["\']?([^"\')]*)["\']?\)', element['style'])
            urls.update(css_urls)

        # Download files
        for url in urls:
            try:
                full_url = urljoin(page_url, url)
                parsed = urlparse(full_url)
                filename = os.path.basename(parsed.path)

                if not filename or '.' not in filename:
                    continue

                ext = os.path.splitext(filename)[1].lower()

                # Determine folder based on extension
                if ext in ['.png', '.svg', '.webp', '.jpg', '.jpeg']:
                    folder = "image"
                elif ext in ['.mp3', '.wav', '.flac', '.m4a']:
                    folder = "audio"
                elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
                    folder = "video"
                else:
                    continue

                filepath = os.path.join(folder, filename)

                if not os.path.exists(filepath):
                    file_response = requests.get(full_url, stream=True)
                    file_response.raise_for_status()

                    with open(filepath, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded: {filename} to {folder}/")

            except Exception as e:
                print(f"Error downloading {url}: {e}")

    except Exception as e:
        print(f"Error scraping page: {e}")

# Download with yt-dlp
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': {
        'default': 'video/%(title)s.%(ext)s',
        'thumbnail': 'image/%(title)s.%(ext)s',
    },
    'merge_output_format': 'mp4',
    'writethumbnail': False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
except Exception as e:
    print(f"yt-dlp error: {e}")

# Scrape all media files
scrape_media(url)