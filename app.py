#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import sys
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, url_for
import numpy as np
import math
import nltk; nltk.download('punkt')
from nltk import word_tokenize
from elasticsearch import Elasticsearch


app = Flask(__name__, static_url_path='/static')


# 전역 변수
word_d = {}
word_d_2 = {}

sent_list = []
sent_list_2 = []

# global로 바꾸자
v1 = []; v2 = []; v3 = []; v4 = []
dotpro_1 = 0; dotpro_2 = 0; dotpro_3 = 0
cosSimil_1 = 0; cosSimil_2 = 0; cosSimil_3 = 0

dic = {}
w_list = []
tf_list = []




# 특수문자 제거 (공백 제외)
def clean_word_list(input_list):

    output_list = []

    for word in input_list:
        symbols = """!•@#$%^&*()_-+={[}]|\\;:"‘'·<>?/.,"""

        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')

        if len(word) > 0 :
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


# { '단어' : '빈도수' } - tf-idf용
def process_new_sentence_2(input_list):
		
	sent_list_2.append(input_list)

	tokenized = word_tokenize(input_list)

	for word in tokenized:

		if word not in word_d_2.keys():
			word_d_2[word] = 0

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


# idf 계산
def compute_idf():

	Dval = len(sent_list_2)
	bow = set()

	for i in range(0, len(sent_list_2)):

		tokenized = word_tokenize(sent_list_2[i])

		for tok in tokenized:
			bow.add(tok)


	idf_d = {}

	for t in bow:

		cnt = 0

		for s in sent_list_2:

			if t in word_tokenize(s):
				cnt += 1

				idf_d[t] = math.log(Dval/cnt)

	return idf_d


# 시작 화면
@app.route('/')

def index():
    return render_template('home.html')


# 단일 URL 입력
@app.route('/box', methods=['POST'])

def box():

	global v1, v2, v3, v4, dotpro_1, dotpro_2, dotpro_3, cosSimil_1, cosSimil_2, cosSimil_3
	# 1 (기준)
	url = requests.get("https://nutch.apache.org/")
	html = BeautifulSoup(url.content, 'html.parser')


	body = html.select('body')

	word = []

	for tag in body:

		word.append(tag.get_text().strip())


	word_list = []
	word_list = ''.join(word).lower().split()


	clean_list = []
	clean_list = clean_word_list(word_list)


	process_new_sentence(clean_list)
	process_new_sentence_2(' '.join(clean_list))



	# 2
	url_2 = requests.get("http://attic.apache.org/")
	html_2 = BeautifulSoup(url_2.content, 'html.parser')


	body_2 = html_2.select('body')

	word_2 = []

	for tag in body_2:

		word_2.append(tag.get_text().strip())


	word_list_2 = []
	word_list_2 = ''.join(word_2).lower().split()


	clean_list_2 = []
	clean_list_2 = clean_word_list(word_list_2)


	process_new_sentence(clean_list_2)
	process_new_sentence_2(' '.join(clean_list_2))



	# 3
	url_3 = requests.get("https://brooklyn.apache.org/")
	html_3 = BeautifulSoup(url_3.content, 'html.parser')


	body_3 = html_3.select('body')

	word_3 = []

	for tag in body_3:

		word_3.append(tag.get_text().strip())


	word_list_3 = []
	word_list_3 = ''.join(word_3).lower().split()


	clean_list_3 = []
	clean_list_3 = clean_word_list(word_list_3)


	process_new_sentence(clean_list_3)
	process_new_sentence_2(' '.join(clean_list_3))



	# 4
	url_4 = requests.get("https://allura.apache.org/")
	html_4 = BeautifulSoup(url_4.content, 'html.parser')


	body_4 = html_4.select('body')

	word_4 = []

	for tag in body_4:

		word_4.append(tag.get_text().strip())


	word_list_4 = []
	word_list_4 = ''.join(word_4).lower().split()


	clean_list_4 = []
	clean_list_4 = clean_word_list(word_list_4)


	process_new_sentence(clean_list_4)
	process_new_sentence_2(' '.join(clean_list_4))



	# 벡터 생성
	v1 = np.array(make_vector(0, clean_list))

	v2 = np.array(make_vector(1, clean_list_2))

	v3 = np.array(make_vector(2, clean_list_3))

	v4 = np.array(make_vector(3, clean_list_4))


	# 내적
	dotpro_1 = np.dot(v1, v2)
	cosSimil_1 = dotpro_1 / (sum(v1**2) * sum(v2**2))

	dotpro_2 = np.dot(v1, v3)
	cosSimil_2 = dotpro_2 / (sum(v1**2) * sum(v3**2))

	dotpro_3 = np.dot(v1, v4)
	cosSimil_3 = dotpro_3 / (sum(v1**2) * sum(v4**2))



	# tf-idf
	
	global dic
	
	idf_d = compute_idf()

	for i in range(0, len(sent_list_2)):

		tf_d = compute_tf(sent_list_2[i])

		for word, tfval in tf_d.items():

			dic[word] = tfval * idf_d[word]


	dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)


	count = 0

	# w_list = []
	# tf_list = []

	while count < 10:

		w_list.append(dic[count][0])
		tf_list.append(dic[count][1])

		count = count + 1



	return render_template('home.html', sim1 = cosSimil_1, sim2 = cosSimil_2, sim3 = cosSimil_3, word = w_list, tf = tf_list)





