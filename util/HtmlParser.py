#! /usr/bin/python3
from typing import List, Tuple
from io import StringIO
import os
import os.path
from bs4 import BeautifulSoup
from model.Article import *

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import sys
sys.path.append('../model')
from model.Article import *


WEB_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
# Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0

class HtmlParser:

    selenium_browser = None

    def clean_str(val: str) -> str:
        strb = StringIO()
        for s in val.replace('\n', '').split(' '):
            if len(s) == 0:
                continue
            strb.write(s)
            strb.write(' ')

        return strb.getvalue().strip()

    def escape_double_quote(val: str) -> str:
        return val.replace("\"", "'")

    def export_to_csv(path: str, list: List[Article]):
        file = open(path, 'w')
        file.write('"title", "abstract", "doi", "url"\n')

        for article in list:
            title = HtmlParser.escape_double_quote(article.title)
            abstract = HtmlParser.escape_double_quote(article.abstract)
            file.write(
                f"\"{title}\", \"{abstract}\", \"{article.doi}\", \"{article.url}\"\n")

        file.close()

    def download_source_page(file: str, url: str, use_selenium: bool = False, cookies_file: str = None) -> None:
        if not os.path.exists(file):
            HtmlParser.download_url(file, url, use_selenium, cookies_file)

        return file

    def load_browser():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.binary = "/usr/bin/firefox"

        return webdriver.Firefox(options=options)

    def download_url_selenium(filename: str, url: str) -> None:
        if HtmlParser.selenium_browser == None:
            HtmlParser.selenium_browser = HtmlParser.load_browser()

        HtmlParser.selenium_browser.get(url)
        file = open(filename, mode='w')
        file.write(HtmlParser.selenium_browser.page_source)
        file.close()

    def download_url(filename: str, url: str, use_selenium: bool = False, cookies_file: str = None) -> None:
        print(f"downloading {filename}...")
        if use_selenium:
            HtmlParser.download_url_selenium(filename, url)
            return
        else:
            command = f"wget --quiet \"{url}\" -O {filename} -U '{WEB_USERAGENT}'"
            if cookies_file:
                command += f" --load-cookies {cookies_file}"

        result = os.system(command)
        if result != 0:
            os.remove(filename)
            print('failed!\n')
            print(f'link: {url}\n')
            print(f'command: {command}\n')
            exit(0)

    def read_file(filename: str, remove_after_read: bool = False) -> BeautifulSoup:
        file = open(filename, mode='r')
        html_doc = file.read()
        file.close()
        if remove_after_read:
            os.remove(filename)

        return BeautifulSoup(html_doc, 'html.parser')
