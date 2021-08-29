import os, requests
from pathlib import Path
from urllib.request import urlopen, Request, urlretrieve

scrptPth = os.path.dirname(os.path.realpath(__file__))

def download_link(imgId, imgUrl, destDir):
    ext = "."+imgUrl.split(".")[-1]
    ext = ext.split("!")[0]
    ext = ext.split("&")[0]
    ext = ext.split("?")[0]
    ext = ext.split("=")[0]
    # strArr = str(imgUrl).split('.')
    # imgName = imgId + '.' + strArr[3]
    imgName = imgId + ext
    imgPath = os.path.join(destDir, imgName)
    try:
        res = requests.get(imgUrl)  
    except Exception as e:
        print(e)
    else:
        if res.status_code == 200:
            with open(imgPath, 'wb') as f:
                f.write(res.content)
            f.close()

# def download_images(url, dest_dir):
#   urlretrieve(url, dest_dir+os.path.basename(url))

for root, dirs, files in os.walk(scrptPth):
    for filename in files:
        filename = os.path.join(root, filename)
        if filename.endswith('.txt'):
            with open(filename, 'r') as f:
                content = f.readlines()
                for line in content:
                    line.strip()
                    if len(line)>0:
                        x = line.split("|")
                        print('\nProcessing Download Image:')
                        download_link(str(x[0]), str(x[2]), root)
                
                
                

# import json
# import logging
# import os


# logger = logging.getLogger(__name__)

# types = {'image/jpeg', 'image/png'}



#    logger.info('Downloaded %s', link)


# def setup_download_dir():
#     download_dir = Path('images')
#     if not download_dir.exists():
#         download_dir.mkdir()
#     return download_dir
                