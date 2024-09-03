
import sys
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')
from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *

class SourceWiley (ArticleSource):

    enable_download_abstract: bool

    def __init__(self):
        self.enable_download_abstract = False

    def parseListArticles(self, file: str) -> List[Article]:
        html = HtmlParser.read_file(file, False)

        article_tags = html.body.find_all('div', attrs={'class': "item__body"})
        res: List[Article] = []

        for atag in article_tags:
            title_link_tag = atag.find(
                'a', attrs={'class': "publication_title"})
            link = title_link_tag.get('href')
            text = HtmlParser.clean_str(title_link_tag.get_text())
            doi = link.replace('/doi/', '')
            abstr_link_tag = atag.find(
                'div', attrs={'class': "accordion__content"})

            if (abstr_link_tag != None and self.enable_download_abstract):
                abstr_link = f"https://onlinelibrary.wiley.com{abstr_link_tag.get('data-ajax-content')}"
                tmp_abstract_file = "temp_abstract.html"

                HtmlParser.download_url(
                    tmp_abstract_file, abstr_link, use_selenium=True)
                HtmlParser.close_browser()

                abstr_file_html = HtmlParser.read_file(
                    tmp_abstract_file, remove_after_read=True)

                abstract = HtmlParser.clean_str(abstr_file_html.get_text())
            else:
                abstract = ""

            res.append(Article(
                title=text, url=f"https://onlinelibrary.wiley.com{link}", abstract=abstract, doi=doi))
        return res

    def parseCountArticles(self, file: str) -> int:
        html = HtmlParser.read_file(file)
        p = html.body.find('span', attrs={'class': "result__count"})
        if (p == None):
            return 0
        return int(p.get_text().strip())

    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        query = terms["query"]
        res = SearchLinkResult()
        res.source_name = "Wiley"
        res.search_query = f"({query})"
        res.search_link = f"https://onlinelibrary.wiley.com/action/doSearch?AllField={ArticleSource.transform_url(query)}&AfterMonth=1&AfterYear=2014&BeforeMonth=12&BeforeYear=2025&ConceptID=68"
        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        
        os.system(f"mkdir -p {download_path}/wiley")

        filename_list = []

        filename_list.append(HtmlParser.download_source_page(
            f"{download_path}/wiley/wiley_0.html", f"{searchLink.search_link}&pageSize=50&startPage=0", use_selenium=True))

        self.enable_download_abstract = False
        num_records = self.parseCountArticles(filename_list[0])

        pages = self.count_pages(num_records, 50)
        print(f"found {num_records} records - paginating in {pages}\n")

        for i in range(0, pages):
            self.enable_download_abstract = True
            url = f"{searchLink.search_link}&pageSize=50&startPage={i}\n"
            filename_list.append(HtmlParser.download_source_page(f"{download_path}/wiley/wiley_{i}.html", url, use_selenium=True, wait_after=10))
            HtmlParser.close_browser()

        print("processing files\n")

        self.exportCSVData(filename_list, f"{output_csv_path}/wiley.csv")

