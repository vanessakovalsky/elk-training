# Module 1 - Exercices DDL
## Gestion des Index ElasticSearch

---

## 🔧 Prérequis environnement

### Accès à la stack ELK (Docker)
- **ElasticSearch** : http://localhost:9200
- **Kibana** : http://localhost:5601
- **Credentials** : 
  - Username: `elastic`
  - Password: `changeme` (ou celui configuré dans `.env`)

### Outils à utiliser
1. **Kibana Dev Tools** : Menu ☰ → Management → Dev Tools
2. **PowerShell** (Windows) : pour curl si besoin

---

## 📝 Exercice 1 : Création d'un index bibliothèque (15 min)

### Objectif
Créer un index pour gérer un catalogue de livres avec un mapping personnalisé.

### Consignes
Créez un index nommé `bibliotheque` avec les caractéristiques suivantes :

**Settings :**
- 1 shard primaire
- 1 replica

**Mapping avec les champs :**
- `titre` : texte recherchable (type text) avec un sous-champ keyword
- `auteur` : texte recherchable (type text) avec un sous-champ keyword
- `isbn` : identifiant unique (type keyword)
- `annee_publication` : nombre entier (type integer)
- `nb_pages` : nombre entier (type integer)
- `disponible` : booléen (type boolean)
- `categorie` : valeur exacte (type keyword)
- `prix` : nombre décimal (type float)

**Étapes :**
1. Ouvrez Kibana Dev Tools
2. Créez l'index avec le mapping complet
3. Vérifiez que l'index est créé : `GET /_cat/indices?v`
4. Affichez le mapping : `GET /bibliotheque/_mapping`

### 💡 Aide
```json
PUT /nom_index
{
  "settings": {
    "number_of_shards": ...,
    "number_of_replicas": ...
  },
  "mappings": {
    "properties": {
      "nom_champ": {
        "type": "...",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      }
    }
  }
}
```

---

## ✅ Correction Exercice 1

```json
PUT /bibliotheque
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "titre": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "auteur": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "isbn": {
        "type": "keyword"
      },
      "annee_publication": {
        "type": "integer"
      },
      "nb_pages": {
        "type": "integer"
      },
      "disponible": {
        "type": "boolean"
      },
      "categorie": {
        "type": "keyword"
      },
      "prix": {
        "type": "float"
      }
    }
  }
}

# Vérification
GET /_cat/indices?v

# Afficher le mapping
GET /bibliotheque/_mapping
```

**Points clés :**
✅ Les champs `text` ont un sous-champ `keyword` pour permettre tri et agrégations  
✅ `isbn` et `categorie` sont en `keyword` car ce sont des valeurs exactes  
✅ Les nombres sont typés correctement (integer pour entiers, float pour décimaux)  
✅ 1 shard suffit pour un petit index (optimisation)  

---

## 📝 Exercice 2 : Template pour logs (20 min)

### Objectif
Créer un template qui s'appliquera automatiquement à tous les index de logs d'application.

### Consignes
Créez un index template avec les caractéristiques suivantes :

**Nom du template :** `logs-application-template`

**Pattern :** `logs-application-*`

**Settings :**
- 2 shards primaires
- 1 replica
- Analyzer personnalisé pour le français

