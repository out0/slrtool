from typing import List
import sys
sys.path.append('model/')
sys.path.append('util/')

from model.Article import *
from util.ArticleCSVReader import *

class ExportDeletedDOI:    

    def __import_csv_files(path: str) -> List[Article]:
        articles: List[Article] = []
        articles = ArticleCSVReader.import_from_csv(f"{path}/ieee.csv")
        articles.extend(ArticleCSVReader.import_from_csv(f"{path}/science.csv"))
        articles.extend(ArticleCSVReader.import_from_csv(f"{path}/acm.csv"))
        articles.extend(ArticleCSVReader.import_from_csv(f"{path}/springer.csv"))
        articles.extend(ArticleCSVReader.import_from_csv(f"{path}/wiley.csv"))
        return articles


    def export(origin_path: str, compare_path:str, result_file: str):
        source: List[Article] = ExportDeletedDOI.__import_csv_files(origin_path)
        target: List[Article] = ExportDeletedDOI.__import_csv_files(compare_path)
        excluded_articles_doi: List[str] = []

        target_title_set = dict()

        for ta in target:
            if ta != None:
                target_title_set[ta.title] = True

        for sa in source:
            if sa != None and sa.title not in target_title_set.keys():
                excluded_articles_doi.append(sa.doi)

        file = open(result_file, mode='w')
        file.write("{\n")
        for doi in excluded_articles_doi:
            file.write(f"    \"{doi}\",\n")
        file.write("}\n")            
        file.close()
