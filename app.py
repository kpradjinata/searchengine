from flask import Flask, render_template, request
from indexer import Indexer
import os
import sys
from nltk.stem import PorterStemmer
import json
from query import query
#import openai chatbot
import openai
import backoff  # for exponential backoff


# from query import process_queries_in_parallel
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
# @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def search():
    uinput = request.form['query']
    #time taken to query in milli seconds
    time_taken = time.perf_counter()
    top_five = query(5, uinput)
    time_taken = time.perf_counter() - time_taken

    chatbot_responses = []

    #openai chatbot
    openai.api_key = "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"
    
    for url in top_five:
        if(top_five.index(url) < 0):
            response = openai.Completion.create(model="text-davinci-003 ", prompt="Tell me briefly about this website" + str(url))
            chatbot_responses.append(response.choices[0].text)
        else:
            response = 'ai response placeholder due to openai api limit'
            chatbot_responses.append(response)
        
    
    for result in top_five:
        top_five[top_five.index(result)] = [result[0], result[1], chatbot_responses[top_five.index(result)]]

    return render_template('result.html', results=top_five, time_taken=time_taken)

app.run(port=8000)  # Change the port number to 8000 or any available port
