# stackoverflow_api_wrapper
This is a wrapper for Stack Overflow API

Instructions:

1) git clone https://github.com/athaser/stackoverflow_api_wrapper
2) cd to the folder
3) docker-compose build
4) docker-compose up

OBJECTIVE:

The objective is to create a Python service that retrieves data from the StackExchange API and calculates some simple statistics.

DESCRIPTION:

The high-level objective is to deliver an application that runs as a long-running service which provides a REST API with an endpoint that takes as input a date/time range, retrieves data from the StackExchange API, calculates some statistics and reports them back to the user. The service should also cache any request and provide the cached results to any subsequent same request.

COMMUNICATION WITH STACKEXCAHNGE API AND STATISTICS:

The service communicates with the StackExchange API and perform the following tasks:
Retrieve the StackOverflow answer data for the given date/time range (Endpoint: https://api.stackexchange.com/docs/answers).
Retrieve the comment data for this set of answers  (Endpoint: https://api.stackexchange.com/docs/comments-on-answers).

CALCULATES THE FOLLOWING STATISTICAL VALUES:

1. The total number of accepted answers.
2. The average score for all the accepted answers.
3. The average answer count per question.
4. The comment count for each of the 10 answers with the highest score.

CACHING LAYER

A caching layer has also been implemented. The purpose of caching is to minimize the response time when executing the same request more than once.
The caching layer that is used to the specific project is requests-cache>=0.9.5 (https://requests-cache.readthedocs.io/en/stable/).

Redis cache is also installed in the docker-compose.yml and works together with requests-cahce:__pycache__ folder is the redis cache.

REQUIREMENTS (requirement.txt):
1. Flask>=2.0.1
2. flask[async]>=2.0.1
3. requests-cache>=0.9.5
4. Flask-Cors>=3.0.10
5. requests>=2.18.4
6. python-dateutil>=2.8.1
7. python-dotenv>=0.17.1

FILES:
1. app.py the main flask-api file
2. functions.py: contains the functions to process the data in order for the final static values to be calculated and the original - starting values
3. timestamp.py: converts the timestamp from human form (2022-07-02 00:00:00) to unix form (1656633600)
4. api_test.py: The file that contains 8 tests 6 pass and 2 fail. This file contains the test for the API, the timestamp function that is imported from the timestamp.py file and the function_is_accepted function that is imported from the function.py file
5. api_test_2.py: The file contains one test for the function: function_is_accepted_last_page that is imported from the function.py file
6. dockerfile: the docker setting
7. docker-compose.yml: all the services that are going to be compiled in docker
8. requirement.txt: The requirements of the app. This file is imported in dockerfile
9. demo_cache.sqlite: The cash for the request regarding the answers statistical values
10. comments_cache.sqllite: The cash for the request regarding the comments statistical values
11. __pycache__ (folder): redis cache which has been also implemented with docker
12. backup (folder): backup scripts

FUNCTIONS:

Functions in app.py file
1. payload: the requested payload structure
2. api_encode: tha most importand api function that calls all the other functions to calculate the statistical values
3. main

Functions in functions.py file
1. function_is_accepted: calculates the statistical values of the data that is included in the pages while 'has_more' attribute is true. 'has_more' equals to true means that there are more pages contain data for the specific timeframe.
2. function_is_accepted_last_page: calculates the final statistical values and rerurns them. 'has_more' equals to false

Functions in timestamp.py file
1. function_convert_timestamp: Converts timestamp from human form (2022-07-02 00:00:00) to unix form (1656633600) to use it in stackoverflow api


DEMONSTRATION REQUESTS:

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
2. run python3 api_test.py and python3 api_test_2.py
3. There are 8 tests in api_test.py. 6 pass and 2 fail. The failures are because app.py uses queries in a proper request. The requests that pass are requests to the DNS and the IP that the FLASK API is hosted. For 1 day (1st July 2022-2nd July 2022)
and for 2 days (1st July 2022-3rd July 2022) as an example. 
4. There is just one test in api_test_2.py because of throttle violation in StackOverflow api in case there are 2 requests in the same time. The test passes
5. All the functions were tested

