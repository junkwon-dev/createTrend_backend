FROM python:3.7.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /createTrend
WORKDIR /createTrend
ADD requirements.txt /createTrend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /createTrend
RUN python manage.py collectstatic