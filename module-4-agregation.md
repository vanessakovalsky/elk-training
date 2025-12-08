# Module 4 - Exercices Agrégations
## Google Play Store - Cas Pratique Complet

---

## 🔧 Prérequis

### Environnement
- Stack ELK Docker en cours d'exécution
- Index `playstore` chargé avec 50 applications

### Vérification
```json
GET /playstore/_count
# Devrait retourner: {"count": 50}

GET /playstore/_search
{
  "size": 1
}
```

---

## 📝 Exercice 1 : Agrégations simples (30 min)

### Objectif
Maîtriser les agrégations métriques et buckets de base.

### Consignes

**Question 1 - Statistiques globales :**
Calculez :
- La note moyenne globale de toutes les apps
- Le nombre total d'avis (somme du champ reviews)
- Le nombre total d'applications
- La note minimale et maximale

**Question 2 - Top catégories :**
Trouvez :
- Les 10 catégories avec le plus d'applications
- Pour chaque catégorie, calculez la note moyenne
- Triez par nombre d'applications décroissant

**Question 3 - Distribution des notes :**
Créez un histogram montrant la distribution des notes :
- Intervalles de 0.5 (0-0.5, 0.5-1.0, 1.0-1.5, etc.)
- Comptez le nombre d'apps dans chaque intervalle

**Question 4 - Apps gratuites vs payantes :**
Comparez les apps Free et Paid :
- Nombre d'apps de chaque type
- Note moyenne par type
- Nombre moyen d'avis par type

### 💡 Aide
```json
{
  "size": 0,
  "aggs": {
    "nom_agregation": {
      "avg": { "field": "champ" }
    }
  }
}
```

---

## ✅ Correction Exercice 1

### Question 1 - Statistiques globales
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "note_moyenne": {
      "avg": {
        "field": "rating"
      }
    },
    "total_avis": {
      "sum": {
        "field": "reviews"
      }
    },
    "nombre_apps": {
      "value_count": {
        "field": "_id"
      }
    },
    "stats_notes": {
      "stats": {
        "field": "rating"
      }
    }
  }
}
```

**Résultat attendu :**
```json
{
  "aggregations": {
    "note_moyenne": {
      "value": 4.42
    },
    "total_avis": {
      "value": 550000000
    },
    "nombre_apps": {
      "value": 50
    },
    "stats_notes": {
      "count": 50,
      "min": 4.0,
      "max": 4.7,
      "avg": 4.42,
      "sum": 221.0
    }
  }
}
```

### Question 2 - Top catégories
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category",
        "size": 10,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        }
      }
    }
  }
}
```

**Résultat attendu :**
```json
{
  "aggregations": {
    "top_categories": {
      "buckets": [
        {
          "key": "COMMUNICATION",
          "doc_count": 8,
          "note_moyenne": {
            "value": 4.3125
          }
        },
        {
          "key": "SOCIAL",
          "doc_count": 7,
          "note_moyenne": {
            "value": 4.371428
          }
        },
        {
          "key": "GAME_ACTION",
          "doc_count": 2,
          "note_moyenne": {
            "value": 4.1
          }
        }
      ]
    }
  }
}
```

### Question 3 - Distribution des notes
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "distribution_notes": {
      "histogram": {
        "field": "rating",
        "interval": 0.5,
        "min_doc_count": 0,
        "extended_bounds": {
          "min": 0,
          "max": 5
        }
      }
    }
  }
}
```

**Résultat attendu :**
```json
{
  "aggregations": {
    "distribution_notes": {
      "buckets": [
        {"key": 0.0, "doc_count": 0},
        {"key": 0.5, "doc_count": 0},
        {"key": 1.0, "doc_count": 0},
        {"key": 1.5, "doc_count": 0},
        {"key": 2.0, "doc_count": 0},
        {"key": 2.5, "doc_count": 0},
        {"key": 3.0, "doc_count": 0},
        {"key": 3.5, "doc_count": 0},
        {"key": 4.0, "doc_count": 12},
        {"key": 4.5, "doc_count": 38}
      ]
    }
  }
}
```

### Question 4 - Free vs Paid
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_type": {
      "terms": {
        "field": "type"
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "avis_moyen": {
          "avg": {
            "field": "reviews"
          }
        },
        "stats_completes": {
          "stats": {
            "field": "rating"
          }
        }
      }
    }
  }
}
```

