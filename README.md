VERBO     RUTA / URL
* GET       /api/v1/orders                200 OK
POST      /api/v1/orders        BODY    201 OK / 202 ACCEPT
* GET       /api/v1/orders/{id}           200 OK
PUT       /api/v1/orders/{id}   BODY    200 OK
PATCH     /api/v1/orders/{id}   BODY    200 OK
DELETE    /api/v1/orders/{id}           204 NO CONTENT

OPTIONS
HEAD

401 NOT AUTHENTICATED
403 FORBIDDEN
404 NOT FOUND
429 Throttling DDoS

>= 500

minikube delete --all --purge
minikube start --driver=docker
eval $(minikube docker-env)
docker build -t order-service:latest -f Dockerfile.dev .
minikube image load order-service:latest
minikube addons enable ingress
minikube addons enable metrics-server

kubectl rollout restart deployment order-service
