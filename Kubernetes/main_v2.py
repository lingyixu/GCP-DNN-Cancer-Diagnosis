#from flask import Flask
#app = Flask(__name__)
from deep_nexus import tiling
import pandas as pd
import os
from google.cloud import storage


# import slide IDs
df = pd.read_csv('slide_id.csv')


# generate image path info from df
img_dict = {}
for idx, row in df.iterrows():
    img_dict[row['file_gcs_url'].split('/')[-1][:-4]] = row['file_gcs_url']


# connect to public gcloud bucket
bkt_client = storage.Client()
bucket = bkt_client.bucket('gdc-tcga-phs000178-open')

# output setup
bucket_name = 'deep-nexus'
outdir = 'TCGA/tiles/CHOL'
outlocaldir = './image'


# download and tile slides
prefix_len = len('gs://gdc-tcga-phs000178-open/')
for img_name, img_path in img_dict.items():
    partial_path = img_path[prefix_len:]
    blob = bucket.blob(partial_path)
    blob.download_to_filename(img_name)
    tiling.TileSVS(img_name, outdir, outlocaldir, bucket_name)
    os.remove(img_name)
    print('local slide removed')


#if __name__ == "__main__":
#    app.run(host='0.0.0.0')