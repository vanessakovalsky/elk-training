# Module 5 - Exercices Kibana
## Visualisation et Dashboards

---

## 🔧 Prérequis

### Environnement
- Stack ELK Docker en cours d'exécution
- Kibana : http://localhost:5601
- Index `playstore` avec données chargées
- Credentials : elastic / changeme

---

## 📝 Exercice 1 : Discover - Exploration des données (20 min)

### Objectif
Maîtriser l'interface Discover pour explorer et filtrer les données.

### Consignes

**Étape 1 : Créer une Data View (5 min)**
1. Allez dans **Menu ☰** → **Stack Management** → **Data Views**
2. Cliquez sur **Create data view**
3. Name : `Play Store Apps`
4. Index pattern : `playstore`
5. Champs temps choisir : I don't wan't to use a date filter
6. Cliquez sur **Save data view**

**Étape 2 : Explorer dans Discover (15 min)**
1. Allez dans **Menu ☰** → **Analytics** → **Discover**
2. Sélectionnez la Data View `Play Store Apps`

**Questions à résoudre avec KQL :**

**Q1 :** Trouvez toutes les applications de jeux (catégories commençant par "GAME")
```
category: GAME*
```

**Q2 :** Trouvez les applications :
- Gratuites (type: Free)
- Avec note >= 4.5
- Catégorie SOCIAL ou COMMUNICATION

**Q3 :** Trouvez les applications ayant plus de 10 millions d'avis

**Q4 :** Sauvegardez cette dernière recherche sous le nom "Apps très populaires"

**Étape 3 : Personnaliser l'affichage**
1. Ajoutez les colonnes : app_name, category, rating, reviews, type
2. Triez par nombre d'avis décroissant
3. Sauvegardez cette vue sous le nom "Top Apps by Reviews"

---

## ✅ Correction Exercice 1

### Q1 - Apps de jeux
```kql
category: GAME*
```
ou
```kql
category: GAME_ACTION or category: GAME_CASUAL or category: GAME_STRATEGY or category: GAME_ARCADE or category: GAME_ADVENTURE
```

**Résultat attendu :** ~8 applications

### Q2 - Apps sociales gratuites bien notées
```kql
type: Free and rating >= 4.5 and (category: SOCIAL or category: COMMUNICATION)
```

**Résultat attendu :** Instagram, TikTok, Telegram, etc.

### Q3 - Apps très populaires
```kql
reviews > 10000000
```

**Résultat attendu :** YouTube, Facebook, WhatsApp, Instagram, Spotify, etc.

### Sauvegarder une recherche
1. Cliquez sur **Save** en haut à droite
2. Nom : "Apps très populaires"
3. Cochez "Store time with saved search" si nécessaire
4. Cliquez sur **Save**

### Colonnes personnalisées
Dans la sidebar gauche :
- Cliquez sur le **+** à côté de `app_name`
- Cliquez sur le **+** à côté de `category`
- Cliquez sur le **+** à côté de `rating`
- Cliquez sur le **+** à côté de `reviews`
- Cliquez sur le **+** à côté de `type`

Pour trier : cliquez sur l'en-tête de colonne `reviews`

---

## 📝 Exercice 2 : Dashboard Google Play Store (1h00)

### Objectif
Créer un dashboard complet d'analyse du Google Play Store.

### Consignes

Créez un dashboard nommé "Google Play Store Analytics" avec les visualisations suivantes :

#### Ligne 1 - KPIs (4 métriques)

**Viz 1 : Total Apps**
- Type : Metric
- Agrégation : Count
- Label : "Total Apps"

**Viz 2 : Note Moyenne**
- Type : Metric
- Agrégation : Average de `rating`
- Format : 0.00
- Label : "Average Rating"

**Viz 3 : Total Avis**
- Type : Metric
- Agrégation : Sum de `reviews`
- Format : 0,0 (avec séparateurs)
- Label : "Total Reviews"

**Viz 4 : % Apps Gratuites**
- Type : Metric
- Formule : Count de type=Free / Count total * 100
- Format : 0%
- Label : "% Free Apps"

#### Ligne 2 - Analyses par catégorie (2 visualisations)

