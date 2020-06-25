#!/usr/bin/python
#-*- coding: utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
import sys
from flask import Flask, request, render_template


app = Flask(__name__, static_url_path='/static')

@app.route('/')

def index():
    return render_template('page.html')


@app.route('/box', methods=['GET'])


def read_url():

	if request.method == 'GET':

		url = requests.get("https://nutch.apache.org/")
		html = BeautifulSoup(url.content, 'html.parser')


		body = html.select('body')

		word = []


		for tag in body:

			word.append(tag.get_text().strip())


		"""
		freq
		"""

		word_list = []

		# word 리스트를 문자열로 변환 후, 공백 기준으로 나누기
		word_list = ''.join(word).lower().split()


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
			

		clean_list = []

		clean_list = clean_word_list(word_list)


		# { '단어' : '빈도수' }
		def counter(input_list):

			word_count = {}
			
			for word in input_list:

				if word in  word_count:

					word_count[word] += 1

				else:
					word_count[word] = 1

			return word_count


		word_count = counter(clean_list)

		word_count = sorted(word_count.items(), key=lambda x:x[1], reverse=True)



		count = 0

		w_list = []
		f_list = []

		while count < 30:

			w_list.append(word_count[count][0])
			f_list.append(word_count[count][1])

			count = count + 1

	
		"""
		res = requests.args.get('https://github.com/trending/python?since=monthly')
		#https://github.com/trending/python?since=monthly
		"""
		return render_template('page.html', url1 = url, word_list = w_list, freq = f_list)


@app.route('/txt', methods=['POST'])

def read_txt():

    if request.method == 'POST':
        f = request.files['file'].read()

        return f

if __name__ == '__main__':
    app.run(debug=True)
