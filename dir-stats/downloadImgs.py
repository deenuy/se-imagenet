import os
from pathlib import Path
from urllib.request import urlopen, Request

scrptPth = os.path.dirname(os.path.realpath(__file__))

def download_link(directory, link):
    # download_path = directory / os.path.basename(link)
    # print(download_path)
    with urlopen(link) as image, directory.open('wb') as f:
        f.write(image.read())
        
for root, dirs, files in os.walk(scrptPth):
    
    for filename in files:
        
        filename = os.path.join(root, filename)
        if filename.endswith('.txt'):
            print(root)
            print(filename)
            with open(filename, 'r') as f:
                content = f.readlines()
                # data = [x.strip() for x in content]
                # print(data)
                print(content)
                for line in content:
                    line.strip()
                    x = line.split("|")
                    print(x[0])
                    print(x[2])
                    
                    download_link(root, str(x[2]))
                
                
                

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
                