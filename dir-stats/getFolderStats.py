"""
Get files, file type, folders stats.

Copyright (C) 2021 Deenu Gengiti <deenuy@gmail.com> | York University
This file is licensed under the MIT license. See LICENSE for more details.
"""
import requests, json, os, sys, time, logging, traceback, threading, urllib, stat
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
logFileName = 'seimagenet_multiprocessing_stats_'+date+'.log'
try:
    os.mkdir(os.path.join(curr_path, 'stats'))
except:
    pass
fh = logging.FileHandler(os.path.join(curr_path, 'stats', logFileName), mode='w+')
fh.setFormatter(logFormat)
log.addHandler(fh)

log.info('Script execution started')

# Exception handling and logging
def excpPrint():
    """ Log trace for exception message, type, filename, line number """
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    log.error(f'Exception type: {exception_type}')
    log.error(f'Exception in file: {filename}') 
    log.error(f'Exception occured at line number: {line_number}')
# END of function: excpPrint

def getFolderSize(root_dir, files):
    total_size = 0
    seen = {}
    for f in files:
        fp = os.path.join(root_dir, f)
        print(fp)
        try:
            stat = os.stat(fp)
        except OSError:
            continue
        try:
            seen[stat.st_ino]
        except KeyError:
            seen[stat.st_ino] = True
        else:
            continue

        total_size += stat.st_size
    return total_size

def getDirStats(root_dir):
    # walk the directory
    result = {}
    for root, dirs, files in os.walk(root_dir):
        # count the files size
        for dir in dirs:
            # print(dir)
            currentDir = root_dir+'/'+dir
            # file_count = sum(len(files) for _, _, files in os.walk(currentDir))
            file_count = 0
            total_size = 0
            seen = {}
            # folderSize = getFolderSize(root_dir+'/'+dir, files)
            for _,_, files in os.walk(currentDir):
                file_count += len(files)
                for f in files:
                    fp = os.path.join(currentDir, f)
                    try:
                        stat = os.stat(fp)
                    except OSError:
                        continue
                    try:
                        seen[stat.st_ino]
                    except KeyError:
                        seen[stat.st_ino] = True
                    else:
                        continue

                    total_size += stat.st_size

            # print(f'Term: ({dir}) | Images Count: {file_count-1} | Directory size: {round(total_size/(1024*1024), 2)} Mb')
            # log.info(f'Term: ({dir}) | Images Count: {file_count-1} | Directory size: {round(total_size/(1024*1024), 2)} Mb')
            log.info(f'|{dir}|{file_count-1}|{round(total_size/(1024*1024), 2)}')

print("\n")
getDirStats(ROOT_DIR+'/staging')
getDirStats(ROOT_DIR+'/staging2')
getDirStats(ROOT_DIR+'/staging3')
getDirStats(ROOT_DIR+'/staging4')
getDirStats(ROOT_DIR+'/staging_multi_thread4')
getDirStats(ROOT_DIR+'/staging_multi_thread2')
getDirStats(ROOT_DIR+'/staging_multi_thread3')
getDirStats(ROOT_DIR+'/staging_multi_thread1')
getDirStats(ROOT_DIR+'/staging_mul_proc_31_completed')
print("\n")

# End of the script
end = time.time()
log.info(f'Script execution completed in {round(end-start, 2)} second(s) or {round((end-start)/60,2)} minute(s)')
print(f'Script execution completed in {round(end-start, 2)} second(s) or {round((end-start)/60,2)} minute(s)')