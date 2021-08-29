import nltk
# nltk.download('wordnet')
import os
from nltk.corpus import wordnet as wn
import deleteme
from pprint import pprint
from datetime import datetime
import pydot

# Return a score denoting how similar two word senses are, based on the shortest path 
# that connects the senses in the is-a (hypernym/hypnoym) taxonomy. 

def getHypernyms(synset):
    return synset.hypernyms()

def getSynsetList(word):
  return wn.synsets(word)

def getPathSimilarity(synObj1, synObj2):
  return synObj1.path_similarity(synObj2)

def getWUPPathSimilarity(synObj1, synObj2):
    return synObj1.wup_similarity(synObj2)

def getShortestPathDistanceBetweenTwoWord(synObj1, synObj2):
  return synObj1.shortest_path_distance(synObj2)

def removeDuplicates(list):
  return dict.fromkeys(list)

# Write to file
date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")

# function to get wordnet hypernyms
def getWordNetHierarchy(fname, arry):
  with open(fname, 'wt') as out: 
    for item in arry:
      # print("synset obj: ", item)
      synsetObj = getSynsetList(item)
      if synsetObj:
        for obj in synsetObj:
          # print("\tsynset obj: ", obj)
          pprint(obj.tree(rel=getHypernyms), stream=out)

# Collection for Word 1 coloum list from SEWordSim database
SEWordSimW1 = []

fname_wordnet_se = f"./staging/synset_count.txt"
f=open(fname_wordnet_se, "r")
lines = f.readlines()
for line in lines:
  str = line.strip()
  str = str.split(',')[0]
  SEWordSimW1.append((str))

# print(SEWordSimW1)

fSEWordSimW1Tree = f"./staging/SEWordSimW1tree_{date}.txt"
getWordNetHierarchy(fSEWordSimW1Tree, SEWordSimW1)

# getWordNetHierarchy(fAcmTree, acm_se_classes)