import requests
import requests_cache

from request_answers import function_request_answers

j=0
number0fcomments=[]
answerids_comments=[]
dict_answers_comments={}

def function_request_comments(fromdate, todate):
  global j, dict_answers_comments
  dict_answerids = function_request_answers(fromdate, todate)
  
  while j <10:
    url = "https://api.stackexchange.com/2.3/answers/{}/comments?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&order=desc&sort=creation&filter=default".format(str(dict_answerids[3][j][0]))
    requests_cache.install_cache('comments_cache')
    response = requests.request("GET", url)
    json_response = response.json()
    length_json_response = len(json_response['items'])
    answerids_comments.append(str(dict_answerids[3][j][0]))
    number0fcomments.append(length_json_response)
    dict_answers_comments = dict(zip(answerids_comments, number0fcomments))
    j+=1
  return(dict_answers_comments)