# -*- coding: utf-8 -*-

# N-gram Language Models
# N元语言模型

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
		self.data = {}
		fp = open(fileName, 'r', encoding = 'utf-8')
		line = fp.readline()
		while len(line):
			for word in line:
				if not word in self.wordSet:
					self.wordSet.add(word)
			line = self.history * '\n' + line + self.history * '\n'
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
			line = fp.readline()
		fp.close()

	def plusOneSmooth(self):
		pass

	def parse(self, s):
		s = self.history * '\n' + s + self.history * '\n'
		if len(s) < self.history + 1:
			print('string too short')
		else:
			result = 1
			for i in range(self.history, len(s)):
				if s[i - self.history : i] in self.data:
					result *= self.data[s[i - self.history : i]][s[i]] / self.dataTimes[s[i - self.history : i]]
				else:
					print('error')
			print('result =', result)


if __name__ == '__main__':
	unigram = N_Gram(1, 'data/TheThreeBodyProblem.txt')
	s = input('input a line to parse, input a blank line to stop:')
	while len(s):
		unigram.parse(s)
		s = input('input a line to parse, input a blank line to stop:')
