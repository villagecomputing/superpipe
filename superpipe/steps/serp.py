import os
import requests
import json
import pandas as pd
from typing import Callable, Union, Optional, Dict
from superpipe.steps.step import Step


class SERPEnrichmentStep(Step):
    """
    A step in a SuperPipe pipeline to enrich data with Search Engine Results Page (SERP) data.

    This step uses a provided prompt function to generate search queries from input data, fetches the search
    results, and optionally applies a post-processing function to the results.

    Attributes:
        prompt (Callable[[Union[pd.Series, Dict]], str]): A callable that generates a search query string from
            a row of data.
        postprocess (Optional[Callable[[str], str]]): An optional callable for post-processing the search results.
        name (Optional[str]): An optional name for the step.

    Methods:
        _get_search_results(q: str) -> str: Fetches search results for a given query string.
        _apply(row: Union[pd.Series, Dict]) -> Dict: Applies the SERP enrichment step to a single row of data.
    """

    def __init__(self,
                 prompt: Callable[[Union[pd.Series, Dict]], str],
                 postprocess: Optional[Callable[[str], str]] = None,
                 name=None):
        """
        Initializes the SERPEnrichmentStep with a prompt function, an optional postprocess function, and an optional name.

        Args:
            prompt (Callable[[Union[pd.Series, Dict]], str]): A callable that generates a search query string from
                a row of data.
            postprocess (Optional[Callable[[str], str]]): An optional callable for post-processing the search results.
            name (Optional[str]): An optional name for the step.
        """
        super().__init__(name)
        self.prompt = prompt
        self.postprocess = postprocess

    def _get_search_results(self, q):
        """
        Fetches search results for a given query string.

        Args:
            q (str): The search query string.

        Returns:
            str: The search results.
        """
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": q})
        headers = {
            'X-API-KEY': os.environ.get("SERPAPI_API_KEY"),
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        """
        Applies the SERP enrichment step to a single row of data.

        This method generates a search query using the prompt function, fetches the search results,
        optionally applies a post-processing function, and returns the results in a dictionary.

        Args:
            row (Union[pd.Series, Dict]): A single row of data, either as a pandas Series or a dictionary.

        Returns:
            Dict: A dictionary containing the enriched data.
        """
        prompt = self.prompt
        postprocess = self.postprocess
        result = self._get_search_results(prompt(row))
        if postprocess is not None:
            result = postprocess(result)
        return {
            self.name: result
        }
