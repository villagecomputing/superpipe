# Steps

At a high level Superpipe works by taking input data and transforming it in steps to get the desired output. Each step takes in an input dataframe or Python dictionary and returns a new dataframe or dictionary with the outputs of the step appended.

## Built in steps

Superpipe comes with a handful of built-in steps that you can use to build your pipelines.

- [LLM Step](./LLMStep.md) - Standard LLM calls with a single output.
- [Structured LLM Step](./LLMStructuredStep.md) - LLM calls with structured output.
- [SERP Step](./SERPStep.md) - Enrich data with Google Search.
- [Embedding Search Step](EmbeddingSearchStep.md) - Embed strings and search over them.

## Custom Steps

It's easy (and recommended) to create your own steps by subclassing [Custom Step](./CustomStep.md). This allows you to do pretty much anything inside a step - call a third party api, lookup a DB, etc.
