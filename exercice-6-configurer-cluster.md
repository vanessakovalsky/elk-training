# Exercice 6 -  Configurer son cluster

## Ajouter des noeuds à notre cluster

* Pour commencer on va ajouter deux noeuds à notre cluster en ajoutant dans le fichier docker-compose les lignes suivantes :
```
`  elasticsearch2:
    build:
      context: elasticsearch/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z
      - elasticsearch:/usr/share/elasticsearch/data:z
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      - ES_JAVA_OPTS: -Xms512m -Xmx512m
      # Bootstrap password.
      # Used to initialize the keystore during the initial startup of
      # Elasticsearch. Ignored on subsequent runs.
      - ELASTIC_PASSWORD: ${ELASTIC_PASSWORD:-}
      - node.name=es02
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es03
      - cluster.initial_master_nodes=es01,es02,es03
    networks:
      - elk
    elasticsearch3:
    build:
      context: elasticsearch/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z
      - elasticsearch:/usr/share/elasticsearch/data:z
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      - ES_JAVA_OPTS: -Xms512m -Xmx512m
      # Bootstrap password.
      # Used to initialize the keystore during the initial startup of
      # Elasticsearch. Ignored on subsequent runs.
      - ELASTIC_PASSWORD: ${ELASTIC_PASSWORD:-}
      - node.name=es03
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es02
      - cluster.initial_master_nodes=es01,es02,es03 
      - elk
  ```
  * Une fois les deux services ajouter, remplacer dans les variables d'environnement de notre service elasticsearch la ligne `discovery.type: single-node` par :
  ```
      - node.name=es01
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es02,es03
      - cluster.initial_master_nodes=es01,es02,es03    
 
  ```
  * Redémarrer votre docker-compose

## Gérer la configuration

* actuellement les trois noeuds utilisent le même fichier de configuration qui est dans le dossier que vous avez cloner elasticsearch
* Vérifier à l'aide de la documentation ici : https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html que la configuraton est conforme aux recommandations
 
## Gérer les volumes importants

* Vérifier dans votre index heroes si l'utilisation du champs source est activé ?
* Créer un index en désactivant cette option
* Indexer dans ce nouvel index les mêmes données que dans votre index heroes
* Vérifier à l'aide de Kibana ou de l'API REST la taille des deux index, que constatez vous ?
