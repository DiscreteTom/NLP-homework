# -*- coding: utf-8 -*-

# chinese word segmentation
# 中文分词问题

import lcs

class Segmentor():
	def __init__(self, fileName = '', lookAhead = 1):
		self.wordSet = set()
		self.lookAhead = lookAhead
		if len(fileName):
			self.openFile(fileName)

	def openFile(self, fileName):
		'load word set from a file'
		self.wordSet.clear()
		fp = open(fileName, 'r', encoding = 'utf-8')
		self.wordSet = set(fp.read().split('\n'))
		fp.close()

	def parse(self, string):
		'parse string using word set and return result as an array'
		
		resultWords = []
		currentLookAhead = 0
		startIndex = 0 # index of string, start of word
		currentIndex = 0 # index of string, end of word

		while currentIndex < len(string):
			if currentLookAhead < self.lookAhead:
				currentLookAhead += 1
				if currentIndex + currentLookAhead < len(string) and string[startIndex : currentIndex + currentLookAhead + 1] in self.wordSet:
					currentIndex += currentLookAhead
					currentLookAhead = 0
				elif currentIndex + currentLookAhead >= len(string):
					resultWords.append(string[startIndex : currentIndex + 1])
					startIndex = currentIndex + 1
					currentIndex += 1
					currentLookAhead = 0
			else:
				resultWords.append(string[startIndex : currentIndex + 1])
				startIndex = currentIndex + 1
				currentIndex += 1
				currentLookAhead = 0

		# last word
		if startIndex < currentIndex:
			resultWords.append(string[startIndex : currentIndex + 1])

		return resultWords

if __name__ == '__main__':
	# init segmentor
	segmentor = Segmentor('data/pku_training_words.utf8', 5)

	# init counter
	wordsSegmented = 0
	correctlySegmented = 0
	shouldBeSegmented = 0

	# parse file one line at a time
	testFile = open('data/pku_test.utf8', 'r', encoding = 'utf-8')
	goldFile = open('data/pku_test_gold.utf8', 'r', encoding = 'utf-8')
	testLine = testFile.readline()
	goldWords = goldFile.readline().split('  ')
	while len(testLine) and len(goldWords):
		testWords = segmentor.parse(testLine)
		wordsSegmented += len(testWords)
		correctlySegmented += lcs.LCS_Length(testWords, goldWords)
		shouldBeSegmented += len(goldWords)
		testLine = testFile.readline()
		goldWords = goldFile.readline().split('  ')
	testFile.close()
	goldFile.close()

	print('wordsSegmented =', wordsSegmented)
	print('correctlySegmented =', correctlySegmented)
	print('shouldBeSegmented =', shouldBeSegmented)
	p = correctlySegmented / wordsSegmented
	r = correctlySegmented / shouldBeSegmented
	print('precision = ', p)
	print('recall = ', r)
	print('F-measure =', 2 * p * r / (p + r))