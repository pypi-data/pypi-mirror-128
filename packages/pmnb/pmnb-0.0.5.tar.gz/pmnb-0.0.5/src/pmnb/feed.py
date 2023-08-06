# coding: utf-8

#比较两个句子的相似度
import sys

def xsd(text1,text2):
	#集合必须满足互斥性，所以去重
	text1=set(text1)
	text2=set(text2)
	sml=(len(text1&text2))/(len(text1|text2))
	print("两个句子的相似度为:{0}".format(sml))

