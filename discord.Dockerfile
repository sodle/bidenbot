FROM python:3.9

COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install 

ENTRYPOINT ["pipenv", "run", "discord"]