**Viz 5 : Top 15 Catégories**
- Type : Bar vertical
- Axe X : Terms de `category` (top 15)
- Axe Y : Count
- Tri : Par count décroissant
- Titre : "Top Categories by Number of Apps"

**Viz 6 : Meilleures Notes par Catégorie**
- Type : Bar horizontal
- Axe Y : Terms de `category` (top 10)
- Axe X : Average de `rating`
- Tri : Par rating décroissant
- Couleur : par valeur (gradient)
- Titre : "Best Rated Categories"

#### Ligne 3 - Distribution et types (3 visualisations)

**Viz 7 : Free vs Paid**
- Type : Pie ou Donut
- Slice by : Terms de `type`
- Size by : Count
- Titre : "Free vs Paid Apps"

**Viz 8 : Distribution des Notes**
- Type : Bar vertical
- Axe X : Histogram de `rating` (intervalle 0.5)
- Axe Y : Count
- Titre : "Rating Distribution"

**Viz 9 : Content Rating**
- Type : Pie
- Slice by : Terms de `content_rating`
- Size by : Count
- Titre : "Apps by Content Rating"

#### Ligne 4 - Détails (2 visualisations)

**Viz 10 : Top 20 Apps**
- Type : Data table
- Rows : Terms de `app_name.keyword` (top 20)
- Metrics : 
  - Average de `rating`
  - Sum de `reviews`
  - Max de `installs_numeric`
- Tri : Par reviews décroissant
- Titre : "Top 20 Apps by Reviews"

**Viz 11 : Taille vs Popularité**
- Type : Scatter plot (ou histogram)
- Axe X : `size_mb` (buckets de 50MB)
- Axe Y : Average de `reviews`
- Titre : "App Size vs Popularity"

### Assemblage du Dashboard

1. **Menu ☰** → **Analytics** → **Dashboard**
2. Cliquez sur **Create dashboard**
3. Cliquez sur **Create visualization** pour chaque viz
4. Organisez les visualisations par glisser-déposer
5. Ajustez les tailles pour une disposition harmonieuse
6. Sauvegardez le dashboard sous "Google Play Store Analytics"

### Filtres globaux à ajouter

Ajoutez ces filtres en haut du dashboard :
1. **Filtre 1 :** `rating >= 4.0` (Apps bien notées)
2. **Filtre 2 :** `type: Free` (Apps gratuites)
3. **Filtre 3 :** `category: GAME*` (Jeux uniquement)

Les utilisateurs pourront activer/désactiver ces filtres.

---

## ✅ Correction Exercice 2 - Guide pas à pas

### Création des visualisations avec Lens

#### Viz 1 : Total Apps (Metric)
1. Dashboard → Create visualization → Lens
2. Déposez un champ dans l'espace central (ex: category)
3. Changez le type de viz à **Metric**
4. Le métrique par défaut est **Count of records** → parfait !
5. Cliquez sur le compteur et changez le label : "Total Apps"
6. **Save and return** → Nom : "Total Apps"

#### Viz 2 : Note Moyenne (Metric)
1. Create visualization → Lens
2. Type : **Metric**
3. Glissez `rating` dans la zone centrale
4. Lens va automatiquement créer une **Average**
5. Format : Cliquez sur la métrique → **Value format** → Number → Decimals : 2
6. Label : "Average Rating"
7. **Save and return** → Nom : "Average Rating"

#### Viz 3 : Total Avis (Metric)
1. Create visualization → Lens
2. Type : **Metric**
3. Glissez `reviews` dans la zone centrale
4. Changez l'agrégation en **Sum**
5. Format : Number avec séparateur de milliers
6. Label : "Total Reviews"
7. **Save and return** → Nom : "Total Reviews"

#### Viz 4 : % Apps Gratuites (Metric avec formule)
1. Create visualization → Lens
2. Type : **Metric**
3. Cliquez sur **Formula** dans le panneau de droite
4. Formule : 
```
count(kql='type: "Free"') / count() * 100
```
5. Format : Percent
6. Label : "% Free Apps"
7. **Save and return**

#### Viz 5 : Top 15 Catégories (Bar vertical)
1. Create visualization → Lens
2. Type : **Bar vertical**
3. Glissez `category` sur l'axe horizontal
4. Lens applique automatiquement **Top 15 by count**
5. L'axe vertical montre le **Count**
6. Dans les options de `category` :
   - Number of values : 15
   - Order by : Metric (Count)
   - Order direction : Descending
