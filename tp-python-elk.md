# Monitorer les logs d'une application Python avec ELK

Cet exercice a pour objectifs :
* de récupérer les logs générés par une application Python
* De les indexer dans un ElasticSearch pour permettre la recherche
* De monitorer l'application au travers d'un tableau de bord Kibana


## Mise en place de l'application Python

* Nous allons instancier un conteneur avec Python avec l'image officielle
* Dans ce conteneur (ou dans un DockerFile qui s'appuie sur cette image au choix), installer avec pip flask et python-logstash
* Le module Python-logstash permet d'envoyer les logs à logstash. 
* Une fois les modules installé crée une application python contenant le code suivant en adaptant les lignes HOST à votre configuration pour atteindre logstash  
```python
from flask import Flask
app = Flask(__name__)

import logging
import logstash
import sys

HOST = 'logstash'

app.test_logger = logging.getLogger('python-logstash-logger')
app.test_logger.setLevel(logging.INFO)
app.test_logger.addHandler(logstash.LogstashHandler(HOST, 5959, version=1))


@app.route('/')
def hello_world():
    app.test_logger.info("Hello there")
    return 'Hello, World!'

app.run(host='0.0.0.0', port=5555)
```
* Lancer l'application Python et vérifier dans le navigateur si votre application s'affiche bien

## Créer un Pipeline Logstash

* Sur votre environnement contenant Logstash, créer un nouveau pipeline, celui-ci contiendra les élements suivant : 
  * en entrée (input) : l'utilisation du plugin beats sur le port 5044 
  * en sortie (output) : envoie des données à un index elasticsearch
* Vérifier côté elasticsearch si l'index se créé bien et si les données sont bien indexées

## Créer un tableau de bord Kibana 

* Dans Kibana créer un nouveau tableau de bord en récupérant les données indexées
* Choisir un graphique et un tableau pertinent en fonction des logs à ajouter à ce tableau de bord.

--> Envoyer dans Teams un screenshot de votre tableau de bord
