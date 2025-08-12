# 1. Créer une politique ILM

```
PUT _ilm/policy/transactions-marc-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": { "max_age": "30m", "max_size": "500mb", "max_docs": 50000 }
        }
      },
      "delete": {
        "min_age": "1d",
        "actions": { "delete": {} }
      }
    }
  }
}
```

# 2. Assigner la politique à un index
```
PUT /transactions-marc-alias/_settings
{
  "index": {
    "lifecycle.name": "transactions-marc-policy"
  }
}
```
