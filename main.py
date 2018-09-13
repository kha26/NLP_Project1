from collections import Counter
import random

startingWord = '<s>';
endingWord = '.';

## ===== GENERATE TABLES =======================================================
def unigramTable(text):
    data = text.split(' ');
    size = len(data);
    data = dict(Counter(data)); # Calculate no. occurences of each word
    #if callable(smoothing):
        #data = smoothing(data);
    for key, value in data.items():
        data[key] = (float) (value) / size; # Calculate prob of each word
    return data;

def bigramTable(text):
    text = text.lower();
    data = text.split(' ');
    size = len(data);
    wordCount = dict(Counter(data)); # Calculate no. occurences of each word
    wordCount[startingWord] = 1;
    bigramData = {};
    for x in range(0, size): # Iterate through every word
        if (x == 0):
            bigramData[startingWord] = { data[x] : 1 };
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
            else:
                bigramData[prevWord] = { word : 1 }
    for prevWord, possibleWords in bigramData.items():
        for nextWord, value in possibleWords.items():
            possibleWords[nextWord] = (float) (value) / wordCount[prevWord]

    return bigramData;

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

## ===== ADD ONE SMOOTHING =====================================================
# def addOneSmoothingUnigram(data):



if __name__ == '__main__':
    f = open('Assignment1_resources/development/trump.txt', 'r');
    if f.mode == 'r':
        contents = f.read();
        # contents = 'the students liked the assignment . the rowing is fun .';

        print('========== UNIGRAM ========== ');
        tableUnigram = unigramTable(contents);
        #print(tableUnigram);
        print(generateUniSentence(50, tableUnigram));

        print('========== BIGRAM  ========== ');
        tableBigram = bigramTable(contents);
        #print(tableBigram);
        print(generateBiSentence(50, tableBigram));
    else:
        print('Something went wrong bro!');
