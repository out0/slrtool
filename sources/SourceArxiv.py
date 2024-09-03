import sys, csv
from abc import ABC, abstractmethod
sys.path.append('../model')
sys.path.append('../util')
from model.Article import *
from typing import List
from ArticleSource import *
from HtmlParser import *

class SourceArxiv (ArticleSource):
        
    def parseListArticles(self, file: str) -> List[Article]:
        html = HtmlParser.read_file(file, False)

        article_tags = html.body.find_all(
            'li', attrs={'class': "arxiv-result"})
        res: List[Article] = []

        for atag in article_tags:
            title_tag = atag.find('p', attrs={'class': "title is-5 mathjax"})
            if title_tag == None:
                continue

            link = ""
            
            aref = atag.find('p', attrs={'class': 'list-title is-inline-block'})
            if aref != None:
                link = aref.find('a').get('href')

            text = HtmlParser.clean_str(title_tag.get_text())
            abstract = HtmlParser.clean_str(
                atag.find('span', attrs={'class': 'abstract-full'}).get_text())
                       
            doi = ''
            res.append(Article(
                title=text, url=link, abstract=abstract, doi=doi))
        return res

    def parseCountArticles(self, file: str) -> int:
        html = HtmlParser.read_file(file)
        p = html.body.find('h1', attrs={'class': "title is-clearfix"})
        if (p == None):
            return 0

        p = p.get_text()
        i = p.find("of")

        return int(p[i+2:].replace('results', '').replace(',', '').strip())
    
    def buildSearchLink(self, terms: dict) -> SearchLinkResult:
        search_url = "&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2014-01-01&date-to_date=2024-12-31&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first"
        search_query = ""

        i:int = 0
        for term in terms["terms"]:
            search_url += f"&terms-{i}-operator=OR&terms-{i}-term={term}&terms-{i}-field=all"
            if i > 0:
                search_query += " OR"
            search_query += f" \"{term}\""
            i += 1

        res = SearchLinkResult()
        res.source_name = "Arxiv"
        res.search_query = search_query
        res.search_link = f"https://arxiv.org/search/advanced?advanced={ArticleSource.transform_url(search_url)}"
        
        return res

    def buildUnfilteredArticleCSV(self, searchLink: SearchLinkResult, download_path: str, output_csv_path: str) -> None:
        os.system(f"mkdir -p {download_path}/arxiv")

        filename_list = []

        filename_list.append(HtmlParser.download_source_page(f"{download_path}/arxiv/arxiv_0.html",
            f"{searchLink.search_link}"))
        
        records = self.parseCountArticles(filename_list[0])

        pages = self.count_pages(records, 200)
        print(f"{searchLink.source_name}: found {records} records - paginating in {pages}\n")

        for i in range(1, pages):
            url = f"{searchLink.search_link}&start={i*200}\n"
            filename_list.append(HtmlParser.download_source_page(f"{download_path}/arxiv/arxiv_{i}.html", url))

        print("processing files\n")

        self.exportCSVData(filename_list, f"{output_csv_path}/arxiv.csv")
