import requests
import datetime
import flask
from flask_cors import CORS, cross_origin
from flask import request, Flask, g
from flask_oidc import OpenIDConnect
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

app = Flask(__name__)

app.config.update({
    'SECRET_KEY': 'a41060dd-b5a8-472e-a91f-6a3ab0e04715',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_OPENID_REALM': 'demonstration',
    #'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'TEMPLATES_AUTO_RELOAD': True,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
})

oidc = OpenIDConnect(app)

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

#Initialize route - Main API
@app.route('/', methods=['GET'])
@cross_origin("*")
def api_no_auth():
    global i, statistics, avegare_answers_per_question, first10values, j, dict_answers_comments, count_accepted_answers, average_score, count_score, questionids, answerids, number0fcomments

    fromdate = request.args.get('since'.format(datetime.date.isoformat))
    #unix_time_since = function_convert_timestamp(fromdate)
    unix_time_since = 1656633600
    
    todate = request.args.get('until'.format(datetime.date.isoformat))
    #unix_time_until = function_convert_timestamp(todate)
    unix_time_until = 1656720000
    

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

#Initialize route - Main API
@app.route('/token', methods=['GET'])
@cross_origin("*")
#@oidc.require_login
@oidc.accept_token(True, ['email'])
def api_token():
    global i, statistics, avegare_answers_per_question, first10values, j, dict_answers_comments, count_accepted_answers, average_score, count_score, questionids, answerids, number0fcomments

    fromdate = request.args.get('since'.format(datetime.date.isoformat))
    #unix_time_since = function_convert_timestamp(fromdate)
    unix_time_since = 1656633600
    
    todate = request.args.get('until'.format(datetime.date.isoformat))
    #unix_time_until = function_convert_timestamp(todate)
    unix_time_until = 1656720000
    

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

#Initialize route - Main API
@app.route('/login', methods=['GET', 'POST'])
@cross_origin("*")
@oidc.require_login
#@oidc.accept_token(True, ['email'])
def api_login_form():
    return ('Hello, %s, <a href="/login_payload">See private</a> '
                '<a href="/logout">Log out</a>') % \
            g.oidc_id_token

#Initialize route - Main API
@app.route('/login_payload', methods=['GET', 'POST'])
@cross_origin("*")
@oidc.require_login
#@oidc.accept_token(True, ['email'])
def api_login_payload():
    global i, statistics, avegare_answers_per_question, first10values, j, dict_answers_comments, count_accepted_answers, average_score, count_score, questionids, answerids, number0fcomments

    fromdate = request.args.get('since'.format(datetime.date.isoformat))
    #unix_time_since = function_convert_timestamp(fromdate)
    unix_time_since = 1656633600
    
    todate = request.args.get('until'.format(datetime.date.isoformat))
    #unix_time_until = function_convert_timestamp(todate)
    unix_time_until = 1656720000
    

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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Performs local logout by removing the session cookie."""

    oidc.logout()
    
    return ('Hi, you have been logged out! <a href="https://keycloak.karmanirvami.com:8443/auth/realms/demonstration/protocol/openid-connect/logout?redirect_uri=https://keycloak.karmanirvami.com/login">Return</a>')

#Main function
if __name__ == '__main__':
    app.run(host=rest_hostname, port=rest_port, debug=True)