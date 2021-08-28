# vink8s
ksync for Spring Boot apps on VSCode 


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



## Enable hot reload of java code in VSCode

1.
--
Enable hot reload of Java program

In settings.json, have both of below as true/auto

```
java.debug.settings.hotCodeReplace
java.autobuild.enabled
```

and have below configuration in vscode launch.json
```
 "configurations": [
    {
        "type": "java",
        "name": "Launch Current File",
        "request": "launch",
        "mainClass": "${file}"
    }
```

and run your Spring Boot main class

when you make changes to your Java code, you should see changes reflecting in http://localhost:8080/name

2. For syncing local to kubectl environment, we will leverahe KSync (https://github.com/ksync/ksync)

You can read the documentation in above Github page. Below is list of commands in order that works

a)
```
curl https://ksync.github.io/gimme-that/gimme.sh | bash
```

b)
```
ksync init
```

c)
```
ksync watch &
```

d) in new terminal, we will try our own pod
```
kubectl get po --selector=app=demo
```

e) this is interesting piece, we will setup Ksync between our java target classes folder with our pod's classes folder

Since we used Spring Boot Build Image command, our code (class files and application.properties) will be under /workspace/BOOT-INF/classes - you can read more on why Spring stores in that way at https://spring.io/guides/topicals/spring-boot-docker/

(you can verify folder structure inside pod by navigating using 
```
kubectl exec --stdin --tty your-pod-name-here -- /bin/bash
```
)

f)
we establish Kysnc with below command

```
ksync create --selector=app=demo $(pwd)/target/classes /workspace/BOOT-INF/classes
```

g)
and check ksync status
```
ksync get
```

h)
and we setup port forwarding

```
kubectl get po --selector=app=demo -o=custom-columns=:metadata.name --no-headers | \
    xargs -IPOD kubectl port-forward POD 8083:8080 &
```

you can now make changes to your Java code and see that reflecting in pod automatically
at http://localhost:8083/name

(ocassionally, you may see the changes take 1 or 2 seconds to reflect, neverthless it's fast and avoids all the pain)

and that's it! 
