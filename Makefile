
install: 
	python -m venv testenv && \
		. testenv/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt

test: 
	. testenv/bin/activate && \
		python -m pytest -vv --cov=main --cov=mypackage test_*.py

format:	
	. testenv/bin/activate && \
		black *.py 

lint: 
	. testenv/bin/activate && \
		ruff check *.py mypackage/*.py

container-lint: 
	docker run --rm -i hadolint/hadolint < .devcontainer/Dockerfile

refactor: format lint

deploy:
	.d testenv/bin/activate && \
		docker build -f .devcontainer/Dockerfile -t arko_cli_tool:latest . && \
		docker rm -f arko_cli_tool || true && \
		docker run -d --name arko_cli_tool -p 80:80 arko_cli_tool:latest
		echo "Deployment completed."

all: install format lint test
