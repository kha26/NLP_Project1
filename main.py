#coding=iso-8859-1
from collections import Counter
import random
import math

startingWord = '<s>';
endingWord = '.';

## ===== PREPROCESSING ==========
def preprocessText(text):
    text = text.lower();
    text = text.replace(' ``', ''); # Get rid of ``
    text = text.replace(' \'\'', ''); # Get rid of ''
    text = text.replace(' “', ''); # Get rid of “
    text = text.replace(' ”', ''); # Get rid of ”

    text = text.replace(' \'', '\''); # it 's => it's, teachers ' => teachers'
    text = text.replace(' ’ ', '’'); # can ’ t => can’t
    # text = text.replace(' n\'', 'n\''); # did n't => didn't
    return text;

## ===== GENERATE TABLES =======================================================
def unigramTable(text):
    data = text.split(' ');
    data = dict(Counter(data)); # Calculate no. occurences of each word
    return data;

def bigramTable(text):
    data = text.split(' ');
    size = len(data);
    wordCount = dict(Counter(data)); # Calculate no. occurences of each word
    wordCount[startingWord] = 1;
    bigramData = {};
    continuation = {}
    for x in range(0, size): # Iterate through every word
        if (x == 0):
            bigramData[startingWord] = { data[x] : 1 };
            continuation[data[x]] = 1
        else:
            prevWord = data[x-1];
            if prevWord == endingWord:
                prevWord = startingWord;
                wordCount[startingWord] += 1;

            word = data[x];
            if prevWord in bigramData:
                if word in bigramData[prevWord]:
                    bigramData[prevWord][word] += 1;
                else:
                    bigramData[prevWord][word] = 1;
                    if word in continuation:
                        continuation[word] = continuation[word] + 1
                    else:
                        continuation[word] = 1
            else:
                bigramData[prevWord] = { word : 1 }
                if word in continuation:
                    continuation[word] = continuation[word] + 1
                else:
                    continuation[word] = 1

    return (wordCount, bigramData), continuation;

def unigramProbTable(data):
    size = sum(data.values());
    table = {}
    for key, value in data.items():
        table[key] = (float) (value) / size; # Calculate prob of each word
    return table;

def bigramProbTable(data, bigramData):
    table = {}
    for prevWord, possibleWords in bigramData.items():
        table[prevWord] = {}
        for nextWord, value in possibleWords.items():
            table[prevWord][nextWord] = (float) (value) / data[prevWord]
    return table;


## ===== GENERATE RANDOM SENTENCE ==============================================
def pickRandomWord(data):
    rnd = random.uniform(0, 1)
    lastKey = None;
    for key, value in data.items():
        lastKey = key;
        if rnd < value:
            return key;
        else:
            rnd -= value;
    return key;

def generateUniSentence(length, data):
    sentence = '';
    for x in range(0, length):
        sentence += pickRandomWord(data) + ' ';
    return sentence;

def generateBiSentence(length, data):
    sentence = '';
    prevWord = startingWord;
    for x in range(0, length):
        nextWord = pickRandomWord(data[prevWord]);
        if nextWord == endingWord:
            sentence += '. ';
            prevWord = startingWord;
        else:
            sentence += nextWord + ' ';
            prevWord = nextWord;
    return sentence;

## ===== ADD SMOOTHING =====================================================
# def addOneSmoothingUnigram(data):

##KneserNey Smoothing
#We expect the contents of unigrams to be a dictionary, containing Strings: counts
#We expect the contents of bigrams to be a dictionary of dictionaries, containing a mapping of String:Count
#We expect the contents of continuation to be a dictionary mapping stirngs to int, containing the number of unique bigrams the string is the second token of
def kneserNey(unigrams, bigrams, continuation):
    discount = 0.75
    print(continuation)
    numBigramTypes = float(sum(continuation.itervalues()))
    newProbabilities = {}

    for bigramToken, dictionaries in bigrams.iteritems():
        newProbabilities[bigramToken] = {}
        countPrev = sum(dictionaries.itervalues())
        lmbda = discount/ countPrev * len(dictionaries)
        for token in unigrams:
            if token in dictionaries:
                count = dictionaries[token]
            else:
                count = 0
            discountedProbability = max(count - discount, 0)/countPrev
            continuationValue = continuation[token] / numBigramTypes
            newProbabilities[bigramToken][token] = discountedProbability + lmbda * continuationValue
    print(newProbabilities)
    return newProbabilities

## ===== PERPLEXITY ========================================================
##Expect modelData to be a dictionary of word: probability
def perplexity(modelData):
    logSum = 0
    numOfWords = len(modelData)
    for probability in modelData.values():
        logSum -= math.log(probability)
    perplexity = math.exp(logSum/float(numOfWords))
    return perplexity

def flatten(bigrams):
    flattenedBigrams = {}
    for word, nextWordProbs in bigrams.items():
        for nextWord, prob in nextWordProbs.items():
            flattenedBigrams[nextWord] = prob
    return flattenedBigrams

def evaluate(unigram, bigrams):
    unigramPP = perplexity(tableUnigram)
    bigramPP = perplexity(flatten(tableBigram))
    print("UNIGRAM: " + str(unigramPP))
    print("BIGRAM: " + str(bigramPP))



if __name__ == '__main__':
    f = open('Assignment1_resources/development/trump.txt', 'r');
    if f.mode == 'r':
        contents = f.read();
        contents = 'the students liked the assignment .';

        contents = preprocessText(contents);

        print('========== UNIGRAM ========== ');
        unigramData = unigramTable(contents);
        print(unigramData)
        tableUnigram = unigramProbTable(unigramData);
        print(tableUnigram)

        print('========== BIGRAM  ========== ');
        (wordCount, bigramData), continuation = bigramTable(contents);
        print(bigramData)
        tableBigram = bigramProbTable(wordCount, bigramData);
        print(tableBigram)

        print('===Modified Kneser-Ney===')
        kneserNey(unigramData, bigramData, continuation)

        print('==========PERPLEXITY==============')
        evaluate(tableUnigram, tableBigram)

    else:
        print('Something went wrong bro!');
