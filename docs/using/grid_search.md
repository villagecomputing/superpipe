# Grid Search
The core of Superpipe is running a grid search to optimize your pipeline.  A grid search allows you to perform a hyperparameter search over every permutation of your parameters and retrun a dataframe with cost, accuracy, and latency information.

`GridSearch` takes as inputs a pipeline and a dictionary of parameters to search over for each step.

In our [Comparing Pipelines](https://github.com/villagecomputing/superpipe/blob/main/examples/comparing_pipelines/furniture.ipynb) example, we use a grid search to search over models and number of embedding results. 

```python
from superpipe import grid_search

params_grid = {
    short_description_step.name: {
        'model': [models.gpt35, models.gpt4], 
    },
    embedding_search_step.name: {
        'k': [3, 5, 7],  
    },
    categorize_step.name: {
        'model': [models.gpt35, models.gpt4], 
    },
}


search_embeddings = grid_search.GridSearch(categorizer, params_grid)
search_embeddings.apply(df)
```
<details>
<summary>
Output
</summary>

|   | short_description__model | embedding_search__k | categorize__model  | score  | input_tokens                                                | output_tokens                                                | input_cost | output_cost | num_success | num_failure | total_latency | index                  |
|---|---------------------------|---------------------|---------------------|-------|-------------------------------------------------------------|--------------------------------------------------------------|------------|-------------|-------------|-------------|---------------|------------------------|
| 0 | gpt-3.5-turbo-0125        | 3                   | gpt-3.5-turbo-0125  | 0.833 | {'gpt-3.5-turbo-0125': 11315}                               | {'gpt-3.5-turbo-0125': 2108}                                 | 0.005657   | 0.003162    | 30          | 0           | 103.464159    | -7791233023527820859   |
| 1 | gpt-3.5-turbo-0125        | 3                   | gpt-4-turbo-preview | 0.933 | {'gpt-3.5-turbo-0125': 5852, 'gpt-4-turbo-preview': 5852}  | {'gpt-3.5-turbo-0125': 1837, 'gpt-4-turbo-preview': 1837}    | 0.057896   | 0.011756    | 30          | 0           | 82.123847     | -1229872059569985205   |
| 2 | gpt-3.5-turbo-0125        | 5                   | gpt-3.5-turbo-0125  | 0.9   | {'gpt-3.5-turbo-0125': 11824}                               | {'gpt-3.5-turbo-0125': 1998}                                 | 0.005912   | 0.002997    | 30          | 0           | 60.67743      | -2156008638839003309   |
| 3 | gpt-3.5-turbo-0125        | 5                   | gpt-4-turbo-preview | 0.967 | {'gpt-3.5-turbo-0125': 5852, 'gpt-4-turbo-preview': 5852}  | {'gpt-3.5-turbo-0125': 1792, 'gpt-4-turbo-preview': 1792}    | 0.063456   | 0.011688    | 30          | 0           | 85.082716     | -373516568509500608    |
| 4 | gpt-3.5-turbo-0125        | 7                   | gpt-3.5-turbo-0125  | 0.9   | {'gpt-3.5-turbo-0125': 12575}                               | {'gpt-3.5-turbo-0125': 2141}                                 | 0.006287   | 0.003211    | 30          | 0           | 149.574122    | 5513717612912975259    |
| 5 | gpt-3.5-turbo-0125        | 7                   | gpt-4-turbo-preview | 0.967 | {'gpt-3.5-turbo-0125': 5852, 'gpt-4-turbo-preview': 5852}  | {'gpt-3.5-turbo-0125': 1733, 'gpt-4-turbo-preview': 1733}    | 0.069126   | 0.011599    | 30          | 0           | 78.444735     | 2766483574959374285    |
| 6 | gpt-4-turbo-preview       | 3                   | gpt-3.5-turbo-0125  | 0.867 | {'gpt-4-turbo-preview': 5852, 'gpt-3.5-turbo-0125': 5852} | {'gpt-4-turbo-preview': 1836, 'gpt-3.5-turbo-0125': 1836}    | 0.061260   | 0.055532    | 30          | 0           | 138.30416     | 7602228094953899657    |
| 7 | gpt-4-turbo-preview       | 3                   | gpt-4-turbo-preview | 0.867 | {'gpt-4-turbo-preview': 11298}                             | {'gpt-4-turbo-preview': 2095}                                | 0.112980   | 0.062850    | 30          | 0           | 164.999652    | -6892174709507839108   |
| 8 | gpt-4-turbo-preview       | 5                   | gpt-3.5-turbo-0125  | 0.867 | {'gpt-4-turbo-preview': 5852, 'gpt-3.5-turbo-0125': 5852} | {'gpt-4-turbo-preview': 1803, 'gpt-3.5-turbo-0125': 1803}    | 0.061548   | 0.054541    | 30          | 0           | 140.513508    | -8924542522527535100   |
| 9 | gpt-4-turbo-preview       | 5                   | gpt-4-turbo-preview | 0.967 | {'gpt-4-turbo-preview': 11977}                             | {'gpt-4-turbo-preview': 2158}                                | 0.119770   | 0.064740    | 30          | 0           | 178.206688    | -9078237607708088845   |
|10 | gpt-4-turbo-preview       | 7                   | gpt-3.5-turbo-0125  | 0.9   | {'gpt-4-turbo-preview': 5852, 'gpt-3.5-turbo-0125': 5852} | {'gpt-4-turbo-preview': 1806, 'gpt-3.5-turbo-0125': 1806}    | 0.061864   | 0.054631    | 30          | 0           | 141.250665    | -1609701935912568703   |
|11 | gpt-4-turbo-preview       | 7                   | gpt-4-turbo-preview | 0.967 | {'gpt-4-turbo-preview': 12528}                             | {'gpt-4-turbo-preview': 2090}                                | 0.125280   | 0.062700    | 30          | 0           | 169.717205    | -7994583890545252174   |

</details>
