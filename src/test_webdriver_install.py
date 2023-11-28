import os
from selenium import webdriver
import requests
from requests import Response

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import WDMDownloadManager
from webdriver_manager.core.http import HttpClient
from webdriver_manager.core.logger import log
from requests.adapters import HTTPAdapter

class CustomHttpClient(HttpClient):
    def __init__(self, proxy) -> None:
        super().__init__()
        self.proxy = proxy

    def get(self, url, params=None, **kwargs) -> Response:
        """
        Add you own logic here like session or proxy etc.
        """
        log("The call will be done with custom HTTP client")

        if self.proxy:
            # If a proxy is provided, use it
            session = requests.Session()
            session.mount('http://', HTTPAdapter(max_retries=3))
            session.mount('https://', HTTPAdapter(max_retries=3))
            session.proxies = {'http': self.proxy, 'https': self.proxy}
            response = session.get(url, params=params, **kwargs)  # Use params as a keyword argument
        else:
            # If no proxy is provided, make a regular request
            response = requests.get(url, params=params, **kwargs)

        return response


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