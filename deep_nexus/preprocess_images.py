import pandas as pd
import random
#from google.cloud import storage
import tensorflow as tf

def random_split(df,
                 train_prop = 0.70, 
                 test_prop = 0.15, 
                 valid_prop = 0.15,
                 seed = 42):
    """Split train/test/valid dataset"""
    patient_id_list = list(pd.unique(df['case_barcode']))
    random.seed(seed)
    train_list = random.sample(patient_id_list,int(round(len(patient_id_list)*train_prop)))
    rest_id = [x for x in patient_id_list if x not in train_list]
    random.seed(seed)
    valid_list= random.sample(rest_id,int(round(len(rest_id)*(test_prop/(test_prop+valid_prop)))))
    test_list = [x for x in rest_id if x not in valid_list]
    train_df = df[df['case_barcode'].isin(train_list)]
    test_df = df[df['case_barcode'].isin(test_list)]
    valid_df = df[df['case_barcode'].isin(valid_list)]
    print('The length of train_df: {}'.format(len(train_df)))
    print('The length of test_df: {}'.format(len(test_df)))
    print('The length of valid_df: {}'.format(len(valid_df)))
    return train_df, test_df, valid_df


def create_path(my_pd):
    """Creating the tile paths"""
    tile_labels = pd.DataFrame()

    for i in range(len(my_pd)):
        tiles_list = []
        storage_client = storage.Client()
        globals()['blobs%s' % i] = storage_client.list_blobs('deep-nexus', prefix='TCGA/tcga-chol/{}/'.format(my_pd.iloc[i]['svsFilename'][:-4]),
                                          delimiter=None)

        for blob in globals()['blobs%s' % i]:
            tiles_list.append('gs://deep-nexus/'+str(blob.name))

        labels = [my_pd.iloc[i]['label']]*len(tiles_list)
        tile_labels_ = pd.DataFrame(list(zip(tiles_list, labels)), 
                   columns =['filename', 'label'])
        tile_labels = pd.concat([tile_labels, tile_labels_], axis=0)
    print("The total number of tiles: {}".format(len(tile_labels)))
    return tile_labels


# The following 2 functions can be used to convert a value to a type compatible
# with tf.Example.

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def image_example(image_path, label, bucket_name):
    """Create a dictionary with relevant features."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    source_blob_name = image_path.decode("utf-8").split("gs://"+bucket_name+"/")[-1]
    blob = bucket.blob(source_blob_name)
    image_string = blob.download_as_string()
    image_shape = tf.image.decode_jpeg(image_string).shape

    feature = {
        'height': _int64_feature(image_shape[0]),
        'width': _int64_feature(image_shape[1]),
        'depth': _int64_feature(image_shape[2]),
        'label': _int64_feature(label),
        'image_raw': _bytes_feature(image_string),
    }
    return tf.train.Example(features=tf.train.Features(feature=feature))


def create_dataset(tiles):
    """Creating the dataset"""
    image_paths = tf.convert_to_tensor(tiles["filename"], dtype=tf.string)
    labels = tf.convert_to_tensor(tiles["label"])
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    return dataset


def write_tfrecord(GCS_OUTPUT, batch_size, dataset):
    """Writing tfrecords to GCS_OUTPUT"""
    bucket_name = GCS_OUTPUT.split("gs://")[-1].split("/")[0]
    dataset = dataset.batch(batch_size)
    print("Writing TFRecords to {}xxxxxx-xxxx.tfrec".format(GCS_OUTPUT,))
    for shard, (image_path, label) in enumerate(dataset):
        # batch size used as shard size here
        shard_size = image_path.numpy().shape[0]

        # good practice to have the number of records in the filename
        filename = GCS_OUTPUT + "{:06d}-{}.tfrec".format(shard, shard_size)

        with tf.io.TFRecordWriter(filename) as out_file:
            for i in range(shard_size):
                example = image_example(image_path[i].numpy(),
                                        label[i].numpy(),
                                        bucket_name)
                out_file.write(example.SerializeToString())
            print("Wrote file {} containing {} records".format(filename, shard_size))
            

