#!/usr/bin/python
#-*- coding: utf-8 -*-



import re
import requests
from bs4 import BeautifulSoup
import sys
import numpy as np
import math
import nltk; nltk.download('punkt')
from nltk import word_tokenize



# 전역 변수
word_d = {}
sent_list = []



# 특수문자 제거 (공백 제외)
def clean_word_list(input_list):

	output_list = []

	for word in input_list:

		symbols = """!•@#$%^&*()_-+={[}]|\;:"‘'·<>?/.,‹›"""

		for i in range(len((symbols))):
			word = word.replace(symbols[i], '')

		if len(word) > 0:
			output_list.append(word)

	return output_list


# { '단어' : '빈도수' }
def process_new_sentence(input_list):
		
	sent_list.append(input_list)

	tokenized = word_tokenize(input_list)

	for word in tokenized:

		if word not in word_d.keys():
			word_d[word] = 0

		word_d[word] += 1


# tf 계산
def compute_tf(input_list):	# sent_list를 input으로

	bow = set()
	wordcount_d = {}


	tokenized = word_tokenize(input_list)
	
	for tok in tokenized:

		if tok not in wordcount_d.keys():
			wordcount_d[tok] = 0

		wordcount_d[tok] += 1

		bow.add(tok)


	tf_d = {}

	for word, count in wordcount_d.items():

		tf_d[word] = count / len(bow)

	return tf_d


def compute_idf():

	Dval = len(sent_list)
	bow = set()

	for i in range(0, len(sent_list)):

		tokenized = word_tokenize(sent_list[i])

		for tok in tokenized:
			bow.add(tok)

	#print(bow)	

	idf_d = {}

	for t in bow:

		cnt = 0

		for s in sent_list:

			if t in word_tokenize(s):
				cnt += 1

				idf_d[t] = math.log(Dval/cnt)

	return idf_d



if __name__=='__main__':

	print()


	process_new_sentence("this is a good day to study what happend to your study plan today you need more study")

	process_new_sentence("i need a coffee but coffee is bad for your health")

	process_new_sentence("my cat jumped off the car today")
	process_new_sentence("let's study together at the cafe")
	process_new_sentence("yesterday i saw you study in the house")
	process_new_sentence("where were you yesterday i have been looking for you all over")


	idf_d = compute_idf()

	for i in range(0, len(sent_list)):

		tf_d = compute_tf(sent_list[i])

		for word, tfval in tf_d.items():

			print(word, tfval * idf_d[word])

		print("	")
