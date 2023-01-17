
import sys
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')
from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *

class SourceScienceDirect (ArticleSource):

    def __get_abstract(self, link: str) -> str:
        tmp_abstract_file = "downloads/science/temp_abstract.html"
        HtmlParser.download_url(tmp_abstract_file, link)
        html_doc = HtmlParser.read_file(
            tmp_abstract_file, remove_after_read=True)

        doi_tag = html_doc.find(
            'div', attrs={'id': 'article-identifier-links'})
        doi_tag_a = doi_tag.find('a', attrs={'class': 'doi'})
        doi = ""
        if doi_tag != None:
            doi = doi_tag_a.get('href')
        if doi != None:
            doi = doi.replace("https://doi.org/", "")

        abstr = html_doc.find('div',  attrs={'id': "abstracts"})
        if abstr != None and (len(abstr.contents) > 0) and (len(abstr.contents[0].contents) > 1):
            return doi, abstr.contents[0].contents[1].get_text()
        else:
            abstr = html_doc.find('div',  attrs={'class': "abstract"})
            if abstr != None and (len(abstr.contents) > 0 and len(abstr.contents[0].contents) > 1):
                return doi, abstr.contents[0].contents[1].get_text()

        print("i dont know how to deal with this abstract...")
        return doi, ""

    def parseListArticles(self, file: str) -> List[Article]:

        html = HtmlParser.read_file(file, False)

        article_tags = html.body.find_all(
            'a', attrs={'class': "result-list-title-link"})
        res: List[Article] = []

        for atag in article_tags:
            link = atag.get('href')
            text = HtmlParser.clean_str(atag.get_text())
            doi, abstract = self.__get_abstract(link)
            res.append(Article(title=text, url=link,
                       abstract=HtmlParser.clean_str(abstract), doi=doi))
        return res

    def parseCountArticles(self, file: str) -> int:
        html_doc = HtmlParser.read_file(file)
        p = html_doc.body.find(
            'span', attrs={'class': "search-body-results-text"})
        if (p == None):
            return 0
        return int(p.get_text().replace("results", "").strip())

    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        query = terms["query"]
        res = SearchLinkResult()
        res.source_name = "Science Direct"
        res.search_query = f"({query})"
        res.search_link = f"https://www.sciencedirect.com/search?date=2010-2023&qs={ArticleSource.transform_url(query)}&lastSelectedFacet=publicationTitles&publicationTitles=271599%2C280203"
        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        os.system(f"mkdir -p {download_path}/science")
        
        first = f"{download_path}/science/science_0.html"

        if not os.path.exists(first):
            print(f"Currently, I don't support downloading the article list by myself due to some crazy iframes issues!! Please download them and save them on the path: {download_path}/science with names science_i.html, where i is the page number")
            exit(1)

        filename_list = []
        filename_list.append(first)
        records = self.parseCountArticles(filename_list[0])

        pages = ArticleSource.count_pages(records, 100)
        print(f"found {records} records - expecting {pages}\n")

        for i in range(1, pages):
            if not os.path.exists(first):
                print(f"* * Warning, a file {download_path}/science/science_{i}.html is missing, this means that their articles will be ignored!")
            else:
                filename_list.append(f"{download_path}/science/science_{i}.html")

        print("processing files\n")

        self.parseListArticles(filename_list, f"{output_csv_path}/science.csv")

