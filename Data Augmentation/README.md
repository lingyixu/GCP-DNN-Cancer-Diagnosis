# Data Augmentation Function Guide


## Overview
* Function: **`keras.preprocessing.image.ImageDataGenerator()`**
* Parameter and default value:
  * featurewise_center=False
  * samplewise_center=False
  * featurewise_std_normalization=False
  * samplewise_std_normalization=False
  * zca_whitening=False
  * zca_epsilon=1e-06
  * rotation_range=0
  * width_shift_range=0.0
  * height_shift_range=0.0
  * brightness_range=None
  * shear_range=0.0
  * zoom_range=0.0
  * channel_shift_range=0.0
  * fill_mode='nearest'
  * cval=0.0
  * horizontal_flip=False
  * vertical_flip=False
  * rescale=None
  * preprocessing_function=None
  * data_format=None
  * validation_split=0.0
  * dtype=None



## Parameter Explanation

Expalin some difficult-to-understand parameters here.

* featurewise_center & featurewise_std_normalization
  * Standardize pixel values across the entire dataset.
  * The effect of feature standardization is different, seemingly darkening and lightening different images.
  * It mirrors the type of standardization often performed for each column in a tabular dataset.

* width_shift_range & height_shift_range
  * Objects or patterns in the images may not be centered in the frame, as they may be off-center in a variety of different ways.
  * We can train a deep learning network to expect and currently handle off-center objects by artificially creating shifted versions of the training data.

* brightness_range
  * Min and max range as a float representing a percentage (fraction) for selecting a brightening amount.
  * Values less than 1.0 darken the image, e.g. [0.5, 1.0], whereas values larger than 1.0 brighten the image, e.g. [1.0, 1.5], where 1.0 has no effect on brightness.
  * This allows a model to generalize across images trained on different lighting levels.

* zoom_range
  * Randomly zooms the image in, and either adds new pixel values around the image or interpolates pixel values respectively. The zoom amount is uniformly randomly sampled from the zoom region for each dimension (width, height) separately.
  * We can specify the percentage of the zoom as a single float or a range as an array or tuple. If a float is specified, then the range for the zoom will be [1-value, 1+value]. A zoom of [1.0,1.0] has no effect.
  * **Note that zoom values less than 1.0 will zoom the image in, e.g. [0.5,0.5] makes the object in the image 50% larger or closer, and values larger than 1.0 will zoom the image out by 50%, e.g. [1.5, 1.5] makes the object in the image smaller or further away.**

* shear_range
  * Actually not a real "range". We only need to specify the max possible shearing angle.
  * Perform shear transformation / shear mapping on the image, which displaces each point in fixed direction, by an amount proportional to its signed distance from the line that is parallel to that direction and goes through the origin.
  * Differentiate shear mappings with rotations: Applying a shear map to a set of points of the plane will change all angles between them (except straight angles), and the length of any line segment that is not parallel to the direction of displacement. **Therefore it will usually distort the shape of a geometric figure, for example turning squares into non-square parallelograms, and circles into ellipses.**
  * An example:
A horizontal shearing of the plane, illustrated by its effect (in green) on a rectangular grid and some figures (in blue). The black dot is the origin.   
https://user-images.githubusercontent.com/35391238/63564591-ae501a80-c533-11e9-85d1-174ceeafbb1c.png

* zca_whitening
  * A whitening transform of an image, which is a linear algebra operation that reduces the redundancy in the matrix of pixel images. Less redundancy in the image is intended to better highlight the structures and features in the image to the learning algorithm.



## Relevant Notebook
* Data augmentation with cat image: https://colab.research.google.com/drive/1A1BTulv3QuDDQS5U9Ga4CWg2BhfMC1YY
* Data augmentation with tissue image: https://colab.research.google.com/drive/1puJHR1Nv65sOJJVkffHWbywRc0MGy58n
* Apply data augmentation with transfer learning: https://colab.research.google.com/drive/1dtyJGdcuhAoNBdNcEsfaAbrbVjusYEAP



## Reference
* https://machinelearningmastery.com/how-to-configure-image-data-augmentation-when-training-deep-learning-neural-networks/
* https://machinelearningmastery.com/image-augmentation-deep-learning-keras/
* https://en.wikipedia.org/wiki/Shear_mapping
* https://keras.io/preprocessing/image/
