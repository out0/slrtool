from util.ArticleCSVReader import *
from model.Article import *
from model.ArticleDatabase import *
from typing import List, Tuple, Callable
import os
import sys
import os.path

sys.path.append('../model')
sys.path.append('../util')


class ExclusionFilter:
    unique: ArticleDatabase
    filtered: ArticleDatabase
    filter_articles_config: dict
    output_path: str

    def __init__(self, filter_articles_config: dict, unfiltered_path: str, output_filtered_path: str):
        self.output_path = output_filtered_path
        self.filter_articles_config = filter_articles_config

        self.unique = ArticleDatabase(
            ieee=ArticleCSVReader.import_from_csv(
                f"{unfiltered_path}/ieee.csv"),
            science=ArticleCSVReader.import_from_csv(
                f"{unfiltered_path}/science.csv"),
            acm=ArticleCSVReader.import_from_csv(f"{unfiltered_path}/acm.csv"),
            springer=ArticleCSVReader.import_from_csv(
                f"{unfiltered_path}/springer.csv"),
            wiley=ArticleCSVReader.import_from_csv(
                f"{unfiltered_path}/wiley.csv"),
            arxiv=ArticleCSVReader.import_from_csv(
                f"{unfiltered_path}/arxiv.csv")                
        )

    def __filter_dedup(base: List[Article], target: List[Article]) -> Tuple[List[Article], List[Article]]:
        base_title = dict()
        base_doi = dict()

        dup: List[Article] = []
        non_dup: List[Article] = []
        unique: bool = True

        i = 0
        for b in base:
            if len(b.doi.strip()) > 0:
                base_doi[b.doi.upper().strip()] = i
            if len(b.title.strip()) > 0:
                base_title[b.title.upper().strip()] = i
            i += 1

        for t in target:
            unique = True

            if len(t.doi) > 0 and t.doi.upper().strip() in base_doi.keys():
                dup.append(t)
                unique = False

            if (unique and len(t.title) > 0 and t.title.upper().strip() in base_title.keys()):
                dup.append(t)
                unique = False

            if unique:
                non_dup.append(t)

        return (dup, non_dup)

    def __filter_dedup_self(base: List[Article]) -> Tuple[List[Article], List[Article]]:
        base_title = dict()
        base_doi = dict()

        dup: List[Article] = []
        non_dup: List[Article] = []

        i = 0
        for b in base:
            if len(b.doi.strip()) > 0:
                if b.doi.upper().strip() in base_doi:
                    dup.append(b)
                else:
                    base_doi[b.doi.upper().strip()] = 1
                    non_dup.append(b)
            elif len(b.title.strip()) > 0:
                if b.title.upper().strip() in base_title:
                    dup.append(b)
                else:
                    base_title[b.title.upper().strip()] = 1
                    non_dup.append(b)
            i += 1

        return (dup, non_dup)

    def __dedup_message(source: str, target: str, dup_list: List[Article]) -> None:
        print(f"\t{source}: {target} duplicated {len(dup_list)}")

    def __dedup_science(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        science_dup, science_nondup = ExclusionFilter.__filter_dedup(
            unique.ieee, unique.science)
        ExclusionFilter.__dedup_message("ieee", "science", science_dup)

        duplicated.science.extend(science_dup)
        unique.science = science_nondup

    def __dedup_acm(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        acm_dup, acm_nondup = ExclusionFilter.__filter_dedup(
            unique.ieee, unique.acm)
        ExclusionFilter.__dedup_message("ieee", "acm", acm_dup)
        duplicated.acm.extend(acm_dup)

        acm_dup, acm_nondup = ExclusionFilter.__filter_dedup(
            unique.science, acm_nondup)
        ExclusionFilter.__dedup_message("science", "acm", acm_dup)
        duplicated.acm.extend(acm_dup)

        unique.acm = acm_nondup

    def __dedup_springer(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        springer_dup, springer_nondup = ExclusionFilter.__filter_dedup(
            unique.ieee, unique.springer)
        ExclusionFilter.__dedup_message("ieee", "springer", springer_dup)
        duplicated.springer.extend(springer_dup)

        springer_dup, springer_nondup = ExclusionFilter.__filter_dedup(
            unique.science, springer_nondup)
        ExclusionFilter.__dedup_message("science", "springer", springer_dup)
        duplicated.springer.extend(springer_dup)

        springer_dup, springer_nondup = ExclusionFilter.__filter_dedup(
            unique.acm, springer_nondup)
        ExclusionFilter.__dedup_message("acm", "springer", springer_dup)
        duplicated.springer.extend(springer_dup)

        unique.springer = springer_nondup

    def __dedup_wiley(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.ieee, unique.wiley)
        ExclusionFilter.__dedup_message("ieee", "wiley", wiley_dup)
        duplicated.wiley.extend(wiley_dup)

        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.science, wiley_nondup)
        ExclusionFilter.__dedup_message("science", "wiley", wiley_dup)
        duplicated.wiley.extend(wiley_dup)

        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.acm, wiley_nondup)
        ExclusionFilter.__dedup_message("acm", "wiley", wiley_dup)
        duplicated.wiley.extend(wiley_dup)

        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.springer, wiley_nondup)
        ExclusionFilter.__dedup_message("springer", "wiley", wiley_dup)
        duplicated.wiley.extend(wiley_dup)

        unique.wiley = wiley_nondup

    def __dedup_arxiv(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.ieee, unique.arxiv)
        ExclusionFilter.__dedup_message("ieee", "arxiv", arxiv_dup)
        duplicated.arxiv.extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.science, arxiv_nondup)
        ExclusionFilter.__dedup_message("science", "arxiv", arxiv_dup)
        duplicated.arxiv.extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.acm, arxiv_nondup)
        ExclusionFilter.__dedup_message("acm", "arxiv", arxiv_dup)
        duplicated.arxiv.extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.springer, arxiv_nondup)
        ExclusionFilter.__dedup_message("springer", "arxiv", arxiv_dup)
        duplicated.arxiv.extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.wiley, arxiv_nondup)
        ExclusionFilter.__dedup_message("wiley", "arxiv", arxiv_dup)
        duplicated.arxiv.extend(arxiv_dup)


        unique.arxiv = arxiv_nondup


    def __dedup_self(unique: ArticleDatabase) -> int:
        dup_lst: List[Article] = []
        [dup, unique.acm] = ExclusionFilter.__filter_dedup_self(unique.acm)
        dup_lst.extend(dup)
        [dup, unique.ieee] = ExclusionFilter.__filter_dedup_self(unique.ieee)
        dup_lst.extend(dup)
        [dup, unique.science] = ExclusionFilter.__filter_dedup_self(unique.science)
        dup_lst.extend(dup)
        [dup, unique.springer] = ExclusionFilter.__filter_dedup_self(unique.springer)
        dup_lst.extend(dup)
        [dup, unique.wiley] = ExclusionFilter.__filter_dedup_self(unique.wiley)
        dup_lst.extend(dup)
        [dup, unique.arxiv] = ExclusionFilter.__filter_dedup_self(unique.arxiv)
        dup_lst.extend(dup)

        return len(dup_lst)

    def __apply_filter_remove(keys: List[str], unique: ArticleDatabase, remove_func: Callable) -> ArticleDatabase:
        removed = ArticleDatabase(
            acm=[], ieee=[], science=[], springer=[], wiley=[], arxiv = [])
        removed.acm, unique.acm = remove_func(keys, unique.acm)
        removed.ieee, unique.ieee = remove_func(keys, unique.ieee)
        removed.science, unique.science = remove_func(keys, unique.science)
        removed.springer, unique.springer = remove_func(keys, unique.springer)
        removed.wiley, unique.wiley = remove_func(keys, unique.wiley)
        removed.arxiv, unique.arxiv = remove_func(keys, unique.arxiv)
        return removed

    def __apply_filter_remove_source(keys: List[str], articles: List[Article]) -> Tuple[List[Article], List[Article]]:
        removed: List[Article] = []
        non_filtered: List[Article] = []
        is_filtered: bool = False

        for art in articles:
            is_filtered = False

            for key in keys:
                p = key.upper()
                if p in art.title.upper():
                    removed.append(art)
                    is_filtered = True

                if not is_filtered and p in art.abstract.upper():
                    removed.append(art)
                    is_filtered = True

            if not is_filtered:
                non_filtered.append(art)

        return (removed, non_filtered)

    def __apply_filter_include_source(keys: List[str], articles: List[Article]) -> Tuple[List[Article], List[Article]]:
        removed: List[Article] = []
        non_filtered: List[Article] = []
        is_filtered: bool = False

        for art in articles:
            is_filtered = True

            for key in keys:
                p = key.upper()
                if p in art.title.upper():
                    is_filtered = False
                    break

                if p in art.abstract.upper():
                    is_filtered = False
                    break

            if is_filtered:
                removed.append(art)
            else:
                non_filtered.append(art)

        return (removed, non_filtered)

    def __apply_filter_remove_doi_source(doi: List[str], articles: List[Article]) -> Tuple[List[Article], List[Article]]:
        removed: List[Article] = []
        non_filtered: List[Article] = []
        is_filtered: bool = False

        for art in articles:
            is_filtered = False

            for key in doi:
                p = key.upper()
                if p in art.doi.upper():
                    removed.append(doi)
                    is_filtered = True

            if not is_filtered:
                non_filtered.append(art)

        return (removed, non_filtered)

    def __escape_double_quote(val: str) -> str:
        return val.replace("\"", "'")

    def __export_to_csv(path: str, list: List[Article]):
        file = open(path, 'w')
        file.write('"title", "abstract", "doi", "url"\n')

        for article in list:
            title = ExclusionFilter.__escape_double_quote(article.title)
            abstract = ExclusionFilter.__escape_double_quote(article.abstract)
            file.write(
                f"\"{title}\", \"{abstract}\", \"{article.doi}\", \"{article.url}\"\n")
        file.close()

    def filter(self) -> None:
        os.system(f"rm -rf {self.output_path}")
        os.system(f"mkdir -p {self.output_path}")

        print(f"Initial total {len(self.unique)} articles")

        duplicated = ArticleDatabase(
            acm=[],
            ieee=[],
            science=[],
            springer=[],
            wiley=[],
            arxiv=[]
        )

        num_self_dup = ExclusionFilter.__dedup_self(self.unique)
        ExclusionFilter.__dedup_science(self.unique, duplicated)
        ExclusionFilter.__dedup_acm(self.unique, duplicated)
        ExclusionFilter.__dedup_springer(self.unique, duplicated)
        ExclusionFilter.__dedup_wiley(self.unique, duplicated)
        ExclusionFilter.__dedup_arxiv(self.unique, duplicated)
        print(f"removed from deduplication: {len(duplicated) + num_self_dup}")

        not_included = ExclusionFilter.__apply_filter_remove(
            self.filter_articles_config["include_key"], self.unique, ExclusionFilter.__apply_filter_include_source)
        print(
            f"keywords filter: ignored for not having the keywords {len(not_included)} articles")

        removed_doi = ExclusionFilter.__apply_filter_remove(
            self.filter_articles_config["remove_doi"], self.unique, ExclusionFilter.__apply_filter_remove_doi_source)
        print(f"DOI filter: ignored {len(removed_doi)} articles")

        removed = ExclusionFilter.__apply_filter_remove(
            self.filter_articles_config["remove_key"], self.unique, ExclusionFilter.__apply_filter_remove_source)
        print(f"keywords filter: removed {len(removed)} articles")

        to_analyze = ExclusionFilter.__apply_filter_remove(
            self.filter_articles_config["analyze_key"], self.unique, ExclusionFilter.__apply_filter_remove_source)
        print(
            f"keywords filter: removed for analisys {len(to_analyze)} articles")

        print(f"Remaining:{len(self.unique)} articles")

        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/acm.csv", self.unique.acm)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/ieee.csv", self.unique.ieee)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/science.csv", self.unique.science)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/springer.csv", self.unique.springer)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/wiley.csv", self.unique.wiley)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/arxiv.csv", self.unique.arxiv)

        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/acm_del.csv", removed.acm)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/ieee_del.csv", removed.ieee)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/science_del.csv", removed.science)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/springer_del.csv", removed.springer)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/wiley_del.csv", removed.wiley)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/arxiv_del.csv", removed.arxiv)

        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/acm_chk.csv", to_analyze.acm)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/ieee_chk.csv", to_analyze.ieee)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/science_chk.csv", to_analyze.science)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/springer_chk.csv", to_analyze.springer)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/wiley_chk.csv", to_analyze.wiley)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/arxiv_chk.csv", to_analyze.arxiv)

        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/acm_not_included.csv", not_included.acm)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/ieee_not_included.csv", not_included.ieee)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/science_not_included.csv", not_included.science)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/springer_not_included.csv", not_included.springer)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/wiley_not_included.csv", not_included.wiley)
        ExclusionFilter.__export_to_csv(
            f"{self.output_path}/arxiv_not_included.csv", not_included.arxiv)
