# Créer un tableau de bord pour nos logs Apache avec Kibana

Cet exercice a pour objectifs :
* de créer un tableau de bord a partir des logs apaches

## Pré-requis : 
* Avoir une instance d'ElasticSearch, de Logstash et de Kibana qui tourne
* Avoir fait l'exercice 4 pour avoir des logs dans un index elastic search

## Définition des données à utiliser :
### Ajout de filtre dans Logstash 
* Nous avons besoin d'ajouter deux filtres dans le pipeline de logstash, ajouter les dans le fichier apache.conf et redémarrer logstash :
```
filter {
    grok {
        match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
    
    date {
        match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    }

    mutate {
        convert => {
            "response" => "integer"
            "bytes" => "integer"
        }
    }
}
```
  * Le premier, timestamp permet de récupèrer la date au bon format pour la visualisation des données par date
  * Le second, mutate,  l'action convert permet de convertir la réponse HTTP et la taille de la requête qui sont par défaut en type string vers le type entier, car en effet, Kibana gère ses visualisations différemment selon le type de données que vous lui envoyez. 

### Ajout des données dans Kibana

* Rendez-vous sur votre Kibana en local :http://localhost:5601/
* Aller sur le menu de gauche et cliquer sur Stack management : 

![](https://devopssec.fr/images/articles/elk/apache/menu-stack-management.jpg)

* Nous devons définir l'index à utiliser. Pour cela cliquer sur Index Patterns dans le volet de Gauche, puis sur "Create index pattern"

![](https://devopssec.fr/images/articles/elk/apache/create-pattern-index.jpg)

* Le nom de notre index commence par Apache, le pattern sera donc : apache-* 

![](https://devopssec.fr/images/articles/elk/apache/define-pattern-index.jpg)

* Kibana demande alors comment gérer le filtre temporel (sur quel champs il doit s'appuyer), utiliser le champs @timestamp défini par les filtres de logstash

![](https://devopssec.fr/images/articles/elk/apache/timestamp-pattern-index.jpg)

* Enfin cliquer sur le bouton "Create index pattern" et vous verrez la liste des champs apparaître :

![](https://devopssec.fr/images/articles/elk/apache/view-pattern-index.jpg)

## Visualisation des données



### Rechercher et filtrer dans les données

* Pour accéder à vos données, cliquer sur le menu, puis cliquer sur Discover dans le menu

![](https://devopssec.fr/images/articles/elk/apache/menu-discover.jpg)

* Vous arriver alors sur une page qui liste vos données :

![](https://devopssec.fr/images/articles/elk/apache/index-pattern-view.jpg)

* Vous pouvez depuis le champs recherche filtrer les données obtenus 

![](https://devopssec.fr/images/articles/elk/apache/index-pattern-search.jpg) 

### Créer un tableau de bord pour ses données

#### Nombre de visiteurs uniques 

* Nous allons maintenant créer un tableau de bord pour nos données. 
* Pour cela on utilise le menu de gauche, et on clique sur Dashboard

![](https://devopssec.fr/images/articles/elk/apache/kibana-menu-dashboard.jpg)

* Pour ajouter des éléments à notre tableau de bord, il est nécessaire de créer des visualisations dans Kibana
* Voici la liste des visualisations les plus utilisés : 
  * Line, area, et bar charts : compare différentes métriques sur l'axe X et Y.
  * Pie chart : graphique circulaire.
  * Data table : données en format de tableau.
  * Metric : affiche une seule métrique.
  * Goal and gauge : affiche un nombre avec des indicateurs de progression.
  * Tag cloud : affiche les mots dans un nuage, où la taille du mot correspond à son importance.

![](https://devopssec.fr/images/articles/elk/apache/metric_visualisation_kibana.jpg)

* Ici nous choisissons "Metric"
* Ensuite Kibana vous demande de paramètrer votre visualisation. 
* Voici la liste des paramètres les plus communs : 
  * Average : valeur moyenne.
  * Count : nombre total de documents correspondant à une requête.
  * Max : la valeur la plus élevée.
  * Median : médiane.
  * Min : la valeur la plus basse.
  * Sum : La valeur totale.
  * Unique Count : nombre unique d'une métrique.

![](https://devopssec.fr/images/articles/elk/apache/apache-kibana-uniq-user.jpg)

* Ici nous avons choisi "Unique count" sur le champs hote afin de récupérer le nombre d'hôtes différents qui viennent sur notre site web
* Il nous reste à sauvegarder et à choisir un nom pour notre graphique

#### Temps moyen passé sur le site

* Nous créons un autre graphique de type "area" pour obtenir le temps moyen des visites sur le site
* Pour l'axe Y nous utilisons une aggregation de type "Average" sur le champs "bytes"

![](https://devopssec.fr/images/articles/elk/apache/apache-kibana-bytes-y-axis.jpg)

* Pour l'axe X nous allons utiliser les buckets d'aggregations qui trient les documents en compartiments selon le contenu du document 
* Voici les valeurs les plus communes pour les buckets :
  * Date histogram : fractionne un champ de date en compartiments par intervalle.
  * Date range : valeurs comprises dans une plage de dates que vous spécifiez.
  * Filter : filtre les données récupérées (ex : traiter que les erreurs 404).
  * IPv4 range : plages d'adresses IPv4.
  * Range : plages de valeurs pour un champ numérique.
  * Terms : Spécifiez le nombre d'éléments supérieurs ou inférieurs d'un champ donné à afficher, classés par nombre ou par une métrique personnalisée.

![](https://devopssec.fr/images/articles/elk/apache/apache-kibana-bytes-x-axis.jpg)

* Ici nous utilisons "Date histogram"
* Il nous reste à enregistrer et nommer notre graphique.

#### Top des requêtes en erreurs
* Nous ajoutons un dernier graphique, qui liste dans un tableau le top des requêtes en erreurs 
* Cette fois nous créons un graphique de type "Data table" avec la configuration suivante : 
  * une aggregation de type "Count"
  * une Bucket aggregation de type "Terms" sur le champ "request"
  * tri par ordre décroissant par l'agrégation "Count"

![](https://devopssec.fr/images/articles/elk/apache/kibana-requests-error-part1.jpg) 

* Il nous reste à ajouter un filtrer pour n'avoir que les requêtes en erreur (code réponse différent de 200) 
* Pour cela, cliquer sur le bouton "Add filter"
* Ajouter un filtre sur le field : "response", avec l'operateur "is not" et la valeur : "200"

![](https://devopssec.fr/images/articles/elk/apache/kibana-requests-error-part2.jpg)

### Mise en page et enregistrement du tableau de bord
* Nous avons maintenant les 3 visualisationsd de prêtes, il vous reste à les organiser sur la page comme vous le souhaiter
* Une fois que cela vous convient, vous pouvez cliquer sur le bouton "Save" en haut de l'écran

![](https://devopssec.fr/images/articles/elk/apache/kibana-dashboard-save.jpg)

* Par exemple, vous pouvez obtenir quelque chose de proche de ça : 

![](https://devopssec.fr/images/articles/elk/apache/kibana-final-dashboard.jpg)

--> Félicitations vous savez maintenant créer des tableaux de bords avec Kibana

## Pour aller plus loin : travailler sur de l'OpenData SNCF : 
* https://stph.scenari-community.org/contribs/nos/es5/co/es5.html 
