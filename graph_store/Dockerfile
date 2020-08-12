FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY graph_store.py graph_store.py
COPY src/ src/
