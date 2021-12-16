FROM python:3.7

RUN pip install pip-tools
COPY requirements.in requirements.in
RUN pip-compile
RUN pip install -r requirements.txt

COPY build_graph.py build_graph.py
COPY build_indices.py build_indices.py
COPY src/ src/
