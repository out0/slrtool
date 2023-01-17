
import sys
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')

from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *


class SourceAcm (ArticleSource):
    def __init__(self):
        pass

    def parseListArticles(self, file: str) -> List[Article]:

        html = HtmlParser.read_file(file, False)

        article_tags = html.body.find_all(
            'div', attrs={'class': "issue-item__content"})
        res: List[Article] = []

        for atag in article_tags:
            title_tag = atag.find('h5', attrs={'class': "issue-item__title"})
            if title_tag == None:
                continue
            link = title_tag.find('a').get('href')
            text = HtmlParser.clean_str(title_tag.get_text())
            abstract = HtmlParser.clean_str(
                atag.find('div', attrs={'class': 'issue-item__abstract'}).get_text())
            doi = link.replace('/doi/', '')
            res.append(Article(
                title=text, url=f"https://dl.acm.org{link}", abstract=abstract, doi=doi))
        return res

    def parseCountArticles(self, file: str) -> int:
        html = HtmlParser.read_file(file)
        p = html.body.find('span', attrs={'class': "result__count"})
        if (p == None):
            return 0
        return int(p.get_text().replace("Results", "").strip())

    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        search_text = ""
        first_or = True

        title = ""
        if ("title" in terms.keys() and len(terms["title"]) > 0):
            title = terms["title"]
            search_text += f"Title:{title}\n"
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
            search_text += f"Keyword:{keywords}\n"
            first_or = False

        res = SearchLinkResult()
        res.source_name = "ACM Digital Library"
        res.search_query = search_text
        res.search_link = f"https://dl.acm.org/action/doSearch?expand=all&AfterMonth=1&AfterYear=2010&AllField={ArticleSource.transform_url(search_text)}"

        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        
        os.system(f"mkdir -p {download_path}/acm")

        filename_list = []

        filename_list.append(HtmlParser.download_source_page(f"{download_path}/acm/acm_0.html",
            f"{searchLink.search_link}&pageSize=50&startPage=0"))
        
        records = self.parseCountArticles(filename_list[0])

        pages = self.count_pages(records, 50)
        print(f"{searchLink.source_name}: found {records} records - paginating in {pages}\n")

        for i in range(1, pages):
            url = f"{searchLink.search_link}&pageSize=50&startPage={i}\n"
            filename_list.append(HtmlParser.download_source_page(f"{download_path}/acm/acm_{i}.html", url))

        print("processing files\n")

        self.exportCSVData(filename_list, f"{output_csv_path}/acm.csv")

        