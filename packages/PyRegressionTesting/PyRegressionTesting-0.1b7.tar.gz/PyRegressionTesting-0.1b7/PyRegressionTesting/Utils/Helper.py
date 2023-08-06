import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlsplit, quote, urlunsplit

from PyRegressionTesting.Utils.Constants import BASE_DIR


class Helper:
    @staticmethod
    def format_url(url):
        url = urlsplit(url)
        url = list(url)
        url[2] = quote(url[2])
        url = urlunsplit(url)
        return url

    @staticmethod
    def pop(items, num):
        item_sub = set()
        for index in range(0, min(len(items), num)):
            item_sub.add(items.pop())
        return item_sub

    @staticmethod
    def get_batch(items, batch_size, batch_num):
        items = list(Helper.pop(items, batch_size*batch_num))
        batches = Helper.split_list(items, batch_num)
        return batches

    @staticmethod
    def split_list(seq, size):
        chunks = list((seq[i::size] for i in range(size)))
        return [x for x in chunks if x != []]

    @staticmethod
    def createWebDriver(driver_path=None, headless=True):
        if driver_path is None:
            driver_path = os.path.join(BASE_DIR, 'src', 'bin', 'chromedriver.exe')
        options = Options()
        chrome_options = webdriver.ChromeOptions()

        options.binary_location = driver_path

        if headless:
            options.add_argument('--headless')
            chrome_options.add_argument('headless')

        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('disable-infobars')

        desiredCapabilities = {'browserName': 'chrome'}

        driver = webdriver.Chrome(options=options, chrome_options=chrome_options, executable_path=driver_path,
                                  desired_capabilities=desiredCapabilities)
        return driver