7. Titre : "Top Categories by Number of Apps"
8. **Save and return**

#### Viz 6 : Meilleures Notes (Bar horizontal)
1. Create visualization → Lens
2. Type : **Bar horizontal**
3. Glissez `category` sur l'axe vertical (gauche)
4. Glissez `rating` sur l'axe horizontal → Lens crée Average
5. Configuration de category :
   - Top 10 values
   - Order by : Average of rating
   - Descending
6. Couleurs : Color by value (gradient)
7. **Save and return**

#### Viz 7 : Free vs Paid (Pie)
1. Create visualization → Lens
2. Type : **Pie** ou **Donut**
3. Glissez `type` dans **Slice by**
4. La métrique par défaut (Count) est correcte
5. Options : Show labels, Show percentages
6. **Save and return**

#### Viz 8 : Distribution Notes (Bar vertical)
1. Create visualization → Lens
2. Type : **Bar vertical**
3. Glissez `rating` sur l'axe horizontal
4. Changez en **Histogram** avec interval 0.5
5. L'axe vertical montre Count
6. **Save and return**

#### Viz 9 : Content Rating (Pie)
1. Similar à Viz 7
2. Slice by : `content_rating`
3. **Save and return**

#### Viz 10 : Top 20 Apps (Data table)
1. Create visualization → Lens
2. Type : **Table**
3. Glissez `app_name.keyword` dans **Rows**
4. Configuration : Top 20 values
5. Ajoutez métriques :
   - Glissez `rating` → Average
   - Glissez `reviews` → Sum
   - Glissez `category` → Top 1 value (pour afficher)
6. Tri : Par Sum of reviews, Descending
7. **Save and return**

#### Viz 11 : Taille vs Popularité
1. Create visualization → Lens
2. Type : **Bar vertical**
3. Axe X : `size_mb` en Histogram (interval 50)
4. Axe Y : Average de `reviews`
5. **Save and return**

### Organisation du Dashboard

**Layout suggéré :**
```
+--------+--------+--------+--------+
|  Viz1  |  Viz2  |  Viz3  |  Viz4  |  (KPIs - hauteur 1)
+--------+--------+--------+--------+
|       Viz5      |      Viz6       |  (Barres - hauteur 2)
+-----------------+-----------------+
| Viz7  | Viz8  |      Viz9       |  (Pies - hauteur 2)
+-------+-------+-----------------+
|           Viz10                  |  (Table - hauteur 2)
+----------------------------------+
|           Viz11                  |  (Scatter - hauteur 2)
+----------------------------------+
```

### Ajout de filtres globaux

1. En haut du dashboard, cliquez sur **Add filter**
2. Filtre 1 :
   - Field : `rating`
   - Operator : is between
   - Values : 4.0 et 5.0
   - Label : "Rating >= 4.0"
3. Filtre 2 :
   - Field : `type`
   - Operator : is
   - Value : Free
   - Label : "Free Apps"
4. Filtre 3 :
   - Field : `category`
   - Operator : is one of
   - Values : Toutes les catégories GAME_*
   - Label : "Games Only"

---

## 📝 Exercice 3 : Time Series avec Bakery (40 min)

### Préparation des données

Créez un index `bakery` pour simuler des ventes de boulangerie.

```json
PUT /bakery
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      },
      "produit": {
        "type": "keyword"
      },
      "categorie": {
        "type": "keyword"
      },
      "quantite": {
        "type": "integer"
      },
      "prix_unitaire": {
        "type": "float"
      },
      "total": {
        "type": "float"
      },
      "vendeur": {
        "type": "keyword"
      }
    }
  }
}

# Charger les données (voir fichier dataset_bakery.md)
```

### Consignes

**Étape 1 : Créer la Data View**
1. Name : `Bakery Sales`
2. Index pattern : `bakery`
3. Time field : `timestamp`
4. Save

**Étape 2 : Visualisations Time Series**

**Viz 1 : CA par heure**
- Type : Line
- Axe X : Date histogram de `timestamp` (intervalle : hourly)
- Axe Y : Sum de `total`
- Titre : "Revenue by Hour"

