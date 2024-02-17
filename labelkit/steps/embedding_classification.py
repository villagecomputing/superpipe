from typing import TypedDict, Callable, Union, Dict, List, Optional
import pandas as pd
import numpy as np
from numpy.typing import NDArray
import faiss
from . import Step
from labelkit.util import append_dict_to_df, validate_dict


class EmbeddingClassificationParams(TypedDict, total=False):
    search_prompt: Callable[[Union[Dict, pd.Series]], str]
    embed: Callable[[List[str]], NDArray[np.float32]]
    k: Optional[int]


class EmbeddingClassificationStep(Step):
    DEFAULT_K = 5

    def __init__(self,
                 params: EmbeddingClassificationParams,
                 categories: List[str],
                 name=None):
        super().__init__(name)
        validate_dict(params, EmbeddingClassificationParams)
        self.params = params
        self.categories = categories
        self.index = self._create_index(categories)

    def update_params(self, params):
        super().update_params(params)
        if "embed" in params:
            self.index = self._create_index(self.categories)

    def _create_index(self, texts):
        embed = self.params['embed']
        embeddings = embed(texts)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        return index

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        pass

    def apply(self, data: Union[pd.DataFrame, Dict]):
        embed = self.params['embed']
        k = self.params.get('k', self.DEFAULT_K)
        search_prompt = self.params['search_prompt']

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
