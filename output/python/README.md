# LabelkitApp Python SDK 1.0.0

A Python SDK for LabelkitApp.

- API version: 1.0
- SDK version: 1.0.0

## Table of Contents

- [Installation](#installation)
- [Using Union Types in Function Parameters](#using-union-types-in-function-parameters)
- [Services](#services)

## Installation

```bash
pip install labelkit_app
```

## Using Union Types in Function Parameters

In Python, a parameter can be annotated with a Union type, indicating it can accept values of multiple types.

### Passing Instances or Dictionaries

When we have a model such as:

```py
ParamType = Union[TypeA, TypeB]
```

utilized in a service as follows

```py
def service_method(param: ParamType):
    # Function implementation
```

You can call `service_method` with an instance of `TypeA`, `TypeB`, or a dictionary that can be converted to an instance of either type.

```python
type_a = TypeA(key="value")
type_b = TypeB(key="value")

sdk.service.service_method(type_a)
sdk.service.service_method(type_b)
sdk.service.service_method({"key": "value"})
```

### Note on Union Instances

You cannot create an instance of a Union type itself. Instead, pass an instance of one of the types in the Union, or a dictionary that can be converted to one of those types.

## Services

A list of all SDK services. Click on the service name to access its corresponding service methods.

| Service                                 |
| :-------------------------------------- |
| [DatasetService](#datasetservice)       |
| [ExperimentService](#experimentservice) |

### DatasetService

A list of all methods in the `DatasetService` service. Click on the method name to view detailed information about that method.

| Methods                                   | Description                                             |
| :---------------------------------------- | :------------------------------------------------------ |
| [add_dataset_data](#add_dataset_data)     | Inserts data into a dataset                             |
| [get_dataset_data](#get_dataset_data)     | Retrieve the details of a specific dataset by its Id.   |
| [list_datasets](#list_datasets)           | Retrieves a list of datasets and their total row counts |
| [initialize_dataset](#initialize_dataset) | Initializes a new dataset.                              |
| [upload_dataset](#upload_dataset)         | Uploads a dataset file and its associated data          |

#### **add_dataset_data**

Inserts data into a dataset

- HTTP Method: `POST`
- Endpoint: `/api/dataset/{datasetId}/addData`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| request_body | AddDataPayload | ✅ | The request body. |
| datasetId | str | ✅ | Inserts data into a dataset |

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment
from labelkit_app.models import AddDataPayload

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

request_body = AddDataPayload(**{
    "dataset_id": "datasetId",
    "dataset_rows": [
        {}
    ]
})

result = sdk.dataset.add_dataset_data(
    request_body=request_body,
    dataset_id="datasetId"
)

print(result)
```

#### **get_dataset_data**

Retrieve the details of a specific dataset by its Id.

- HTTP Method: `GET`
- Endpoint: `/api/dataset/{datasetId}`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| datasetId | str | ✅ | Retrieve the details of a specific dataset by its Id. |

**Return Type**

`DatasetViewResponse`

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

result = sdk.dataset.get_dataset_data(dataset_id="datasetId")

print(result)
```

#### **list_datasets**

Retrieves a list of datasets and their total row counts

- HTTP Method: `GET`
- Endpoint: `/api/dataset/list`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|

**Return Type**

`List[DatasetListResponse]`

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

result = sdk.dataset.list_datasets()

print(result)
```

#### **initialize_dataset**

Initializes a new dataset.

- HTTP Method: `POST`
- Endpoint: `/api/dataset/new`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| request_body | NewDatasetPayload | ✅ | The request body. |

**Return Type**

`NewDatasetResponse`

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment
from labelkit_app.models import NewDatasetPayload

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

request_body = NewDatasetPayload(**{
    "dataset_name": "datasetName",
    "columns": [
        "columns"
    ],
    "ground_truths": [
        "groundTruths"
    ]
})

result = sdk.dataset.initialize_dataset(request_body=request_body)

print(result)
```

#### **upload_dataset**

Uploads a dataset file and its associated data

- HTTP Method: `POST`
- Endpoint: `/api/dataset/upload`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| request_body | dict | ✅ | The request body. |

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment
from labelkit_app.models import UploadDatasetPayload

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

request_body = {
    "dataset_data": {
        "dataset_title": "datasetTitle",
        "ground_truth_column_index": 9,
        "blank_column_title": "blankColumnTitle"
    },
    "file": "file"
}

result = sdk.dataset.upload_dataset(request_body=request_body)

print(result)
```

### ExperimentService

A list of all methods in the `ExperimentService` service. Click on the method name to view detailed information about that method.

| Methods                                         | Description                                                                                     |
| :---------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| [insert_experiment_row](#insert_experiment_row) | Ensures the experiment is created and inserts the given steps as a row for the given experiment |
| [get_experiment_data](#get_experiment_data)     | Fetches the details of an experiment with the specified Id.                                     |
| [list_experiments](#list_experiments)           | List all experiments                                                                            |
| [declare_experiment](#declare_experiment)       | Declare a new experiment for a given dataset Id                                                 |

#### **insert_experiment_row**

Ensures the experiment is created and inserts the given steps as a row for the given experiment

- HTTP Method: `POST`
- Endpoint: `/api/experiment/{experimentId}/insert`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| request_body | ExperimentInsertPayload | ✅ | The request body. |
| experimentId | str | ✅ | Ensures the experiment is created and inserts the given steps as a row for the given experiment |

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment
from labelkit_app.models import ExperimentInsertPayload

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

request_body = ExperimentInsertPayload(**{
    "steps": [
        {
            "name": "name",
            "metadata": {},
            "outputs": [
                {
                    "name": "name",
                    "value": "value"
                }
            ]
        }
    ]
})

result = sdk.experiment.insert_experiment_row(
    request_body=request_body,
    experiment_id="experimentId"
)

print(result)
```

#### **get_experiment_data**

Fetches the details of an experiment with the specified Id.

- HTTP Method: `GET`
- Endpoint: `/api/experiment/{experimentId}`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| experimentId | str | ✅ | Fetches the details of an experiment with the specified Id. |

**Return Type**

`ExperimentViewResponse`

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

result = sdk.experiment.get_experiment_data(experiment_id="experimentId")

print(result)
```

#### **list_experiments**

List all experiments

- HTTP Method: `GET`
- Endpoint: `/api/experiment/list`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|

**Return Type**

`List[ListExperimentResponse]`

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

result = sdk.experiment.list_experiments()

print(result)
```

#### **declare_experiment**

Declare a new experiment for a given dataset Id

- HTTP Method: `POST`
- Endpoint: `/api/experiment/new`

**Parameters**
| Name | Type| Required | Description |
| :-------- | :----------| :----------:| :----------|
| request_body | NewExperimentPayload | ✅ | The request body. |

**Return Type**

`NewExperimentResponse`

**Example Usage Code Snippet**

```py
from labelkit_app import LabelkitApp, Environment
from labelkit_app.models import NewExperimentPayload

sdk = LabelkitApp(
    base_url=Environment.DEFAULT.value
)

request_body = NewExperimentPayload(**{
    "dataset_id": "datasetId",
    "name": "name",
    "description": "description",
    "parameters": {}
})

result = sdk.experiment.declare_experiment(request_body=request_body)

print(result)
```

<!-- This file was generated by liblab | https://liblab.com/ -->
