  
.PHONY: clean lint test pipeline populate--no-tests populate

default: populate

clean:
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf ./*/__pycache__

lint:
	isort enricher/**/*.py graph_store/**/*.py
	black . --line-length 80
	flake8 .

test:
	docker-compose up --build tests

pipeline: 
	docker-compose up --build enricher graph_store 

populate--no-tests: clean lint pipeline

populate: clean lint test pipeline
 
api: clean lint
	docker-compose up --build query_api