# txt 파일 입력
@app.route('/txt', methods=['POST'])
def txt():
    # 주소 받는 거
    # # submit 시 request 된 파일 데이터 처리
    # f = request.files['file']

    # # 이렇게 하면 앞에 b' 뒤에 \n' 이 붙어서 나옴
    # myurl2 = []
    # for lines in f:
    #     myurl2.append(lines)

    # return render_template('home.html', file=myurl2)

    #1 기준
    url = requests.get("https://nutch.apache.org/")
    html = BeautifulSoup(url.content, 'html.parser')

    body = html.select('body')

    word = []

    for tag in body:
        word.append(tag.get_text().strip())
    
    # word를 문자열로 변환 후, 공백 기준으로 나누기
    word_list = []
    word_list = ''.join(word).lower().split

    clean_list = []
    clean_list = clean_word_list(word_list)

    process_new_sentence(clean_list)


    #2
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
    #print("Cosine Similarity (v1, v2) : ", cosSimil_1)

    dotpro_2 = np.dot(v1, v3)
    cosSimil_2 = dotpro_2 / (sum(v1**2) * sum(v3**2))

    #print(dotpro_2)
    #print("Cosine Similarity (v1, v3) : ", cosSimil_2)

    dotpro_3 = np.dot(v1, v4)
    cosSimil_3 = dotpro_3 / (sum(v1**2) * sum(v4**2))

    #print(dotpro_3)
    #print("Cosine Similarity (v1, v4) : ", cosSimil_3)
    return render_template('home.html', sim1 = cosSimil_1, sim2 = cosSimil_2, sim3 = cosSimil_3)



@app.route('/elastic', methods = ['POST'])

def elastic():

	es_host = "127.0.0.1"
	es_port = "9200"
	# http://127.0.0.1:9200/final/project/1?pretty

	es = Elasticsearch([{'host': es_host, 'port': es_port}], timeout=30)

	doc = {
		"v1": v1,
		"v2": v2,
		"v3": v3,
		"v4": v4,

		"dotpro_1": dotpro_1,
		"dotpro_2": dotpro_2,
		"dotpro_3": dotpro_3,

		"cosSimil_1": cosSimil_1,
		"cosSimil_2": cosSimil_2,
		"cosSimil_3": cosSimil_3,

		"word list": w_list,
		"tf-idf list": tf_list
	}


	res = es.index(index="final", doc_type="project", id=1, body=doc)

	return render_template('home.html')


if __name__ == '__main__':

	

	app.run(debug=True)

	
    # with open(url_for('static'), filename=file) as f:
    #     for line in f:
    #         str = line
    #         arr = str.split('\n')



