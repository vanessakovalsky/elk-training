# TP - Recherche d'information

## Import des données :
* Sur une machine faisant fonctionner elasticsearch, importer le fichier : http://b3d.bdpedia.fr/files/big-movies-elastic.json 
* Importer les données depuis ce fichiers dans elasticsearch : 
```
curl -s -XPOST http://localhost:9200/_bulk/ -H "Content-Type: application/json" --data-binary @big-movies-elastic.json
```
* A l'aide de l'API, visualiser la structure de données 

## Rechercher des données :
* Rechercher les films dont le titre contient "Star Wars"
<details>
  <summary>Solution</summary>
    
  ```json
{
    "query": {
        "match": {
            "fields.title": "Star Wars"
        }
    }
}
  ```
</details>

* Recherche les Films dont le titre contient “Star Wars” et dont le réalisateur (directors) est “George Lucas” (requête booléenne)
<details>
  <summary>Solution</summary>
    
  ```json
    {
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "fields.title": "Star Wars"
              }
            },
            {
              "match": {
                "fields.directors": "George Lucas"
              }
            }
          ]
        }
      }
    }
  ```
</details>

* Rechercher les films dans lequel "Harisson Ford" est acteur
<details>
  <summary>Solution</summary>
    
  ```json
{
  "query": {
    "match": {
      "fields.actors": "Harrison Ford"
    }
  }
}
  ```
</details>

* Rechercher les Films dans lesquels “Harrison Ford” a joué et dont le résumé (plot) contient “Jones”.
<details>
  <summary>Solution</summary>
    
  ```json
{"query":{
  "bool": {
    "should": [
      { "match": { "fields.actors": "Harrison Ford" }},
      { "match": { "fields.plot": "Jones" }}
    ]
}}}
  ```
</details>

* Rechercher les Films dans lesquels “Harrison Ford” a joué et dont le résumé (plot) contient “Jones” mais sans le mot “Nazis”
<details>
  <summary>Solution</summary>
    
  ```json
{"query":{
  "bool": {
    "should": [
      { "match": { "fields.actors": "Harrison Ford" }},
      { "match": { "fields.plot": "Jones" }}
    ],
    "must_not" : { "match" : {"fields.plot":"Nazis"}}
}}}
  ```
</details>

* Rechercher les Films dont le realisateur (director) est  “James Cameron” et dont le rang devrait être inférieur à 1000 (boolean + range query).
<details>
  <summary>Solution</summary>
    
  ```json
{"query":{
  "bool": {
    "should": [
      { "match": { "fields.directors": "James Cameron" }},
      { "range": { "fields.rank": {"lt":1000 }}}
    ]
}}}
  ```
</details>

* Rechercher les Films  dont le realisateur (director) est “James Cameron” et dont le rang doit être inférieur à 400 (réponse exacte : 2)
<details>
  <summary>Solution</summary>
    
  ```json
{
  "query": {
    "bool": {
      "must": [{
          "match_phrase": {
            "fields.directors": "James Cameron"
          }
        },
        {
          "range": {
            "fields.rank": {
              "lt": 400
            }
          }
        }
      ]
    }
  }
}
  ```
</details>

* Rechercher les Films dont le realisateur (director) est “Quentin Tarantino” et dont la note (rating) doit être supérieure à 5, sans être un film d’action ni un drame
<details>
  <summary>Solution</summary>
    
  ```json
{
  "_source": {
    "includes": [
      "*.title"
    ],
    "excludes": [
      "*.actors*"
    ]
  },
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "fields.directors": "Quentin Tarantino"
          }
        },
        {
          "range": {
            "fields.rating": {
              "gte": 5
            }
          }
        }
      ],
      "must_not": [
        {
          "match": {
            "fields.genres": "Action"
          }
        },
        {
          "match": {
            "fields.genres": "Drama"
          }
        }
      ]
    }
  }
}
  ```
</details>

* Recherche les Films dont le réalisateur (director) est  “J.J. Abrams” et sortis (released) entre 2010 et 2015
<details>
  <summary>Solution</summary>
    
  ```json
{
  "query": {
    "bool":{
      "must": {"match": {"fields.directors": "J.J. Abrams"}},
      "filter": {
        "range": {
          "fields.release_date": { "from": "2010-01-01", "to": "2015-12-31"}
        }
      }
    }
  }
}
  ```
</details>

## Aggregation de données
* Donner la note (rating) moyenne des films.
<details>
  <summary>Solution</summary>
    
  ```json
{"size":0,
"aggs" : {
    "note_moyenne" : {
      "avg" : {"field" : "fields.rating"}
    }}}
  ```
</details>

* Donner la note (rating) moyenne, et le rang moyen des films de George Lucas (cliquer sur (-) à côté de « hits » dans l’interface pour masquer les résultats et consulter les valeurs calculées)
<details>
  <summary>Solution</summary>
    
  ```json
{"query" :{
    "match" : {"fields.directors": {"query": "George Lucas", "operator": "and"}}
  }
 ,"aggs" : {
    "note_moyenne" : {
      "avg" : {"field" : "fields.rating"}
    },
    "rang_moyen" : {
      "avg" : {"field" : "fields.rank"}
    }
}}
  ```
</details>

* Donnez la note (rating) moyenne des films par année. Attention, il y a ici une imbrication d’agrégats (on obtient par exemple 456 films en 2013 avec un rating moyen de 5.97).
<details>
  <summary>Solution</summary>
    
  ```json
{"aggs" : {
    "group_year" : {
      "terms" : {
        "field" : "fields.year"
      },
      "aggs" : {
        "note_moyenne" : {
          "avg" : {"field" : "fields.rating"}
        }}
    }}}
  ```
</details>

* Donner la note (rating) minimum, maximum et moyenne des films par année.
<details>
  <summary>Solution</summary>
    
  ```json
{"aggs" : {
    "group_year" : {
      "terms" : {
        "field" : "fields.year"
      },
      "aggs" : {
        "note_moyenne" : {"avg" : {"field" : "fields.rating"}},
        "note_min" : {"min" : {"field" : "fields.rating"}},
        "note_max" : {"max" : {"field" : "fields.rating"}}
      }
    }}}
  ```
</details>

* Donner le rang (rank) moyen des films par année et trier par ordre décroissant.
<details>
  <summary>Solution</summary>
    
  ```json
{"aggs" : {
    "group_year" : {
      "terms" : {
        "field" : "fields.year",
        "order" : { "rating_moyen" : "desc" }
      },
      "aggs" : {
        "rating_moyen" : {
          "avg" : {"field" : "fields.rating"}
      }}
}}}
  ```
</details>

* Compter le nombre de films par tranche de note (0-1.9, 2-3.9, 4-5.9…). Indice : group_range.
<details>
  <summary>Solution</summary>
    
  ```json
{"aggs" : {
    "group_range" : {
      "range" : {
        "field" : "fields.rating",
        "ranges" : [
          {"to" : 1.9},
          {"from" : 2, "to" : 3.9},
          {"from" : 4, "to" : 5.9},
          {"from" : 6, "to" : 7.9},
          {"from" : 8}
        ]
      }
    }}}
  ```
</details>

