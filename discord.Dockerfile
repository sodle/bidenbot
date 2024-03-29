FROM python:3.9

RUN useradd -m biden
USER biden

COPY . /home/biden
WORKDIR /home/biden
RUN pip3 install --user -r requirements.txt

ENTRYPOINT ["python3", "bidenbot-discord.py"]