**Viz 2 : Quantités vendues par catégorie**
- Type : Area (stacked)
- Axe X : Date histogram de `timestamp` (hourly)
- Axe Y : Sum de `quantite`
- Break down by : `categorie`
- Titre : "Sales Volume by Category"

**Viz 3 : Top 10 Produits**
- Type : Bar horizontal
- Axe Y : Terms de `produit` (top 10)
- Axe X : Sum de `total`
- Time range : Last 24 hours
- Titre : "Best Selling Products (24h)"

**Viz 4 : CA par vendeur**
- Type : Metric
- Rows : Terms de `vendeur`
- Metrics : Sum de `total`
- Titre : "Revenue by Seller"

**Étape 3 : Dashboard Bakery**
Assemblez ces visualisations dans un dashboard nommé "Bakery Dashboard".

**Étape 4 : Time Picker**
1. En haut à droite, configurez le time picker
2. Testez différentes périodes : Last 24 hours, Last 7 days, Today
3. Activez l'auto-refresh (15 seconds)

---

## ✅ Correction Exercice 3

### Visualisations détaillées

#### Viz 1 : CA par heure (Line chart)
1. Lens → Line
2. Axe X (horizontal) :
   - Glissez `timestamp`
   - Lens applique automatiquement **Date histogram**
   - Interval : **Auto** ou **Hourly**
3. Axe Y (vertical) :
   - Glissez `total`
   - Agrégation : **Sum**
4. Options :
   - Curve type : Smooth
   - Fill : None ou 0.3 opacity
5. Save

#### Viz 2 : Quantités par catégorie (Area stacked)
1. Lens → Area
2. Axe X : `timestamp` (Date histogram, hourly)
3. Axe Y : Sum de `quantite`
4. Break down by : Glissez `categorie` dans la zone **Break down by**
5. Options :
   - Stacked : By value (ou percentage)
   - Fill opacity : 0.6
6. Save

#### Viz 3 : Top produits (Bar horizontal)
1. Lens → Bar horizontal
2. Axe Y : Terms de `produit` (top 10, by Sum of total)
3. Axe X : Sum de `total`
4. Save

#### Viz 4 : CA par vendeur (Table)
1. Lens → Table
2. Rows : Terms de `vendeur`
3. Metrics :
   - Sum de `total`
   - Count of records (nombre de ventes)
   - Average de `total` (panier moyen)
4. Save

### Configuration du Time Picker

1. En haut à droite du dashboard : icône d'horloge
2. **Quick select** :
   - Today
   - Last 24 hours
   - Last 7 days
3. **Commonly used** :
   - Last 15 minutes
   - Last 30 minutes
   - Last 1 hour
4. **Refresh** :
   - Click on **Refresh every**
   - Sélectionnez 15 seconds

**Note :** Le time picker s'applique à toutes les visualisations du dashboard qui utilisent un champ de temps.

---

## 🎯 Points à retenir du Module 5

### Discover
- KQL pour filtrer rapidement les données
- Colonnes personnalisables et triables
- Sauvegarde de recherches réutilisables
- Export CSV possible

### Lens (Visualizations)
- Interface moderne par glisser-déposer
- Suggestions automatiques de visualisations
- Formules pour calculs complexes
- Multi-layers pour visualisations avancées

### Dashboards
- Agrégation de plusieurs visualisations
- Filtres globaux partagés
- Drill-down automatique (clic sur élément)
- Time picker pour données temporelles
- Partageables et exportables

### Types de visualisations courants
- **Metric** : KPIs, valeurs uniques
- **Bar** : Comparaisons
- **Line** : Évolutions temporelles
- **Area** : Volumes cumulés
- **Pie** : Proportions, répartitions
- **Table** : Données détaillées
- **Heatmap** : Densité, matrices

### Bonnes pratiques
- Commencer par les KPIs en haut
- Limiter à 10-15 visualisations par dashboard
- Utiliser des couleurs cohérentes
- Nommer clairement visualisations et dashboards
- Tester avec différentes périodes
- Optimiser les requêtes (filtres, limites)

---

**Temps estimé total : 2h00 avec manipulations et discussion**
