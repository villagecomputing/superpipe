# Embedding Classification Step

The `EmbeddingSearchStep` is used to embed a list of strings and search over them.

The list of strings can either be fixed and provided upon initialization in the `candidates` argument, or can be generated dynamically from each input row by passing in the `candidates_fn` argument which returns a list of strings.

In either case, the candidates will be embedded and saved to an in memory vector store using `faiss`. You can provide whatever embedding function you want in the `embed_fn` argument, for example Cohere, OpenAI, or custom embeddings.

The `k` value determines the number of embeddings returned and is often a parameter you may want to permute in a grid search.

For best results, it is best to provide a `search_prompt` that is dense with identifying information about the category.

## Example

In this example we use Cohere to embed our categories and search over them with a "short description" that we generated with a previous step.

```python
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

def embed(texts: List[str]):
  embeddings = co.embed(
    model="embed-english-v3.0",
    texts=texts,
    input_type='classification'
  ).embeddings
  return np.array(embeddings).astype('float32')

embedding_search_prompt = lambda row: row["short_description"]

embedding_search_step = steps.EmbeddingSearchStep(
  search_prompt= embedding_search_prompt,
  embed=embed,
  k=5,
  candidates=taxonomy,
  name="embedding_search"
)
```

See this [example](https://github.com/villagecomputing/superpipe/blob/main/examples/product_categorization/product_categorization.ipynb) for a full walkthrough.
