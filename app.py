#!/usr/bin/python
#-*- coding: utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
import sys
from flask import Flask, request, render_template
from nltk import word_tokenize
import numpy


app = Flask(__name__, static_url_path='/static')

@app.route('/')

def index():
    return render_template('page.html')


@app.route('/box', methods=['GET'])


def read_url():


	# 특수문자 제거
	def clean_word_list(input_list):

		output_list = []

		for word in input_list:

			symbols = """!•@#$%^&*()_-+={[}]|\;:"‘'·<>?/., """

			for i in range(len((symbols))):
				word = word.replace(symbols[i], '')

			if len(word) > 0:
				output_list.append(word)

		return output_list


	# { '단어' : '빈도수' }
	def counter(input_list):	# process_new_sentence(s)

		word_count = {}
			
		for word in input_list:

			if word in  word_count:

				word_count[word] += 1

			else:
				word_count[word] = 1

		return word_count



	if request.method == 'GET':

		url = requests.get("https://nutch.apache.org/")
		html = BeautifulSoup(url.content, 'html.parser')


		body = html.select('body')

		word = []	# 맨 처음 크롤링한 데이터


		for tag in body:

			word.append(tag.get_text().strip())


		"""
		freq
		"""

		word_list = []

		word_list = ''.join(word).lower().split()	# word를 문자열로 변환 후, 공백 기준으로 나누기



			

		clean_list = []

		clean_list = clean_word_list(word_list)	# 특수 문자 제거





		word_count = counter(clean_list)	# 딕셔너리

		word_count = sorted(word_count.items(), key=lambda x:x[1], reverse=True)	# 정렬 후 튜플



		count = 0

		w_list = []
		f_list = []

		while count < 30:

			w_list.append(word_count[count][0])
			f_list.append(word_count[count][1])

			count = count + 1





		url_2 = requests.get("http://attic.apache.org/")
		html_2 = BeautifulSoup(url_2.content, 'html.parser')


		body_2 = html_2.select('body')

		word_2 = []	# 맨 처음 크롤링한 데이터


		for tag in body_2:

			word_2.append(tag.get_text().strip())


		"""
		freq
		"""

		word_list_2 = []

		word_list_2 = ''.join(word_2).lower().split()	# word를 문자열로 변환 후, 공백 기준으로 나누기



			

		clean_list_2 = []

		clean_list_2 = clean_word_list(word_list_2)	# 특수 문자 제거





		word_count_2 = counter(clean_list_2)	# 딕셔너리

		word_count_2 = sorted(word_count_2.items(), key=lambda x:x[1], reverse=True)	# 정렬 후 튜플



		count = 0

		w_list_2 = []
		f_list_2 = []

		while count < 30:

			w_list_2.append(word_count_2[count][0])
			f_list_2.append(word_count_2[count][1])

			count = count + 1




		dotpro = numpy.dot(f_list, f_list_2)
		cosSimil = dotpro / (norm(f_list) * norm(f_list_2))
	
		"""
		res = requests.args.get('https://github.com/trending/python?since=monthly')
		#https://github.com/trending/python?since=monthly
		"""
		return render_template('page.html', url1 = url, word_list = w_list, freq = f_list, cos = cosSimil)


@app.route('/txt', methods=['POST'])

def read_txt():

    if request.method == 'POST':
        f = request.files['file'].read()

        return f

if __name__ == '__main__':
    app.run(debug=True)
