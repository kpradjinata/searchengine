from flask import Flask, render_template, request
from indexer import Indexer
import os
import sys
from nltk.stem import PorterStemmer
import json
from query import query
# from query import process_queries_in_parallel
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    uinput = request.form['query']
    #time taken to query in milli seconds
    time_taken = time.perf_counter()
    top_five = query(5, uinput)
    time_taken = time.perf_counter() - time_taken
    return render_template('result.html', results=top_five, time_taken=time_taken)

app.run(port=8000)  # Change the port number to 8000 or any available port
