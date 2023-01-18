from model.Article import *
from typing import List
import sys
import csv
import os
sys.path.append('../model')

class ArticleCSVReader:
    def import_from_csv(csv_file: str) -> List[Article]:
        if not os.path.exists(csv_file):
            return []
            
        file = open(csv_file, mode='r')
        csv_doc = file.read()
        file.close()

        lines = csv_doc.splitlines()
        articles: List[Article] = []

        reader = csv.reader(
            lines[1:], quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            title = row[0].replace("\"", "").strip()
            abstract = row[1].replace("\"", "").strip()
            doi = row[2].replace("\"", "").strip()
            url = row[3].replace("\"", "").strip()

            articles.append(Article(title=title, url=url,
                            abstract=abstract, doi=doi))

        return articles