# stackoverflow_api_wrapper
This is a wrapper for Stack Overflow API

Instructions:

1) git clone https://github.com/athaser/stackoverflow_api_wrapper
2) cd to the folder
3) docker-compose build
4) docker-compose up

Objective:

The objective is to create a Python service that retrieves data from the StackExchange API and calculates some simple statistics.

Description
The high-level objective is to deliver an application that runs as a long-running service which provides a REST API with an endpoint that takes as input a date/time range, retrieves data from the StackExchange API, calculates some statistics and reports them back to the user. The service should also cache any request and provide the cached results to any subsequent same request.

Communication with StackExchange API and statistics
The service communicates with the StackExchange API and perform the following tasks:
Retrieve the StackOverflow answer data for the given date/time range (Endpoint: https://api.stackexchange.com/docs/answers).
Retrieve the comment data for this set of answers  (Endpoint: https://api.stackexchange.com/docs/comments-on-answers).

Calculates the following statistics:
The total number of accepted answers.
The average score for all the accepted answers.
The average answer count per question.
The comment count for each of the 10 answers with the highest score.

Response body example
{
    "total_accepted_answers": 10,
    "accepted_answers_average_score": 23.8,
    "average_answers_per_question": 1.3,
    "top_ten_answers_comment_count": {
        "38149500": 1,
        "38152507": 7,
        "38147398": 5,
        "38142598": 2,
        "38149856": 0,
        "38143675": 3,
        "38143335": 1,
        "38143566": 0,
        "38143884": 9,
        "38143115": 1
    }
}

Caching layer
A caching layer has also been implemented. The purpose of caching is to minimize the response time when executing the same request more than once.
The caching layer that is used to the specific project is requests-cache>=0.9.5 (https://requests-cache.readthedocs.io/en/stable/)

Requirements (requirement.txt):
Flask>=2.0.1
flask[async]>=2.0.1
requests-cache>=0.9.5
Flask-Cors>=3.0.10
requests>=2.18.4
python-dateutil>=2.8.1
python-dotenv>=0.17.1

Demonstration Requests:

https://encode.karmanirvami.com/api/v1/stackstats?since=2022-07-01%2000:00:00&until=2022-07-02%2000:00:00

or

https://encode.karmanirvami.com/api/v1/stackstats?since=2022-07-01 00:00:00&until=2022-07-02 00:00:00

or

http://88.80.188.249:5000/api/v1/stackstats?since=2022-07-01%2000:00:00&until=2022-07-02%2000:00:00

Hosted on Linode CLoud Environment (https://www.linode.com/)

DNS SETTINGS

NGINX (https://www.nginx.com/)
Forwards the traffic from 5000 to 443 port

CLOUDFLARE (https://dash.cloudflare.com/)
Is a free CDN framework that offers security and analysis tools

TESTS:
1. Unittest Library was utilized 
2. run python3 api_test.py
3. There are 6 tests in total. 4 pass and 2 fail. The failures are because app.py uses queries in a proper request.
The requests that pass are requests to the DNS and the IP that the FLASK API is hosted. For 1 day (1st July 2022-2nd July 2022)
and for 2 days (1st July 2022-3rd July 2022) as an example. 
