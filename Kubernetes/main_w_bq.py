#from flask import Flask
#app = Flask(__name__)
from deep_nexus import tiling
import os
from google.cloud import storage, bigquery


# connect to bigquery table
bq_client = bigquery.Client()
table = bq_client.get_table('deep-nexus.tcga.TCGA_slides_metadata')


# check table if necessary
#print("Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id))
#print("Table schema: {}".format(table.schema))
#print("Table description: {}".format(table.description))
#print("Table has {} rows".format(table.num_rows))


# write query
query = """
    SELECT *
    FROM `deep-nexus.tcga.tcga_slides_metadata`
    WHERE is_ffpe='NO' AND disease_code='CHOL' AND (avg_percent_tumor_cells>95.0 OR sample_type_name = 'Solid Tissue Normal')
"""

# get query results
query_job = bq_client.query(query)


# generate image path info from query results
img_dict = {}
for row in query_job:
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