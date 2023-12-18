import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import WDMDownloadManager

from asvz_bot import CustomHttpClient


def test_custom_http_client():
    proxy_url = "proxy.ethz.ch:3128"
    custom_client = CustomHttpClient(proxy=proxy_url)
    response = custom_client.get("https://google.com")
    print(response)
    assert response is not None


def test_can_get_chrome_driver_with_custom_http_client():
    http_client = CustomHttpClient(proxy="proxy.ethz.ch:3128")
    download_manager = WDMDownloadManager(http_client)
    path = ChromeDriverManager(download_manager=download_manager).install()
    assert os.path.exists(path)


def test_selenium_driver():
    # Create a WebDriver instance
    http_client = CustomHttpClient(proxy="proxy.ethz.ch:3128")
    download_manager = WDMDownloadManager(http_client)
    # Configure ChromeOptions as needed, e.g., set proxy options
    # Create a WebDriver instance with ChromeOptions
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=http://proxy.ethz.ch:3128")
    path = ChromeDriverManager(download_manager=download_manager).install()
    driver = webdriver.Chrome(options=options)

    # Navigate to the Google homepage
    driver.get("https://www.google.com")

    # Wait for a few seconds to see the search results
    driver.implicitly_wait(5)

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    test_custom_http_client()
    test_can_get_chrome_driver_with_custom_http_client()
    test_selenium_driver()
