# ElasticSearchCollections
Collections of ElasticSearch pyscripts for human

## Example
```python
from elasticSearch_collections.elasticSearch_collections import ElasticSearchCollections
from typing import Dict, List

# Connect to es hosts
es = ElasticSearchCollections(["https://127.0.0.1"],
                              http_auth=("username", "password"),
                              ca_certs=False,
                              verify_certs=False,
                              timeout=600)

def fn_data_update(_data: List[Dict]):
    actions = []
    for i in _data:
        #  do something
        action = {
            "_op_type": "update",
            "_index": i["_index"],
            "_type": "_doc",
            "_id": i["_id"],
            "doc": {
                # update logic
            }
        }
        actions.append(action)
    if actions:
        es.bulk(actions)
        

es_search_info = {
        "index": '_index',
        "scroll": '1m',
        "size": 1000,
        "body": """{
              "query": {
                "match_all": {}
              }
            }""",
        "timeout": "10m"
    }

_res_list = es.scroll_source_generator(es_search_info)
# run multiple threads with threado
from threado.simple_thread_runner import SimpleThreadsRunner
# Define the num_workers and batch_size
# refer to https://github.com/AlexNg9527/threado
sr = SimpleThreadsRunner(num_workers=10,fn=fn_data_update)
sr.run_threads(iter_data=_res_list, batch_size=10)

# clear scroll_id
es.delete_scroll_id()

```
## Installing and Supported Versions

elasticSearch_collections is available on PyPI:

```console
$ python -m pip install elasticSearch_collections
```