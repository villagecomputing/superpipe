# Custom step

Custom steps allow you to implement arbitrary python in your pipeline.

Custom steps require a function, called a `transform` as well as pydandic model that defines the output schema. Optionally you can provide a name.

The logic really can be arbitrary, including API calls, Langchain chains, local generative models or simple data cleaning.

## Example

This is an extremely simple custom step, implemented merely as a lambda function.

```python
select_category_step = steps.CustomStep(
  transform=lambda row: row[f'category{row["category_index"]}'],
  name="select_category"
)
```

### API call as a custom step

In this example we wrap an API call in a custom step. The result will be three new columns to our dataframe as defined by the pydantic model.

```python
import json
from datetime import datetime
import requests
from pydantic import BaseModel, Field

api_key = 'API_KEY'

def get_linkedin_data(profile, api_key=api_key):

    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    params = {
        'linkedin_profile_url': 'https://www.linkedin.com/in/{profile}/',
        'extra': 'include',
        'github_profile_id': 'include',
        'facebook_profile_id': 'include',
        'twitter_profile_id': 'include',
        'personal_contact_number': 'include',
        'personal_email': 'include',
        'inferred_salary': 'include',
        'skills': 'include',
        'use_cache': 'if-present',
        'fallback_to_cache': 'on-error',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)

    # JSON string provided
    json_str = response.content

    # Load the JSON string into a Python dictionary
    profile = json.loads(json_str)

    # Extract occupation
    headline = profile.get('headline', 'Not provided')

    # Extract the most recent job
    experiences = profile.get('experiences', [])
    most_recent_job = experiences[0] if experiences else 'Not provided'

    # Calculate years of work experience since college
    education = profile.get('education', [])
    college_graduation_year = None
    for edu in education:
        if 'Bachelor' in edu.get('degree_name', ''):
            college_graduation_year = edu.get('ends_at', {}).get('year')
            break

    years_of_experience = datetime.now().year - college_graduation_year if college_graduation_year else 'Not provided'

    return({'headline': headline, 'most_recent_job': most_recent_job.get('title'), 'years_of_experience': years_of_experience})

linkedin_step = steps.CustomStep(
    transform=get_linkedin_data,
    name='linkedin'
)

```
