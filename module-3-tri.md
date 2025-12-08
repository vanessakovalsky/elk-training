# Module 3 - Exercices Tri, Pertinence et Géolocalisation
## Tri, Function Score et Données Géographiques

---

## 🔧 Prérequis

### Environnement
- Stack ELK Docker en cours d'exécution
- Kibana Dev Tools : http://localhost:5601
- Index `produits` du Module 2

---

## 📝 Exercice 1 : Tri multi-critères et pagination (15 min)

### Objectif
Maîtriser le tri sur plusieurs champs et la pagination efficace.

### Consignes

**Question 1 :** Recherchez tous les produits disponibles et :
- Triez par prix décroissant
- Puis par nom croissant (alphabétique)
- Affichez les résultats 21 à 40 (page 2 avec 20 résultats par page)
- N'affichez que les champs : nom, prix, stock

**Question 2 :** Trouvez tous les produits de catégorie "Electronique" ou "Audio" :
- Triés par note décroissante
- Puis par nombre d'avis décroissant
- Affichez les 10 premiers
- Incluez le score dans les résultats

**Question 3 :** Utilisez `search_after` pour paginer :
- Recherchez tous les produits
- Triez par date_creation descendant et _id ascendant
- Récupérez la première page (10 résultats)
- Puis récupérez la page suivante avec search_after

### 💡 Aide
```json
{
  "from": ...,
  "size": ...,
  "sort": [
    { "champ1": "desc" },
    { "champ2": "asc" }
  ]
}
```

---

## ✅ Correction Exercice 1

### Question 1 - Tri et pagination classique
```json
GET /produits/_search
{
  "_source": ["nom", "prix", "stock"],
  "from": 20,
  "size": 20,
  "query": {
    "term": {
      "disponible": true
    }
  },
  "sort": [
    {
      "prix": "desc"
    },
    {
      "nom.keyword": "asc"
    }
  ]
}
```

**Explication :**
- `from: 20` = commence au 21ème résultat (index 0)
- `size: 20` = affiche 20 résultats
- Tri sur `nom.keyword` car `nom` seul (text) ne peut pas être trié

### Question 2 - Tri par pertinence métier
```json
GET /produits/_search
{
  "size": 10,
  "query": {
    "terms": {
      "categorie": ["Electronique", "Audio"]
    }
  },
  "sort": [
    {
      "note": "desc"
    },
    {
      "nb_avis": "desc"
    }
  ],
  "track_scores": true
}
```

**Note :** `track_scores: true` calcule le score même quand on trie sur autre chose.

### Question 3 - Search After (pagination profonde)
```json
# Première page
GET /produits/_search
{
  "size": 10,
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "date_creation": "desc"
    },
    {
      "_id": "asc"
    }
  ]
}

# Dans la réponse, récupérez les valeurs "sort" du dernier document
# Exemple: ["2023-03-10", "4"]

# Page suivante avec search_after
GET /produits/_search
{
  "size": 10,
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "date_creation": "desc"
    },
    {
      "_id": "asc"
    }
  ],
  "search_after": ["2023-03-10", "4"]
}
```

**Avantages de search_after :**
✅ Pas de limite à 10000 résultats  
✅ Plus performant pour la pagination profonde  
✅ Résultats cohérents même si l'index change  

---

## 📝 Exercice 2 : Function Score - Boost personnalisé (30 min)

### Objectif
Contrôler le score de pertinence avec function_score pour créer un ranking personnalisé.

### Consignes

**Scénario :** Vous êtes un e-commerce qui veut privilégier certains produits dans les résultats de recherche.

**Question 1 :** Recherchez "smartphone" et boostez :
- Les produits avec une note >= 4.5 (x2)
- Les produits avec beaucoup d'avis (field_value_factor sur nb_avis)

**Question 2 :** Recherchez les produits de catégorie "Audio" et :
- Boostez selon le prix (plus c'est cher, mieux c'est) avec modifier "log1p"
- Multipliez le score par la note du produit

