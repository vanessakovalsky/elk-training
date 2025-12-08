# Module 2 - Exercices Recherches et Filtres
## Data Manipulation Language (DML)

---

## 🔧 Prérequis

### Environnement
- Stack ELK Docker en cours d'exécution
- Kibana Dev Tools : http://localhost:5601

### Préparation des données
Nous allons créer un index `produits` avec des données de test.

```json
# Création de l'index produits
PUT /produits
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "nom": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "description": {
        "type": "text"
      },
      "prix": {
        "type": "float"
      },
      "stock": {
        "type": "integer"
      },
      "disponible": {
        "type": "boolean"
      },
      "categorie": {
        "type": "keyword"
      },
      "marque": {
        "type": "keyword"
      },
      "note": {
        "type": "float"
      },
      "nb_avis": {
        "type": "integer"
      },
      "date_creation": {
        "type": "date"
      },
      "tags": {
        "type": "keyword"
      }
    }
  }
}

# Chargement des données de test
POST /produits/_bulk
{"index":{"_id":"1"}}
{"nom":"Smartphone Samsung Galaxy S23","description":"Smartphone haut de gamme avec écran AMOLED 6.1 pouces","prix":899.99,"stock":15,"disponible":true,"categorie":"Electronique","marque":"Samsung","note":4.5,"nb_avis":1250,"date_creation":"2023-02-01","tags":["smartphone","5G","android"]}
{"index":{"_id":"2"}}
{"nom":"iPhone 14 Pro","description":"iPhone dernière génération avec puce A16 Bionic","prix":1159.00,"stock":8,"disponible":true,"categorie":"Electronique","marque":"Apple","note":4.7,"nb_avis":2100,"date_creation":"2022-09-15","tags":["smartphone","5G","iOS"]}
{"index":{"_id":"3"}}
{"nom":"MacBook Pro 14","description":"Ordinateur portable professionnel avec puce M2 Pro","prix":2299.00,"stock":5,"disponible":true,"categorie":"Informatique","marque":"Apple","note":4.8,"nb_avis":890,"date_creation":"2023-01-20","tags":["laptop","mac","professionnel"]}
{"index":{"_id":"4"}}
{"nom":"Dell XPS 13","description":"Ultrabook compact et puissant pour la mobilité","prix":1499.00,"stock":12,"disponible":true,"categorie":"Informatique","marque":"Dell","note":4.4,"nb_avis":654,"date_creation":"2023-03-10","tags":["laptop","windows","ultrabook"]}
{"index":{"_id":"5"}}
{"nom":"Sony WH-1000XM5","description":"Casque audio sans fil avec réduction de bruit active","prix":399.99,"stock":25,"disponible":true,"categorie":"Audio","marque":"Sony","note":4.6,"nb_avis":1567,"date_creation":"2022-05-12","tags":["casque","bluetooth","ANC"]}
{"index":{"_id":"6"}}
{"nom":"AirPods Pro 2","description":"Écouteurs sans fil avec réduction de bruit et son spatial","prix":279.00,"stock":30,"disponible":true,"categorie":"Audio","marque":"Apple","note":4.5,"nb_avis":3421,"date_creation":"2022-09-23","tags":["écouteurs","bluetooth","ANC"]}
{"index":{"_id":"7"}}
{"nom":"Samsung Galaxy Tab S8","description":"Tablette Android premium avec stylet S Pen inclus","prix":749.00,"stock":0,"disponible":false,"categorie":"Tablette","marque":"Samsung","note":4.3,"nb_avis":432,"date_creation":"2022-02-25","tags":["tablette","android","stylet"]}
{"index":{"_id":"8"}}
{"nom":"iPad Air 5","description":"Tablette Apple avec puce M1 pour les créatifs","prix":699.00,"stock":18,"disponible":true,"categorie":"Tablette","marque":"Apple","note":4.7,"nb_avis":1876,"date_creation":"2022-03-18","tags":["tablette","iOS","créatif"]}
{"index":{"_id":"9"}}
{"nom":"Logitech MX Master 3","description":"Souris ergonomique sans fil pour professionnels","prix":99.99,"stock":45,"disponible":true,"categorie":"Accessoire","marque":"Logitech","note":4.8,"nb_avis":2345,"date_creation":"2021-06-10","tags":["souris","bluetooth","ergonomique"]}
{"index":{"_id":"10"}}
{"nom":"Clavier mécanique Keychron K2","description":"Clavier mécanique compact sans fil RGB","prix":89.00,"stock":22,"disponible":true,"categorie":"Accessoire","marque":"Keychron","note":4.6,"nb_avis":987,"date_creation":"2021-11-05","tags":["clavier","mécanique","RGB"]}
{"index":{"_id":"11"}}
{"nom":"Monitor LG UltraWide 34","description":"Écran ultrawide 34 pouces QHD pour productivité","prix":599.00,"stock":7,"disponible":true,"categorie":"Moniteur","marque":"LG","note":4.5,"nb_avis":543,"date_creation":"2023-01-15","tags":["écran","ultrawide","QHD"]}
{"index":{"_id":"12"}}
{"nom":"Webcam Logitech Brio 4K","description":"Webcam professionnelle 4K avec autofocus","prix":199.00,"stock":0,"disponible":false,"categorie":"Accessoire","marque":"Logitech","note":4.4,"nb_avis":876,"date_creation":"2020-03-20","tags":["webcam","4K","streaming"]}
{"index":{"_id":"13"}}
{"nom":"Disque SSD Samsung 980 Pro 1TB","description":"SSD NVMe ultra-rapide pour gaming et création","prix":129.00,"stock":35,"disponible":true,"categorie":"Stockage","marque":"Samsung","note":4.7,"nb_avis":2134,"date_creation":"2021-09-30","tags":["SSD","NVMe","stockage"]}
{"index":{"_id":"14"}}
{"nom":"Enceinte Bluetooth JBL Charge 5","description":"Enceinte portable waterproof avec batterie longue durée","prix":179.99,"stock":28,"disponible":true,"categorie":"Audio","marque":"JBL","note":4.6,"nb_avis":1432,"date_creation":"2021-04-15","tags":["enceinte","bluetooth","portable"]}
{"index":{"_id":"15"}}
{"nom":"Chargeur Anker 65W","description":"Chargeur USB-C compact avec technologie GaN","prix":45.00,"stock":60,"disponible":true,"categorie":"Accessoire","marque":"Anker","note":4.7,"nb_avis":3210,"date_creation":"2022-08-10","tags":["chargeur","USB-C","GaN"]}
```

