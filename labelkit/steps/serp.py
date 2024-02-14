from typing import Callable, Union, Dict
import os
import requests
import json
import pandas as pd
from .step import Step


class SERPEnrichmentStep(Step):
    def __init__(self,
                 prompt: Callable[[Union[pd.Series, Dict]], str],
                 postprocess=None,
                 name=None):
        # TODO: currently base step expects out_model to be passed, but it is not needed here
        super().__init__(None, name, prompt=prompt, postprocess=postprocess)

    def _get_search_results(self, q):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": q})
        headers = {
            'X-API-KEY': os.environ.get("SERPAPI_API_KEY"),
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def apply(self, data: Union[pd.DataFrame, Dict]):
        prompt = self.params.get('prompt')
        postprocess = self.params.get('postprocess')
        if isinstance(data, pd.DataFrame):
            data[self.name] = data.apply(prompt, axis=1).apply(
                self._get_search_results)
            if postprocess is not None:
                data[self.name] = data[self.name].apply(
                    postprocess)
        else:
            data[self.name] = self._get_search_results(prompt(data))
            if postprocess is not None:
                data[self.name] = postprocess(data[self.name])
        return data
