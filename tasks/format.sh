pip install autoflake isort black --quiet --disable-pip-version-check

# format python
autoflake -i --remove-all-unused-imports --ignore-init-module-imports --recursive .
isort ./**/*.py
black . --line-length 80
