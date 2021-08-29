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
logFileName = 'sedict_find_in_wordnet_log_'+date+'.log'
try:
    os.mkdir(os.path.join(curr_path, 'logs'))
except:
    pass
fh = logging.FileHandler(os.path.join(curr_path, 'logs', logFileName), mode='w+')
fh.setFormatter(logFormat)
log.addHandler(fh)

log.info('Script execution started')

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

# Read SEDict.json input file for query term
with open(SE_TERMS_INPUT_FILE) as f:
    content = f.readlines()
    qryTermsList = [x.strip() for x in content]



# End of the script
end = time.time()
log.info(f'Script execution completed in {round(end-start, 2)} second(s) or {round((end-start)/60,2)} minute(s)')
print(f'Script execution completed in {round(end-start, 2)} second(s) or {round((end-start)/60,2)} minute(s)')