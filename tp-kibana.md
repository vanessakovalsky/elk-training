# Créer un tableau de bord pour nos films avec Kibana

## Ajout de l'index

* POur commencer nous allons ajouter l'index elasticsearch dans les données de Kibana
* Utiliser le menu pour aller Dans Stack management
* Puis cliquer sur Index Pattern, et suivre les étapes
* Pour le nom d'index utiliser ```movies``` (ou celui de l'index qui ;contient vos données) et le champ fields.release_date pour le champs de temps

![](https://user.oc-static.com/upload/2017/09/27/15065439987946_kibana-home.png)



## Discover

* Dans le menu aller sur Kibana (Analytics, et cliquer sur Discover
* Vous arrivez alors sur l'écran de découverte qui vous permet de visualiser vos données et de faire des recherches 
* Vous ne voyer probablement aucune données, car par défaut seul les données correspondant au 15 dernière minutes sont affichées. 
* Aller voir en haut à droite pour changer cela 
![](https://user.oc-static.com/upload/2017/09/27/1506544078945_kibana-timerange.png) 
* Vous obtenez alors la liste de tous les documents(films) qui correspondent aux dates que vous avez sélectionné :
![](https://user.oc-static.com/upload/2017/09/27/15065441390644_kibana-discover.png) 
* Vous pouvez alors faire des requêtes en utilisants le DSL (les mêmes requêtes que pour Elasticsearch), voir la documentation icihttps://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html 
* En reprenant les recherches du précédentes, afficher différentes données, cela vous permet de les visualiser. 
* Vous pouvez en plus filtrer les données obtenus à l'aide des filtres à gauches de l'écran
* Ou même définir les informations à afficher
![](https://user.oc-static.com/upload/2017/09/27/15065441663374_kibana-limitfields.png)

* Enregistrer vos recherches et partager les avec la formatrice

## Visualisation des données dans les graphiques

* Kibana permet d'aggregéer ces données et de les afficher dans des diagrammes parlant
* Pour créer une visualisation, il est indispensable de d'abord s'avoir quel résultat vous souhaitez obtenir
* Par exemple ici, on souhaite afficher les 10 réalisateurs ayant fait le plus de films dans un camambert et pour chaque réalisateur, les genres de ses films
![](https://user.oc-static.com/upload/2017/09/27/15065443826025_kibana-sketch-small.jpeg)

* Une fois l'objectif clair, vous pouvez commencer à réaliser le graphe, pour cela on va définir les données
* Ici on définit la liste des 1à réalisateurs les plus profiliques, puis pour chaque réalisateur un aggregat (bucket) de ses 5 genres de prédilection.
![](https://user.oc-static.com/upload/2017/09/27/1506544409065_kibana-directors.png)

* La documentation officielle permet de connaitre l'ensemble des outils graphique disponible : https://www.elastic.co/guide/en/kibana/current/create-panels-with-editors.html 

* On souhaite rajouter un autre graphique qui permet de visualiser l'évolution des notes dans le temps. 
* Pour cela on souhaite visualiser pour chaque décénnie, la répartition (en %) des notes obtenues par les films
![](https://user.oc-static.com/upload/2017/10/03/15070380444889_kibana-sketch-activite.jpeg)

* Les données sont présentées comme suit : 
    * En abscisse les décénnies de 1920 à aujourd'hui
    * En ordonnées le pourcentage de film par note données


## Création d'un tableau de bord

* Créer un tableau de bord qui reprend les deux graphiques que vous avez créer 
* Ajouter un compteur qui indique le nombre de films présent en base
* Partager le tableau de bord avec la formatrice