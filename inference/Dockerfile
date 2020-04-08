FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src /src
COPY ./config.json /config.json
COPY ./main.py /main.py

CMD [ "python", "main.py" ]
