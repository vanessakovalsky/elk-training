 # 📊 Exercice – Dashboard Google Play Store sous Grafana

⏱️ 1h
🎯 Objectif : Reproduire le même dashboard que Kibana, mais dans Grafana
📂 Source : Index Elasticsearch playstore

## 🟥 DASHBOARD À CRÉER

Nom du Dashboard :
Google Play Store Analytics

## Structure recommandée en 4 lignes comme dans Kibana.

🔹 Ligne 1 — KPIs (4 Stat Panels)

Viz	Type	Métrique	Détails
1. Total Apps	Stat	Metric → Count	Titre : Total Apps
2. Note Moyenne	Stat	Metric → Average(rating)	Format : 2 décimales · Titre : Average Rating
3. Total Avis	Stat	Metric → Sum(reviews)	Format : avec séparateur 1 000 · Label Total Reviews
4. % Apps Gratuites	Stat	Expression → 🧮	Count(type="Free") / Count(total) * 100 → Format : %
Pour la Viz 4 (% Free Apps) → Métrique combinée

Dans Grafana → onglet Transformations :

Ajouter 2 queries :
A = Count(type="Free")
B = Count(type="*")

Transformation Add field from calculation
Formule : (A/B) * 100

Format en pourcentage

🔹 Ligne 2 — Analyses par catégorie (2 Graphs)
Viz	Type Grafana	X	Y	Options

5. Top 15 Catégories	Bar chart (Vertical)	Terms(category, size=15)	Count	Tri ↓ par valeur
6. Meilleures Notes par Catégorie	Bar chart (Horizontal)	Terms(category, size=10)	Average(rating)	Tri ↓ Average(rating), mode horizontal, palette gradient recommandée
7. 
🔹 Ligne 3 — Types & Distributions (3 Charts)
Viz	Type Grafana	Breakdown	Metric	Options

9. Free vs Paid	Pie ou Donut	Terms(type)	Count	Titre : Free vs Paid Apps
10. Distribution des Notes	Histogram (Vertical)	Histogram(rating)	Count	Bucket size = 0.5
11. Content Rating	Pie chart	Terms(content_rating)	Count	Titre : Apps by Content Rating
🔹 Ligne 4 — Détails & Analyse avancée (2 visualisations)
Viz	Type Grafana	Dimensions	Métriques

13. Top 20 Apps	Table	Terms(app_name.keyword, top=20)	Avg(rating) · Sum(reviews) · Max(installs_numeric)
14. Taille vs Popularité	Scatter Plot	X = size_mb (bucket 50MB)	Y = Avg(reviews)

Pour le Scatter Plot, penser à mode Points + bucket size manuel si nécessaire.

## 🧱 Assemblage du Dashboard (version Grafana)

Dashboard → + New Dashboard

Pour chaque visualisation → Add panel

Datasource : Elasticsearch → Index playstore

Créer les 11 Viz listées ci-dessus

Organiser en grille :

📍 Ligne 1 : 4 KPIs alignés
📍 Ligne 2 : 2 bar charts pleine largeur chacun 50%
📍 Ligne 3 : 3 charts 33% / 33% / 33%
📍 Ligne 4 : Table large + Scatter 40%/60%


Sauvegarde :
Titre dashboard → Google Play Store Analytics

## 🎚 Filtres Globaux à ajouter (via Variables)
Nom	Type	Valeur
Filtre 1	Query filter	rating >= 4.0
Filtre 2	Query filter	type:Free
Filtre 3	Query filter	category:GAME*

→ L’utilisateur peut les activer/désactiver dans le panneau supérieur.

## 🔥 Résultat final attendu sous Grafana

✔ Même layout que Kibana
✔ Même KPIs
✔ Même analyses segmentées
✔ Dashboard interactif, filtrable & exploitable
