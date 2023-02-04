from typing import List, Tuple

from Article import *


class ArticleDatabase:
    source: dict

    def __init__(self, 
        acm: List[Article] = [], 
        ieee: List[Article] = [], 
        science: List[Article] = [], 
        springer: List[Article] = [], 
        wiley: List[Article] = [], 
        mdpi: List[Article] = [], 
        arxiv: List[Article] = []) -> None:
        
        self.source = {
            "acm": acm,
            "ieee": ieee,
            "science": science,
            "springer": springer,
            "wiley": wiley,
            "mdpi": mdpi,
            "arxiv": arxiv
        }

    def get(self, key:str) -> List[Article]:
        return self.source[key]

    def set(self, key:str, data:List[Article]) -> None:
        self.source[key] = data

    def __len__(self) -> int:
        res:int = 0
        for _, val in self.source.items():
            res += len(val)
        return res
