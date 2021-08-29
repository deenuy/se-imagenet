"""
Images download from Microsoft Bing subscription for academic research on image processing and classification for SEImageNet paper.

Copyright (C) 2021 Deenu Gengiti <deenuy@gmail.com> | York University
This file is licensed under the MIT license. See LICENSE for more details.
"""
import requests, json, os, sys, time, logging, traceback, threading, urllib
from pprint import pprint
from datetime import datetime
import config

# generate session uid with datetime
start = time.time()
startTime = datetime.now().strftime("%H:%M:%S")
date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

# ROOT dir of repo or source code
ROOT_DIR = os.path.abspath(os.getcwd())

""" Logger generation """
curr_path = os.path.dirname(__file__)
log = logging.getLogger(__name__)
log.setLevel('DEBUG')
# datetime | process ID | log level | message
logFormat = logging.Formatter('%(asctime)s|%(process)d|%(levelname)s|: %(message)s')
logFileName = 'seimagenet_log_'+date+'.log'
try:
    os.mkdir(os.path.join(curr_path, 'logs'))
except:
    pass
fh = logging.FileHandler(os.path.join(curr_path, 'logs', logFileName), mode='w+')
fh.setFormatter(logFormat)
log.addHandler(fh)

log.info('Script execution started')

# Micrsoft BING REST API authentication
subscriptionKey = config.BING_CUSTOM_SEARCH_SUBSCRIPTION_KEY
endpoint = config.BING_CUSTOM_SEARCH_ENDPOINT
customConfig = config.BING_CUSTOM_CONFIG_ID
headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

# Instance variables 
termCount = 0
totalImgsDownloaded = 0
termImgsDownloaded = 0

# Exception handling and logging
def excpPrint():
    """ Log trace for exception message, type, filename, line number """
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    log.error("Exception type: "+ str(exception_type) + "\n")
    log.error("Exception in file: "+ str(filename) + "\n")
    log.error("Exception occured at line number: "+ str(line_number) + "\n")
# END of function: excpPrint

def downloadTermImg(res, term, dir, filesCount):
    """ Download images from bing api response items content url """
    itmCnt = 0
    filesCount = 0
    try:
        for item in res['value']:
            itmCnt += 1
            # GET the image url path
            try:
                img_data = requests.get(item['contentUrl']).content
                #log.info('print item content url: ' + item['contentUrl'] )
            except Exception as e:
                excpPrint()
            # GET url image file type extension 
            try:
                imgType = item['encodingFormat']
                if(imgType):
                    imgFileName = item['imageId']+"_"+str(itmCnt)+"."+imgType
                else:
                    imgFileName = item['imageId']+"_"+str(itmCnt)
            except Exception as e:
                excpPrint()
            # Download image to dir 
            try:
                with open(dir+"/"+ imgFileName, "wb") as handler:
                    handler.write(img_data)
                    
            except Exception as e:          
                excpPrint()
            # generate CSV for metadata 
            if(e):
                continue
            else:
                filesCount+=1
                generateCSV(item, term, dir)
    except Exception as e:             
        excpPrint()
    return filesCount
    
def generateCSV(item, term, dir):
    """ Download term metadata in CSV """
    #append the metadata to the csv file
    try:
        csv_file = open(dir+ "/"+term+ ".csv" , "a", encoding = "utf8")
        csv_file.write(
                        str(item['imageId']) +'|'+
                        str(item['encodingFormat']) +'|'+
                        str(item['name']) +'|'+
                        str(item['contentSize']) +'|'+                        
                        str(item['height']) +'|'+
                        str(item['width']) +'|'+
                        str(item['contentUrl']) +'|'+
                        str(item['datePublished']) +'|'+
                        str(item['webSearchUrl']) +'|'+
                        str(item['accentColor']) +'|'+
                        str(item['hostPageDisplayUrl'] )+'|'+
                        str(item['hostPageUrl']) +'|'+"\n" )
        csv_file.close()
    except Exception as e:             
        excpPrint()
# END of function: generateCSV

def deleteMe(items):
    for item in items:
        log.info(item['imageId']  +'|'+ str(item['encodingFormat'])   +'|'+  str(item['name']) +'|')

def getSETermImgs(term, termCount, termImgsDownloaded):
    """ GET images for given term """
    resultsPerReq = 10

    # Term start time of execution
    termStartTime = time.time()
    log.info('Term count: ' + str(termCount) + '; Term name: ' + term)

    # create term folder
    try:
        dir_path = '{}/{}'.format(ROOT_DIR+'/staging', term)
        os.makedirs(dir_path)
    except:
        log.error("Directory already exists")
    # create term metadata csv
    try:
        csv_file = open(dir_path+ "/"+term + ".csv" , "w", encoding="utf8")
        #manually modify this CSV file header
        csv_file.write("imageId | encodingFormat | name | contentSize | height | width | contentUrl | datePublished | webSearchUrl | accentColor | hostPageDisplayUrl | hotPageUrl"+"\n") 
        csv_file.close()
    except Exception as e:
            excpPrint()
    
    offset = 0
    totalImages = 0
    # Trigger BING API reqests to download 500 imgs per term
    for i in range(0, 500, resultsPerReq):
        params = {'q': term, 'customConfig': customConfig, 'count': resultsPerReq, 'offset' : offset}
        print(offset)
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            # response.raise_for_status()
            res = response.json()
            log.info('Number of results per request for term '+ term + ' : '+ str(len(res['value'])))
        except Exception as e:          
            excpPrint()

        # Setting offset to nextOffset
        offset = res['nextOffset']


        # Download image and generate CSV
        #deleteMe(res['value'])
        downloadedImages = 0
        downloadTermImg(res, term, dir_path, downloadedImages)
        totalImages += downloadedImages

        # Orchestration process delay for multithreaded operation
        time.sleep(1)

    # Term execution end time
    termEndTime = time.time()

    # Appending log for total execution time for term
    log.info('Total execution time for term (seconds): '+ str(termEndTime-termStartTime))
# END of function: getSETermImgs

# Read SEDict.json input file for query term
with open("images_qry_sedict.txt") as f:
    content = f.readlines()
    qryTermsList = [x.strip() for x in content]

# Multithreaded execution to triger BING API request with 5 parallel threads
termIndx = 0
threads = [None] * 1
ImgsDownloaded = [None] * len(qryTermsList)

while(termIndx <= len(qryTermsList)-1):
    for i in range(len(threads)):
        threads[i] = threading.Thread(target=getSETermImgs, args=(qryTermsList[termIndx], termIndx, ImgsDownloaded[i]))
        threads[i].start()
        termIndx += 1
    # Thread pipeline to wait until all thread terminates
    for i in range(len(threads)):
        threads[i].join()
# END of Multitread operation

end = time.time()

#log.info('Total images downloaded: '+ str(total_imgs_download))
log.info('Script execution completed')
log.info('Total script execution time (seconds): '+str(end-start))