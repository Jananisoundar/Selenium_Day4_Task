import os
import shutil
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


def set_download_directory():
    """Set up and clean the download directory."""
    cd = os.getcwd()
    download_dir = os.path.join(cd, "Notes")
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.mkdir(download_dir)
    return download_dir


def initialize_driver(download_dir):
    """Initialize Chrome WebDriver with specified options."""
    chrome_options = Options()
    chrome_prefs = {
        "plugins.always_open_pdf_externally": True,
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    chrome_options.add_argument("--safebrowsing-disable-download-protection")
    chrome_options.add_argument("--safebrowsing-disable-extension-blacklist")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


def open_website(driver, url):
    """Open the specified website."""
    driver.get(url)


def click_monthly_progress_report(driver):
    """Click on the 'Monthly Progress Report' link."""
    try:
        act = ActionChains(driver)
        documents = driver.find_element(By.XPATH, "//a[normalize-space()='Documents']")
        act.move_to_element(documents).perform()

        monthly_progress_link = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Monthly Progress Report")]'))
        )
        monthly_progress_link.click()

    except TimeoutException:
        print("Timeout exception while clicking Monthly Progress Report")


def download_specific_report(driver, report_name):
    """Click on the download link for a specific report."""
    try:
        download_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//td[contains(text(),"{report_name}")]/following::a[1]'))
        )
        download_link.click()

        # Wait for the alert to appear
        time.sleep(5)

        # Accept the alert (click "OK")
        pyautogui.press('enter')
        time.sleep(5)

    except TimeoutException:
        print(f"Timeout exception while downloading {report_name}")


if __name__ == "__main__":
    download_dir = set_download_directory()
    driver = initialize_driver(download_dir)

    try:
        open_website(driver, "https://labour.gov.in/")
        click_monthly_progress_report(driver)
        download_specific_report(driver, "January-2024")

    finally:
        driver.quit()
