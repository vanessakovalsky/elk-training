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
!()[https://devopssec.fr/images/articles/elk/apache/menu-stack-management.jpg]

* Nous devons définir l'index à utiliser. Pour cela cliquer sur Index Patterns dans le volet de Gauche, puis sur "Create index pattern"
!()[https://devopssec.fr/images/articles/elk/apache/create-pattern-index.jpg]

* Le nom de notre index commence par Apache, le pattern sera donc : apache-* 
!()[https://devopssec.fr/images/articles/elk/apache/define-pattern-index.jpg]

* Kibana demande alors comment gérer le filtre temporel (sur quel champs il doit s'appuyer), utiliser le champs @timestamp défini par les filtres de logstash
!()[https://devopssec.fr/images/articles/elk/apache/timestamp-pattern-index.jpg]

* Enfin cliquer sur le bouton "Create index pattern" et vous verrez la liste des champs apparaître :
!()[https://devopssec.fr/images/articles/elk/apache/view-pattern-index.jpg]

## Visualisation des données

### Rechercher et filtrer dans les données

### Créer un tableau de bord pour ses données

## Pour aller plus loin : travailler sur de l'OpenData SNCF : 
* https://stph.scenari-community.org/contribs/nos/es5/co/es5.html 
