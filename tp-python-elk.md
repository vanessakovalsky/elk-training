# Monitorer les logs d'une application Python avec ELK

Cet exercice a pour objectifs :
* de récupérer les logs générés par une application Python
* De les indexer dans un ElasticSearch pour permettre la recherche
* De monitorer l'application au travers d'un tableau de bord Kibana


## Mise en place de l'application Python

* Nous allons instancier un conteneur avec Python avec l'image officielle
* Dans ce conteneur (ou dans un DockerFile qui s'appuie sur cette image au choix), installer avec pip flask et python-logstash-async
* Le module Python-logstash-async permet de stocker les données de manière temporaires avant de les envoyer logstash. 
* Une fois les modules installé crée une application python contenant le code suivant en adaptant les lignes LOGSTASH_HOST et LOGSTAH_DB_PATH à votre configuration pour atteindre logstash et à votre chemin pour stocker les données 
```python
from flask import Flask
app = Flask(__name__)

from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import FlaskLogstashFormatter

LOGSTASH_HOST = "192.168.200.19"
LOGSTASH_DB_PATH = "/home/vagrant/app-data"
LOGSTASH_TRANSPORT = "logstash_async.transport.BeatsTransport"
LOGSTASH_PORT = 5044

logstash_handler = AsynchronousLogstashHandler(
    LOGSTASH_HOST,
    LOGSTASH_PORT,
    database_path=LOGSTASH_DB_PATH,
    transport=LOGSTASH_TRANSPORT,
)
logstash_handler.formatter = FlaskLogstashFormatter(metadata={"beat": "myapp"})
app.logger.addHandler(logstash_handler)

@app.route('/')
def hello_world():  
    app.logger.info("Hello there")
    return 'Hello, World!'
```
* Lancer l'application Python et vérifier si des logs sont bien créé dans le chemin que vous avez défini

## Créer un Pipeline Logstash

* Sur votre environnement contenant Logstash, créer un nouveau pipeline, celui-ci contiendra les élements suivant : 
  * en entrée (input) : l'utilisation du plugin beats sur le port 5044 
  * en sortie (output) : envoie des données à un index elasticsearch
* Vérifier côté elasticsearch si l'index se créé bien et si les données sont bien indexées

## Créer un tableau de bord Kibana 

* Dans Kibana créer un nouveau tableau de bord en récupérant les données indexées
* Choisir un graphique et un tableau pertinent en fonction des logs à ajouter à ce tableau de bord.

--> Envoyer dans Teams un screenshot de votre tableau de bord
