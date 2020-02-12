# GCP Keras Deep Learning Research 
 
This repo contains my research work about DNN algorithms on GCP. It's an ongoing research and updates will be made from time to time.

* About data:   
MINST datset (numbers), [Kather dataset](https://www.nature.com/articles/srep27988) (small tissue slides), and [TCGA dataset](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/data/TCGA-images.html) (large tissue slides).

* About codes:   
Mainly in Python and Shell. Written in notebooks run on Google Cloud Datalab and/or JupterLab.

* About models:   
We design NN models for image classification. We also use pre-trained models for transfer learning, including VGG16, VGG19, DenseNet, ResNet, Inception, Xception.

* About data augmentation:   
Kather dataset is a small-size dataset with 5000 images. Thus we apply transformation methods including flip, shift, rotation, etc. to increase train set size. For details please refer to [Wiki](https://github.com/lingyixu/GCP-Keras-Deep-Learning/wiki/Data-Augmentation-Function-Guide).

* About image tiling:
We use `openslide` and self-defined funtions to tile large tissue slides. Reference: [HistCNN](https://github.com/javadnoorb/HistCNN). For small datasets, we let Python to do tiling. For large datasets like TCGA, we are utilizing Kubernetes through [Google Cloud GKE](https://cloud.google.com/kubernetes-engine) to speed up the process and improve algorithm scalability.

* **A research poster about DNN framework on GCP is [here](https://github.com/lingyixu/GCP-Keras-Deep-Learning/blob/master/Scalable_DNN_Framework_on_GCP.pdf). It's presented at the MSMF Reseach Exhibition on Oct 7, 2019.**
