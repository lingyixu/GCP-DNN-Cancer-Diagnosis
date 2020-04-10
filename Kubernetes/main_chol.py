#from flask import Flask
#app = Flask(__name__)
import tiling
#import subprocess
#import glob
from google.cloud import storage


bucket_name = 'deep-nexus'
outdir = 'TCGA/chol-tiles-k8s'
outlocaldir = './image'

#img_list = glob.glob('slides/*.svs')
storage_client = storage.Client()
bucket = storage_client.get_bucket('deep-nexus-tcga-raw')
img_list = list(bucket.list_blobs(prefix='CHOL/CHOL_all_images/'))
img_list = img_list[1:]
bucket_pre = 'gs://deep-nexus-tcga-raw/'

for img in img_list:
    img_path = str(img).split(',')[-2][1:]
    img_path_full = bucket_pre + img_path
    img_name = img_path.split('/')[-1]
    blob = bucket.blob(img_path)
    blob.download_to_filename(img_name)
    tiling.TileSVS(img_name, outdir, outlocaldir, bucket_name)

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')
