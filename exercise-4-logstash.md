# Récupérer et traiter des logs avec les pipelines de Logstash

Cet exercice a pour objectif : 
* De définir un pipeline logstash récupérant des logs Apache
* De transformer le format de log pour le rendre exploitable
* D'envoyer les données dans ElasticSearch


## Pré-requis : 
* Avoir une machine avec Elasticsearch d'installé ainsi qu'une machine avec Logstash
* Sur la machine ou Logstash est installé, nous allons installé apache et le lancer 
* Exemple sous Linux Debian / Ubuntu : 
```
sudo apt install apache2
sudo systemctl start apache2
sudo usermod -aG adm logstash
```
* Vérifier que cela fonctionne en appelant via curl http://localhost , vous devriez avoir une page it's works

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
    file { path => "/var/log/apache2/access.log" }
}
```
* Dans ce cas là, on appelle le ficheir de logs d'accès que Apache génère
* A l'aide de la documentation, https://www.elastic.co/guide/en/logstash/current/plugins-inputs-file.html, on voit qu'on peut donner d'autre paramètres à notre entrée :
```
input {
    file { 
        path => "/var/log/apache2/access.log"
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
    file { path => "/var/log/apache2/access.log" }
}

filter {
    grok {
        match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
}
```

### Ajouter une sortie à notre pipeline Logstash

* 
