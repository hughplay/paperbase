from typing import Dict
import arxiv


class PDFToolkit:

    def __init__(self) -> None:
        pass

    def url2info(self, url) -> dict:
        return self.arxiv_id2info(self.get_arxiv_id(url))

    def get_arxiv_id(self, url) -> str:
        LEN_ARXIV_ID = 9
        arxiv_id = ''
        try:
            arxiv_id = url.split('/')[-1][:(LEN_ARXIV_ID + 1)]
        except:
            pass
        return arxiv_id

    def arxiv_id2info(self, arxiv_id) -> dict:
        info = {}
        try :
            paper = next(arxiv.Search(id_list=[arxiv_id]).get())
            info = {
                'title': paper.title,
                'year': paper.published.year,
                'authors': [author.name for author in paper.authors]
            }
        except:
            pass
        return info