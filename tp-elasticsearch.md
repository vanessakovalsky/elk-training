# TP - Recherche d'information

## Import des données :
* Sur une machine faisant fonctionner elasticsearch, importer le fichier : http://b3d.bdpedia.fr/files/big-movies-elastic.json 
* Importer les données depuis ce fichiers dans elasticsearch : 
```
curl -s -XPOST http://localhost:9200/_bulk/ --data-binary @big-movies-elastic.json
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
