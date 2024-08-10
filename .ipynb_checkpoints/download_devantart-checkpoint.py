import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_image(image_url, save_dir):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_name = image_url.split('/')[-1]
            with open(os.path.join(save_dir, image_name), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {image_name}")
        else:
            print(f"Failed to download image: {image_url}")
    except Exception as e:
        print(f"An error occurred while downloading {image_url}: {e}")

def crawl_deviantart(url, save_dir):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    create_directory(save_dir)

    # Find all image tags with a download button
    for img_tag in soup.find_all('img'):
        parent_div = img_tag.find_parent('div')
        if parent_div and 'dev-view-deviation' in parent_div.get('class', []):
            link_tag = parent_div.find('a', class_='dev-page-download')
            if link_tag:
                image_url = link_tag['href']
                download_image(image_url, save_dir)

if __name__ == "__main__":
    # Replace this URL with the URL of the DeviantArt page you want to scrape
    deviantart_url = "https://www.deviantart.com/your-gallery-url"
    save_directory = "downloaded_images"

    crawl_deviantart(deviantart_url, save_directory)
