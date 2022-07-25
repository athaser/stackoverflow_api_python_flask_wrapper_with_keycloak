import requests
import json
import datetime
import time
import flask
from flask_cors import CORS, cross_origin
from flask import request

from request_answers import function_request_answers
from request_comments import function_request_comments

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


@app.route('/api/v1/stackstats', methods=['GET'])
@cross_origin("*")
def api_encode():
    
    fromdate = request.args.get('since'.format(datetime.date.isoformat))
    convert_to_timestamp_since = datetime.datetime.strptime(fromdate, "%Y-%m-%d %H:%M:%S")
    unix_time_since = int(datetime.datetime.timestamp(convert_to_timestamp_since))
    
    todate = request.args.get('until'.format(datetime.date.isoformat))
    convert_to_timestamp_until = datetime.datetime.strptime(todate, "%Y-%m-%d %H:%M:%S")
    unix_time_until = int(datetime.datetime.timestamp(convert_to_timestamp_until))


    statistics_payload_answer = function_request_answers(unix_time_since, unix_time_until)
    statistis_payload_commend = function_request_comments(unix_time_since, unix_time_until)

    a = payload(statistics_payload_answer[0], statistics_payload_answer[1], statistics_payload_answer[2], statistis_payload_commend)
    return a


if __name__ == '__main__':
    app.run(host=rest_hostname, port=rest_port, debug=True)