---

## 📝 Exercice 1 : Filtres combinés avec Bool Query (15 min)

### Objectif
Maîtriser la combinaison de filtres avec la requête `bool` pour créer des recherches complexes.

### Consignes
En utilisant l'index `produits`, créez les requêtes suivantes :

**Requête 1 :** Trouver tous les produits qui sont :
- Disponibles (disponible = true)
- Prix entre 100€ et 500€
- Catégorie "Electronique" OU "Audio"
- PAS de la marque "Samsung"

**Requête 2 :** Trouver tous les produits qui :
- Note >= 4.5
- Stock > 10
- Prix <= 1000€
- Contiennent le tag "bluetooth"

**Requête 3 :** Recherche avancée :
- Catégorie "Accessoire"
- Prix < 100€
- Note >= 4.6 OU nb_avis > 2000
- Afficher seulement les champs : nom, prix, note

### 💡 Aide
```json
{
  "query": {
    "bool": {
      "must": [ ... ],      // Doit correspondre
      "filter": [ ... ],    // Doit correspondre (pas de score)
      "should": [ ... ],    // Peut correspondre
      "must_not": [ ... ]   // Ne doit pas correspondre
    }
  }
}
```

---

## ✅ Correction Exercice 1

### Requête 1
```json
GET /produits/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "disponible": true
          }
        },
        {
          "range": {
            "prix": {
              "gte": 100,
              "lte": 500
            }
          }
        },
        {
          "terms": {
            "categorie": ["Electronique", "Audio"]
          }
        }
      ],
      "must_not": [
        {
          "term": {
            "marque": "Samsung"
          }
        }
      ]
    }
  }
}
```

**Résultats attendus :** iPhone 14 Pro (non, trop cher), Sony WH-1000XM5 (oui), AirPods Pro 2 (oui)

### Requête 2
```json
GET /produits/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "note": {
              "gte": 4.5
            }
          }
        },
        {
          "range": {
            "stock": {
              "gt": 10
            }
          }
        },
        {
          "range": {
            "prix": {
              "lte": 1000
            }
          }
        },
        {
          "term": {
            "tags": "bluetooth"
          }
        }
      ]
    }
  }
}
```

**Résultats attendus :** AirPods Pro 2, Logitech MX Master 3, Clavier Keychron K2, Enceinte JBL

### Requête 3
```json
GET /produits/_search
{
  "_source": ["nom", "prix", "note"],
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "categorie": "Accessoire"
          }
        },
        {
          "range": {
            "prix": {
              "lt": 100
            }
          }
        }
      ],
      "should": [
        {
          "range": {
            "note": {
              "gte": 4.6
            }
          }
        },
        {
          "range": {
            "nb_avis": {
              "gt": 2000
            }
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}
```

**Résultats attendus :** Logitech MX Master 3, Clavier Keychron K2, Chargeur Anker

**Points clés :**
✅ `filter` est plus rapide que `must` (pas de calcul de score)  
✅ `terms` permet de tester plusieurs valeurs  
✅ `must_not` exclut des résultats  
✅ `minimum_should_match` force au moins N conditions should  

