from typing import Union, Dict, Callable, List
import pandas as pd
import numpy as np
from numpy.typing import NDArray
import faiss
from . import Step
from labelkit.util import append_dict_to_df


class EmbeddingClassificationStep(Step):
    def __init__(self,
                 taxonomy,
                 search_prompt: Callable[[Union[pd.Series, Dict]], str],
                 embed: Callable[[List[str]], NDArray[np.float32]],
                 k=5,
                 name=None):
        super().__init__(name, search_prompt=search_prompt, embed=embed, k=k)
        self.taxonomy = taxonomy
        self.index = self._create_index(taxonomy)

    def update_params(self, params):
        super().update_params(params)
        if "embed" in params:
            self.index = self._create_index(self.taxonomy)

    def _create_index(self, texts):
        embed = self.params.get('embed')
        embeddings = embed(texts)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        return index

    def apply(self, data: Union[pd.DataFrame, Dict]):
        embed = self.params.get('embed')
        k = self.params.get('k')
        search_prompt = self.params.get('search_prompt')

        if isinstance(data, pd.DataFrame):
            texts = list(data.apply(search_prompt, axis=1))
        else:
            texts = [search_prompt(data)]
        embeddings = embed(texts)
        D, I = self.index.search(embeddings, k)
        categories = [{f"category{i+1}": self.taxonomy[x[i]]
                       for i in range(k)} for x in I.tolist()]
        if isinstance(data, pd.DataFrame):
            append_dict_to_df(data, categories)
        else:
            data.update(categories[0])
        return data
