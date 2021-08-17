FROM python:3.9

RUN pip install pipenv

RUN useradd -m biden
USER biden

COPY . /home/biden
WORKDIR /home/biden
RUN pipenv install 

RUN pipenv run splunk-py-trace-bootstrap

ENTRYPOINT ["pipenv", "run", "discord"]
