rawData = [] # format: [['word/tag', 'word/tag', ..., 'word/tag'], ...]

# load file
fp = open('data/data.txt', 'r', encoding = 'utf-8')
line = fp.readline()
while len(line):
	rawData.append(line.split('  '))
	line = fp.readline()
fp.close()

# divide into trainingData and testData
trainingData = [] # format: [['word/tag', 'word/tag', ..., 'word/tag'], ...]
testData = [] # format: [['word/tag', 'word/tag', ..., 'word/tag'], ...]
for i in range(len(rawData)):
	if i < len(rawData) * 0.8:
		# 80% data for training
		trainingData.append(rawData[i])
	else:
		# 20% data for test
		testData.append(rawData[i])