**Résultat attendu :**
```json
{
  "aggregations": {
    "par_type": {
      "buckets": [
        {
          "key": "Free",
          "doc_count": 48,
          "note_moyenne": {"value": 4.4146},
          "avis_moyen": {"value": 11450000}
        },
        {
          "key": "Paid",
          "doc_count": 2,
          "note_moyenne": {"value": 4.5},
          "avis_moyen": {"value": 9876543}
        }
      ]
    }
  }
}
```

---

## 📝 Exercice 2 : Agrégations imbriquées (30 min)

### Objectif
Créer des agrégations multi-niveaux pour des analyses complexes.

### Consignes

**Question 1 - Analyse par catégorie et type :**
Pour chaque catégorie :
- Nombre d'apps Free vs Paid
- Note moyenne par type
- Taille moyenne (size_mb) par type

**Question 2 - Content Rating détaillé :**
Pour chaque content_rating :
- Nombre total d'apps
- Top 5 catégories dans ce rating
- Note moyenne globale du rating

**Question 3 - Analyse temporelle :**
Groupez les apps par mois de dernière mise à jour (last_updated) :
- Nombre d'apps mises à jour ce mois
- Note moyenne des apps mises à jour
- Catégories les plus actives

### 💡 Aide
```json
{
  "aggs": {
    "niveau1": {
      "terms": { "field": "..." },
      "aggs": {
        "niveau2": {
          "terms": { "field": "..." },
          "aggs": {
            "metrique": {
              "avg": { "field": "..." }
            }
          }
        }
      }
    }
  }
}
```

---

## ✅ Correction Exercice 2

### Question 1 - Analyse par catégorie et type
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_categorie": {
      "terms": {
        "field": "category",
        "size": 20
      },
      "aggs": {
        "par_type": {
          "terms": {
            "field": "type"
          },
          "aggs": {
            "note_moyenne": {
              "avg": {
                "field": "rating"
              }
            },
            "taille_moyenne": {
              "avg": {
                "field": "size_mb"
              }
            }
          }
        }
      }
    }
  }
}
```

### Question 2 - Content Rating détaillé
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_content_rating": {
      "terms": {
        "field": "content_rating"
      },
      "aggs": {
        "nombre_apps": {
          "value_count": {
            "field": "_id"
          }
        },
        "top_categories": {
          "terms": {
            "field": "category",
            "size": 5
          }
        },
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        }
      }
    }
  }
}
```

**Résultat attendu :**
```json
{
  "aggregations": {
    "par_content_rating": {
      "buckets": [
        {
          "key": "Everyone",
          "doc_count": 18,
          "note_moyenne": {"value": 4.45},
          "top_categories": {
            "buckets": [
              {"key": "COMMUNICATION", "doc_count": 6},
              {"key": "MAPS_AND_NAVIGATION", "doc_count": 3}
            ]
          }
        },
        {
          "key": "Teen",
          "doc_count": 22,
          "note_moyenne": {"value": 4.39},
          "top_categories": {
            "buckets": [
              {"key": "SOCIAL", "doc_count": 6},
              {"key": "ENTERTAINMENT", "doc_count": 4}
            ]
          }
        }
      ]
    }
  }
}
```

### Question 3 - Analyse temporelle
```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_mois": {
      "date_histogram": {
        "field": "last_updated",
        "calendar_interval": "month",
        "format": "yyyy-MM"
      },
      "aggs": {
        "nombre_updates": {
          "value_count": {
            "field": "_id"
          }
        },
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "categories_actives": {
          "terms": {
            "field": "category",
            "size": 5
          }
        }
      }
    }
  }
}
```

