import sys, os, zipfile
import urllib.request

#where_to_save = '../Data/'
where_to_save = 'Data/'

#create data directory
if not os.path.exists(where_to_save):
    os.makedirs(where_to_save)
    

url = 'http://mirror.imagej.net/images/Spindly-GFP.zip'
urllib.request.urlretrieve(url, where_to_save+'mitosis.zip')
#unzip
with zipfile.ZipFile(where_to_save+'mitosis.zip', 'r') as zip_ref:
    zip_ref.extractall(where_to_save)
os.remove(where_to_save+'mitosis.zip')