---

## 📝 Exercice 2 : Recherche multi-champs avec boost (10 min)

### Objectif
Utiliser `multi_match` avec pondération des champs pour améliorer la pertinence.

### Consignes
Créez une requête de recherche pour le terme "**bluetooth sans fil**" qui :
1. Recherche dans les champs `nom` et `description`
2. Donne 3 fois plus d'importance au champ `nom`
3. Affiche les 5 premiers résultats
4. Trie par score décroissant puis par prix croissant

**Bonus :** Ajoutez un filtre pour n'afficher que les produits disponibles.

### 💡 Aide
```json
{
  "query": {
    "multi_match": {
      "query": "...",
      "fields": ["champ1^3", "champ2"]
    }
  }
}
```

---

## ✅ Correction Exercice 2

```json
GET /produits/_search
{
  "size": 5,
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "bluetooth sans fil",
            "fields": ["nom^3", "description"],
            "type": "best_fields",
            "operator": "or"
          }
        }
      ],
      "filter": [
        {
          "term": {
            "disponible": true
          }
        }
      ]
    }
  },
  "sort": [
    {
      "_score": "desc"
    },
    {
      "prix": "asc"
    }
  ]
}
```

**Résultats attendus (ordre) :**
1. Sony WH-1000XM5 (casque bluetooth dans le nom)
2. AirPods Pro 2 (écouteurs bluetooth dans le nom)
3. Logitech MX Master 3 (souris sans fil)
4. Enceinte JBL Charge 5

**Variante avec type `cross_fields` :**
```json
GET /produits/_search
{
  "query": {
    "multi_match": {
      "query": "bluetooth sans fil",
      "fields": ["nom^3", "description"],
      "type": "cross_fields"
    }
  }
}
```

**Points clés :**
✅ Le `^3` booste le champ nom  
✅ `type: best_fields` cherche le meilleur match sur un champ  
✅ `type: cross_fields` traite les champs comme un seul grand champ  
✅ On peut combiner requête full-text et filtres  

---

## 📝 Exercice 3 : Autocomplete avec edge n-gram (30 min)

### Objectif
Créer un système d'autocomplétion performant avec l'analyzer edge n-gram.

### Consignes

**Partie 1 : Création de l'index (15 min)**

1. Créez un index `villes_fr` avec :
   - Un analyzer `autocomplete` utilisant edge n-gram (2 à 20 caractères)
   - Un analyzer `autocomplete_search` pour la recherche (lowercase + standard)
   - Un champ `nom_ville` de type text avec l'analyzer autocomplete

2. Indexez les villes suivantes :
   - Paris, Marseille, Lyon, Toulouse, Nice, Nantes, Strasbourg, Montpellier, Bordeaux, Lille
   - Rennes, Reims, Saint-Étienne, Toulon, Le Havre, Grenoble, Dijon, Angers, Nîmes, Villeurbanne

**Partie 2 : Tests (15 min)**

3. Testez l'autocomplete avec les requêtes :
   - "par" → devrait trouver Paris
   - "mar" → devrait trouver Marseille
   - "mon" → devrait trouver Montpellier
   - "re" → devrait trouver Reims, Rennes

### 💡 Aide
```json
{
  "settings": {
    "analysis": {
      "analyzer": { ... },
      "tokenizer": {
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      }
    }
  }
}
```

---

## ✅ Correction Exercice 3

### Partie 1 : Création de l'index

