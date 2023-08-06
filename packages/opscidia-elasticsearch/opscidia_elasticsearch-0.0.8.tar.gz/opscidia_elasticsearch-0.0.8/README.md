# opscidia_elastisearch
Tools to manage elasticsearch indexes 

# Installation 

## From pip

```bash
pip install opscidia-elasticsearch
```

# Python usage

```python
from opscidia_elasticsearch import Manager

mg = Manager(hosts='url-to-es')      # Connect to ES

mg.create_index(index_name='')       # to create index
mg.save_to_index(generator=None)     # to save generator
```

