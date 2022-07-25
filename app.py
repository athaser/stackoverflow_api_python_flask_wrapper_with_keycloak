import requests
import json
import datetime
import time
import flask
from flask_cors import CORS, cross_origin
from flask import request
import requests_cache

def payload(a, b, c, d):
    x = {
        "total_accepted_answers":a,
        "accepted_answers_average_score":b,
        "average_answers_per_question":c,
        "top_ten_answers_comment_count":d
    }        
    return x

################FLASK ############

rest_hostname = "0.0.0.0"
rest_port = 5000

FLASK_DEBUG = True
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = FLASK_DEBUG

headers = {
  'Content-Type': 'application/json'
}

app.config.update({
    'TESTING': True,
    'DEBUG': True,
    'TEMPLATES_AUTO_RELOAD': True
})

page_size=100
i=1
questionids=[]
answerids=[]
scoretable=[]
statistics=[]
number0fcomments=[]
answerids_comments=[]
dict_answers_comments={}
first10values={}
avegare_answers_per_question=0
count_accepted_answers = 0
average_score=0
count_score = 0
j=0
count_accepted_answers=0
count_score=0
average_score = 0

@app.route('/api/v1/stackstats', methods=['GET'])
@cross_origin("*")
def api_encode():
    global i, statistics, avegare_answers_per_question, first10values, j, dict_answers_comments, count_accepted_answers, average_score, count_score, questionids, answerids, number0fcomments

    fromdate = request.args.get('since'.format(datetime.date.isoformat))
    convert_to_timestamp_since = datetime.datetime.strptime(fromdate, "%Y-%m-%d %H:%M:%S")
    unix_time_since = int(datetime.datetime.timestamp(convert_to_timestamp_since))
    
    todate = request.args.get('until'.format(datetime.date.isoformat))
    convert_to_timestamp_until = datetime.datetime.strptime(todate, "%Y-%m-%d %H:%M:%S")
    unix_time_until = int(datetime.datetime.timestamp(convert_to_timestamp_until))

    url = "https://api.stackexchange.com/2.3/answers?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&pagesize={}&fromdate={}&todate={}&order=desc&sort=activity&filter=default&page={}".format(page_size, unix_time_since, unix_time_until, i)
    requests_cache.install_cache('demo_cache')
    response = requests.request("GET", url)
    json_response = response.json()

    while json_response['has_more']==True:
        function_is_accepted(json_response['items'], i)
        url = "https://api.stackexchange.com/2.3/answers?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&pagesize={}&fromdate={}&todate={}&order=desc&sort=activity&filter=default&page={}".format(page_size, unix_time_since, unix_time_until, i)
        requests_cache.install_cache('demo_cache')
        response = requests.request("GET", url)
        json_response = response.json()
        i+=1
    else:   
        last_page_size = len(json_response['items'])
        statistics=function_is_accepted_last_page(json_response['items'], last_page_size)
        avegare_answers_per_question = len(statistics[2])/len(set(statistics[2]))
        first10values=statistics[3][:10]
        
        for j in range (len(first10values)):
          url2 = "https://api.stackexchange.com/2.3/answers/{}/comments?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&order=desc&sort=creation&filter=default".format(str(first10values[j][0]))
          requests_cache.install_cache('comments_cache')
          response = requests.request("GET", url2)
          json_response = response.json()
          length_json_response = len(json_response['items'])
          answerids_comments.append(str(first10values[j][0]))
          number0fcomments.append(length_json_response)
          dict_answers_comments = dict(zip(answerids_comments, number0fcomments))
          
    a = payload(statistics[0], statistics[1], avegare_answers_per_question, dict_answers_comments)
    list(statistics).clear()
    average_answers_per_question=0
    questionids.clear()
    answerids.clear()
    scoretable.clear()
    average_score=0
    i=1
    count_accepted_answers=0
    count_score = 0 
    first10values.clear()
    answerids_comments.clear()
    number0fcomments.clear()
    j=0
    return a

def function_is_accepted(resp, ii):
  y=0
  global count_accepted_answers, count_score
  while y<page_size and ii!=1:
    is_accepted = resp[y]['is_accepted']
    questionids.append(resp[y]["question_id"])
    answerids.append(resp[y]["answer_id"])
    scoretable.append(resp[y]["score"])
    if is_accepted==True:
      count_accepted_answers+=1
      count_score += resp[y]['score']
      y+=1
    else:
      y+=1
  return(count_accepted_answers)

def function_is_accepted_last_page(resp, size_last):
  y=0
  global count_accepted_answers, count_score, average_score, sort_answers_by_score
  while y<size_last:
    is_accepted = resp[y]['is_accepted']
    questionids.append(resp[y]["question_id"])
    answerids.append(resp[y]["answer_id"])
    scoretable.append(resp[y]["score"])
    dict_answers_score = dict(zip(answerids, scoretable))
    sort_answers_by_score = sorted(dict_answers_score.items(), key=lambda x: x[1], reverse=True)
    if is_accepted==True:
      count_accepted_answers+=1
      count_score += resp[y]['score']
      average_score = count_score / count_accepted_answers
      y+=1
    else:
      y+=1
  return(count_accepted_answers, average_score, questionids, sort_answers_by_score)

if __name__ == '__main__':
    app.run(host=rest_hostname, port=rest_port, debug=True)