```json
# Création de l'index avec analyzer edge n-gram
PUT /villes_fr
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "autocomplete_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20,
          "token_chars": ["letter"]
        }
      },
      "analyzer": {
        "autocomplete": {
          "type": "custom",
          "tokenizer": "autocomplete_tokenizer",
          "filter": ["lowercase", "asciifolding"]
        },
        "autocomplete_search": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "nom_ville": {
        "type": "text",
        "analyzer": "autocomplete",
        "search_analyzer": "autocomplete_search"
      },
      "code_postal": {
        "type": "keyword"
      },
      "population": {
        "type": "integer"
      }
    }
  }
}

# Indexation des villes
POST /villes_fr/_bulk
{"index":{"_id":"1"}}
{"nom_ville":"Paris","code_postal":"75000","population":2161000}
{"index":{"_id":"2"}}
{"nom_ville":"Marseille","code_postal":"13000","population":869000}
{"index":{"_id":"3"}}
{"nom_ville":"Lyon","code_postal":"69000","population":513000}
{"index":{"_id":"4"}}
{"nom_ville":"Toulouse","code_postal":"31000","population":471000}
{"index":{"_id":"5"}}
{"nom_ville":"Nice","code_postal":"06000","population":342000}
{"index":{"_id":"6"}}
{"nom_ville":"Nantes","code_postal":"44000","population":303000}
{"index":{"_id":"7"}}
{"nom_ville":"Strasbourg","code_postal":"67000","population":277000}
{"index":{"_id":"8"}}
{"nom_ville":"Montpellier","code_postal":"34000","population":277000}
{"index":{"_id":"9"}}
{"nom_ville":"Bordeaux","code_postal":"33000","population":246000}
{"index":{"_id":"10"}}
{"nom_ville":"Lille","code_postal":"59000","population":232000}
{"index":{"_id":"11"}}
{"nom_ville":"Rennes","code_postal":"35000","population":215000}
{"index":{"_id":"12"}}
{"nom_ville":"Reims","code_postal":"51100","population":183000}
{"index":{"_id":"13"}}
{"nom_ville":"Saint-Étienne","code_postal":"42000","population":171000}
{"index":{"_id":"14"}}
{"nom_ville":"Toulon","code_postal":"83000","population":170000}
{"index":{"_id":"15"}}
{"nom_ville":"Le Havre","code_postal":"76600","population":170000}
{"index":{"_id":"16"}}
{"nom_ville":"Grenoble","code_postal":"38000","population":158000}
{"index":{"_id":"17"}}
{"nom_ville":"Dijon","code_postal":"21000","population":155000}
{"index":{"_id":"18"}}
{"nom_ville":"Angers","code_postal":"49000","population":151000}
{"index":{"_id":"19"}}
{"nom_ville":"Nîmes","code_postal":"30000","population":150000}
{"index":{"_id":"20"}}
{"nom_ville":"Villeurbanne","code_postal":"69100","population":147000}
```

### Partie 2 : Tests de l'autocomplete

```json
# Test 1 : "par" → Paris
GET /villes_fr/_search
{
  "query": {
    "match": {
      "nom_ville": "par"
    }
  }
}

# Test 2 : "mar" → Marseille
GET /villes_fr/_search
{
  "query": {
    "match": {
      "nom_ville": "mar"
    }
  }
}

# Test 3 : "mon" → Montpellier
GET /villes_fr/_search
{
  "query": {
    "match": {
      "nom_ville": "mon"
    }
  }
}

# Test 4 : "re" → Reims, Rennes
GET /villes_fr/_search
{
  "query": {
    "match": {
      "nom_ville": "re"
    }
  }
}

# Test 5 : "to" → Toulouse, Toulon
GET /villes_fr/_search
{
  "query": {
    "match": {
      "nom_ville": "to"
    }
  }
}

# Test avec gestion des accents : "stra" → Strasbourg
GET /villes_fr/_search
{
  "query": {
    "match": {
      "nom_ville": "stra"
    }
  }
}
```

### Vérifier l'analyzer

```json
# Voir comment le texte est analysé à l'indexation
POST /villes_fr/_analyze
{
  "analyzer": "autocomplete",
  "text": "Marseille"
}

# Résultat : ma, mar, mars, marse, marsei, marseii, marseill, marseille

# Voir comment le texte est analysé à la recherche
POST /villes_fr/_analyze
{
  "analyzer": "autocomplete_search",
  "text": "mar"
}

# Résultat : mar
```

**Points clés :**
✅ L'analyzer `autocomplete` génère tous les préfixes (edge n-grams)  
✅ Le `search_analyzer` utilise le terme complet (pas de n-gram)  
✅ `asciifolding` permet de chercher sans accents  
✅ `min_gram: 2` évite les résultats avec 1 seule lettre  
✅ Beaucoup plus performant que les wildcards  

**Amélioration possible :**
```json
# Requête avec boost sur correspondance exacte
GET /villes_fr/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "nom_ville": {
              "query": "mar",
              "boost": 1
            }
          }
        },
        {
          "term": {
            "nom_ville.keyword": {
              "value": "Marseille",
              "boost": 2
            }
          }
        }
      ]
    }
  }
}
```

---

## 🎯 Points à retenir du Module 2

### Filtres vs Requêtes
- **Filtres** (filter) : rapides, cachables, pas de score
- **Requêtes** (must) : calculent un score de pertinence
- Utilisez les filtres pour les critères binaires (oui/non)

### Bool Query
- `must` : doit matcher (affecte le score)
- `filter` : doit matcher (n'affecte pas le score)
- `should` : peut matcher (booste le score)
- `must_not` : ne doit pas matcher

### Multi-match
- Rechercher dans plusieurs champs simultanément
- Utiliser `^N` pour booster un champ
- Types : best_fields, cross_fields, most_fields

### Autocomplete
- Edge n-gram = préfixes pour l'autocomplétion
- Analyzer différent pour indexation et recherche
- Plus performant que wildcards

---

**Temps estimé total : 1h25 + 15 min de discussion**
