
import sys, csv
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')
from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *


class SourceIEEE (ArticleSource):
        
    def parseListArticles(self, csv_file: str) -> List[Article]:
        file = open(csv_file, mode='r')
        csv_doc = file.read()
        file.close()

        lines = csv_doc.splitlines()
        articles: List[Article] = []

        reader = csv.reader(lines[1:], delimiter=',', quotechar='"',)
        for row in reader:
            title = row[0]
            doi = row[13]
            url = row[15]
            abstract = row[10]

            articles.append(Article(title=title, url=url,
                            abstract=HtmlParser.clean_str(abstract), doi=doi))
        
        return articles

    def parseCountArticles(self, csv_file: str) -> int:
        file = open(csv_file, mode='r')
        csv_doc = file.read()
        file.close()

        lines = csv_doc.splitlines()
        return len(lines)
    
    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        search_text = ""
        first_or = True

        title = ""
        if ("title" in terms.keys() and len(terms["title"]) > 0):
            title = terms["title"]
            search_text += f"{title}\n"
            first_or = False

        abstract = ""
        if ("abstract" in terms.keys() and len(terms["abstract"]) > 0):
            abstract = terms["abstract"]
            if (not first_or):
                search_text += " OR "
            search_text += f"Abstract:{abstract}\n"
            first_or = False

        keywords = ""
        if ("keywords" in terms.keys() and len(terms["keywords"]) > 0):
            keywords = terms["keywords"]
            if (not first_or):
                search_text += " OR "
            search_text += f"AuthorKeywords:{keywords}\n"
            first_or = False

        res = SearchLinkResult()
        res.source_name = "IEEE Xplore"
        res.search_query = f"({search_text})"
        res.search_link = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&ranges=2014_2024_Year&queryText={ ArticleSource.transform_url(search_text)}"

        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        os.system(f"mkdir -p {download_path}/ieee")
        input_csv_filename = f"{download_path}/ieee/export.csv"
        if not os.path.exists(input_csv_filename):
            print(f"IEEE exports the search result directly from the website. Please export the CSV first to {input_csv_filename}")
            exit(1)
    
        self.exportCSVData([input_csv_filename], f"{output_csv_path}/ieee.csv")
