FROM python:3.7.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /muna-4/createTrend
WORKDIR /muna-4/createTrend
ADD requirements.txt /muna-4/createTrend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /muna-4/createTrend
RUN python manage.py collectstatic