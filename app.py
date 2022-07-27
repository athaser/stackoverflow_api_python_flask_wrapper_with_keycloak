import requests
import datetime
import flask
from flask_cors import CORS, cross_origin
from flask import request
import requests_cache

#Import Variables from functions.py
from functions import page_size, i , questionids, answerids, scoretable, statistics, number0fcomments, answerids_comments, dict_answers_comments, first10values, avegare_answers_per_question, count_accepted_answers, average_score, count_score, j, count_accepted_answers, count_score, average_score
#Import Functions from functions.py
from functions import function_is_accepted, function_is_accepted_last_page
#import timestamp function from timestamp.py
from timestamp import function_convert_timestamp

#Requested Payload Structure
def payload(a, b, c, d):
    payload_json = {
        "total_accepted_answers":a,
        "accepted_answers_average_score":b,
        "average_answers_per_question":c,
        "top_ten_answers_comment_count":d
    }        
    return payload_json

#Flask configuration
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

#Initialize route - Main API
@app.route('/api/v1/stackstats', methods=['GET'])
@cross_origin("*")
def api_encode():
    global i, statistics, avegare_answers_per_question, first10values, j, dict_answers_comments, count_accepted_answers, average_score, count_score, questionids, answerids, number0fcomments

    fromdate = request.args.get('since'.format(datetime.date.isoformat))
    unix_time_since = function_convert_timestamp(fromdate)
    
    todate = request.args.get('until'.format(datetime.date.isoformat))
    unix_time_until = function_convert_timestamp(todate)

#Stack overflow queries 30-100 results each page. In this example page site was set 100
#When 'has more' attribute is true it means that there are more results for the requested timeframe
#First Request
    url = "https://api.stackexchange.com/2.3/answers?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&pagesize={}&fromdate={}&todate={}&order=desc&sort=activity&filter=default&page={}".format(page_size, unix_time_since, unix_time_until, i)
    requests_cache.install_cache('demo_cache')
    response = requests.request("GET", url)
    json_response = response.json()

#Same request as above to calculate statistics. If 'has more' atrribute is true go to the next page and calculate the data
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

#Request to calculate the questions part of the assesment
        for j in range (len(first10values)):
          url2 = "https://api.stackexchange.com/2.3/answers/{}/comments?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&order=desc&sort=creation&filter=default".format(str(first10values[j][0]))
          requests_cache.install_cache('comments_cache')
          response = requests.request("GET", url2)
          json_response = response.json()
          length_json_response = len(json_response['items'])
          answerids_comments.append(str(first10values[j][0]))
          number0fcomments.append(length_json_response)
          dict_answers_comments = dict(zip(answerids_comments, number0fcomments))
    
    final_payload = payload(statistics[0], statistics[1], avegare_answers_per_question, dict_answers_comments)

#Clear variables - set variables to original values
    list(statistics).clear()
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

    return final_payload

#Main function
if __name__ == '__main__':
    app.run(host=rest_hostname, port=rest_port, debug=True)