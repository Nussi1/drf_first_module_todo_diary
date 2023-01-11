FROM python:3.10

WORKDIR /apps

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD . /apps

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python manage.py makemigrations && python manage.py migrate
COPY . /