---

## 📝 Exercice 3 : TP Google Play Store - Analyse complète (1h00)

### Objectif
Réaliser une analyse marketing complète du Play Store pour préparer un dashboard.

### Contexte
Vous êtes analyste pour un éditeur d'applications. Votre manager vous demande un rapport complet sur l'état du marché.

### Consignes détaillées

#### Partie 1 : KPIs principaux (15 min)

Créez une requête qui retourne :
1. **Nombre total d'applications**
2. **Note moyenne globale**
3. **Nombre total d'avis** (somme)
4. **Pourcentage d'apps gratuites**

#### Partie 2 : Analyse concurrentielle (15 min)

**Question A :** Top 10 catégories par popularité
- Classées par nombre d'apps
- Avec la note moyenne de chaque catégorie
- Avec le nombre moyen d'avis

**Question B :** Apps les plus populaires
- Top 10 apps par nombre d'avis
- Afficher : nom, catégorie, note, nombre d'avis

#### Partie 3 : Analyse de marché (15 min)

**Question A :** Distribution par taille d'application
- Créez des tranches : <50MB, 50-100MB, 100-500MB, >500MB
- Nombre d'apps par tranche
- Note moyenne par tranche

**Question B :** Analyse des installations
- Groupez par tranche d'installations (installs)
- Comptez les apps dans chaque tranche
- Calculez la note moyenne par tranche

#### Partie 4 : Insights avancés (15 min)

**Question A :** Catégories premium
- Trouvez les catégories avec note moyenne > 4.5
- Comptez le nombre d'apps
- Calculez le nombre moyen d'avis

**Question B :** Tendances récentes
- Apps mises à jour en novembre 2023
- Groupées par catégorie
- Avec statistiques de notes

### 💡 Tips
- Utilisez `size: 0` pour ne retourner que les agrégations
- Combinez plusieurs agrégations dans une seule requête
- Utilisez des sous-agrégations pour enrichir l'analyse

---

## ✅ Correction Exercice 3

### Partie 1 : KPIs principaux

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "kpi_total_apps": {
      "value_count": {
        "field": "_id"
      }
    },
    "kpi_note_moyenne": {
      "avg": {
        "field": "rating"
      }
    },
    "kpi_total_avis": {
      "sum": {
        "field": "reviews"
      }
    },
    "apps_par_type": {
      "terms": {
        "field": "type"
      }
    }
  }
}
```

**Calcul du pourcentage :**
```
% Free = (48 / 50) * 100 = 96%
```

### Partie 2A : Top 10 catégories

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "top_categories": {
      "terms": {
        "field": "category",
        "size": 10,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "avis_moyen": {
          "avg": {
            "field": "reviews"
          }
        },
        "tri_par_popularite": {
          "bucket_sort": {
            "sort": [
              {"_count": {"order": "desc"}}
            ],
            "size": 10
          }
        }
      }
    }
  }
}
```

### Partie 2B : Apps les plus populaires

```json
GET /playstore/_search
{
  "_source": ["app_name", "category", "rating", "reviews"],
  "size": 10,
  "sort": [
    {
      "reviews": "desc"
    }
  ]
}
```

**Résultat attendu (top 3) :**
1. YouTube - 89,565,241 avis
2. Facebook - 78,158,306 avis
3. WhatsApp - 69,119,316 avis

### Partie 3A : Distribution par taille

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_taille": {
      "range": {
        "field": "size_mb",
        "ranges": [
          {
            "key": "< 50MB",
            "to": 50
          },
          {
            "key": "50-100MB",
            "from": 50,
            "to": 100
          },
          {
            "key": "100-500MB",
            "from": 100,
            "to": 500
          },
          {
            "key": "> 500MB",
            "from": 500
          }
        ]
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "nombre_apps": {
          "value_count": {
            "field": "_id"
          }
        }
      }
    }
  }
}
```

### Partie 3B : Analyse des installations

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_installations": {
      "terms": {
        "field": "installs",
        "size": 15,
        "order": {
          "installs_numeric_avg": "desc"
        }
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "installs_numeric_avg": {
          "avg": {
            "field": "installs_numeric"
          }
        }
      }
    }
  }
}
```

