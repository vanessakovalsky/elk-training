# Installation

Cet exercice a pour objectif de :
* installer elastic et kibana en local sur votre poste (ou dans une VM)


## Pré-requis :  Java

ElasticSearch étant basé sur le langage Java, veillez à disposer de **Java 8** installé sur votre machine. Vous pouvez vérifier l'installation de Java à l'aide de la commande `java -version`.

### ElasticSearch

* Téléchargez la dernière version d'ElasticSearch sur [www.elastic.co](https://www.elastic.co/downloads/elasticsearch).

* Dézippez l'archive dans le dossier de votre choix, par exemple `~/progs/elasticsearch-7`.

* Les exécutables nécessaires au fonctionnement d'ElasticSearch se trouvent dans le dossier `$HOME/progs/elasticsearch-<version>/bin`, **elasticsearch** permet de lancer le noeud et **plugin** permet d'installer des plugins.

* Le fichier `$HOME/progs/elasticsearch-7/config/elasticsearch.yml`, au format [YAML](http://fr.wikipedia.org/wiki/YAML), permet de configurer ElasticSearch.

* La configuration par défaut nous suffit pour l'instant.

* Vous pouvez à présent démarrer le serveur.

```bash
bin/elasticsearch
```

* Il est possible d'ajouter des options Java pour augmenter la mémoire allouée à ElasticSearch en passant directement les paramètres de la JVM à l'exécutable ElsasticSearch.

```bash
bin/elasticsearch -Xmx=2G -Xms=2G
```

* Pour vérifier le démarrage de votre noeud ElasticSearch : [http://localhost:9200/](http://localhost:9200/)

Vous devriez obtenir une réponse qui ressemble à celle là :
```json
{
  "name" : "kovalsky.local",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "Y6_xP3W-TZWeqwvq5ks8NQ",
  "version" : {
    "number" : "7.5.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "8bec50e1e0ad29dad5653712cf3bb580cd1afcdf",
    "build_date" : "2020-01-15T12:11:52.313576Z",
    "build_snapshot" : false,
    "lucene_version" : "8.3.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

## Kibana

* Téléchargez la dernière version de Kibana correspondante à votre OS sur [www.elastic.co](https://www.elastic.co/downloads/kibana).

* Dézippez l'archive dans le dossier de votre choix, par exemple `~/progs/kibana-7`.

* Pour vérifier l'installation de Kibana, vous pouvez lancer la commande suivante :

```bash
bin/kibana --version
```

* Vous pouvez maintenant lancer Kibana :

```bash
bin/kibana
```

* Connectez-vous à votre instance de Kibana locale avec votre browser : [http://localhost:5601](http://localhost:5601)

## Suivant

Vous pouvez passer à l'étape suivante : [Opérations CRUD](./exercice-2-crud.md)
