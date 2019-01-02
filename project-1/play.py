# -*- coding: utf-8 -*-

# chinese word segmentation

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
			resultWords.append(str[startIndex : currentIndex + 1])

		return resultWords

if __name__ == '__main__':
	segmentor = Segmentor('data/pku_training_words.utf8', 5)
	while True:
		str = input('Input a string to parse, or a blank string to stop:')
		if len(str) == 0:
			break
		print(segmentor.parse(str))