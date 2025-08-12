
# Créer un nouvel index avec l'alias
```
PUT /transactions-new-marc
{
  "aliases": {
    "transactions-new-marc-alias": {
      "is_write_index": true
    }
  }
}
```

# reindexer le nouvel index avec les données de l'ancien
```
POST _reindex
{
  "source": {
    "index": "transaction_marc"
  },
  "dest": {
    "index": "transactions-marc"
  }
}
```

# appliquer le rollover manuellement
```
POST transactions-new-marc-alias/_rollover
{
  "conditions": {
    "max_docs": 50000
  }
}
```
