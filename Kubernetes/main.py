#from flask import Flask
#app = Flask(__name__)
import tiling
import glob
from google.cloud import storage

#@app.route("/")
#def hello():  
bucket_name = 'deep-nexus'
outdir = 'TCGA/tiles'
outlocaldir = './image'

img_list = glob.glob('slides/*.svs')
# img = 'TCGA-AA-3713-01Z-00-DX1.8148ACEB-7C1E-4D29-B908-F3729657EA4F.svs'

for img in img_list:
    tiling.TileSVS(img, outdir, outlocaldir, bucket_name)
    
    
#if __name__ == "__main__":
#    app.run(host='0.0.0.0')
