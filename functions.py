#Variables, Tables, Dicts
#Initialize original-starting values
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

#FUNCTIONS
#This is the function to count all requested statistics except last page 
def function_is_accepted(api_response, ii):
  y=0
  global count_accepted_answers, count_score
  if ii==1:
    count_accepted_answers=0
    count_score=0
  while y<page_size and ii!=1:
    is_accepted = api_response[y]['is_accepted']
    questionids.append(api_response[y]["question_id"])
    answerids.append(api_response[y]["answer_id"])
    scoretable.append(api_response[y]["score"])
    if is_accepted==True:
      count_accepted_answers+=1
      count_score += api_response[y]['score']
      y+=1
    else:
      y+=1
  return(count_accepted_answers)

#Function to calculate the final requested statistical values of the last page and calculates the oucome of the results which is returned
def function_is_accepted_last_page(api_response, size_last):
  y=0
  global count_accepted_answers, count_score, average_score, sort_answers_by_score
  while y<size_last:
    is_accepted = api_response[y]['is_accepted']
    questionids.append(api_response[y]["question_id"])
    answerids.append(api_response[y]["answer_id"])
    scoretable.append(api_response[y]["score"])
    dict_answers_score = dict(zip(answerids, scoretable))
    sort_answers_by_score = sorted(dict_answers_score.items(), key=lambda x: x[1], reverse=True)
    if is_accepted==True:
      count_accepted_answers+=1
      count_score += api_response[y]['score']
      average_score = count_score / count_accepted_answers
      y+=1
    else:
      y+=1
  return(count_accepted_answers, average_score, questionids, sort_answers_by_score)