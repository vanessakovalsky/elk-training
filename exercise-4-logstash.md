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
* Définir une section input qui permet de déclarer le point d'entrée de données que l'on souhaite que logstash utilise
```

```

