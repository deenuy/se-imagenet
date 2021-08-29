from itertools import permutations, product
from datetime import datetime

# generate List type from csv file
def getListFromFile(fname, list):
  f=open(fname, "r")
  lines = f.readlines()
  for line in lines:
    str = line.strip()
    list.append((str))

# Write to file
date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

# List for SEWordSim |word1| >= 5 - WR_Entry
SEWordSimW1W2 = []
fname_SEWordSimW1W2 = f"./staging/synset_w1w2.csv"

getListFromFile(fname_SEWordSimW1W2, SEWordSimW1W2)

# List for CON_Terms
conTerms= []
fname_conTerms = f"./staging/june-1-wbs/wordnet_se_2021_06_08-02-07-36.txt"

getListFromFile(fname_conTerms, conTerms)

# Generate combimations using iterTools
permutations = product(conTerms, SEWordSimW1W2)

# print(list(permutations))
fnamePerm = f"./staging/june-1-wbs/dr_query_{date}.txt"
with open(fnamePerm, 'wt') as f: 
    for item in list(permutations):
      f.write(str(item))
      f.write("\n")

# for item in list(permutations):
#   print(item)