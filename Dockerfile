FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN python -m pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /code/