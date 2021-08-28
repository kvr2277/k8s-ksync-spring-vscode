# vink8s
Playing Kubernetes


# Steps
1. Install Docker

https://hub.docker.com/editions/community/docker-ce-desktop-mac

```
docker run -d -p 80:80 docker/getting-started
```

2. Install minikube [Source: https://minikube.sigs.k8s.io/docs/start/]

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
minikube start
```

Complete all test steps from 1 to 4

3. In VSCode add Kubernetes extension

4. Set up docker local registry [Source: https://docs.docker.com/registry/deploying/]

```
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

4. Point minikube to local registry [Source: https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d]

```
eval $(minikube -p minikube docker-env)
```

5. Clone code and run [Source: https://spring.io/guides/gs/spring-boot-kubernetes/]

a)
Check simple run command
```
./mvnw install
java -jar target/*.jar
curl localhost:8080/name
```

b)
Build image
```
./mvnw spring-boot:build-image  
```

c)
tag to local repository
```
docker tag demo:0.0.1-SNAPSHOT localhost:5000/testdemo
```

d)
push to local repository
```
docker push localhost:5000/testdemo
```

e)
run on K8s
```
kubectl delete -f deployment.yaml
kubectl apply -f deployment.yaml
```

f)
Check pod status
```
kubectl get all
```

g)
Expose on different port
```
kubectl port-forward svc/demo 8083:8080
```

h)
Curl
```
curl http://localhost:8083/name
```


i)
On side note - to create your own deployment.yaml file, you can use
```
kubectl create deployment demo --image=localhost:5000/testdemo --dry-run -o=yaml > deployment.yaml
kubectl create service clusterip demo --tcp=8080:8080 --dry-run -o=yaml >> deployment.yaml
```

When you make any changes to code and want to see in minikube, repeat steps b to f