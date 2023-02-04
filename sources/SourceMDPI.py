
import sys
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')

from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *


class SourceMDPI (ArticleSource):
    def __init__(self):
        pass

    def parseListArticles(self, file: str) -> List[Article]:

        html = HtmlParser.read_file(file, False)

        article_tags = html.body.find_all(
            'div', attrs={'class': "article-content"})
        res: List[Article] = []

        for atag in article_tags:
            title_tag = atag.find('a', attrs={'class': "title-link"})
            if title_tag == None:
                continue
            link = title_tag.get('href')
            text = HtmlParser.clean_str(title_tag.get_text())
            abstract = HtmlParser.clean_str(
                atag.find('div', attrs={'class': 'abstract-full'}).get_text())
            doi_link = atag.find('div', attrs={'class': 'color-grey-dark'})
            doi = ""
            if doi_link != None:
                doi = doi_link.find('a').get_text().replace("https://doi.org/", "")

            res.append(Article(
                title=text, url=f"https://www.mdpi.com/{link}", abstract=abstract, doi=doi))
        return res

    def parseCountArticles(self, file: str) -> int:
        html = HtmlParser.read_file(file)
        p = html.body.find('div', attrs={'class': "content__container content__container--overflow-initial"})
        if (p == None):
            return 0

        return int(p.find("h1").get_text().replace("Search Results", "").replace("(", "").replace(")", "").replace(",", "").strip())

    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        search_text = ""
        search_query = ""
       
        for term in terms["terms"]:
            search_text += f"%7C(%40(title%2Cabstract%2Ckeywords%2Cauthors%2Caffiliations%2Cdoi%2Cfull_text%2Creferences){ArticleSource.transform_url(term)})"
            search_query += f"|(@(title,abstract,keywords,authors,affiliations,doi,full_text,references){term})"

        res = SearchLinkResult()
        res.source_name = "MDPI"
        res.search_query = search_query
        res.search_link = f"https://www.mdpi.com/search?sort=pubdate&page_count=200&year_from=2010&year_to=2022&subjects=engineering%2Ccomputer-math&view=default&advanced={search_text}"

        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        
        os.system(f"mkdir -p {download_path}/mdpi")

        filename_list = []

        filename_list.append(HtmlParser.download_source_page(f"{download_path}/mdpi/mdpi_0.html",
            f"{searchLink.search_link}&page_no=1"))
        
        records = self.parseCountArticles(filename_list[0])

        pages = self.count_pages(records, 200)
        print(f"{searchLink.source_name}: found {records} records - paginating in {pages}\n")

        for i in range(1, pages):
            url = f"{searchLink.search_link}&page_no={i+1}\n"
            filename_list.append(HtmlParser.download_source_page(f"{download_path}/mdpi/mdpi_{i}.html", url))

        print("processing files\n")

        self.exportCSVData(filename_list, f"{output_csv_path}/mdpi.csv")

        