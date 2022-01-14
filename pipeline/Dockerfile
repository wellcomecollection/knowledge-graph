FROM python:3.7

RUN pip install pip-tools
COPY requirements.in requirements.in
RUN pip-compile
RUN pip install -r requirements.txt

COPY stories /app/stories
COPY src /app/stories/src

COPY works /app/works
COPY src /app/works/src
