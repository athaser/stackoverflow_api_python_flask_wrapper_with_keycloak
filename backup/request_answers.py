import requests
import requests_cache
import json
import time

page_size=100
xa=1
i=0
questionids=[]
answerids=[]
scoretable=[]
first10values={}
statistics=[]
avegare_answers_per_question=0

def function_request_answers(fromdate, todate):
  global i, xa, statistics, avegare_answers_per_question, first10values
  i+=1  
  url = "https://api.stackexchange.com/2.3/answers?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&pagesize={}&fromdate={}&todate={}&order=desc&sort=activity&filter=default&page={}".format(page_size, fromdate, todate, i)
  requests_cache.install_cache('demo_cache')
  response = requests.request("GET", url)
  json_response = response.json()

  if json_response['has_more']==True and xa==1:
    function_is_accepted(json_response['items'])
    function_request_answers(fromdate, todate) 
  elif json_response['has_more']==False:
    last_page_size = len(json_response['items'])
    statistics=function_is_accepted_last_page(json_response['items'], last_page_size)
    avegare_answers_per_question = len(statistics[2])/len(set(statistics[2]))
    first10values=statistics[3][:10]
    xa=2
    print("The end of specific timeframe, Total_Accepted_Answers:{}, Score:{}, Average_answers_per_question:{}, Top 10 Score Answers:{} ".format(statistics[0], statistics[1], avegare_answers_per_question, first10values))
  return(statistics[0], statistics[1], avegare_answers_per_question, first10values)

count_accepted_answers=0
count_score=0
average_score = 0

def function_is_accepted(resp):
  y=0
  global count_accepted_answers, count_score
  while y<page_size:
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


