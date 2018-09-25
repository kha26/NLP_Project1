from main import *
from collections import Counter, OrderedDict
import numpy as np

devFile = open('Assignment1_resources/development/trump.txt', 'r');
trainFile = open('Assignment1_resources/train/trump.txt', 'r');
devText = devFile.read();
trainText = trainFile.read();

dev = preprocessText(devText).split(" ")
train = preprocessText(trainText).split(" ")

################Raw Unigram################
print "Unigram Perplexity Without Smoothing(Trump):"
count = Counter(train)
total = sum(count.values(), 0.0)
unk = {k:v for k,v in count.items() if v == 1}
countAll = {k:v-1 for k,v in count.items() if v > 1}
unkTotal = sum(unk.values())
countAll["<unk>"] = unkTotal + len(countAll)
unimodel = {k:v/total for k,v in countAll.items()}
print perplexity(dev, unimodel)

################Add One################
print "Unigram Perplexity With Add One Smoothing(Trump):"
smCount = {k:v+1 for k,v in countAll.items()}
nWordType = len(smCount)
smUnimodel = {k:v/(total+nWordType) for k,v in smCount.items()}
print perplexity(dev, smUnimodel)

devFile = open('Assignment1_resources/development/obama.txt', 'r');
trainFile = open('Assignment1_resources/train/obama.txt', 'r');
devText = devFile.read();
trainText = trainFile.read();

dev = preprocessText(devText).split(" ")
train = preprocessText(trainText).split(" ")

################Raw Unigram################
print "Unigram Perplexity Without Smoothing(Obama):"
count = Counter(train)
total = sum(count.values(), 0.0)
unk = {k:v for k,v in count.items() if v == 1}
countAll = {k:v-1 for k,v in count.items() if v > 1}
unkTotal = sum(unk.values())
countAll["<unk>"] = unkTotal + len(countAll)
unimodel = {k:v/total for k,v in countAll.items()}
print perplexity(dev, unimodel)

################Add One################
print "Unigram Perplexity With Add One Smoothing(Obama):"
smCount = {k:v+1 for k,v in countAll.items()}
nWordType = len(smCount)
smUnimodel = {k:v/(total+nWordType) for k,v in smCount.items()}
print perplexity(dev, smUnimodel)