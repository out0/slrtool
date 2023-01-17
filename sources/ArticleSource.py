import sys
import math
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')
from model.Article import *
from util.HtmlParser import *
from typing import List

class SearchLinkResult:
    source_name: str
    search_query: str
    search_link: str

class ArticleSource(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parseListArticles(self, file: str) -> List[Article]:
        pass

    @abstractmethod
    def parseCountArticles(self, file: str) -> int:
        pass

    def exportCSVData(self, input_files: List[str], output_csv_file: str) -> None:
        articles = []
        for f in input_files:
            arts = self.parseListArticles(f)
            articles.extend(arts)

        HtmlParser.export_to_csv(output_csv_file, articles)

    @abstractmethod
    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        pass

    @abstractmethod
    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_file: str) -> None:
        pass



    def count_pages(self, num_records: int, num_records_per_page: int) -> int:
        inc = 0
        if num_records % num_records_per_page > 0:
            inc = 1
        return math.floor(num_records / num_records_per_page) + inc


    def transform_url(txt: str) -> str:
        p = txt.replace('\n', '')
        p = p.replace(':', '%3A')
        p = p.replace('(', '%28')
        p = p.replace(')', '%29')
        p = p.replace('[', '%5B')
        p = p.replace(']', '%5D')
        p = p.replace(' ', '+')
        p = p.replace('"', '%22')
        return p