FROM python:3.6.1

WORKDIR /app

ADD . /app

CMD [ "python", "./facebook_gather.py" ]

