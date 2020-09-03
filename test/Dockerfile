FROM python:3.7

# aggregate and install the requirements for containers and tests
RUN pip install pip-tools
COPY test/requirements.in test/requirements.in
COPY enricher/requirements.in enricher/requirements.in
COPY graph_store/requirements.in graph_store/requirements.in
RUN pip-compile --output-file=requirements.txt test/requirements.in enricher/requirements.in graph_store/requirements.in
RUN pip install -r requirements.txt

# copy over the source code and the tests
COPY enricher/test enricher/test
COPY graph_store/test graph_store/test
COPY enricher/app enricher/app 
COPY graph_store/src graph_store/src 
