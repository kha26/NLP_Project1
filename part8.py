from collections import Counter, OrderedDict
import numpy as np
import math
import random
import csv

def loadGloveData(gloveFile):
    #print 'Getting gloVe data';
    data = {};
    f = open(gloveFile,'r')
    lineNo = 0;
    for line in f:
        #if lineNo % 4000 == 0:
        #    print('%' + str(lineNo / 4000) + ' done');
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        data[word] = embedding;
        lineNo += 1;
    #print 'Finished getting gloVe data';
    return data;

def loadGloveModelW(anaWords, gloveData):
    model = OrderedDict()
    for word in anaWords:
        if word in gloveData:
            model[word] = gloveData[word];
    return model;

def loadGloveModel(anaWords, wordMap, gloveFile):
    # print "loading GloVe model ..."
    f = open(gloveFile,'r')
    model = OrderedDict()
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        if word in anaWords:
            model[word] = embedding
            wordMap.append(word)
    # print "... done:",len(model)," words loaded!"
    f.close()
    return model

def getAnaWords(file):
    anaText = open(file, 'r')
    anaTokens = anaText.read().lower().split()
    anaWords = set(anaTokens)
    return anaWords;

def cosineSimilarity(v1, v2):
    cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2));
    return cos;

def writeResults(results):
    with open('submission_part8.csv', mode='w') as employee_file:
        result_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result_writer.writerow(['Id', 'Prediction']);
        i = 0;
        for result in results:
            result_writer.writerow([i, result]);
            i += 1;


if __name__ == '__main__':
    gloveFile = 'embeddings/reduced_glove50d.txt';

    gloveData = loadGloveData(gloveFile);

    #print 'Getting Obama data';
    obamaWords = getAnaWords('Assignment1_resources/train/obama.txt');
    obamaWordMap = [];
    # obamaModel = loadGloveModel(obamaWords, obamaWordMap, gloveFile);
    obamaModel = loadGloveModelW(obamaWords, gloveData);
    obamaRep = np.average(obamaModel.values(), axis=0); # xR for Obama
    #print 'Finished Obama data: ' + str(obamaRep);

    #print 'Getting Trump data';
    trumpWords = getAnaWords('Assignment1_resources/train/trump.txt');
    trumpWordMap = [];
    # trumpModel = loadGloveModel(trumpWords, trumpWordMap, gloveFile);
    trumpModel = loadGloveModelW(trumpWords, gloveData);
    trumpRep = np.average(trumpModel.values(), axis=0); # xR for Trump
    #print 'Finished Trump data: ' + str(trumpRep);

    dataSet = [];
    testSet = open('Assignment1_resources/test/test.txt', 'r');
    # For each paragraph in test.txt, create xR vector
    lineNo = 0;
    #print 'Getting line data';
    for line in testSet:
        paragraphWords = set(line.lower().split());
        # paragraphModel = loadGloveModel(paragraphWords, [], gloveFile);
        paragraphModel = loadGloveModelW(paragraphWords, gloveData);
        paragraphRep = np.average(paragraphModel.values(), axis=0);
        dataSet.append(paragraphRep);
        lineNo += 1;
    #print 'Finished line data';

    results = [];
    for rep in dataSet:
        if str(rep) == 'nan':
            trumpValue = random.random();
            obamaValue = random.random();
        else:
            trumpValue = cosineSimilarity(rep, trumpRep);
            obamaValue = cosineSimilarity(rep, obamaRep);
        result = '0' if obamaValue > trumpValue else '1';
        results.append(result);

    writeResults(results);
