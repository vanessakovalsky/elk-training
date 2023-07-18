# Récupérer et traiter des logs avec les pipelines de Logstash

Cet exercice a pour objectif : 
* De définir un pipeline logstash récupérant des logs Apache
* De transformer le format de log pour le rendre exploitable
* D'envoyer les données dans ElasticSearch


## Pré-requis : 
* Avoir une machine avec Elasticsearch d'installé ainsi qu'une machine avec Logstash
* Sur la machine ou Logstash est installé, récupérer le fichier apache-access.log https://raw.githubusercontent.com/vanessakovalsky/elk-training/main/apache-access.log  et noter l'endroit où est le fichier

## Définir le pipeline de Logstash
* Créer un fichier apache.conf 
```
input {}

filter {}

output {}
```
* Ce fichier contient les 3 élements de notre pipeline :
* * input : quelles sont les données que l'on traite
* * filter : quels sont les filtres que l'on applique sur les données
* * output : où logstash envoit t'il les données 

### Input : définition des données d'entrées 

* Définir une section input qui permet de déclarer le point d'entrée de données que l'on souhaite que logstash utilise. 
```
input {
    file { path => "/usr/share/logstash/apache-access.log" }
}
```
* Dans ce cas là, on appelle le ficheir de logs d'accès de Apache 
* A l'aide de la documentation, https://www.elastic.co/guide/en/logstash/current/plugins-inputs-file.html, on voit qu'on peut donner d'autre paramètres à notre entrée :
```
input {
    file { 
        path => "/usr/share/logstash/apache-access.log"
        start_position => "beginning"
        sincedb_path => "/dev/null"
    }
}
```
* On rajoute donc les deux paramètres suivant : 
  * start_position : permet de définir à quel endroit logstash commence à traiter le fichier
  * sincedb_path : garde la trace de la position courante du curseur dans le fichier de logs, ici on recommence systèmatiquement du début, donc on désactive cette trace 

### Filtres les données

* Pour filtrer les données il est possible d'utiliser différents plugins de filtrage : https://www.elastic.co/guide/en/logstash/current/filter-plugins.html 
* Ici nous allons utiliser grok : https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html 
* La syntaxe d'un pattern grok est la suivante :
```
%{SYNTAX:SEMANTIC}
```
  * SYNTAX : nom du pattern, utilisant un filtre prédéfini : exemple IP ou WORD
  * SEMANTIC : identifiant de la valeur récupérée (que vous devez définir vous même)
* Par exemple pour traiter la ligne de logs suivante
```
55.3.244.1 GET /index.html 15824 0.043
```
* Le pattern Grok pourrait être celui-là
```
filter {
    grok {
        match => { "message" => "%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}" }
    }
}
```
* Ce qui donnerait le résultat suivant :
```
client: 55.3.244.1
method: GET
request: /index.html
bytes: 15824
duration: 0.043
```
*  Dans notre cas, nous utiliserons un pattern prédéfini pour les logs apache nommé COMMONAPACHELOG
*  Tous les patterns https://github.com/hpcugent/logstash-patterns/blob/master/files/grok-patterns
* Ajoutons ce pattern à notre fichier apache.conf
```
input {
    file { path => "/usr/share/logstash/apache-access.log" }
}

filter {
    grok {
        match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
}
```

### Ajouter une sortie à notre pipeline Logstash

* Il nous reste à rajouter la sortie vers ElasticSearch dans notre fichier apache.conf :
```
output {
    elasticsearch {
         hosts => "localhost:9200"
         index => "apache-%{+YYYY.MM.dd}"
         user => "logstash_internal"
		 password => "${LOGSTASH_INTERNAL_PASSWORD}"
    }
}
```
* On définit alors deux paramètre : 
  * hosts : permet de définir l'adresse pour accéder au elasticsearch
  * index : de donner un nom à l'index dans lequel sont envoyé les données
  * user : l'utilisateur à utiliser pour se connecter
  * password : le mot de passe associé

--> Notre pipeline est prêt à être testé

## Tester notre pipeline

* On va commencer par modifier le fichier de configuration pour désactiver la connexion, pour cela ouvrir le fichier qui est dans le dossier elasticsearch/config et qui s'appelle elasticsearch.yml et replacer son contenu par le contenu suivant :
```
---
## Default Elasticsearch configuration from Elasticsearch base image.
## https://github.com/elastic/elasticsearch/blob/master/distribution/docker/src/docker/config/elasticsearch.yml
#
cluster.name: "docker-cluster"
network.host: 0.0.0.0

## X-Pack settings
## see https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html
#
xpack.license.self_generated.type: basic
xpack.security.enabled: false

xpack.security.authc:
  anonymous:
    username: anonymous_user 
    roles: role1
    authz_exception: true
```
* Copier le fichier de log utilisé dans le conteneur : 
```
docker cp ./apache-access.log docker-elk_logstash_1:/usr/share/logstash/apache-access.log
```
* Copier le fichier de configuration de logstash :
```
docker cp ./apache.conf docker-elk_logstash_1:/usr/share/logstash/apache.conf
```
* Rédémarrer les services pour prendre en compte le fichier de configuration que nous avons crées : 
```
 docker-compose restart 
```
* Une fois le service redémarré, nous pouvons vérifier que l'index a bien été crée via l'API d'ElasticSearch ou via le devtools de Kibana : 
```
curl "http://localhost:9200/_cat/indices?v"
```
* Vous devriez voir un index donc le nom commence par apache
* Afficher alors la structure de données de l'index, puis comparer les données présentes dans elasticsearch et celle présente dans le fichier de logs Apache d'origine

## Pour aller plus loin : 

* [Envoyer ses logs docker vers elastic search](https://logz.io/blog/docker-logging/)
* [récupérer et traiter des données depuis l'API de Twitter ](https://github.com/daniellavoie/formation-elk/tree/master/exercice-twitter)
