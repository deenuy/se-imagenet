import os
import shutil
ROOT_DIR = os.path.abspath(os.getcwd())
print(ROOT_DIR)
""" final_directory = os.path.join(ROOT_DIR,"Excels")
os.mkdir(final_directory) """
final_directory = 'C:/Users/Gargi/Desktop/SEImgnet/Excels'
print(final_directory)
for root, dirs, files in os.walk(ROOT_DIR):
    for f in files:
        if f.endswith('.csv'):
            shutil.copy(os.path.join(root,f), final_directory)