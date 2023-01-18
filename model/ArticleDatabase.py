from typing import List, Tuple

from Article import *

class ArticleDatabase:
    acm: List[Article]
    ieee: List[Article]
    science: List[Article]
    springer: List[Article]
    wiley: List[Article]

    def __init__(self, acm: List[Article], ieee: List[Article], science: List[Article], springer: List[Article], wiley: List[Article]) -> None:
        self.acm = acm
        self.ieee = ieee
        self.science = science
        self.springer = springer
        self.wiley = wiley

    def __len__(self) -> int:
        return len(self.acm) + len(self.ieee) + len(self.science) + len(self.springer) + len(self.wiley)


