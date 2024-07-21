import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ImageDownloader:
    def __init__(self, download_dir="PhotoGallery"):
        self.download_dir = os.path.join(os.getcwd(), download_dir)
        self.driver = None
        self.setup_download_directory()
        self.setup_driver()

    def setup_download_directory(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("prefs", {
            "plugins.always_open_pdf_externally": True,
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def navigate_to_photo_gallery(self, url):
        self.driver.get(url)

        try:
            media_menu = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Media']"))
            )
            media_menu.click()

            more_info = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Click for more info of Press Releases']"))
            )
            more_info.click()

            photo_gallery = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='Photo Gallery'])[2]"))
            )
            href = photo_gallery.get_attribute('href')
            self.driver.get(href)
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred while navigating: {str(e)}")
            self.driver.quit()
            raise

    def fetch_image_urls(self, limit=10):
        try:
            image_elements = self.driver.find_elements(By.XPATH, "//table//img")
            time.sleep(2)
            image_urls = [element.get_attribute('src') for element in image_elements[:limit]]
            return image_urls
        except Exception as e:
            print(f"An error occurred while fetching image URLs: {str(e)}")
            return []

    def download_images(self, image_urls):
        for i, url in enumerate(image_urls, 1):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(os.path.join(self.download_dir, f"image_{i}.jpg"), "wb") as f:
                        f.write(response.content)
                        print(f"Downloaded image {i}")
                else:
                    print(f"Failed to download image {i}")
            except Exception as e:
                print(f"Error occurred while downloading image {i}: {str(e)}")

    def close_driver(self):
        self.driver.quit()

    def run(self, url):
        try:
            self.navigate_to_photo_gallery(url)
            image_urls = self.fetch_image_urls()
            self.download_images(image_urls)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            self.close_driver()


if __name__ == "__main__":
    url = "https://labour.gov.in/"
    downloader = ImageDownloader()
    downloader.run(url)
