# Annotell OpenLABEL

## Installation
Install the Annotell OpenLABEL package from pip with

    pip install annotell-openlabel

## Serialization and deserialization

Since all models inherit from `pydantic`'s `BaseModel`, serialization and deserialization from dicts or json strings are relatively straight forward. 

```py
data = {
    "openlabel": {
        "metadata": {
            "schema_version": "1.0.0"
        }
    }
}

import annotell.openlabel.models as OLM

# Deserialize dict
openlabel_annotation = OLM.OpenLabelAnnotation.parse_obj(data)

# Serialize to json
json_data = openlabel_annotation.json(exclude_none=True)

# Deserialize json
openlabel_annotation = OLM.OpenLabelAnnotation.parse_raw(json_data)

# Serialize to dict
dict_data = openlabel_annotation.dict(exclude_none=True)
```
    
## Further reading
https://www.asam.net/project-detail/asam-openlabel-v100/

# Changelog

## [0.1.0] - 2021-11-18
- Updated json schema and model to be true to the 1.0.0 release of openlabel. Previously it was based on the release-candidate