**Mapping :**
- `@timestamp` : date au format ISO8601
- `level` : keyword (DEBUG, INFO, WARN, ERROR)
- `logger` : keyword (nom du logger)
- `message` : text (message du log)
- `thread` : keyword (nom du thread)
- `application` : keyword (nom de l'application)
- `environment` : keyword (dev, staging, prod)

**Étapes :**
1. Créez le template
2. Créez un index qui matche le pattern : `logs-application-2025-01`
3. Vérifiez que le template a été appliqué
4. Créez un autre index : `logs-application-2025-02`

### 💡 Aide
```json
PUT _index_template/nom_template
{
  "index_patterns": ["pattern-*"],
  "template": {
    "settings": { ... },
    "mappings": { ... }
  }
}
```

---

## ✅ Correction Exercice 2

```json
# Création du template
PUT _index_template/logs-application-template
{
  "index_patterns": ["logs-application-*"],
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "analysis": {
        "analyzer": {
          "french_analyzer": {
            "type": "french"
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis"
        },
        "level": {
          "type": "keyword"
        },
        "logger": {
          "type": "keyword"
        },
        "message": {
          "type": "text",
          "analyzer": "french_analyzer"
        },
        "thread": {
          "type": "keyword"
        },
        "application": {
          "type": "keyword"
        },
        "environment": {
          "type": "keyword"
        }
      }
    }
  }
}

# Vérification du template
GET _index_template/logs-application-template

# Création d'un index qui matche le pattern
PUT /logs-application-2025-01

# Vérification que le mapping a été appliqué
GET /logs-application-2025-01/_mapping

# Création d'un second index
PUT /logs-application-2025-02

# Vérifier les index créés
GET /_cat/indices/logs-application-*?v
```

**Points clés :**
✅ Le pattern `logs-application-*` s'applique à tous les index correspondants  
✅ L'analyzer français améliore la recherche sur le champ message  
✅ Les champs structurés (level, logger, etc.) sont en keyword  
✅ Le timestamp utilise le format ISO8601 standard  
✅ Tous les index créés héritent automatiquement de cette configuration  

---

## 📝 Exercice 3 : Alias avec filtre (15 min)

### Objectif
Créer des alias pour faciliter l'accès aux données et améliorer les performances.

### Consignes
En utilisant l'index `bibliotheque` créé précédemment :

1. **Créer un alias simple** nommé `livres` pointant vers `bibliotheque`

2. **Créer un alias avec filtre** nommé `livres-disponibles` qui :
   - Pointe vers `bibliotheque`
   - Filtre uniquement les livres disponibles (disponible = true)

3. **Créer un alias avec filtre** nommé `livres-recents` qui :
   - Pointe vers `bibliotheque`
   - Filtre uniquement les livres publiés après 2020

4. **Tester les alias** :
   - Effectuer une recherche via `GET /livres/_search`
   - Effectuer une recherche via `GET /livres-disponibles/_search`
   - Comparer les résultats

### 💡 Aide
```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "nom_index",
        "alias": "nom_alias",
        "filter": {
          "term": { "champ": "valeur" }
        }
      }
    }
  ]
}
```

---

## ✅ Correction Exercice 3

Avant de créer les alias, indexons quelques documents de test :

```json
# Indexer des livres de test
POST /bibliotheque/_bulk
{"index":{"_id":"1"}}
{"titre":"ElasticSearch Guide","auteur":"John Doe","isbn":"978-1234567890","annee_publication":2023,"nb_pages":450,"disponible":true,"categorie":"Informatique","prix":45.99}
{"index":{"_id":"2"}}
{"titre":"Python pour tous","auteur":"Jane Smith","isbn":"978-0987654321","annee_publication":2019,"nb_pages":380,"disponible":false,"categorie":"Informatique","prix":39.99}
{"index":{"_id":"3"}}
{"titre":"Machine Learning","auteur":"Bob Johnson","isbn":"978-1122334455","annee_publication":2021,"nb_pages":520,"disponible":true,"categorie":"Informatique","prix":52.50}
{"index":{"_id":"4"}}
{"titre":"Le Petit Prince","auteur":"Antoine de Saint-Exupéry","isbn":"978-2070612758","annee_publication":1943,"nb_pages":96,"disponible":true,"categorie":"Roman","prix":12.00}
{"index":{"_id":"5"}}
{"titre":"Kubernetes en action","auteur":"Alice Brown","isbn":"978-1617293726","annee_publication":2022,"nb_pages":612,"disponible":true,"categorie":"Informatique","prix":48.00}
```

Maintenant, créons les alias :

```json
# 1. Alias simple
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "bibliotheque",
        "alias": "livres"
      }
    }
  ]
}

# 2. Alias avec filtre - livres disponibles
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "bibliotheque",
        "alias": "livres-disponibles",
        "filter": {
          "term": {
            "disponible": true
          }
        }
      }
    }
  ]
}

# 3. Alias avec filtre - livres récents (après 2020)
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "bibliotheque",
        "alias": "livres-recents",
        "filter": {
          "range": {
            "annee_publication": {
              "gt": 2020
            }
          }
        }
      }
    }
  ]
}

# Vérifier les alias créés
GET /_cat/aliases?v

# Tester l'alias simple (devrait retourner 5 livres)
GET /livres/_search
{
  "query": {
    "match_all": {}
  }
}

# Tester l'alias avec filtre disponibles (devrait retourner 4 livres)
GET /livres-disponibles/_search
{
  "query": {
    "match_all": {}
  }
}

# Tester l'alias avec filtre récents (devrait retourner 3 livres: 2021, 2022, 2023)
GET /livres-recents/_search
{
  "query": {
    "match_all": {}
  }
}

# Bonus : combiner alias et requête
GET /livres-disponibles/_search
{
  "query": {
    "term": {
      "categorie": "Informatique"
    }
  }
}
```

**Créer plusieurs alias en une seule commande :**
```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "bibliotheque",
        "alias": "livres"
      }
    },
    {
      "add": {
        "index": "bibliotheque",
        "alias": "livres-disponibles",
        "filter": {
          "term": {
            "disponible": true
          }
        }
      }
    },
    {
      "add": {
        "index": "bibliotheque",
        "alias": "livres-recents",
        "filter": {
          "range": {
            "annee_publication": {
              "gt": 2020
            }
          }
        }
      }
    }
  ]
}
```

**Points clés :**
✅ Les alias permettent d'accéder aux données sans connaître le nom exact de l'index  
✅ Les alias filtrés améliorent les performances en réduisant le volume de données  
✅ Les alias peuvent pointer vers plusieurs index (utile pour les séries temporelles)  
✅ Les filtres dans les alias sont transparents pour l'utilisateur  
✅ On peut combiner filtre d'alias et requête utilisateur  

**Cas d'usage réels :**
- `logs-current` → pointe vers l'index actif
- `logs-read` → pointe vers tous les index de lecture
- `logs-write` → pointe vers l'index d'écriture uniquement

---

## 🎯 Points à retenir du Module 1

### Gestion des index
- Toujours définir un mapping explicite en production
- Choisir le bon nombre de shards dès le départ
- Utiliser des templates pour les séries temporelles

### Types de champs
- `text` → recherche full-text
- `keyword` → valeurs exactes, tri, agrégations
- `integer/float` → nombres
- `boolean` → true/false
- `date` → dates et timestamps

### Alias
- Permettent la flexibilité dans l'évolution des index
- Les filtres améliorent les performances
- Essentiels pour les stratégies de réindexation

---

## 📊 Commandes utiles pour la suite

```json
# Lister tous les index
GET /_cat/indices?v

# Supprimer un index
DELETE /nom_index

# Voir le mapping
GET /nom_index/_mapping

# Voir les settings
GET /nom_index/_settings

# Compter les documents
GET /nom_index/_count

# Fermer/ouvrir un index
POST /nom_index/_close
POST /nom_index/_open
```

---

**Temps estimé total : 50 minutes + 10 min de discussion**