**Question 3 :** Créez un système de recommandation qui :
- Recherche tous les produits disponibles
- Privilégie les produits récents (decay gaussien sur date_creation)
- Booste les produits avec beaucoup d'avis
- Combine les deux facteurs

### 💡 Aide
```json
{
  "query": {
    "function_score": {
      "query": { ... },
      "functions": [
        {
          "filter": { ... },
          "weight": 2
        },
        {
          "field_value_factor": {
            "field": "...",
            "modifier": "log1p"
          }
        }
      ],
      "boost_mode": "multiply"
    }
  }
}
```

---

## ✅ Correction Exercice 2

### Question 1 - Boost par note et avis
```json
GET /produits/_search
{
  "query": {
    "function_score": {
      "query": {
        "match": {
          "nom": "smartphone"
        }
      },
      "functions": [
        {
          "filter": {
            "range": {
              "note": {
                "gte": 4.5
              }
            }
          },
          "weight": 2
        },
        {
          "field_value_factor": {
            "field": "nb_avis",
            "factor": 0.001,
            "modifier": "log1p",
            "missing": 1
          }
        }
      ],
      "score_mode": "sum",
      "boost_mode": "multiply"
    }
  }
}
```

**Explication :**
- Produits avec note >= 4.5 ont leur score x2
- `log1p(nb_avis)` évite que les gros nombres dominent
- `factor: 0.001` réduit l'impact du nombre d'avis
- `score_mode: sum` additionne les fonctions
- `boost_mode: multiply` multiplie avec le score de base

### Question 2 - Boost par prix et note
```json
GET /produits/_search
{
  "query": {
    "function_score": {
      "query": {
        "term": {
          "categorie": "Audio"
        }
      },
      "functions": [
        {
          "field_value_factor": {
            "field": "prix",
            "factor": 0.01,
            "modifier": "log1p"
          }
        },
        {
          "field_value_factor": {
            "field": "note",
            "factor": 1,
            "modifier": "none"
          }
        }
      ],
      "score_mode": "multiply",
      "boost_mode": "replace"
    }
  }
}
```

**Résultats attendus :**
Sony WH-1000XM5 devrait être en tête (prix élevé + bonne note)

### Question 3 - Recommandation avec decay
```json
GET /produits/_search
{
  "query": {
    "function_score": {
      "query": {
        "term": {
          "disponible": true
        }
      },
      "functions": [
        {
          "gauss": {
            "date_creation": {
              "origin": "now",
              "scale": "180d",
              "offset": "30d",
              "decay": 0.5
            }
          },
          "weight": 2
        },
        {
          "field_value_factor": {
            "field": "nb_avis",
            "factor": 0.0001,
            "modifier": "log1p"
          },
          "weight": 1
        }
      ],
      "score_mode": "sum",
      "boost_mode": "replace"
    }
  },
  "sort": [
    {
      "_score": "desc"
    }
  ]
}
```

