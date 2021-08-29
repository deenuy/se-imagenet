import os
import requests
import json
import config
from datetime import datetime
from datetime import date
import time
import sys

API_KEY = config.GOOGLE_API_KEY
SEARCH_ID = config.GOOGLE_SE_ID
BASE_PATH = os.path.dirname(os.getcwd())

# Date time stamp for appending filename
now = datetime.now()
nowStr = now.strftime("%Y_%m_%d-%I-%M-%S")
startTime = now.strftime("%H:%M:%S")
start = time.time()

# Number of images to Download
imagesToDown = 10

with open("input_file.txt") as f:
    content = f.readlines()
    toSearch = [x.strip() for x in content]
    
for term in toSearch:
    term1 = term.split(',')[0]
    term2 = term.split(',')[1]
    term3 = term.split(',')[2]
    count = 0
    
    try:
        dir_path = '{}/{}'.format(BASE_PATH, term1)
        os.makedirs(dir_path)
    except:
        print("folder present")
    try:
        dir_inner_path = '{}/{}'.format(dir_path, term2+"_"+term3)
        os.makedirs(dir_inner_path)
    except: 
        print("inner folder present")
    #log file creation and noting 
    log_file = open(BASE_PATH+ "/"+  nowStr+ ".txt", "w", encoding="utf8")
    log_file.write("Script execution date : " +  date.today().strftime("%d/%m/%Y") + "\n")
    log_file.write("Script start execution time : " + startTime + "\n""---------------------------------------------\n")
    log_file.close()
    #csv file creation
    try:
        csv_file = open(dir_inner_path+ "/"+term2+"_"+term3 + ".csv" , "w", encoding="utf8")
        csv_file.write("title, htmlTitle, link, displayLink, snippet, mime, fileFormat, image.contextlink, image.height, image.width, image.byteSize, image.thumbnailLink, image.thumbnailHeight, image.thumbnailWidth"+"\n") #manually modify this CSV file header
        csv_file.close()
    except Exception as e:            
        with open(BASE_PATH+ "/"+  nowStr+ ".txt" , "a") as log_file:    
            log_file.write(str(e)+ "\n")
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            log_file.write("Exception type: "+ str(exception_type) + "\n")
            log_file.write("Exception in file: "+ str(filename) + "\n")
            log_file.write("Exception occured at line number: "+ str(line_number) + "\n")
            log_file.write("Failed at synset :" + term +"\n"+"---------------------------------------------\n")
            log_file.close()
    #pagination
    for i in range(1, imagesToDown , 10):
        url="https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx="+SEARCH_ID+"&searchType=image&start="+str(i)+"&q="+term1+"+"+term2+"+"+term3
        #try catch for handling errors while making request to the Google custom search API

        try:
            res = requests.get(url)
            result =  json.loads(res.text)
        except Exception as e:            
            with open(BASE_PATH+ "/"+  nowStr+ ".txt" , "a") as log_file:    
                log_file.write(str(e)+ "\n")
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                log_file.write("Exception type: "+ str(exception_type) + "\n")
                log_file.write("Exception in file: "+ str(filename) + "\n")
                log_file.write("Exception occured at line number: "+ str(line_number) + "\n"+"---------------------------------------------\n")
                log_file.write("Failed at synset :" + term +"\n")
                log_file.close()
        try:
            for item in result['items']:
            #download the image
                count = count + 1
                try:
                    image_url = item['link']
                    img_data = requests.get(image_url).content
                    img_name = term2+"_"+term3+str(count)
                    with open(dir_inner_path+"/"+ img_name + ".jpg", "wb") as handler:
                        handler.write(img_data)
                except Exception as e:            
                    with open(BASE_PATH+ "/"+  nowStr+ ".txt" , "a") as log_file:    
                        log_file.write(str(e)+ "\n")
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        filename = exception_traceback.tb_frame.f_code.co_filename
                        line_number = exception_traceback.tb_lineno
                        log_file.write("Exception type: "+ str(exception_type) + "\n")
                        log_file.write("Exception in file: "+ str(filename) + "\n")
                        log_file.write("Exception occured at line number: "+ str(line_number) + "\n")
                        log_file.write("Failed at synset :" + term +"\n"+"---------------------------------------------\n")
                        log_file.close()
                
            #append the metadata to the csv file
                try:
                    csv_file = open(dir_inner_path+ "/"+term2+"_"+term3 + ".csv" , "a", encoding = "utf8")
                    csv_file.write(str(item['title']) +','+
                    str(item['htmlTitle']) +','+
                    str(item['link']) +','+
                    str(item['displayLink']) +','+
                    str(item['snippet']) +','+
                    str(item['mime']) +','+
                    str(item['image']['contextLink']) +','+
                    str(item['image']['height']) +','+
                    str(item['image']['width'] )+','+
                    str(item['image']['byteSize']) +','+
                    str(item['image']['thumbnailLink']) +','+
                    str(item['image']['thumbnailHeight']) +','+
                    str(item['image']['thumbnailWidth']) +','+"\n")
                    csv_file.close()
                except Exception as e:
                    with open(BASE_PATH+ "/"+  nowStr+ ".txt" , "a") as log_file:    
                        log_file.write(str(e)+ "\n")
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        filename = exception_traceback.tb_frame.f_code.co_filename
                        line_number = exception_traceback.tb_lineno
                        log_file.write("Exception type: "+ str(exception_type) + "\n")
                        log_file.write("Exception in file: "+ str(filename) + "\n")
                        log_file.write("Exception occured at line number: "+ str(line_number) + "\n")
                        log_file.write("Failed at synset :" + term +"\n"+"---------------------------------------------\n")
                        log_file.close()
        except Exception as e:            
            with open(BASE_PATH+ "/"+  nowStr+ ".txt" , "a") as log_file:    
                log_file.write(str(e)+ "\n")
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                log_file.write("Exception type: "+ str(exception_type) + "\n")
                log_file.write("Exception in file: "+ str(filename) + "\n")
                log_file.write("Exception occured at line number: "+ str(line_number) + "\n")
                log_file.write("Failed at synset :" + term +"\n"+"---------------------------------------------\n")
                log_file.close()
    

#ending the script
done = time.time()
endTime = now.strftime("%H:%M:%S")
totalTime = done-start
log_file = open(BASE_PATH+ "/"+  nowStr+ ".txt", "a", encoding="utf8")
log_file.write("Execution completed at :" + endTime+"\n")
log_file.write("Total execution time : " + str(totalTime) + "\n")
log_file.close()
print("------------Job Completed-------------")  