### Partie 4A : Catégories premium

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "toutes_categories": {
      "terms": {
        "field": "category",
        "size": 50
      },
      "aggs": {
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "avis_moyen": {
          "avg": {
            "field": "reviews"
          }
        },
        "filtre_premium": {
          "bucket_selector": {
            "buckets_path": {
              "noteAvg": "note_moyenne"
            },
            "script": "params.noteAvg > 4.5"
          }
        }
      }
    }
  }
}
```

### Partie 4B : Tendances novembre 2023

```json
GET /playstore/_search
{
  "size": 0,
  "query": {
    "range": {
      "last_updated": {
        "gte": "2023-11-01",
        "lte": "2023-11-30"
      }
    }
  },
  "aggs": {
    "par_categorie": {
      "terms": {
        "field": "category",
        "size": 15
      },
      "aggs": {
        "stats_notes": {
          "stats": {
            "field": "rating"
          }
        },
        "nombre_updates": {
          "value_count": {
            "field": "_id"
          }
        }
      }
    },
    "stats_globales": {
      "stats": {
        "field": "rating"
      }
    }
  }
}
```

---

## 📊 Requêtes bonus avancées

### Pipeline Aggregation - Top 3 catégories par avis moyen

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category",
        "size": 50
      },
      "aggs": {
        "avis_moyen": {
          "avg": {
            "field": "reviews"
          }
        },
        "top_3": {
          "bucket_sort": {
            "sort": [
              {"avis_moyen": {"order": "desc"}}
            ],
            "size": 3
          }
        }
      }
    }
  }
}
```

### Percentiles des notes par catégorie

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "par_categorie": {
      "terms": {
        "field": "category",
        "size": 10
      },
      "aggs": {
        "percentiles_notes": {
          "percentiles": {
            "field": "rating",
            "percents": [25, 50, 75, 90, 95, 99]
          }
        }
      }
    }
  }
}
```

### Corrélation taille/popularité

```json
GET /playstore/_search
{
  "size": 0,
  "aggs": {
    "taille_vs_popularite": {
      "histogram": {
        "field": "size_mb",
        "interval": 50
      },
      "aggs": {
        "avis_moyen": {
          "avg": {
            "field": "reviews"
          }
        },
        "note_moyenne": {
          "avg": {
            "field": "rating"
          }
        },
        "nombre_apps": {
          "value_count": {
            "field": "_id"
          }
        }
      }
    }
  }
}
```

---

## 🎯 Points à retenir du Module 4

### Agrégations métriques
- `avg`, `sum`, `min`, `max`, `stats`, `extended_stats`
- `value_count` pour compter les documents
- `cardinality` pour valeurs uniques
- `percentiles` pour distributions

### Agrégations buckets
- `terms` : grouper par valeurs
- `range` : grouper par plages
- `histogram` : grouper par intervalles fixes
- `date_histogram` : grouper par périodes

### Agrégations imbriquées
- Combiner plusieurs niveaux d'analyse
- Chaque bucket peut contenir des sous-agrégations
- Métriques et buckets peuvent se mélanger

### Pipeline aggregations
- `bucket_sort` : trier et limiter les buckets
- `bucket_selector` : filtrer les buckets
- `avg_bucket`, `sum_bucket` : agréger sur les buckets

### Bonnes pratiques
- Utiliser `size: 0` quand seules les agrégations comptent
- Limiter la profondeur des agrégations imbriquées (3-4 niveaux max)
- Utiliser des filtres pour réduire le volume de données
- `min_doc_count` pour exclure les buckets vides

---

**Temps estimé total : 2h30 avec corrections et discussion**
