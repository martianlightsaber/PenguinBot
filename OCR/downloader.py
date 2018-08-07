#import urllib.request
import requests
import random
import shutil



def downloader(image_url,time_stamp):
    r = requests.get(image_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    #file_name = random.randrange(1,10000)
    #full_file_name = str(file_name) + '.png'
    full_file_name = time_stamp + '.png'
    if r.status_code == 200:
        with open(full_file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def chartDL(img_url):
    r = requests.get(image_url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    full_file_name = 'chart.png'
    if r.status_code == 200:
        with open(full_file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
