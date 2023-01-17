class Article:
    title: str
    url: str
    abstract: str
    doi: str

    def __init__(self, title: str, url: str, abstract: str, doi: str) -> None:
        self.title = title
        self.url = url
        self.abstract = abstract
        self.doi = doi
