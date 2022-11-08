# Exercice 6 -  Configurer son cluster

## Ajouter des noeuds à notre cluster

* Pour commencer on va ajouter deux noeuds à notre cluster en remplaçant le contenu de votre fichier docker-compose par le suivant :

```
version: '3.7'

services:

  # The 'setup' service runs a one-off script which initializes the
  # 'logstash_internal' and 'kibana_system' users inside Elasticsearch with the
  # values of the passwords defined in the '.env' file.
  #
  # This task is only performed during the *initial* startup of the stack. On all
  # subsequent runs, the service simply returns immediately, without performing
  # any modification to existing users.
  setup:
    build:
      context: setup/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    init: true
    volumes:
      - setup:/state:Z
    environment:
      ELASTIC_PASSWORD: ${ELASTIC_PASSWORD:-}
      LOGSTASH_INTERNAL_PASSWORD: ${LOGSTASH_INTERNAL_PASSWORD:-}
      KIBANA_SYSTEM_PASSWORD: ${KIBANA_SYSTEM_PASSWORD:-}
    networks:
      - elk
    depends_on:
      - elasticsearch

  elasticsearch:
    # build:
    #   context: elasticsearch/
    #   args:
    #     ELASTIC_VERSION: ${ELASTIC_VERSION}
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}    
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z
      - elasticsearch:/usr/share/elasticsearch/data:z
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      # Bootstrap password.
      # Used to initialize the keystore during the initial startup of
      # Elasticsearch. Ignored on subsequent runs.
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-}
      - node.name=es01
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es02,es03
      - cluster.initial_master_nodes=es01,es02,es03    

    networks:
      - elk

  elasticsearch2:
    # build:
    #   context: elasticsearch/
    #   args:
    #     ELASTIC_VERSION: ${ELASTIC_VERSION}
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}    
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z
      - elasticsearch2:/usr/share/elasticsearch/data:z
    ports:
      - "9201:9200"
      - "9301:9300"
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      # Bootstrap password.
      # Used to initialize the keystore during the initial startup of
      # Elasticsearch. Ignored on subsequent runs.
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-}
      - node.name=es02
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es03
      - cluster.initial_master_nodes=es01,es02,es03
    networks:
      - elk
  elasticsearch3:
  #   build:
  #     context: elasticsearch/
  #     args:
  #       ELASTIC_VERSION: ${ELASTIC_VERSION}
    image: docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}    
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z
      - elasticsearch3:/usr/share/elasticsearch/data:z
    ports:
      - "9202:9200"
      - "9302:9300"
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      # Bootstrap password.
      # Used to initialize the keystore during the initial startup of
      # Elasticsearch. Ignored on subsequent runs.
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-}
      - node.name=es03
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es02
      - cluster.initial_master_nodes=es01,es02,es03 
    networks:
      - elk

  logstash:
    build:
      context: logstash/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    volumes:
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro,Z
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro,Z
    ports:
      - "5044:5044"
      - "50000:50000/tcp"
      - "50000:50000/udp"
      - "9600:9600"
    environment:
      LS_JAVA_OPTS: -Xms256m -Xmx256m
      LOGSTASH_INTERNAL_PASSWORD: ${LOGSTASH_INTERNAL_PASSWORD:-}
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    build:
      context: kibana/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    volumes:
      - ./kibana/config/kibana.yml:/usr/share/kibana/config/kibana.yml:ro,Z
    ports:
      - "5601:5601"
    environment:
      KIBANA_SYSTEM_PASSWORD: ${KIBANA_SYSTEM_PASSWORD:-}
      # Fleet plugin
      KIBANA_FLEET_SETUP: '1'
    networks:
      - elk
    depends_on:
      - elasticsearch

networks:
  elk:
    driver: bridge

volumes:
  setup:
  elasticsearch:
  elasticsearch2:
  elasticsearch3:
```
* Puis remplacer le contenu du fichier elasticsearch.yml par le suivant :
```
---
## Default Elasticsearch configuration from Elasticsearch base image.
## https://github.com/elastic/elasticsearch/blob/main/distribution/docker/src/docker/config/elasticsearch.yml
#
cluster.name: "docker-cluster"
network.host: 0.0.0.0

## X-Pack settings
## see https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html
#
#xpack.license.self_generated.type: trial
xpack.security.enabled: false

```

* Redémarrer votre docker-compose
```
docker-compose down
docker-compose up -d
```
* Au bout de quelques instants, vous aurez alors un cluster Elasticsearch fonctionnel avec 3 noeuds

## Gérer la configuration

* actuellement les trois noeuds utilisent le même fichier de configuration qui est dans le dossier que vous avez cloner elasticsearch
* Vérifier à l'aide de la documentation ici : https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html que la configuraton est conforme aux recommandations
* Si besoin, créer des fichiers séparés pour la configuration de chaque noeud et modifier les lignes concernées dans le fichier docker-compose.yml
 
## Gérer les volumes importants

* Ajouter du contenu dans votre cluster (voir exercice 2)
* Vérifier dans votre index heroes si l'utilisation du champs source est activé en utilisant l'API ou bien en utilisant Kibana pour cela
* Créer un index en désactivant cette option
* Indexer dans ce nouvel index les mêmes données que dans votre index heroes
* Vérifier à l'aide de Kibana ou de l'API REST la taille des deux index, que constatez vous ?
