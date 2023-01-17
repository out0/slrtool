#! /usr/bin/python3

import sys
sys.path.append('model/')
sys.path.append('util/')
sys.path.append('sources/')


from model.Article import *
from util.LatexBuilder import *
from util.HtmlParser import *
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

    def show_search_link_for_option(conf: dict, opt: int) -> None:
        os.system('clear')
        terms = conf["queries"]

        source:ArticleSource
        terms_key:str

        match opt.rstrip():
            case '1':
                source = SourceAcm()
                terms_key = "acm"
            case '2':
                source = SourceIEEE()
                terms_key = "ieee"
            case '3':
                source = SourceScienceDirect()
                terms_key = "science"
            case '4':
                source = SourceSpringer()
                terms_key = "springer"
            case '5':
                source = SourceWiley()
                terms_key = "wiley"
            case _:
                return

        UI.show_search_result(result=source.buildSearchLink(terms[terms_key])
)
        
    def downloadAndBuildUnfilteredCSVForSourceOption(config: dict, opt: int) -> None: 
        os.system('clear')
        terms = config["queries"]

        source:ArticleSource
        source_key: dict

        match opt.rstrip():
            case '1':
                source = SourceAcm()
                source_key = "acm"
            case '2':
                source = SourceIEEE()
                source_key = "ieee"
            case '3':
                source = SourceScienceDirect()
                source_key = "science"
            case '4':
                source = SourceSpringer()
                source_key = "springer"
            case '5':
                source = SourceWiley()
                source_key = "wiley"
            case _:
                return

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
                search_link_opt = UI.menu_source_list()                
                UI.show_search_link_for_option(config, search_link_opt)
                return
            case '2':
                latex_str = LatexBuilder.build_latex(config)
                pyperclip.copy(latex_str)
                print("CODE Generated and copied to your clipboard")
                return
            case '3':
                os.system("clear")
                print("Select a source for trying to download it's source of articles based on the generated link.")
                download_link_opt = UI.menu_source_list()
                UI.downloadAndBuildUnfilteredCSVForSourceOption(config, download_link_opt)
            case _:
                return

if __name__ == "__main__":
    main()


# <span class="result__count">518 Results</span>
