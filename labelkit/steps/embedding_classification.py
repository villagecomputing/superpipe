from typing import TypedDict, Callable, Union, Dict, List, Optional
import pandas as pd
import numpy as np
from numpy.typing import NDArray
import faiss
from . import Step
from labelkit.util import append_dict_to_df, validate_dict


class EmbeddingClassificationStep(Step):
    DEFAULT_K = 5

    def __init__(self,
                 search_prompt: Callable[[Union[Dict, pd.Series]], str],
                 embed: Callable[[List[str]], NDArray[np.float32]],
                 categories: List[str],
                 k: Optional[int] = DEFAULT_K,
                 name=None):
        super().__init__(name)
        self.search_prompt = search_prompt
        self.embed = embed
        self.categories = categories
        self.k = k
        self.categories = categories
        self.index = self._create_index(categories)

    # TODO: dynamically construct pydantic model to validate params
    def update_params(self, params: Dict):
        super().update_params(params)
        if "embed" in params or "categories" in params:
            self.index = self._create_index(self.categories)

    def _create_index(self, texts: List[str]):
        embed = self.embed
        embeddings = embed(texts)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        return index

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        pass

    def apply(self, data: Union[pd.DataFrame, Dict]):
        embed = self.embed
        k = self.k
        search_prompt = self.search_prompt

        if isinstance(data, pd.DataFrame):
            texts = list(data.apply(search_prompt, axis=1))
        else:
            texts = [search_prompt(data)]
        embeddings = embed(texts)
        D, I = self.index.search(embeddings, k)
        categories = [{f"category{i+1}": self.categories[x[i]]
                       for i in range(k)} for x in I.tolist()]
        if isinstance(data, pd.DataFrame):
            append_dict_to_df(data, categories)
        else:
            data.update(categories[0])
        return data
