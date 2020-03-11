# GKE How to Guide

Use tiling as example.

### 1. Prearation and configuration
* Create a folder in local repository and copy (or create) all necessary files to the folder.
  * Slides.
  * [`main.py`](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/blob/master/Kubernetes/main.py): Python script.
  * [`Dockerfile`](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/blob/master/Kubernetes/Dockerfile): Used to create an image in Docker. Packages needed in `main.py` should be included.
  * [`deployment.yaml`](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/blob/master/Kubernetes/deployment.yaml): Instructions to Kubernetes, indicating service details.
  * `default.json`: Default credentials of the service account. Get the key from [Create service account key page](https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually). It's passed to [`tiling.py`](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/blob/master/Kubernetes/tiling.py) when connecting to storage client.      
_ps. Not necessary if running locally, but Kubernetes require service account information for access. Or we can use [Docker Desktop with Kubernetes](https://www.docker.com/products/kubernetes) and [enable Kubernetes in Docker Desktop](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)._
* Create an account in [Docker Hub](https://hub.docker.com/). Remember the username and password.
* Set a default compute zone and create a cluster.
  > gcloud config set compute/zone us-central1-a   
  > gcloud container clusters create [CLUSTER-NAME]
* Change to the target directory, and log in to Docker.
  > docker login --username=[USERNAME]   
  
  Then enter the password.   
  
### 2. Play with Docker
* Create an image.
  > docker build -f Dockerfile -t [IMAGE-NAME]:latest .
* Check the image.
  > docker image ls    
  
  Output should resemble:
  ![image](https://user-images.githubusercontent.com/35391238/75697877-b4aa1680-5c7b-11ea-81c8-329ac690f46c.png)
* Run locally.
  > docker run [IMAGE-NAME]   
  
  If no error, then move on to Kubernetes. 
  
### 3. Play with Kubernetes (ref: [Container Registry](https://cloud.google.com/container-registry/docs/quickstart))
* Tag the image.
  > docker tag [IMAGE-NAME] gcr.io/[PROJECT-ID]/[IMAGE-NAME]:latest
* Push the image.
  > docker push gcr.io/[PROJECT-ID]/[IMAGE-NAME]:latest
* Now check the image to see if a new one starting with **gcr.io** exists.
  > docker image ls    
  
  Output should resemble:
  ![image](https://user-images.githubusercontent.com/35391238/75697928-c68bb980-5c7b-11ea-95f4-50c153285f07.png)

* Create the deployment server, i.e. send the YAML file to Kubernetes.
  > kubectl apply -f deployment.yaml
* Check pods.
  > kubectl get pods   
  
  Output should resemble:   
  ![image](https://user-images.githubusercontent.com/35391238/75698148-300bc800-5c7c-11ea-81da-b22c95d0cca5.png)   
  If pod **STATUS** is **Running**, then everything is good. After some time **STATUS** will change to **Completed**. If not, then check pod events and figure out the error.
  > kubectl describe pod [POD-NAME]
* Check the cloud bucket for the tiles. Or check the pod logs:
  > kubectl logs -f [POD-NAME]
  
### 4. Clean up (ref [here](https://linuxize.com/post/how-to-remove-docker-images-containers-volumes-and-networks/))
* Delete container, image, service, deployment, pod, cluster...    
   
  **Only after deleting the deployment are we able to delete pods. Otherwise a new pod will be genereated in place of the deleted one.**
  > docker container ls -a   
  > docker container rm [CONTAINER-ID]   
     
  > docker image ls   
  > docker image rm [IMAGE-NAME]  
     
  > kubectl get services   
  > kubectl delete service [SERVICE-NAME]   
     
  > kubectl get deployments   
  > kubectl delete deployment [DEPLOYMENT-NAME]   
     
  > kubectl get pods   
  > kubectl delete pod [POD-NAME]    
     
  > gcloud container clusters delete [CLUSTER-NAME]
