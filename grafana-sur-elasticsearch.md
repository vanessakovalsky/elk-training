# Consignes Grafana + Elasticsearch DSL

Ce document contient les consignes d'utilisation pour exploiter des requêtes DSL dans Grafana.

## 📌 Objectif
Pouvoir interroger des données Elasticsearch dans un dashboard Grafana via des requêtes DSL.

---

## 🔧 Prérequis
- Avoir une instance Grafana fonctionnelle
- Une source de données Elasticsearch configurée
- Index Elasticsearch contenant les champs nécessaires

---

## 📜 Exemple de requête DSL Elasticsearch

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

---

## 📊 Utilisation dans Grafana

1. Aller dans **Dashboards > New panel**
2. Choisir la source Elasticsearch
3. Passer en mode **Query → Lucene/DSL JSON**
4. Coller la requête DSL ci-dessus
5. Sélectionner la visualisation souhaitée (Graph, Pie, Bar, etc.)

---

## 🎯 But final
Visualiser les agrégations `aggs` sous forme d’indicateurs, de tableaux ou de graphiques.
