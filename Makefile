  
.PHONY: clean lint test run 

default: run

clean:
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf ./*/__pycache__

lint:
	isort enricher/*.py graph_store/*.py
	black . --line-length 80
	flake8 .

test:
	python -m pytest ./graph_store/test/ ./enricher/test/

run: clean lint test
	docker-compose up --build

