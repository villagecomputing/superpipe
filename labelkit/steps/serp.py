import os
import requests
import json
import pandas as pd
from typing import TypedDict, Callable, Union, Optional, Dict
from .step import Step
from labelkit.util import validate_dict


class SERPEnrichmentParams(TypedDict, total=False):
    prompt: Callable[[Union[pd.Series, Dict]], str]
    postprocess: Optional[Callable[[str], str]]


class SERPEnrichmentStep(Step):
    def __init__(self,
                 params: SERPEnrichmentParams,
                 name=None):
        super().__init__(name)
        validate_dict(params, SERPEnrichmentParams)
        self.params = params

    def _get_search_results(self, q):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": q})
        headers = {
            'X-API-KEY': os.environ.get("SERPAPI_API_KEY"),
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def _apply(self, row: Union[pd.Series, Dict]) -> Dict:
        prompt = self.params['prompt']
        postprocess = self.params.get('postprocess')
        result = self._get_search_results(prompt(row))
        if postprocess is not None:
            result = postprocess(result)
        return {
            self.name: result
        }
