
# Créer un template d’index avec data_stream
```
PUT _template/transactions-marc-template
{
  "index_patterns": ["transactions-marc-stream*"],
  "data_stream": {},
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "transactions-marc-policy",
      "index.lifecycle.rollover_alias": "transactions-marc-alias"
    }
  }
}
```

# Créer le data-stream
```
PUT _data_stream/transactions-marc-stream
```

