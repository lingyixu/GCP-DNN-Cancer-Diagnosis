# Deep Learning Research on GCP, Image Multi-Classification and Cancer Diagnosis
 
This repo contains my research work on image identification with Prof. Mohammad Soltanieh-ha. It's an ongoing research and updates will be made from time to time.   
   
**A research poster about DNN framework on GCP is [here](https://github.com/lingyixu/GCP-Keras-Deep-Learning/blob/master/Scalable_DNN_Framework_on_GCP.pdf). It's presented at the MSMF Reseach Exhibition on Oct 7, 2019.**

## 

* About data:   
MNIST datset (numbers), [Kather dataset](https://www.nature.com/articles/srep27988) (small tissue slides), and [TCGA dataset](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/data/TCGA-images.html) (large tissue slides).   
See TCGA dataset overview: [Notebook version](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/blob/master/TCGA_Overview.ipynb), [Data Studio report version](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/blob/master/Dataset%20Overview/TCGA_Exploration.pdf)

* About codes:   
Written in Python and Shell. Notebooks are run on Google Cloud Datalab and/or JupterLab.

* About models:   
We design NN models for image multi-classification. We also use pre-trained models for transfer learning, including VGG16, VGG19, DenseNet, ResNet, Inception, Xception.   

* About data augmentation:   
Kather dataset is a small-size dataset with 5000 images. Thus we apply transformation methods including flip, shift, rotation, etc. to increase train set size. For details please refer to [Wiki](https://github.com/lingyixu/GCP-Keras-Deep-Learning/wiki/Data-Augmentation-Function-Guide).

* About image tiling:   
  * Large tissue slides are tiled by `openslide` and self-created funtions. API Reference: [HistCNN](https://github.com/javadnoorb/HistCNN).
  * Workflow: query slides info → connect to public database → download slides → tile slides and save locally → upload tiles to cloud → remove local tiles and slides   
  * For small datasets, Jupyter Notebook with GPU is enough to handle the tiling part. For large datasets like TCGA, docker and Kubernetes are utilized through [Google Cloud GKE](https://cloud.google.com/kubernetes-engine) for speeding up the tiling process and improve algorithm scalability.
  * After tiling, tiles are saved as _TensorFlow TFRecords_ to feed the models.
  * For Cloud Kubernetes operations, please refer to [wiki](https://github.com/lingyixu/GCP-DNN-Cancer-Diagnosis/wiki/GKE-How-to-Guide).

* About class imbalance:   
Generally there are more tumor slides than normal ones in most of the cancer cohorts. Tumor slides are thus selected based on purity. The threshold for the TCGA dataset is now 95%.
