# -*- coding: utf-8 -*-

# N-gram Language Models
# N元语言模型

import itertools

class N_Gram(object):
	def __init__(self, n, fileName = ''):
		'fileName is the training set file'
		self.history = n - 1 # length of history
		self.data = {} # format: key: list of length(history), value: list of {word(str): time(int)}
		self.dataTimes = {} # format: key: list of length n, value: time(int)
		self.wordSet = set()
		if len(fileName):
			self.openFile(fileName)

	def openFile(self, fileName):
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
		for p in itertools.product(self.wordSet, repeat = self.history):
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
					result *= self.data[s[i - self.history : i]][s[i]] / self.dataTimes[s[i - self.history : i]]
				else:
					print('error, unknow situation, please try to smooth data')
					return
			print('Word Perplexity:', result ** -(1 / len(s)))


if __name__ == '__main__':
	# unigram = N_Gram(1, 'data/TheThreeBodyProblem.txt')
	bigram = N_Gram(2, 'data/TheThreeBodyProblem.txt')
	# trigram = N_Gram(3, 'data/TheThreeBodyProblem.txt')
	s = input('input a line to parse, input a blank line to stop:')
	while len(s):
		# unigram.parse(s)
		bigram.parse(s)
		bigram.additiveSmoothing(0.5)
		bigram.parse(s)
		# trigram.parse(s)
		s = input('input a line to parse, input a blank line to stop:')
