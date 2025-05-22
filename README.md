snap install helm --classic

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

kubectl create namespace monitoring

helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.maximumStartupDurationSeconds=300
NAME: kube-prometheus-stack
LAST DEPLOYED: Thu May 22 15:06:12 2025
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
NOTES:
kube-prometheus-stack has been installed. Check its status by running:
  kubectl --namespace monitoring get pods -l "release=kube-prometheus-stack"

Get Grafana 'admin' user password by running:

  kubectl --namespace monitoring get secrets kube-prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo

Access Grafana local instance:

  export POD_NAME=$(kubectl --namespace monitoring get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=kube-prometheus-stack" -oname)
  kubectl --namespace monitoring port-forward $POD_NAME 3000

Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.


helm list -n monitoring


docker build --no-cache -t order-service:latest -f Dockerfile.dev .
minikube start --driver=docker
eval $(minikube -p minikube docker-env)
minikube addons enable metrics-server
minikube addons enable dashboard
minikube addons enable ingress
minikube dashboard
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm uninstall kube-prometheus-stack -n monitoring
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.maximumStartupDurationSeconds=300


kubectl apply -f k8s

kubectl get secret --namespace monitoring kube-prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 -d && echo
minikube service kube-prometheus-stack-grafana -n monitoring &
minikube service kube-prometheus-stack-prometheus -n monitoring &




# Monitoring:

kubectl top pods
kubectl top nodes
kubectl logs -f deployment/order-service
