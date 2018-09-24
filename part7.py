print "====================Glove Model Performance============="
anaText = open('Assignment1_resources/analogy_test.txt', 'r')
anaTokens = anaText.read().lower().split()
anaWords = set(anaTokens)

wordMap = []
def loadGloveModel(gloveFile):
	print "Loading Model"
	f = open(gloveFile,'r')
	model = OrderedDict()
	for line in f:
	    splitLine = line.split()
	    word = splitLine[0]
	    embedding = np.array([float(val) for val in splitLine[1:]])
	    if word in anaWords:
	    	model[word] = embedding
	    	wordMap.append(word)
	    # elif (random.random() > 0.95):
	    # 	model[word] = embedding
	    # 	wordMap.append(word)
	print "Done.",len(model)," words loaded!"
	f.close()
	return model

model = loadGloveModel('embeddings/reduced_glove50d.txt')



M = np.array(model.values())
wordMap = np.array(wordMap)
row_norms = np.linalg.norm(M, axis=1)

anaFile = open('Assignment1_resources/analogy_test.txt', 'r')
trueResult = []
anaVocab = []
unkCount = 0
for line in anaFile:
	splitLine = line.split()
	if (splitLine[0].lower() in model and splitLine[1].lower() in model and splitLine[2].lower() in model):
		similarV = np.array(model[splitLine[1].lower()] - model[splitLine[0].lower()] + model[splitLine[2].lower()])
		trueResult.append(splitLine[3].lower())
	else:
		unkCount += 1
		similarV = np.zeros(50)
	anaVocab.append(similarV)
anaFile.close()

V = np.array(anaVocab)
anaNorms = np.linalg.norm(V, axis=1)
a,b = V.shape
print "predicting " + str(a) + " records."

COS = np.dot(M, V.T)/row_norms[:, None]/anaNorms[None, :]
wordIndices = np.argmax(COS, axis=0)
result = wordMap[wordIndices]
print "The accuracy is "+ str(round(np.mean(result == trueResult),4))


print "====================Dependent-based Model Performance============="
anaText = open('embeddings/R_analogy_test.txt', 'r')
anaTokens = anaText.read().lower().split()
anaWords = set(anaTokens)

wordMap = []
def loadGloveModel(gloveFile):
	print "Loading Model"
	f = open(gloveFile,'r')
	model = OrderedDict()
	for line in f:
	    splitLine = line.split()
	    word = splitLine[0]
	    embedding = np.array([float(val) for val in splitLine[1:]])
	    if word in anaWords:
	    	model[word] = embedding
	    	wordMap.append(word)
	    # elif (random.random() > 0.95):
	    # 	model[word] = embedding
	    # 	wordMap.append(word)
	print "Done.",len(model)," words loaded!"
	f.close()
	return model

model = loadGloveModel('embeddings/reduced_deps.txt')



M = np.array(model.values())
wordMap = np.array(wordMap)
row_norms = np.linalg.norm(M, axis=1)

anaFile = open('embeddings/R_analogy_test.txt', 'r')
trueResult = []
anaVocab = []
unkCount = 0
for line in anaFile:
	splitLine = line.split()
	if (splitLine[0].lower() in model and splitLine[1].lower() in model and splitLine[2].lower() in model):
		similarV = np.array(model[splitLine[1].lower()] - model[splitLine[0].lower()] + model[splitLine[2].lower()])
		trueResult.append(splitLine[3].lower())
	else:
		unkCount += 1
		similarV = np.zeros(50)
	anaVocab.append(similarV)
anaFile.close()

V = np.array(anaVocab)
anaNorms = np.linalg.norm(V, axis=1)
a,b = V.shape
print "predicting " + str(a) + " records."

COS = np.dot(M, V.T)/row_norms[:, None]/anaNorms[None, :]
wordIndices = np.argmax(COS, axis=0)
result = wordMap[wordIndices]
print "The accuracy is "+ str(round(np.mean(result == trueResult),4))