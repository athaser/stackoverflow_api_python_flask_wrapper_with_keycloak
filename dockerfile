FROM python:3.8-alpine
RUN apk update
RUN apk add make automake gcc g++ subversion
WORKDIR /home/
RUN mkdir /flaskapp
WORKDIR /flaskapp
ENV FLASK_ENV="production"
RUN apk add --no-cache gcc musl-dev linux-headers
ADD . .
RUN pip3 install -r requirement.txt
EXPOSE 5000
RUN echo ${PWD}
WORKDIR ./
CMD ["python3", "app.py", "run", "host=0.0.0.0:5000"]
