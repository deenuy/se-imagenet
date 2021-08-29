import nltk
# nltk.download('wordnet')
import os
from nltk.corpus import wordnet as wn
import deleteme
from pprint import pprint
from datetime import datetime
import pydot

# print(antonyms)
def getHypernyms(synset):
    return synset.hypernyms()

def getSynsetList(word):
  return wn.synsets(word)

def getSysetListWithPos(word, pos):
  return wn.synsets(word, pos=pos)

def getDefinition(synObj):
  return wn.synset(synObj).definition()

def getHyponyms(synObj):
  return synObj.hyponyms()

def getRootHypernyms(synObj):
  return synObj.root_hypernyms()

def getLCA(synObj1, synObj2):
  return synObj1.lowest_common_hypernyms(synObj2)

def getPathSimilarity(synObj1, synObj2):
  return synObj1.path_similarity(synObj2)

def getLCHPathSimilarity(synObj1, synObj2):
  return synObj1.lch_similarity(synObj2)

def getWUPPathSimilarity(synObj1, synObj2):
    return synObj1.wup_similarity(synObj2)

def getShortestPathDistanceBetweenTwoWord(self, synObj1, synObj2):
  return synObj1.shortest_path_distance(synObj2)

def removeDuplicates(list):
  return dict.fromkeys(list)
  
se_classes = ['computer', 'computer_science', 'mobile', 'desktop', 'software', 'software_engineering', 'software_artifacts', 'requirements_engineering']

synsetObjs = []
hyponymsObjs = []
synsetDict = {}
hyponymsDict = {}

print("\n")
for se_class in se_classes:
  synsetObj = getSynsetList(se_class)
  if synsetObj:
    for obj in synsetObj:
      synsetObjs.append(obj.name())
      synsetDict
      # print("\t--> ", obj.name())
      hyponymsObj = getHyponyms(obj)
      if hyponymsObj:
        for i in hyponymsObj:
          hyponymsObjs.append(i.name())
          # print("\t--> ", i.name())
# print()
# print("Synset words: ", synsetObjs)
# print()
# print("Hyponyms: ", hyponymsObjs)
# print()

synsets = wn.synsets('computer')

# for synset in synsets:
#   print(synset.name() + " Tree: ")
#   pprint(synset.tree(rel=getHypernyms))
#   print()

# Write to file
date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
fname = f"./staging/wordnet_se_{date}.txt"
# print("Filename: ", fname)
# f = open(fname, "w+")

# for obj in hyponymsObjs:
#   temp = obj.split(".")[0]
#   f.write("\n")
#   f.write(temp)
# f.close()

# fTree = f"./staging/wordnet_tree_{date}.txt"
# with open(fTree, 'wt') as out: 
#   for se_class in se_classes:
#     print("synset obj: ", se_class)
#     synsetObj = getSynsetList(se_class)
#     if synsetObj:
#       for obj in synsetObj:
#         print("\tsynset obj: ", obj)
#         pprint(obj.tree(rel=getHypernyms), stream=out)

# Get hierarchy from ACM
acm_se_classes = []
fname_se = f"./staging/june-1-wbs/acm_se_collection.txt"
# check if size of file is 0
if os.stat(fname_se).st_size == 0:
    print('File is empty')
else:
  f=open(fname_se, "r")
  lines = f.readlines()
  for line in lines:
    # print(line.strip())
    str = line.strip()
    acm_se_classes.append(str)

# print(acm_se_classes)

# function to get wordnet hypernyms
def getWordNetHierarchy(fname, arry):
  with open(fname, 'wt') as out: 
    for item in arry:
      print("synset obj: ", item)
      synsetObj = getSynsetList(item)
      if synsetObj:
        for obj in synsetObj:
          print("\tsynset obj: ", obj)
          pprint(obj.tree(rel=getHypernyms), stream=out)

fAcmTree = f"./staging/acm_tree_{date}.txt"
getWordNetHierarchy(fAcmTree, acm_se_classes)


# Get hierarchy from Wordnet for ACM classes 
acm_wordnet_list = []
fname_acm_se = f"./staging/june-1-wbs/acm_tree_2021_06_08-03-23-25.txt"
# check if size of file is 0
if os.stat(fname_acm_se).st_size == 0:
    print('File is empty')
else:
  f=open(fname_acm_se, "r")
  lines = f.readlines()
  for line in lines:
    # print(line.strip())
    str = line.strip()
    str = str.split("'")[1]
    str = str.split(".")[0]
    # print(str)
    acm_wordnet_list.append(str)

tempList = removeDuplicates(acm_wordnet_list)

fname_acm_wordnet_se = f"./staging/june-1-wbs/acm_wordnet_se.txt"
f=open(fname_acm_wordnet_se, "w")
for item in list(tempList):
  f.write("\n")
  f.write(item)