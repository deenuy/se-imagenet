"""
Images download from Microsoft Bing subscription for academic research on image processing and classification for SEImageNet paper.
Copyright (C) 2021 Deenu Gengiti <deenuy@gmail.com> | York University
This file is licensed under the MIT license. See LICENSE for more details.
"""
import requests, json, os, sys, time, logging, traceback, threading, urllib
from pprint import pprint
from datetime import datetime
import config

# INSTANCE VARIABLES / USER INPUTS
API_RESULTS_PER_REQUEST = 150 # Number of results to retrive per BING SEARCH API REQUEST
IMAGES_PER_TERM = 550 # Images to download from BING SEARCH per SE term
NUM_THREADS = 1000 # Multi-threading count for initializing parallel executions
OUTPUT_DIR = 'staging_multi_thread1' # Images download location
SE_TERMS_INPUT_FILE = 'input_sedict.txt' # SEDict input file

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
logFileName = 'seimagenet_mul_thread_'+date+'.log'
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


# Exception handling and logging
def excpPrint():
    """ Log trace for exception message, type, filename, line number """
    exception_type, exception_object, exception_traceback = sys.exc_info()
    # filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    log.error(f'Exception type: {exception_type}')
    # log.error(f'Exception in file: {filename}')
    log.error(f'Exception occured at line number: {line_number}')
    #log.error(f'Exception occured at term: {}')
# END of function: excpPrint

        
def storeResponse(res, term, dir):
    if len(res['value'])>0:
        for item in res['value']:
            # generate CSV for metadata
            try:
                generateCSV(item, term, dir)
            except Exception as e:
                log.error('Exception occurred generating CSV for term: ' + term)
                excpPrint()
            # Download images (temporarily instead of text)
            try:
                generateTextFile(item, term, dir)
            except Exception as e:
                log.error('Exception occurred for creating file for term ' + term)
                excpPrint()
            # Download image
            try:
                downloadImgUrl(item['imageId'], item['contentUrl'], dir, term)
            except Exception as e:
                log.error('Exception occurred for downloading image for term: ' + term)
                excpPrint()
# END of function: storeResponse
    
def downloadImgUrl(imgId, imgUrl, destDir, term):
    ext = "."+imgUrl.split(".")[-1]
    ext = ext.split("!")[0]
    ext = ext.split("&")[0]
    ext = ext.split("?")[0]
    ext = ext.split("=")[0]
    ext = ext.split("|")[0]
    imgName = imgId + ext
    imgPath = os.path.join(destDir, imgName)
    try:
        res = requests.get(imgUrl)  
    except Exception as e:
        log.error('Exception occurred to download image for ' + imgName)
        excpPrint()
    else:
        if res.status_code == 200:
            with open(imgPath, 'wb') as f:
                f.write(res.content)
            f.close()
# END of function: downloadImgUrl

def generateTextFile(item, term, dir):
    # log.info('Downloading: ' + term)
    try:
        textFile = open(dir+ "/"+term+ ".txt" , "a", encoding = "utf8")
        textFile.write(
            str(item['imageId']) +'|'+
            str(item['encodingFormat']) +'|'+
            str(item['contentUrl']) +'|'+"\n" 
        )
        textFile.close()
    except Exception as e:             
        excpPrint()
# Ending generateTextFile function


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

def getSETermImgs(term, termIndx):
    """ GET images from BING image search for given term """
    resultsPerReq = API_RESULTS_PER_REQUEST
    itemsCnt = 0

    print(f'Processing term {termIndx} - {term}')
    log.info(f'Processing term {termIndx} - {term}')

    # Term start time of execution
    termStartTime = time.time()
    
    # create term folder
    try:
        dir_path = '{}/{}'.format(ROOT_DIR+'/'+OUTPUT_DIR, term)
        os.makedirs(dir_path)
    except:
        # New change accomodated to terminate if already folder exists with count 10
        if len(os.listdir(dir_path))>10:
            log.error("Directory already exists")
            return 
    # create term metadata csv
    try:
        csv_file = open(dir_path+ "/"+term + ".csv" , "w", encoding="utf8")
        # manually modify this CSV file header
        csv_file.write("imageId | encodingFormat | name | contentSize | height | width | contentUrl | datePublished | webSearchUrl | accentColor | hostPageDisplayUrl | hotPageUrl"+"\n") 
        csv_file.close()
    except Exception as e:
            excpPrint()

    params = {'q': term, 'customConfig': customConfig, 'count': resultsPerReq, 'offset' : 0}
    
    i = 0
    while i!=4:
        i+=1
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            res = response.json()
        except Exception as e: 
            excpPrint()

        # Setting offset to nextOffset
        params["offset"] = res["nextOffset"]
        
        # Download image and generate CSV
        try:
            storeResponse(res, term, dir_path)
        except Exception as e:          
            excpPrint()

    # Term execution end time
    termEndTime = time.time()
    
    # Appending log for total execution time for term
    log.info(f'Execution for term ({term}) completed in {round(termEndTime-termStartTime,2)} second(s) or {round((termEndTime-termStartTime)/60,2)} minute(s)')
# END of function: getSETermImgs

# Read SEDict.json input file for query term
with open(SE_TERMS_INPUT_FILE) as f:
    content = f.readlines()
    qryTermsList = [x.strip() for x in content]

# Multithreaded execution to triger BING API request with 5 parallel threads
termIndx = 0
threads = [None] * NUM_THREADS

while(termIndx <= len(qryTermsList)-1):
    for i in range(len(threads)):
        threads[i] = threading.Thread(target=getSETermImgs, args=(qryTermsList[termIndx], termIndx))
        threads[i].start()
        termIndx += 1
    # Thread pipeline to wait until all thread terminates
    for i in range(len(threads)):
        threads[i].join()
# END of Multitread operation

# End of the script
end = time.time()
log.info(f'Script execution completed in {round(end-start, 2)} second(s) or {round((end-start)/60,2)} minute(s)')
print(f'Script execution completed in {round(end-start, 2)} second(s) or {round((end-start)/60,2)} minute(s)')