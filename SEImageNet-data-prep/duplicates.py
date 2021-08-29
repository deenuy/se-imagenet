import os
import numpy as np
import pandas as pd
from os import listdir
path = os.getcwd()
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
filenames = find_csv_filenames(path)
for name in filenames:
    print(name)
    df = pd.read_csv(name, sep="|",usecols=np.arange(12))
    df.drop_duplicates(keep='first',inplace=True)
    df.to_csv('Cleaned'+name, index=False)