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

# training, construct model parameters
tagTrans = dict() # state transition probability of tags 'preTag nextTag'->int
emit = dict() # observation emit probability, 'tag word'->int
for line in trainingData:
	# construct emit
	for item in line:
		key = item.split('/')[1] + ' ' + item.split('/')[0]
		if key not in emit:
			emit[key] = 1
		else:
			emit[key] += 1
	# add start symbol and end symbol
	line = ['$start$/$start$'] + line + ['$end$/$end$']
	# construct tagTrans
	for i in range(len(line) - 1):
		key = line[i].split('/')[0] + ' ' + line[i + 1].split('/')[0]
		if key not in tagTrans:
			tagTrans[key] = 1
		else:
			tagTrans[key] += 1
