from typing import Callable, Union, Dict, List, Optional
import pandas as pd
import numpy as np
from numpy.typing import NDArray
import faiss
from superpipe.steps.step import Step, StepResult
from superpipe.steps.utils import with_statistics


class EmbeddingSearchStep(Step):
    """
    A step in a data processing pipeline for classifying inputs into candidates using vector embeddings.

    This step takes input data, generates embeddings for it using a provided embedding function,
    and classifies these embeddings into predefined candidates based on nearest neighbors search.

    Attributes:
        search_prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes a single row of data
            (as a dictionary or pandas Series) and returns a search prompt string.

        embed (Callable[[List[str]], NDArray[np.float32]]): A function that takes a list of strings (search prompts)
            and returns their embeddings as a numpy array.

        candidates (List[str]): A list of category names corresponding to the embeddings.

        k (Optional[int]): The number of nearest neighbors to consider for classification. Defaults to 5.

        name (Optional[str]): An optional name for the step. Defaults to None.

    Methods:
        __init__: Initializes the step with necessary functions, candidates, and other parameters.
        update_params: Updates parameters of the step and rebuilds the index if necessary.
        run: Applies the classification step to input data, either a pandas DataFrame or a dictionary.
    """

    DEFAULT_K = 5

    def __init__(self,
                 search_prompt: Callable[[Union[Dict, pd.Series]], str],
                 embed_fn: Callable[[List[str]], NDArray[np.float32]],
                 candidates: Optional[List[str]] = None,
                 candidates_fn: Optional[Callable[[
                     Union[Dict, pd.Series]], List[str]]] = None,
                 k: Optional[int] = DEFAULT_K,
                 name=None):
        """
        Initializes the embedding classification step with the necessary functions, candidates, and parameters.

        Parameters:
            search_prompt (Callable[[Union[Dict, pd.Series]], str]): Function to generate search prompts from data.

            embed (Callable[[List[str]], NDArray[np.float32]]): Function to generate embeddings from search prompts.

            candidates (List[str]): List of category names for classification.

            k (Optional[int]): Number of nearest neighbors to use for classification. Defaults to 5.

            name (Optional[str]): Optional name for the step.
        """
        super().__init__(name)
        self.search_prompt = search_prompt
        self.embed_fn = embed_fn
        self.candidates = candidates
        self.candidates_fn = candidates_fn
        self.k = k
        if self.candidates:
            self.index = self._create_index(candidates)
        elif self.candidates_fn:
            self.index = None
        else:
            raise ValueError(
                "Either candidates or candidates_fn must be provided")

    def get_params(self):
        """
        Returns the parameters of the step.

        Returns:
            Dict: A dictionary of the step's parameters.
        """
        return {
            **super().get_params(),
            "search_prompt": self.search_prompt.__name__,
            "embed_fn": self.embed_fn.__name__,
            "candidates": self.candidates.__hash__() if self.candidates else None,
            "candidates_fn": self.candidates_fn.__name__ if self.candidates_fn else None,
            "k": self.k
        }

    def update_params(self, params: Dict):
        """
        Updates the parameters of the step and rebuilds the index if embed_fn or candidates are updated.

        Parameters:
            params (Dict): A dictionary of parameters to update.
        """
        super().update_params(params)
        if ("embed_fn" in params or "candidates" in params) \
                and self.candidates:
            self.index = self._create_index(self.candidates)

    def _create_index(self, texts: List[str]):
        """
        Creates a FAISS index for efficient nearest neighbor search of embeddings.

        Parameters:
            texts (List[str]): A list of texts to create embeddings for and add to the index.

        Returns:
            faiss.IndexFlatL2: A FAISS index with added embeddings.
        """
        embeddings = self.embed_fn(texts)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        return index

    def _run(self, row: Union[pd.Series, Dict]) -> StepResult:
        def run_search():
            if self.candidates_fn:
                candidates = self.candidates_fn(row)
                index = self._create_index(candidates)
            else:
                candidates = self.candidates
                index = self.index
            prompt = self.search_prompt(row)
            embeddings = self.embed_fn([prompt])
            D, I = index.search(embeddings, self.k)
            search_results = I.tolist()[0]
            result = {
                f"category{i+1}": candidates[search_results[i]] for i in range(self.k)}
            return result
        result, statistics = with_statistics(run_search)()
        return StepResult(fields=result, statistics=statistics)
