import os, sys, time, logging, traceback, shutil
from os import listdir
from PIL import Image
from pprint import pprint
from datetime import datetime

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
logFileName = 'find_corrupt_imgs_'+date+'.log'
try:
    os.mkdir(os.path.join(curr_path, 'logs'))
except:
    pass
fh = logging.FileHandler(os.path.join(curr_path, 'logs', logFileName), mode='w+')
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

for root, dirs, files in os.walk(ROOT_DIR+'/staging'):
  try:
    os.mkdir(ROOT_DIR+'/staging/corrupt-imgs')
  except:
    pass
  for dir in dirs:
    for filename in listdir(ROOT_DIR+'/staging/'+dir):
      # print(filename)
      if (filename.endswith('.csv') or filename.endswith('.txt')):
        continue
      try:
        img = Image.open(ROOT_DIR+'/staging/'+dir+'/'+filename) # open the image fileclear
        img.verify() # verify that it is, in fact an image
      except (IOError, SyntaxError) as e:
        # print('Image file is corrupted or unable to open:', filename) # print out the names of corrupt files
        excpPrint()
        log.error(f'Image file is corrupted: {filename} for term: {dir}')
        log.error(f'Image file path: {ROOT_DIR}/{dir}/{filename}')
        try:
          shutil.copy(ROOT_DIR+'/staging/'+dir+'/'+filename, ROOT_DIR+'/staging/corrupt-imgs/'+filename)
        except:
          pass