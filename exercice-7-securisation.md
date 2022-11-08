# Exercice 7 - sécurisation d'elasticsearch


## Mettre en place de l'authentification

* Une authentification basique est en place par défaut et repose sur un fichier d'utilisateurs.
* Nous allons mettre en place une authentification avec Ngninx, afin d'empêcher l'acccès direct à notre elasticsearch
* Pour cela, ajoutons un conteneur ngninx qui servira de proxy devant notre elastic, ajouter les lignes suivantes dans les services du docker compose :
```
  proxy:
    image: nginx:1-alpine
    restart: always
    ports:
      - 5601:80
      - 9200:9201
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - kibana
      - elasticsearch
```
* ajouter un dossier nginx et un sous dossier conf.d
* Créer un fichier elasticsearch.conf dans ce sous dossier avec le contenu suivant :
```
server {
  listen 9201;
  server_name elasticsearch;

  # permit large uploads
  client_max_body_size 25M;

  location / {
    auth_basic "Don't touch me there";
    auth_basic_user_file /etc/nginx/conf.d/htpasswd;

    proxy_http_version  1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_buffering off;
    proxy_pass http://elasticsearch:9200;
  }
}
```
* Créer un fichier kibana.conf dans ce sous dossier avec le contenu suivant :
```
server {
  listen 80;
  server_name kibana;
  
  # permit large uploads
  client_max_body_size 25M;

  location / {
    auth_basic "Don't touch me there";
    auth_basic_user_file /etc/nginx/conf.d/htpasswd;

    proxy_http_version  1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_buffering off;
    proxy_pass http://kibana:5601;
  }
}
```
* Connecter vous sur le conteneur nginx et créer les deux utilisateurs :
```
sudo htpasswd -c /etc/nginx/htpasswd.elastic.users elasticuser01
sudo htpasswd -c /etc/nginx/htpasswd.kibana.users kibanauser01
```
* Redémarrer votre environnement docker-compose 
* Vous devriez maintenant avoir besoin de vous connecter lorsque vous tentez d'accéder à votre utilisateur

## Mise en place d'un certificat SSL

* Commençons par ajouter pour chaque noeud du cluster les variables d'environnement et les secrets nécessaire dans notre fichier docker-compose :
```
    environment:
      - xpack.security.http.ssl.enabled=true
      - xpack.security.http.ssl.key=/usr/share/elasticsearch/config/secrets/certificate.key.pem
      - xpack.security.http.ssl.certificate=/usr/share/elasticsearch/config/secrets/certificate.crt.pem
      - xpack.security.http.ssl.certificate_authorities=/usr/share/elasticsearch/config/secrets/root.pub.pem
      - xpack.security.transport.ssl.enabled=false
      - xpack.security.transport.ssl.key=/usr/share/elasticsearch/config/secrets/certificate.key.pem
      - xpack.security.transport.ssl.certificate=/usr/share/elasticsearch/config/secrets/certificate.crt.pem
      - xpack.security.transport.ssl.certificate_authorities=/usr/share/elasticsearch/config/secrets/root.pub.pem
    secrets:
      - source: root.pub.pem
        target: /usr/share/elasticsearch/config/secrets/root.pub.pem
        uid: '1000'
        gid: '1000'
      - source: certificate.key.pem
        target: /usr/share/elasticsearch/config/secrets/certificate.key.pem
        uid: '1000'
        gid: '1000'
      - source: certificate.crt.pem
        target: /usr/share/elasticsearch/config/secrets/certificate.crt.pem
        uid: '1000'
        gid: '1000'
```
* Faisons de même pour Kibana
```
 environment:
      - SERVER_NAME=kibana.example.com
      - ELASTICSEARCH_HOSTS=https://elasticsearch.example.com:9200
      - ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=/run/secrets/root.pub.pem
      - SERVER_SSL_ENABLED=true
      - SERVER_SSL_CERTIFICATE=/run/secrets/certificate.crt.pem
      - SERVER_SSL_KEY=/run/secrets/certificate.key.pem
      - SERVER_SSL_CERTIFICATEAUTHORITIES=/run/secrets/root.pub.pem
    secrets:
      - root.pub.pem
      - certificate.key.pem
      - certificate.crt.pem
```
* Ensuite rajoutons à notre docker-compose les secrets correspondants :
```
 environment:
      - SERVER_NAME=kibana.example.com
      - ELASTICSEARCH_HOSTS=https://elasticsearch.example.com:9200
      - ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=/run/secrets/root.pub.pem
      - SERVER_SSL_ENABLED=true
      - SERVER_SSL_CERTIFICATE=/run/secrets/certificate.crt.pem
      - SERVER_SSL_KEY=/run/secrets/certificate.key.pem
      - SERVER_SSL_CERTIFICATEAUTHORITIES=/run/secrets/root.pub.pem
    secrets:
      - root.pub.pem
      - certificate.key.pem
      - certificate.crt.pem
```
* Il ne reste plus qu'à redémarer nos conteneurs 

## Pour aller plus loin :

* Il est possible de mettre de l'authentification LDAP au dessus de la distribution OpenSource d'Elasticsearch à l'aide de ce plugin : https://github.com/skysbsb/elk-opendistro-plugins-ldap 