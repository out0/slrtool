#! /usr/bin/python3
import sys
sys.path.append('model/')
sys.path.append('util/')
sys.path.append('sources/')


from model.Article import *
from util.LatexBuilder import *
from util.HtmlParser import *
from util.ExclusionFilter import *
from sources.SourceWiley import *
from sources.SourceSpringer import *
from sources.SourceScienceDirect import *
from sources.SourceIEEE import *
from sources.SourceAcm import *
from sources.ArticleSource import *
from typing import List
import os
import os.path
import pyperclip
import json


class UI:
    def menu_source_list() -> int:
        print("(1) ACM Digital Library")
        print("(2) IEEE Xplore")
        print("(3) Science Direct")
        print("(4) Springer Link")
        print("(5) Wiley\n")
        return input()

    def menu() -> int:
        print("Select an action\n\n")
        print("(1) Search link")
        print("(2) Generate LaTex code")
        print("(3) Download raw list of articles from a source\n")
        print("(4) Apply exclusion criteria to the articles\n")
        return input()

    def show_search_result(result: SearchLinkResult) -> None:
        print(f"** {result.source_name} **\n\n")
        print("QUERY STRING: \n")
        print(result.search_query)
        print("\nLINK: \n")
        print(result.search_link)
        print("\n")

    def select_source() -> Tuple[ArticleSource, str]:
        opt = UI.menu_source_list()

        match opt.rstrip():
            case '1':
                return [SourceAcm(), "acm"]
            case '2':
                return [SourceIEEE(), "ieee"]
            case '3':
                return [SourceScienceDirect(), "science"]
            case '4':
                return [SourceSpringer(), "springer"]
            case '5':
                return [SourceWiley(), "wiley"]
            case _:
                return [ None, None ]

    def show_search_link(conf: dict) -> None:
        os.system('clear')
        terms = conf["queries"]
        source, source_key = UI.select_source()
        if source == None: return
        UI.show_search_result(result=source.buildSearchLink(terms[source_key]))
        
    def download_and_build_unfiltered_CSV_for_source(config: dict) -> None: 
        os.system('clear')
        terms = config["queries"]
        source, source_key = UI.select_source() 
        if source == None: return

        os.system(f"mkdir -p data/raw")
        os.system(f"mkdir -p data/unfiltered")
        searchLink = source.buildSearchLink(terms[source_key])
        source.buildUnfilteredArticleCSV(searchLink, f"data/raw" ,f"data/unfiltered")
        print("Done. please check folder data/unfiltered \n")

def count_files_in_path(path: str) -> int:
    return len(os.listdir(path))


def count_selected_articles_by_source(conf: dict) -> List[int]:
    selected: List[int] = []
    selected.append(count_files_in_path(conf["selected_articles_path"]["acm"]))
    selected.append(count_files_in_path(
        conf["selected_articles_path"]["ieee"]))
    selected.append(count_files_in_path(
        conf["selected_articles_path"]["science"]))
    selected.append(count_files_in_path(
        conf["selected_articles_path"]["springer"]))
    selected.append(count_files_in_path(
        conf["selected_articles_path"]["wiley"]))

    all: List[int] = []
    all.append(int(conf["count-all"]["acm"]))
    all.append(int(conf["count-all"]["ieee"]))
    all.append(int(conf["count-all"]["science"]))
    all.append(int(conf["count-all"]["springer"]))
    all.append(int(conf["count-all"]["wiley"]))

    return [all, selected]



def main() -> None:
    os.system("clear")
    with open('search_config.json', 'r') as f:
        config = json.load(f)
        opt = UI.menu()

        match opt.rstrip():
            case '1':
                os.system("clear")
                print("Select a source")
                UI.show_search_link(config)
                return
            case '2':
                latex_str = LatexBuilder.build_latex(config)
                pyperclip.copy(latex_str)
                print("CODE Generated and copied to your clipboard")
                return
            case '3':
                os.system("clear")
                print("Select a source for trying to download it's source of articles based on the generated link.")
                UI.download_and_build_unfiltered_CSV_for_source(config)
            case '4':
                os.system("clear")
                print("Applying exclusion criteria to the sources")

                with open('filter_config.json', 'r') as filter_config:
                    filter = ExclusionFilter(
                        raw_path="data/raw",
                        output_path="data/filtered",
                        filter_articles_config=filter_config
                    )
                    filter.filter()
                
            case _:
                return

if __name__ == "__main__":
    main()
