### 1. Prearation and configuration
* Create a folder in local repository and copy (or create) all necessary files to the folder.
  * `main.py`: Python script.
  * `Dockerfile`: Used to create an image in Docker. Packages needed in `main.py` should be included.
  * `deployment.yaml`: Instructions to Kubernetes, indicating service details.
  * `default.json`: Deafult credentials of the service account. Get the key from [this page](https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually). It's passed to `tiling.py` when connecting to storage client. (Not necessary if running locally, but Kubernetes require service account information for access.)
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
  > docker images ls
* Run locally.
  > docker run [IMAGE-NAME]   
  
  If no error, then move on to Kubernetes. 
  
### 3. Play with Kubernetes (reference: [Container Registry](https://cloud.google.com/container-registry/docs/quickstart))
* Tag the image.
  > docker tag [USERNAME]/[IMAGE-NAME] gcr.io/[PROJECT-ID]/[IMAGE-NAME]:latest
* Push the image.
  > docker push gcr.io/[PROJECT-ID]/[IMAGE-NAME]:latest
* Create the deployment server, i.e. send the YAML file to Kubernetes.
  > kubectl apply -f deployment.yaml
* Check pods.
  > kubectl get pods   
* If pod **STATUS** is **Running**, then everything is good. After some time the **STATUS** will become **Completed**. If not, then check pod events and figure out the error.
  > kubectl describe pod [POD-NAME]
* Check the cloud bucket for the tiles. Or check the pod logs:
  > kubectl logs -f [POD-NAME]
  
### 4. Clean up
* Delete services, pods, images, and the cluster.
  > kubectl delete service [SERVICE-NAME]   
  > kubectl delete pod [POD-NAME]   
  > kubectl delete image [IMAGE-NAME]   
  > gcloud container clusters delete [CLUSTER-NAME]
