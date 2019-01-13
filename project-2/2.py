# -*- coding: utf-8 -*-

# N-gram Language Models
# N元语言模型

import itertools

class N_Gram(object):
	def __init__(self, n, fileName = ''):
		'fileName is the training set file'
		self.history = n - 1 # length of history
		self.data = {} # format: key: history(str), value: list of {word(str): time(int)}
		self.dataTimes = {} # format: key: string of length n - 1, value: time(int)
		self.wordSet = set()
		if len(fileName):
			self.openFile(fileName)
		self.smoothing = ''

	def openFile(self, fileName):
		print('loading file...')
		self.data = {} # clear

		fp = open(fileName, 'r', encoding = 'utf-8')
		line = fp.readline()
		while len(line):
			# join wordSet
			for word in line:
				if not word in self.wordSet:
					self.wordSet.add(word)
			# add start and end mark
			line = self.history * '\n' + line + self.history * '\n'
			# construct
			for i in range(self.history, len(line)):
				if line[i - self.history : i] in self.data:
					if line[i] in self.data[line[i - self.history : i]]:
						self.data[line[i - self.history : i]][line[i]] += 1
					else:
						self.data[line[i - self.history : i]][line[i]] = 1
				else:
					self.data[line[i - self.history : i]] = {}
					self.data[line[i - self.history : i]][line[i]] = 1
				if line[i - self.history : i] in self.dataTimes:
					self.dataTimes[line[i - self.history : i]] += 1
				else:
					self.dataTimes[line[i - self.history : i]] = 1
			# continue loop
			line = fp.readline()
		fp.close()

	def additiveSmoothing(self, n = 1.0):
		self.smoothing = 'add-' + str(n) + ' smoothing'
		print('apply', self.smoothing, '...')
		for p in itertools.product(self.wordSet, repeat = self.history):
			# change tuple to string
			history = ''
			for word in p:
				history += word
			
			for word in self.wordSet:
				if not history in self.data:
					self.data[history] = {}
				if not word in self.data[history]:
					self.data[history][word] = 0
				self.data[history][word] += n
				if not history in self.dataTimes:
					self.dataTimes[history] = 0
				self.dataTimes[history] += n
	
	def goodTuringSmoothing(self):
		self.smoothing = 'Good-Turing smoothing'
		print('apply', self.smoothing, '...')
		# fill self.data about situation that never happened
		for p in itertools.product(self.wordSet, repeat = self.history):
			# change tuple to string
			history = ''
			for word in p:
				history += word

			for word in self.wordSet:
				if not history in self.data:
					self.data[history] = {}
				if not word in self.data[history]:
					self.data[history][word] = 0
		
		n = {} # n[i] means the count of words which appears i times
		# construct n
		for history in self.data:
			for word in self.data[history]:
				if self.data[history][word] in n:
					n[self.data[history][word]] += 1
				else:
					n[self.data[history][word]] = 1
		# find most often appear
		maxAppearence = max(n.keys())
		# fill n[maxAppearence + 1]
		for i in range(maxAppearence + 2):
			if not i in n:
				n[i] = 0
		# reset self.data and self.dataTimes
		for p in itertools.product(self.wordSet, repeat = self.history):
			# change tuple to string
			history = ''
			for word in p:
				history += word

			for word in self.wordSet:
				c = self.data[history][word]
				if n[c + 1] != 0: # if n[c + 1] == 0, ignore
					self.data[history][word] = (c + 1) * n[c + 1] / n[c]
					# reset self.dataTimes
					self.dataTimes[history] -= c
					self.dataTimes[history] += self.data[history][word]


	def parse(self, s):
		# judge unknow word
		for word in s:
			if not word in self.wordSet:
				print('unknow word')
				return

		s = self.history * '\n' + s + self.history * '\n'
		if len(s) < self.history + 1:
			print('string too short')
		else:
			result = 1
			for i in range(self.history, len(s)):
				if s[i - self.history : i] in self.data and s[i] in self.data[s[i - self.history : i]]:
					result *= (self.data[s[i - self.history : i]][s[i]] / \
					self.dataTimes[s[i - self.history : i]]) ** -(1 / len(s))
				else:
					print('error, unknow situation, please try to smooth data')
					return
			if len(self.smoothing):
				print('After', self.smoothing, ':', end = '')
			print('Word Perplexity:', result)


if __name__ == '__main__':
	b = N_Gram(2, 'data/TheThreeBodyProblem.txt') # bigram
	b_0_5 = N_Gram(2, 'data/TheThreeBodyProblem.txt') # bigram with additive smoothing
	b_0_5.additiveSmoothing(0.5)
	b_1 = N_Gram(2, 'data/TheThreeBodyProblem.txt') # bigram with additive smoothing
	b_1.additiveSmoothing(1)
	b_gt = N_Gram(2, 'data/TheThreeBodyProblem.txt') # bigram with good-turing smoothing
	b_gt.goodTuringSmoothing()

	s = input('input a line to parse, input a blank line to stop:')
	while len(s):
		b.parse(s)
		b_0_5.parse(s)
		b_1.parse(s)
		b_gt.parse(s)
		s = input('input a line to parse, input a blank line to stop:')