**Explication du decay gaussien :**
- `origin: now` = date de référence (aujourd'hui)
- `scale: 180d` = après 180 jours, le score est réduit de 50%
- `offset: 30d` = pas de pénalité pendant 30 jours
- `decay: 0.5` = décroissance à 50% après scale

**Visualisation du decay :**
```
Score
  1.0 |____
      |    \
  0.5 |     \___
      |         \___
  0.0 |____________\____
      0   30  180      360 jours
         offset scale
```

---

## 📝 Exercice 3 : Recherche géographique (15 min)

### Objectif
Manipuler les données géographiques avec geo_point et geo_distance.

### Préparation des données

```json
# Création de l'index restaurants
PUT /restaurants
{
  "mappings": {
    "properties": {
      "nom": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "type_cuisine": {
        "type": "keyword"
      },
      "localisation": {
        "type": "geo_point"
      },
      "note": {
        "type": "float"
      },
      "prix_moyen": {
        "type": "integer"
      },
      "ouvert": {
        "type": "boolean"
      }
    }
  }
}

# Indexation des restaurants (Paris)
POST /restaurants/_bulk
{"index":{"_id":"1"}}
{"nom":"Le Comptoir du Relais","type_cuisine":"Français","localisation":{"lat":48.8534,"lon":2.3387},"note":4.5,"prix_moyen":35,"ouvert":true}
{"index":{"_id":"2"}}
{"nom":"L'Ami Jean","type_cuisine":"Français","localisation":{"lat":48.8566,"lon":2.3059},"note":4.6,"prix_moyen":45,"ouvert":true}
{"index":{"_id":"3"}}
{"nom":"Pink Mamma","type_cuisine":"Italien","localisation":{"lat":48.8814,"lon":2.3392},"note":4.3,"prix_moyen":30,"ouvert":true}
{"index":{"_id":"4"}}
{"nom":"Septime","type_cuisine":"Français","localisation":{"lat":48.8530,"lon":2.3808},"note":4.7,"prix_moyen":60,"ouvert":false}
{"index":{"_id":"5"}}
{"nom":"Breizh Café","type_cuisine":"Crêperie","localisation":{"lat":48.8620,"lon":2.3631},"note":4.4,"prix_moyen":20,"ouvert":true}
{"index":{"_id":"6"}}
{"nom":"Chez Janou","type_cuisine":"Provençal","localisation":{"lat":48.8543,"lon":2.3659},"note":4.2,"prix_moyen":28,"ouvert":true}
{"index":{"_id":"7"}}
{"nom":"Bouillon Chartier","type_cuisine":"Français","localisation":{"lat":48.8718,"lon":2.3422},"note":4.0,"prix_moyen":18,"ouvert":true}
{"index":{"_id":"8"}}
{"nom":"Le Chateaubriand","type_cuisine":"Français","localisation":{"lat":48.8669,"lon":2.3800},"note":4.5,"prix_moyen":55,"ouvert":true}
{"index":{"_id":"9"}}
{"nom":"Miznon","type_cuisine":"Méditerranéen","localisation":{"lat":48.8606,"lon":2.3522},"note":4.4,"prix_moyen":25,"ouvert":true}
{"index":{"_id":"10"}}
{"nom":"Clown Bar","type_cuisine":"Français","localisation":{"lat":48.8645,"lon":2.3710},"note":4.3,"prix_moyen":40,"ouvert":true}
```

### Consignes

**Position de référence : Tour Eiffel**
- Latitude : 48.8584
- Longitude : 2.2945

**Question 1 :** Trouvez tous les restaurants dans un rayon de 2km autour de la Tour Eiffel qui sont :
- Ouverts
- Note >= 4.0
- Triés par distance

**Question 2 :** Créez une recherche dans une zone rectangulaire (bounding box) :
- Top-left : 48.87, 2.33
- Bottom-right : 48.85, 2.39
- Cuisine : Français
- Prix moyen <= 50€

**Question 3 :** Agrégation par distance :
- Comptez le nombre de restaurants par tranche de distance depuis la Tour Eiffel
- Tranches : 0-1km, 1-2km, 2-5km, 5km+

### 💡 Aide
```json
{
  "query": {
    "bool": {
      "filter": {
        "geo_distance": {
          "distance": "5km",
          "localisation": {
            "lat": 48.8584,
            "lon": 2.2945
          }
        }
      }
    }
  }
}
```

---

## ✅ Correction Exercice 3

### Question 1 - Recherche dans un rayon
```json
GET /restaurants/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "geo_distance": {
            "distance": "2km",
            "localisation": {
              "lat": 48.8584,
              "lon": 2.2945
            }
          }
        },
        {
          "term": {
            "ouvert": true
          }
        },
        {
          "range": {
            "note": {
              "gte": 4.0
            }
          }
        }
      ]
    }
  },
  "sort": [
    {
      "_geo_distance": {
        "localisation": {
          "lat": 48.8584,
          "lon": 2.2945
        },
        "order": "asc",
        "unit": "km",
        "distance_type": "arc"
      }
    }
  ]
}
```

**Résultats attendus :**
Le Comptoir du Relais, L'Ami Jean (plus proches de la Tour Eiffel)

### Question 2 - Bounding box
```json
GET /restaurants/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "geo_bounding_box": {
            "localisation": {
              "top_left": {
                "lat": 48.87,
                "lon": 2.33
              },
              "bottom_right": {
                "lat": 48.85,
                "lon": 2.39
              }
            }
          }
        },
        {
          "term": {
            "type_cuisine": "Français"
          }
        },
        {
          "range": {
            "prix_moyen": {
              "lte": 50
            }
          }
        }
      ]
    }
  }
}
```

**Visualisation de la zone :**
```
    top_left (48.87, 2.33)
         +------------------+
         |                  |
         |    Zone de       |
         |    recherche     |
         |                  |
         +------------------+
                          bottom_right (48.85, 2.39)
```

### Question 3 - Agrégation par distance
```json
GET /restaurants/_search
{
  "size": 0,
  "aggs": {
    "par_distance": {
      "geo_distance": {
        "field": "localisation",
        "origin": {
          "lat": 48.8584,
          "lon": 2.2945
        },
        "unit": "km",
        "ranges": [
          {
            "key": "0-1km",
            "to": 1
          },
          {
            "key": "1-2km",
            "from": 1,
            "to": 2
          },
          {
            "key": "2-5km",
            "from": 2,
            "to": 5
          },
          {
            "key": "5km+",
            "from": 5
          }
        ]
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "note"
          }
        },
        "prix_moyen": {
          "avg": {
            "field": "prix_moyen"
          }
        }
      }
    }
  }
}
```

**Résultat exemple :**
```json
{
  "aggregations": {
    "par_distance": {
      "buckets": [
        {
          "key": "0-1km",
          "from": 0,
          "to": 1000,
          "doc_count": 2,
          "note_moyenne": { "value": 4.55 },
          "prix_moyen": { "value": 40.0 }
        },
        {
          "key": "1-2km",
          "from": 1000,
          "to": 2000,
          "doc_count": 3,
          "note_moyenne": { "value": 4.33 },
          "prix_moyen": { "value": 32.67 }
        }
      ]
    }
  }
}
```

### Bonus : Carte de chaleur (heatmap)
```json
GET /restaurants/_search
{
  "size": 0,
  "aggs": {
    "zones": {
      "geohash_grid": {
        "field": "localisation",
        "precision": 6
      },
      "aggs": {
        "note_zone": {
          "avg": {
            "field": "note"
          }
        }
      }
    }
  }
}
```

---

## 🎯 Points à retenir du Module 3

### Tri
- Les champs `text` ne peuvent pas être triés → utiliser `.keyword`
- Le tri désactive le calcul de score (performance)
- `search_after` pour pagination profonde (> 10000 résultats)

### Function Score
- `field_value_factor` : boost basé sur un champ numérique
- Modifiers : `log1p`, `sqrt`, `square`, `ln`, etc.
- Decay functions : `gauss`, `exp`, `linear`
- `boost_mode` : comment combiner (multiply, sum, replace, etc.)

### Géolocalisation
- `geo_point` : stocke lat/lon
- `geo_distance` : recherche dans un rayon
- `geo_bounding_box` : recherche dans un rectangle
- Tri par `_geo_distance` pour "près de moi"
- Agrégation `geo_distance` pour statistiques par zone

### Distance types
- `arc` : distance réelle sur la sphère (précis)
- `plane` : distance plane (plus rapide, moins précis)

---

## 📚 Commandes utiles

```json
# Calculer la distance entre deux points
GET /restaurants/_search
{
  "script_fields": {
    "distance": {
      "script": {
        "source": "doc['localisation'].arcDistance(params.lat, params.lon)",
        "params": {
          "lat": 48.8584,
          "lon": 2.2945
        }
      }
    }
  }
}

# Polygon search (zone complexe)
GET /restaurants/_search
{
  "query": {
    "geo_polygon": {
      "localisation": {
        "points": [
          {"lat": 48.87, "lon": 2.33},
          {"lat": 48.86, "lon": 2.38},
          {"lat": 48.85, "lon": 2.35}
        ]
      }
    }
  }
}
```

---

**Temps estimé total : 60 minutes**
