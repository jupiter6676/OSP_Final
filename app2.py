#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import sys
import requests, time
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, url_for, redirect
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

word_sum = 0

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
    global word_sum
    
    for word in input_list:
        word_sum += 1
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
            if t == word:
                val += 1

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
    # 시작 시간
    start = time.time()
    
    global v1, v2, v3, v4, dotpro_1, dotpro_2, dotpro_3, cosSimil_1, cosSimil_2, cosSimil_3

    # 1
    myurl = request.form['wa']
    res = requests.get(myurl)
    html = BeautifulSoup(res.content, 'html.parser')
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


    #2


    # 누적 xxx
    global word_sum
    total_sum = word_sum
    word_sum = 0

    # tf-idf
    global dic
    
    idf_d = compute_idf()
    
    for i in range(0, len(sent_list_2)):
        tf_d = compute_tf(sent_list_2[i])
        
        for word, tfval in tf_d.items():
            dic[word] = tfval * idf_d[word]
            
    dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    
    count = 0
    
    while count < 10:
        w_list.append(dic[count][0])
        tf_list.append(dic[count][1])
        
        count = count + 1
        
    success = "success"
    
    mytime = time.time() - start    # 처리 시간
    mytime = round(mytime, 3)       # 소수점 셋째 자리까지

    # if request.method == 'POST':
    return render_template('page.html', wa=myurl, status=success, total=total_sum, time=mytime, sim1=cosSimil_1, sim2=cosSimil_2, sim3=cosSimil_3, word=w_list, tf=tf_list)
    

# txt 파일 입력
@app.route('/txt', methods=['POST'])
def txt():
    # 주소 받기
    # submit 시 request 된 파일 데이터 처리
    # f = request.files['file']

    # 이렇게 하면 앞에 b' 뒤에 \n' 붙어서 나옴
    # myurl2 = []
    # for lines in f:
    #   myurl2.append(lines)

    # return render_template('page.html', file=myurl2)


    #1 기준
    url = requests.get("https://nutch.apache.org/")
    html = BeautifulSoup(url.content, 'html.parser')

    body = html.select('body')

    word = []

    for tag in body:
        word.append(tag.get_text().strip())

    # word를 문자열로 변환 후, 공백 기준으로 나누기
    word_list = []
    word_list = ''.join(word).lower().split()

    clean_list = []
    clean_list = clean_word_list(word_list)

    process_new_sentence(clean_list)


    #2
    url2 = requests.get("http://attic.apache.org/")
    html2 = BeautifulSoup(url2.content, 'html.parser')

    body2 = html2.select('body')

    word2 = []      # 맨 처음 크롤링한 데이터

    for tag in body2:
        word2.append(tag.get_text().strip())

    # 공백 기준으로 나누기
    word_list2 = []
    word_list2 = ''.join(word2).lower().split()

    # 특수 문자 제거
    clean_list2 = []
    clean_list2 = clean_word_list(word_list2)

    process_new_sentence(clean_list2)


    #3
    url3 = requests.get("https://brooklyn.apache.org/")
    html3 = BeautifulSoup(url3.content, 'html.parser')

    body3 = html3.select('body')

    word3 = []      # 맨 처음 크롤링한 데이터

    for tag in body3:
        word2.append(tag.get_text().strip())

    # 공백 기준으로 나누기
    word_list3 = []
    word_list3 = ''.join(word3).lower().split()

    # 특수 문자 제거
    clean_list3 = []
    clean_list3 = clean_word_list(word_list3)

    process_new_sentence(clean_list3)


    #4
    url4 = requests.get("https://allura.apache.org/")
    html4 = BeautifulSoup(url4.content, 'html.parser')

    body4 = html4.select('body')

    word4 = []      # 맨 처음 크롤링한 데이터

    for tag in body4:
        word2.append(tag.get_text().strip())

    # 공백 기준으로 나누기
    word_list4 = []
    word_list4 = ''.join(word4).lower().split()

    # 특수 문자 제거
    clean_list4 = []
    clean_list4 = clean_word_list(word_list4)

    process_new_sentence(clean_list4)


    # 벡터 길이 같게 하기 위해 마지막에 생성
    v1 = np.array(make_vector(0, clean_list))
    v2 = np.array(make_vector(1, clean_list2))
    v3 = np.array(make_vector(2, clean_list3))
    v4 = np.array(make_vector(3, clean_list4))


    dotpro_1 = np.dot(v1, v2)
    cosSimil_1 = dotpro_1 / (sum(v1**2) * sum(v2**2))

    dotpro_2 = np.dot(v1, v3)
    cosSimil_2 = dotpro_2 / (sum(v1**2) * sum(v3**2))

    dotpro_3 = np.dot(v1, v4)
    cosSimil_3 = dotpro_3 / (sum(v1**2) * sum(v4**2))

    return render_template('page.html', sim1=cosSimil_1, sim2=cosSimil_2, sim3=cosSimil_3)


@app.route('/elastic', methods = ['POST'])
def elastic():
    es_host = "127.0.0.1"
    es_port = "9200"

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

    res = es.index(index='final', doc_type='project', id=1, body=doc)

    return render_template('page.html')


@app.route('/tfidf')
def tfidf():
    return render_template('word.html', word=w_list)


# @app.route('/cos')
# def cos():


if __name__ == '__main__':
    app.run(debug=True)

    # with open(url_for('static'), filename=file) as f:
    #     for line in f:
    #         str = line
    #         arr = str.split('\n')
