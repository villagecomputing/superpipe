# SERP Step
The `SERPStep` uses [serper.dev](https://serper.dev/) to enrich data for your pipeline via Google search. 

The `SERPStep` takes a search prompt, name and an optional post processing function as inputs. 

The post processing function is useful if only some of the search content is relevant for your pipeline. For example, Serper will return "Knowledge Graph" content about entities Google knows about that can be very useful. 


## Example
```python
def shorten(x):
    short = []
    kgi = json.loads(x).get('knowledgeGraph')
    if kgi is None:
        short.append(kgi)
    else:
        kg = {'title': kgi.get('title'), 'type': kgi.get(
            'type'), 'description': kgi.get('description')},
        short.append(kg)
    y = json.loads(x).get('organic')
    if y is None:
        return None
    for o in y[:3]:
        short.append({
            'title': o['title'],
            'snippet': o['snippet'],
            'link': o['link']
        })
    return short


def serp_prompt(row):
    name = row['name']
    street = row['address']['street']
    city = row['address']['city']
    state = row['address']['state']
    zip = row['address']['zip']
    return f"Review for {name} located at {street} {city} {state} {str(zip)}"


serp_step = steps.SERPEnrichmentStep(
  prompt=serp_prompt,
  postprocess=shorten,
  name="serp")
```