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

# collect data
tags = []
words = []
for line in trainingData:
	for item in line:
		if item.split('/')[0] not in words:
			words.append(item.split('/')[0])
		if item.split('/')[1] not in tags:
			tags.append(item.split('/')[1])

# add start symbol and end symbol
tags.append('$start$').append('$end$')
words.append('$start').append('$end$')

# init model parameters
tagTrans = dict() # state transition probability of tags, 'preTag nextTag'->int
emit = dict() # observation emit probability, 'tag word'->int
for preTag in tags:
	for nextTag in tags:
		tagTrans[preTag + ' ' + nextTag] = 0
	for word in words:
		emit[preTag + ' ' + word] = 0

# training, construct model parameters
for line in trainingData:
	# construct emit
	for item in line:
		emit[item.split('/')[1] + ' ' + item.split('/')[0]] += 1
	# add start symbol and end symbol
	line = ['$start$/$start$'] + line + ['$end$/$end$']
	# construct tagTrans
	for i in range(len(line) - 1):
		tagTrans[line[i].split('/')[0] + ' ' + line[i + 1].split('/')[0]] += 1

# change int to double, change count to probobility
for preTag in tags:
	count = 0
	for nextTag in tags:
		count += tagTrans[preTag + ' ' + nextTag]
	for nextTag in tags:
		tagTrans[preTag + ' ' + nextTag] /= count
for tag in tags:
	count = 0
	for word in words:
		count += emit[tag + ' ' + word]
	for word in words:
		emit[tag + ' ' + word] /= count

# process test data, use Viterbi algorithm
for line in testData:
	# retrive words and tags in test data
	testWords = []
	testTags = []
	for item in line:
		testWords.append(item.split('/')[0])
		testTags.append(item.split('/')[1])
	# process testWords
