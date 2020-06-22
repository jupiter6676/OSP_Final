#!/usr/bin/python
#-*- coding: utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
import sys
from elasticsearch import Elasticsearch



"""
crawling
"""

url_1 = requests.get("http://attic.apache.org/")

html_1 = BeautifulSoup(url_1.content, 'html.parser')


body_1 = html_1.select('body')

word_1 = []


for tag in body_1:
	
	word_1.append(tag.get_text().strip())


"""
freq
"""

word_list_1 = []

# word_1 리스트를 문자열로 변환 후, 공백 기준으로 나누기
word_list_1 = ''.join(word_1).lower().split()

# print(word_list_1)


# 특수문자 제거

def clean_word_list(input_list):

	output_list = []

	for word in input_list:

		symbols = """!@#$%^&*()_-+={[}]|\;:"‘'·<>?/., """

		for i in range(len((symbols))):
			word = word.replace(symbols[i], '')

		if len(word) > 0:
			output_list.append(word)

	return output_list
		

clean_list_1 = []

clean_list_1 = clean_word_list(word_list_1)

# print(clean_list_1)



# { '단어' : '빈도수' }
def counter(input_list):

	word_count = {}
	
	for word in input_list:

		if word in  word_count:

			word_count[word] += 1

		else:
			word_count[word] = 1

	return word_count


word_count_1 = counter(clean_list)

word_count_1 = sorted(word_count_1.items(), key=lambda x:x[1], reverse=True)

#print(word_count_1)



count_1 = 0

w_list_1 = []
f_list_1 = []

while count < 30:

	w_list_1.append(word_count_1[count][0])
	f_list_1.append(word_count_1[count][1])

	count_1 = count_1 + 1

print(w_list_1)
print(f_list_1)
