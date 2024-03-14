# Embedding Classification Step
The `EmbeddingClassificationStep` is used to embed categories and search over them and is built with classification in mind. 

Upon initilaization, the set of provided categories will be embedded and saved to an in memory vector store using `faiss`. You can provide whatever embedding function you want, for example Cohere, OpenAI, or custom embeddings. 

The `k` value determines the number of embeddings returned and is often a parameter you may want to permute in a grid search. 

For best results, it is best to provide a `search_prompt` that is dense with indentifying infromation about the category. 



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

embedding_search_step = steps.EmbeddingClassificationStep(
  search_prompt= embedding_search_prompt,
  embed=embed,
  k=5,    
  categories=taxonomy,
  name="embedding_search"
)
```

See this [example](https://github.com/villagecomputing/superpipe/blob/main/examples/product_categorization/product_categorization.ipynb) for a full walkthrough. 