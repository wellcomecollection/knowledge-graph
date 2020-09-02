  
.PHONY: clean lint test pipeline run--no-tests run

default: run

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

run--no-tests: clean lint pipeline

run: clean lint test pipeline
