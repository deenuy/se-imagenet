"""
Images download from Microsoft Bing subscription for academic research on image processing and classification for SEImageNet paper.
Implementated multi-threaded execution for running parallel executions. 
Copyright (C) 2021 Deenu Gengiti <deenuy@gmail.com> | York University
This file is licensed under the MIT license. See LICENSE for more details.
"""
import requests, json, os, sys, time, logging, traceback, threading, urllib
from pprint import pprint
from datetime import datetime
import config

# INSTANCE VARIABLES / USER INPUTS
API_RESULTS_PER_REQUEST = 100 # Number of results to retrive per BING SEARCH API REQUEST
IMAGES_PER_TERM = 500 # Images to download from BING SEARCH per SE term
NUM_THREADS = 1000 # Multi-threading count for initializing parallel executions
OUTPUT_DIR = 'staging' # Images download location
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
    log.error(f'Exception type: {exception_type}')
    log.error(f'Exception in file: {filename}') 
    log.error(f'Exception occured at line number: {line_number}')
    log.error(f'Exception occured at term: {qryTermsList[termIndx]}')
# END of function: excpPrint

def downloadTermImg(res, term, dir):
    """ Download images from bing api response items content url """
    itmCnt = 0
    imgsDownloaded = 0
    try:
        for item in res['value']:
            isExcpTrue = False
            itmCnt += 1
            # GET the image url path
            try:
                img_data = requests.get(item['contentUrl']).content
            except Exception as e:
                log.error(f'Request returned with code {img_data.status_code}, error msg: {res.text}')
                log.error('Exception occurred for item of ('+ term +') url content: ' + item['contentUrl'])
                excpPrint()
                continue
            # GET url image file type extension
            try:
                imgType = item['encodingFormat']
                if(imgType):
                    imgFileName = item['imageId']+"."+imgType
                else:
                    imgFileName = item['imageId']
            except Exception as e:
                isExcpTrue = True
                log.error(f'Exception occurred for item of ({term}) image type encoding format: {imgType}')
                excpPrint()
                continue
            # Download image to dir 
            try:
                with open(dir+"/"+ imgFileName, "wb") as handler:
                    handler.write(img_data)
            except Exception as e:
                isExcpTrue = True
                log.error('Exception occurred for item of ('+ term +') downloading: ' + item['contentUrl'])
                excpPrint()
                continue
            # generate CSV for metadata
            if(isExcpTrue==False):
                imgsDownloaded+=1
                generateCSV(item, term, dir)
    except Exception as e:             
        excpPrint()

    # log.info('Images downloaded -fun: downloadTermImg: ' + str(imgsDownloaded))
    return int(imgsDownloaded)
    
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

def getSETermImgs(term, termCount):
    """ GET images from BING image search for given term """
    resultsPerReq = API_RESULTS_PER_REQUEST
    termImgsCnt = IMAGES_PER_TERM
    termImgsDownloaded = 0

    # Term start time of execution
    termStartTime = time.time()
    log.info(f'Term count - {termCount}; Term name - {term}')
    print(f'Term name - {term}')
    # create term folder
    try:
        dir_path = '{}/{}'.format(ROOT_DIR+'/'+OUTPUT_DIR, term)
        os.makedirs(dir_path)
    except:
        log.error("Directory already exists")
    # create term metadata csv
    try:
        csv_file = open(dir_path+ "/"+term + ".csv" , "w", encoding="utf8")
        # manually modify this CSV file header
        csv_file.write("imageId | encodingFormat | name | contentSize | height | width | contentUrl | datePublished | webSearchUrl | accentColor | hostPageDisplayUrl | hotPageUrl"+"\n") 
        csv_file.close()
    except Exception as e:
            excpPrint()
    
    offset = 0
    # Trigger BING API reqests to download 500 imgs per term
    for i in range(0, termImgsCnt, resultsPerReq):
        params = {'q': term, 'customConfig': customConfig, 'count': resultsPerReq, 'offset' : offset}
        response = requests.get(endpoint, headers=headers, params=params)
        try:
            res = response.json()
        except Exception as e:
            # log.error(f'Request returned with code %s, error msg: %s' % (res.status_code, res.text))
            log.error(f'Request returned with code {res.status_code}, error msg: {res.text}')
            excpPrint()

        # Setting offset to nextOffset
        offset = res['nextOffset']

        # Download image and generate CSV
        try:
            termImgsDownloaded += downloadTermImg(res, term, dir_path)
        except Exception as e:          
            excpPrint()

        # Orchestration process delay for multithreaded operation
        time.sleep(5)

    # Term execution end time
    termEndTime = time.time()

    # Appending log for total execution time for term
    log.info(f'Execution for term ({term}) completed in {round(termEndTime-termStartTime,2)} second(s) or {round((termEndTime-termStartTime)/60,2)} minute(s)')

    return int(termImgsDownloaded)
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