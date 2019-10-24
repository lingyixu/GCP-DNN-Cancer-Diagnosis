# GCP Keras Deep Learning Research 
 
This repo contains my research work about DNN algorithms on GCP. It's an ongoing task and updates will be made from time to time.

* About data:   
MINST datset (numbers), Kather dataset (small tissue slides), and CHOL dataset (large tissue slides).

* About codes:   
Mainly in Python and Shell. They are written in notebooks run on Google Datalab and/or Colab.

* About models:   
We design CNN models for image classification. We also use pre-trained models for transfer learning, including VGG16, VGG19, DenseNet, ResNet, Inception, Xception.

* About data augmentation:   
Kather dataset is a small-size dataset with 5000 images. Thus we apply transformation methods including flip, shift, rotation, etc. to increase train set size. For details please refer to [Wiki](https://github.com/lingyixu/GCP-Keras-Deep-Learning/wiki/Data-Augmentation-Function-Guide).

* A research poster about DNN framework on GCP is [here](https://github.com/lingyixu/GCP-Keras-Deep-Learning/blob/master/Scalable_DNN_Framework_on_GCP.pdf). It's for the MSMF Reseach Exhibition on Oct 7, 2019. 
