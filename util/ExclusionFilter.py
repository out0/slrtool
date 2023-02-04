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

    sources = [
        "acm",
        "ieee",
        "science",
        "springer",
        "wiley",
        "mdpi",
        "arxiv"
    ]

    def __init__(self, filter_articles_config: dict, unfiltered_path: str, output_filtered_path: str):
        self.output_path = output_filtered_path
        self.filter_articles_config = filter_articles_config

        self.unique = ArticleDatabase()

        for source in self.sources:
            self.unique.set(source,  ArticleCSVReader.import_from_csv(f"{unfiltered_path}/{source}.csv"))

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
            unique.get("ieee"), unique.get("science"))
        ExclusionFilter.__dedup_message("ieee", "science", science_dup)

        duplicated.get("science").extend(science_dup)
        unique.set("science", science_nondup)

    def __dedup_acm(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        acm_dup, acm_nondup = ExclusionFilter.__filter_dedup(
            unique.get("ieee"), unique.get("acm"))
        ExclusionFilter.__dedup_message("ieee", "acm", acm_dup)
        duplicated.get("acm").extend(acm_dup)

        acm_dup, acm_nondup = ExclusionFilter.__filter_dedup(
            unique.get("science"), acm_nondup)
        ExclusionFilter.__dedup_message("science", "acm", acm_dup)
        duplicated.get("acm").extend(acm_dup)

        unique.set("acm", acm_nondup)

    def __dedup_springer(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        springer_dup, springer_nondup = ExclusionFilter.__filter_dedup(
            unique.get("ieee"), unique.get("springer"))
        ExclusionFilter.__dedup_message("ieee", "springer", springer_dup)
        duplicated.get("springer").extend(springer_dup)

        springer_dup, springer_nondup = ExclusionFilter.__filter_dedup(
            unique.get("science"), springer_nondup)
        ExclusionFilter.__dedup_message("science", "springer", springer_dup)
        duplicated.get("springer").extend(springer_dup)

        springer_dup, springer_nondup = ExclusionFilter.__filter_dedup(
            unique.get("acm"), springer_nondup)
        ExclusionFilter.__dedup_message("acm", "springer", springer_dup)
        duplicated.get("springer").extend(springer_dup)

        unique.set("springer", springer_nondup)

    def __dedup_wiley(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.get("ieee"), unique.get("wiley"))
        ExclusionFilter.__dedup_message("ieee", "wiley", wiley_dup)
        duplicated.get("wiley").extend(wiley_dup)

        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.get("science"), wiley_nondup)
        ExclusionFilter.__dedup_message("science", "wiley", wiley_dup)
        duplicated.get("wiley").extend(wiley_dup)

        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.get("acm"), wiley_nondup)
        ExclusionFilter.__dedup_message("acm", "wiley", wiley_dup)
        duplicated.get("wiley").extend(wiley_dup)

        wiley_dup, wiley_nondup = ExclusionFilter.__filter_dedup(
            unique.get("springer"), wiley_nondup)
        ExclusionFilter.__dedup_message("springer", "wiley", wiley_dup)
        duplicated.get("wiley").extend(wiley_dup)

        unique.set("wiley", wiley_nondup)

    def __dedup_mdpi(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        mdpi_dup, mdpi_nondup = ExclusionFilter.__filter_dedup(
            unique.get("ieee"), unique.get("mdpi"))
        ExclusionFilter.__dedup_message("ieee", "mdpi", mdpi_dup)
        duplicated.get("mdpi").extend(mdpi_dup)

        mdpi_dup, mdpi_nondup = ExclusionFilter.__filter_dedup(
            unique.get("science"), mdpi_nondup)
        ExclusionFilter.__dedup_message("science", "mdpi", mdpi_dup)
        duplicated.get("mdpi").extend(mdpi_dup)

        mdpi_dup, mdpi_nondup = ExclusionFilter.__filter_dedup(
            unique.get("acm"), mdpi_nondup)
        ExclusionFilter.__dedup_message("acm", "mdpi", mdpi_dup)
        duplicated.get("mdpi").extend(mdpi_dup)

        mdpi_dup, mdpi_nondup = ExclusionFilter.__filter_dedup(
            unique.get("springer"), mdpi_nondup)
        ExclusionFilter.__dedup_message("springer", "mdpi", mdpi_dup)
        duplicated.get("mdpi").extend(mdpi_dup)

        mdpi_dup, mdpi_nondup = ExclusionFilter.__filter_dedup(
            unique.get("wiley"), mdpi_nondup)
        ExclusionFilter.__dedup_message("wiley", "mdpi", mdpi_dup)
        duplicated.get("mdpi").extend(mdpi_dup)

        unique.set("mdpi", mdpi_nondup)


    def __dedup_arxiv(unique: ArticleDatabase, duplicated: ArticleDatabase) -> None:
        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.get("ieee"), unique.get("arxiv"))
        ExclusionFilter.__dedup_message("ieee", "arxiv", arxiv_dup)
        duplicated.get("arxiv").extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.get("science"), arxiv_nondup)
        ExclusionFilter.__dedup_message("science", "arxiv", arxiv_dup)
        duplicated.get("arxiv").extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.get("acm"), arxiv_nondup)
        ExclusionFilter.__dedup_message("acm", "arxiv", arxiv_dup)
        duplicated.get("arxiv").extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.get("springer"), arxiv_nondup)
        ExclusionFilter.__dedup_message("springer", "arxiv", arxiv_dup)
        duplicated.get("arxiv").extend(arxiv_dup)

        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.get("wiley"), arxiv_nondup)
        ExclusionFilter.__dedup_message("wiley", "arxiv", arxiv_dup)
        duplicated.get("arxiv").extend(arxiv_dup)


        arxiv_dup, arxiv_nondup = ExclusionFilter.__filter_dedup(
            unique.get("mdpi"), arxiv_nondup)
        ExclusionFilter.__dedup_message("mdpi", "arxiv", arxiv_dup)
        duplicated.get("arxiv").extend(arxiv_dup)

        unique.set("arxiv", arxiv_nondup)


    def __dedup_self(self, db: ArticleDatabase) -> int:
        dup_lst: List[Article] = []

        for source in self.sources:
            [dup, res] = ExclusionFilter.__filter_dedup_self(db.get(source))
            db.set(source, res)
            dup_lst.extend(dup)

        return len(dup_lst)

    def __apply_filter_remove(self, keys: List[str], unique: ArticleDatabase, remove_func: Callable) -> ArticleDatabase:
        removed = ArticleDatabase()

        for source in self.sources:
            removed_lst, unique_lst = remove_func(keys, unique.get(source))
            removed.set(source, removed_lst)
            unique.set(source, unique_lst)
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

    def exportArticleDatabase(self, sufix: str, db: ArticleDatabase) -> None:        
        for source in self.sources:
            ExclusionFilter.__export_to_csv(
                f"{self.output_path}/{source}{sufix}.csv", db.get(source))

    def filter(self) -> None:
        os.system(f"rm -rf {self.output_path}")
        os.system(f"mkdir -p {self.output_path}")

        print(f"Initial total {len(self.unique)} articles")

        duplicated = ArticleDatabase()

        num_self_dup = self.__dedup_self(self.unique)
        ExclusionFilter.__dedup_science(self.unique, duplicated)
        ExclusionFilter.__dedup_acm(self.unique, duplicated)
        ExclusionFilter.__dedup_springer(self.unique, duplicated)
        ExclusionFilter.__dedup_wiley(self.unique, duplicated)
        ExclusionFilter.__dedup_mdpi(self.unique, duplicated)
        ExclusionFilter.__dedup_arxiv(self.unique, duplicated)
        print(f"removed from deduplication: {len(duplicated) + num_self_dup}")

        not_included = self.__apply_filter_remove(
            self.filter_articles_config["include_key"], self.unique, ExclusionFilter.__apply_filter_include_source)
        print(
            f"keywords filter: ignored for not having the keywords {len(not_included)} articles")

        removed_doi = self.__apply_filter_remove(
            self.filter_articles_config["remove_doi"], self.unique, ExclusionFilter.__apply_filter_remove_doi_source)
        print(f"DOI filter: ignored {len(removed_doi)} articles")

        removed_doi = self.__apply_filter_remove(
            self.filter_articles_config["revised_doi"], self.unique, ExclusionFilter.__apply_filter_remove_doi_source)
        print(f"DOI filter of the already revised: ignored {len(removed_doi)} articles")


        removed = self.__apply_filter_remove(
            self.filter_articles_config["remove_key"], self.unique, ExclusionFilter.__apply_filter_remove_source)
        print(f"keywords filter: removed {len(removed)} articles")

        to_analyze = self.__apply_filter_remove(
            self.filter_articles_config["analyze_key"], self.unique, ExclusionFilter.__apply_filter_remove_source)
        print(
            f"keywords filter: removed for analisys {len(to_analyze)} articles")

        print(f"Remaining:{len(self.unique)} articles")

        self.exportArticleDatabase("", db=self.unique)
        self.exportArticleDatabase("_del", db=removed)
        self.exportArticleDatabase("_chk", db=to_analyze)
        self.exportArticleDatabase("_not_included", db=not_included)
