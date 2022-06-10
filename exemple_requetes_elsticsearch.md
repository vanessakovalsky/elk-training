# Exemples de requêtes avec DevTools de Kibana 

## CRUD
### Ajouter un héros
```
POST heroes/_doc/spiderman
{
  "firstname": "Peter",
  "lastname": "Parker"
}
```
### Afficher le héroes ajouter
```
GET heroes/_doc/spiderman
```

### Modifier un héros 
```
POST heroes/_doc/spiderman 
{
  "firstname": "Lapin"
}
```
### Supprimer un héros
```
DELETE heroes/_doc/spiderman
```

### Vérifier si un héros existe 
```
HEAD heroes/_doc/spiderman

HEAD heroes/_doc/ironman
```

## Recherche

### Recherche de tous les héros sans filtre
```
GET heroes/_search
```

### Recherche avec un paramètre dans l'URL 
```

GET heroes/_search?q=firstname:Charles
```

### Recherche avec une query string
```
GET heroes/_search
{
  "size": 1,
  "query":
    {
      "query_string": {
        "query": "(firsName=Charles AND lastName=Xavier) OR (firstname=Tony)"
      }
      
    }
}
```

### Recherche avec un opérateur de rang :
```
GET heroes/_search
{
  "query":
    {
      "range": {
        "taille": {
          "gte": 180        }
      }
      
    }
}
```
### Recherche avec un tri sur le champs taille et un filtrage pour n'afficher que les champs firstname et taille
```
GET heroes/_search
{
  "_source": ["firstname","taille"], 
  "sort": [
    {
      "taille.keyword": {
        "order": "asc"
      }
    }
  ], 
  "query": {
    "exists": {
      "field": "taille"
    }
  }
}
```
