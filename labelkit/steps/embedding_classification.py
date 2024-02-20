from typing import Callable, Union, Dict, List, Optional
import pandas as pd
import numpy as np
from numpy.typing import NDArray
import faiss
from . import Step
from labelkit.util import append_dict_to_df


class EmbeddingClassificationStep(Step):
    """
    A step in a data processing pipeline for classifying inputs into categories using vector embeddings.

    This step takes input data, generates embeddings for it using a provided embedding function,
    and classifies these embeddings into predefined categories based on nearest neighbors search.

    Attributes:
        search_prompt (Callable[[Union[Dict, pd.Series]], str]): A function that takes a single row of data
            (as a dictionary or pandas Series) and returns a search prompt string.

        embed (Callable[[List[str]], NDArray[np.float32]]): A function that takes a list of strings (search prompts)
            and returns their embeddings as a numpy array.

        categories (List[str]): A list of category names corresponding to the embeddings.

        k (Optional[int]): The number of nearest neighbors to consider for classification. Defaults to 5.

        name (Optional[str]): An optional name for the step. Defaults to None.

    Methods:
        __init__: Initializes the step with necessary functions, categories, and other parameters.
        update_params: Updates parameters of the step and rebuilds the index if necessary.
        apply: Applies the classification step to input data, either a pandas DataFrame or a dictionary.
    """

    DEFAULT_K = 5

    def __init__(self,
                 search_prompt: Callable[[Union[Dict, pd.Series]], str],
                 embed: Callable[[List[str]], NDArray[np.float32]],
                 categories: List[str],
                 k: Optional[int] = DEFAULT_K,
                 name=None):
        """
        Initializes the embedding classification step with the necessary functions, categories, and parameters.

        Parameters:
            search_prompt (Callable[[Union[Dict, pd.Series]], str]): Function to generate search prompts from data.

            embed (Callable[[List[str]], NDArray[np.float32]]): Function to generate embeddings from search prompts.

            categories (List[str]): List of category names for classification.

            k (Optional[int]): Number of nearest neighbors to use for classification. Defaults to 5.

            name (Optional[str]): Optional name for the step.
        """
        super().__init__(name)
        self.search_prompt = search_prompt
        self.embed = embed
        self.categories = categories
        self.k = k
        self.categories = categories
        self.index = self._create_index(categories)

    # TODO: dynamically construct pydantic model to validate params
    def update_params(self, params: Dict):
        """
        Updates the parameters of the step and rebuilds the index if necessary.

        Parameters:
            params (Dict): A dictionary of parameters to update. Currently supports updating 'embed' and 'categories'.
        """
        super().update_params(params)
        if "embed" in params or "categories" in params:
            self.index = self._create_index(self.categories)

    def _create_index(self, texts: List[str]):
        """
        Creates a FAISS index for efficient nearest neighbor search of embeddings.

        Parameters:
            texts (List[str]): A list of texts to create embeddings for and add to the index.

        Returns:
            faiss.IndexFlatL2: A FAISS index with added embeddings.
        """
        embed = self.embed
        embeddings = embed(texts)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        return index

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        pass

    def apply(self, data: Union[pd.DataFrame, Dict]):
        """
        Applies the classification step to input data.

        This method generates embeddings for the input data, performs nearest neighbor search to classify these
        embeddings into categories, and appends the classification results to the input data.

        Parameters:
            data (Union[pd.DataFrame, Dict]): The input data to classify. Can be a pandas DataFrame or a dictionary.

        Returns:
            Union[pd.DataFrame, Dict]: The input data with appended classification results.
        """
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
