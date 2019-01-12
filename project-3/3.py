# -*- coding: utf-8 -*-

# Part-Of-Speech(Use add-one smoothing)
# 词性标注（使用加一平滑来平滑数据）

rawData = [] # format: [['word/tag', 'word/tag', ..., 'word/tag'], ...]

# load file
fp = open('data/data2.txt', 'r', encoding = 'utf-8')
line = fp.readline()
while len(line):
	line = line[:-1] # discard '\n'
	if len(line):
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
for line in rawData:
	for item in line:
		if item.split('/')[0] not in words:
			words.append(item.split('/')[0])
		if item.split('/')[1] not in tags:
			tags.append(item.split('/')[1])

# add start symbol and end symbol
tags = ['$start$'] + tags + ['$end$']
words = ['$start$'] + words + ['$end$']

# init model parameters to 1(add one smmothing)
tagTrans = dict() # state transition probability of tags, 'preTag nextTag'->int
emit = dict() # observation emit probability, 'tag word'->int
for preTag in tags:
	for nextTag in tags:
		tagTrans[preTag + ' ' + nextTag] = 1
	for word in words:
		emit[preTag + ' ' + word] = 1

# training, construct model parameters
for line in trainingData:
	# construct emit
	for item in line:
		emit[item.split('/')[1] + ' ' + item.split('/')[0]] += 1
	# add start symbol and end symbol
	line = ['$start$/$start$'] + line + ['$end$/$end$']
	# construct tagTrans
	for i in range(len(line) - 1):
		tagTrans[line[i].split('/')[1] + ' ' + line[i + 1].split('/')[1]] += 1

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

# $start$ must emit $start$, $end$ must emit $end$. ignore smoothing
emit['$start$ $start$'] = emit['$end$ $end$'] = 1

# process test data, use Viterbi algorithm
allCorrectCount = 0 # ignore $start$ and $end$
allWordsCount = 0 # ignore $start$ and $end$
# total precision = allCorrectCount / allWordsCount
for index in range(len(testData)):
	line = testData[index]
	allWordsCount += len(line) # ignore $start$ and $end$
	line = ['$start$/$start$'] + line + ['$end$/$end$']
	# retrive words and tags in test data
	testWords = []
	testTags = []
	for item in line:
		testWords.append(item.split('/')[0])
		testTags.append(item.split('/')[1])

	# process testWords, init Viterbi matrix
	v = [[0 for x in range(len(tags))] for y in range(len(line))] # v[len(line)][len(tags)]
	path = [[0 for x in range(len(tags))] for y in range(len(line))] # path[len(line)][len(tags)]
	# init Viterbi matrix
	for j in range(len(tags)):
		v[1][j] = tagTrans[tags[0] + ' ' + tags[j]] * emit[tags[j] + ' ' + testWords[1]]
		path[1][j] = 0 # path[1][j] = $start$
	# recurrence
	for t in range(2, len(testWords)):
		for j in range(len(tags)):
			for i in range(len(tags)):
				p = v[t - 1][i] * tagTrans[tags[i] + ' ' + tags[j]] * emit[tags[j] + ' ' + testWords[t]]
				if p > v[t][j]:
					v[t][j] = p
					path[t][j] = i
	# result probability is v[len(line) - 1][len(tags) - 1]

	# construct result tags
	resultIndex = [0 for x in range(len(line))] # result tag index sequence, include $start$ and $end$
	resultIndex[0] = 0 # $start$
	resultIndex[-1] = len(tags) - 1 # $end$
	for i in reversed(range(len(line) - 1)):
		resultIndex[i] = path[i + 1][resultIndex[i + 1]]
	result = [] # result tag sequence, include $start$ and $end$
	for i in resultIndex:
		result.append(tags[i])

	# output result
	correctCount = 0
	for i in range(len(result)):
		if result[i] == testTags[i]:
			correctCount += 1
			allCorrectCount += 1
	print('progress:', (index + 1) * 100 // len(testData), '%', 'single line precision:', (correctCount - 2) / (len(result) - 2)) # ignore $start$ and $end$
	allCorrectCount -= 2 # ignore $start$ and $end$
print('total precision:', allCorrectCount / allWordsCount)