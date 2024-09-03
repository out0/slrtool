
import sys
import csv
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')
from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *

class SourceSpringer (ArticleSource):
    def parseListArticles(self, csv_file: str) -> List[Article]:
        
        file = open(csv_file, mode='r')
        csv_doc = file.read()
        file.close()

        lines = csv_doc.splitlines()
        articles: List[Article] = []

        reader = csv.reader(lines[1:], delimiter=',', quotechar='"',)
        
        for row in reader:
            title = row[0]
            doi = row[5]
            url = row[8]
            abstract = ""

            tmp_abstract_file = "temp_abstract.html"
            HtmlParser.download_url(tmp_abstract_file, use_selenium=True, url=url)

            if os.path.exists(tmp_abstract_file):
                abstract_html = HtmlParser.read_file(tmp_abstract_file, remove_after_read=True)
                abstract_tag = abstract_html.find('meta', {'property': 'og:description'})
                if abstract_tag != None:
                    abstract = abstract_tag.get('content')

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
        return self.buildSearchLinkEA(terms, False)

    def buildSearchLinkEA(self, terms: dict, export_append: bool) -> SearchLinkResult:
        query = terms["query"]

        if export_append and "append_query_text" in terms:
            p = terms["append_query_text"]
            query += f" + {p}"

        res = SearchLinkResult()
        res.source_name = "Springer Link"
        res.search_query = f"({query})"
        res.search_link = f"https://link.springer.com/search?query={ArticleSource.transform_url(query)}&date-facet-mode=between&facet-start-year=2014&facet-sub-discipline=%22Artificial+Intelligence%22&facet-content-type=%22Article%22&facet-language=%22En%22&facet-end-year=2022&facet-sub-discipline=%22Robotics+and+Automation%22"
        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        os.system(f"mkdir -p {download_path}/springer")
        
        input_csv_filename = f"{download_path}/springer/export.csv"
        if not os.path.exists(input_csv_filename):
            print(f"Springer exports the search result directly from the website. Please export the CSV first to {input_csv_filename}")
            exit(1)
    
        self.exportCSVData([input_csv_filename], f"{output_csv_path}/springer.csv")

