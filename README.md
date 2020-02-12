# GCP Keras Deep Learning Research 
 
This repo contains my research work about DNN algorithms on GCP. It's an ongoing research and updates will be made from time to time.   
   
**A research poster about DNN framework on GCP is [here](https://github.com/lingyixu/GCP-Keras-Deep-Learning/blob/master/Scalable_DNN_Framework_on_GCP.pdf). It's presented at the MSMF Reseach Exhibition on Oct 7, 2019.**

* About data:   
MNIST datset (numbers), [Kather dataset](https://www.nature.com/articles/srep27988) (small tissue slides), and [TCGA dataset](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/data/TCGA-images.html) (large tissue slides).

* About codes:   
Written in Python and Shell. Notebooks are run on Google Cloud Datalab and/or JupterLab.

* About models:   
We design NN models for image multi-classification. We also use pre-trained models for transfer learning, including VGG16, VGG19, DenseNet, ResNet, Inception, Xception.   

* About data augmentation:   
Kather dataset is a small-size dataset with 5000 images. Thus we apply transformation methods including flip, shift, rotation, etc. to increase train set size. For details please refer to [Wiki](https://github.com/lingyixu/GCP-Keras-Deep-Learning/wiki/Data-Augmentation-Function-Guide).

* About image tiling:   
We use `openslide` and self-defined funtions to tile large tissue slides. Reference: [HistCNN](https://github.com/javadnoorb/HistCNN).    
For small datasets, we let Python do tiling and then upload tiles to Google Cloud Bucket. For large datasets like TCGA, we are utilizing Kubernetes through [Google Cloud GKE](https://cloud.google.com/kubernetes-engine) to speed up the process and improve algorithm scalability.   
After tiling, we save tiles into _TensorFlow TFRecords_ and use them as inputs of our model.

* About class imbalance:   
Generally we have more tumor slides than normal ones. We select tumor slides based on purity. The threshold for the TCGA dataset is now 95%.
