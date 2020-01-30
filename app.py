from flask import Flask, jsonify, abort, request, redirect
from bs4 import BeautifulSoup
import requests
import json
import subprocess

app = Flask(__name__)


def html_maker(URL):
    #get url link here
    response = requests.get(URL)
    source = response.text
    soup = BeautifulSoup(source, 'html.parser')
    qname =  soup.find('div',{'class':'title'}).text[3:]
    problem = soup.find('div',{'class':'problem-statement'})
    statement = problem.find_all('div')[10].text
    inputformat = soup.find('div',{'class':'input-specification'}).text[5:]
    outputformat = soup.find('div',{'class':'output-specification'}).text[6:]
    sample = soup.find('div',{'class':'sample-test'})
    inputsample = sample.find('div',{'class':'input'}).text
    outputsample = sample.find('div',{'class':'output'}).text
    html = "<h2>" + qname + "</h2>" + "<h3>Problem Statement</h3>" + "<p>" + statement + "</p>" + "<h3>Input Format</h3>" + inputformat +  "<h3>Output Format</h3>" + outputformat + "<h3>Sample Input</h3><pre>" + inputsample + "</pre><h3>Sample Output</h3><pre>" + outputsample + "</pre>"
    html = html.replace("\le","<=")
    html = html.replace("$$$","")
    html = html.replace("\cdot","*")
    html = html.replace("\dots","...")
    html = html.replace("\sum","Summation")
    html = html.replace(u'\u2014',"-")
    html = html.replace("\,",",")
    return html

def html_makerV2(URL):
    #get url link here
    html = {}
    response = requests.get(URL)
    source = response.text
    soup = BeautifulSoup(source, 'html.parser')
    qname =  soup.find('title').text
    qname, sep, tail = qname.partition('|')
    body = soup.find('body')
    problem = body.find('div',{'class':'primary-colum-width-left'}).text
    n = len(problem)
    x = slice(515,n)
    problem = problem[x]
    problem, sep, tail = problem.partition('Author')
    html = "<h2>" + qname + "</h2>" + "<pre>" + problem + "</pre>"
    html = html.replace("### Input","<h2>Input</h2>")
    html = html.replace("### Output","<h2>Input</h2>")
    html = html.replace("### Constraints","<h2>Constraints</h2>")
    html = html.replace("### Subtasks","<h2>Subtasks</h2>")
    html = html.replace("### Explanation","<h2>Explanation</h2>")
    html = html.replace("### Example Input","<h2>Example Input</h2>")
    html = html.replace("### Example Output","<h2>Example Output</h2>")
    html = html.replace("\le","<=")
    html = html.replace("\ldots","...")
    html = html.replace("*","")
    html = html.replace("\cdot","*")
    html = html.replace("\sum","Summation")
    html = html.replace("$","")
    return html

def output_maker():
    #get solution file here
    subprocess.call("g++ solution.cpp",shell = True)
    subprocess.call("./test.sh",shell = True)

@app.route('/', methods=['POST','GET'])
def main():
    url = request.json['url']
    if "codeforces" in url:
        response = html_maker(url)
    elif "codechef" in url:
        response = html_makerV2(url)
    else:
        response = {"html":{}}
    #output_maker()
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


