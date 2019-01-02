# -*- coding: utf-8 -*-

# 利用基于线性规划的最长公共子序列算法计算输出结果和PKU给出的gold结果的吻合程度

'provide function: LCS_Length(list1, list2)'

def LCS_Length(list1, list2):
	'return LCS length'
	# init a[len(list1)][len(list2)] = {0}
	a = [[0 for i in range(len(list2))] for j in range(len(list1))]

	# calculate
	for i in range(len(list1)):
		for j in range(len(list2)):
			if list1[i] == list2[j]:
				if i > 0 and j > 0:
					a[i][j] = a[i - 1][j - 1] + 1
				else:
					a[i][j] = 1
			else:
				if i > 0 and j > 0:
					a[i][j] = max(a[i][j - 1], a[i - 1][j])
				else:
					a[i][j] = 1

	return a[len(list1) - 1][len(list2) - 1]