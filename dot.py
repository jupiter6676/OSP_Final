#!/usr/bin/python
#-*- coding: utf-8 -*-


"""
https://nutch.apache.org/
http://attic.apache.org/
https://brooklyn.apache.org/
https://allura.apache.org/
"""


import re
import requests
from bs4 import BeautifulSoup
import sys
import numpy as np



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


	for word in input_list:

		if word in word_d:
			word_d[word] += 1

		else:
			word_d[word] = 0

	return word_d


# 길이가 같은 벡터 만들기
def make_vector(i, input_list):

	v = []
	s = sent_list[i]


	for word in word_d.keys():

		val = 0

		for t in input_list:

			if t == word:	val += 1

		v.append(val)


	return v



# 1 (기준)
url = requests.get("https://nutch.apache.org/")
html = BeautifulSoup(url.content, 'html.parser')


body = html.select('body')

word = []

for tag in body:

	word.append(tag.get_text().strip())


word_list = []
word_list = ''.join(word).lower().split()	# word를 문자열로 변환 후, 공백 기준으로 나누기


clean_list = []
clean_list = clean_word_list(word_list)	# 특수 문자 제거

process_new_sentence(clean_list)




# 2
url_2 = requests.get("http://attic.apache.org/")
html_2 = BeautifulSoup(url_2.content, 'html.parser')


body_2 = html_2.select('body')

word_2 = []	# 맨 처음 크롤링한 데이터

for tag in body_2:

	word_2.append(tag.get_text().strip())


word_list_2 = []
word_list_2 = ''.join(word_2).lower().split()	# 공백 기준으로 나누기


clean_list_2 = []
clean_list_2 = clean_word_list(word_list_2)	# 특수 문자 제거


process_new_sentence(clean_list_2)




# 3
url_3 = requests.get("https://brooklyn.apache.org/")
html_3 = BeautifulSoup(url_3.content, 'html.parser')


body_3 = html_3.select('body')

word_3 = []	# 맨 처음 크롤링한 데이터

for tag in body_3:

	word_3.append(tag.get_text().strip())


word_list_3 = []
word_list_3 = ''.join(word_3).lower().split()	# 공백 기준으로 나누기


clean_list_3 = []
clean_list_3 = clean_word_list(word_list_3)	# 특수 문자 제거


process_new_sentence(clean_list_3)




# 4
url_4 = requests.get("https://allura.apache.org/")
html_4 = BeautifulSoup(url_4.content, 'html.parser')


body_4 = html_4.select('body')

word_4 = []	# 맨 처음 크롤링한 데이터

for tag in body_4:

	word_4.append(tag.get_text().strip())


word_list_4 = []
word_list_4 = ''.join(word_4).lower().split()	# 공백 기준으로 나누기


clean_list_4 = []
clean_list_4 = clean_word_list(word_list_4)	# 특수 문자 제거


process_new_sentence(clean_list_4)



# 벡터 길이 같게 하기 위해 마지막에 생성

#print(sent_list[0])
v1 = np.array(make_vector(0, clean_list))
#print(v1)


#print(sent_list[1])
v2 = np.array(make_vector(1, clean_list_2))
#print(v2)


#print(sent_list[2])
v3 = np.array(make_vector(2, clean_list_3))
#print(v3)


#print(sent_list[3])
v4 = np.array(make_vector(3, clean_list_4))
#print(v4)


dotpro_1 = np.dot(v1, v2)
cosSimil_1 = dotpro_1 / (sum(v1**2) * sum(v2**2))

#print(dotpro_1)
print("Cosine Similarity (v1, v2) : ", cosSimil_1)


dotpro_2 = np.dot(v1, v3)
cosSimil_2 = dotpro_2 / (sum(v1**2) * sum(v3**2))

#print(dotpro_2)
print("Cosine Similarity (v1, v3) : ", cosSimil_2)


dotpro_3 = np.dot(v1, v4)
cosSimil_3 = dotpro_3 / (sum(v1**2) * sum(v4**2))


#print(dotpro_3)
print("Cosine Similarity (v1, v4) : ", cosSimil_3)
