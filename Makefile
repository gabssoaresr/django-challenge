service :=

init:
	cp .env.example .env
build:
	sudo docker compose up $(service) --build -d
	sudo docker compose logs -f
restart:
	sudo docker compose restart $(service)
	sudo docker compose logs -f
rebuild:
	sudo docker compose down $(service) --remove-orphans --volumes
	make build
recreate: 
	sudo docker compose up $(service) --build --force-recreate -d 
	sudo docker compose logs -f
run: 
	sudo docker compose down $(service)
	sudo docker compose up $(service) -d
	sudo docker compose logs -f
down: 
	sudo docker compose down $(service) --remove-orphans --volumes

terminal:
	if [ -z "$(service)" ]; then \
		docker compose exec -it application bash; \
	else \
		docker compose exec -it $(service) bash; \
	fi
	
logs:
	docker compose logs $(service) -f

prune-all:
	docker system prune --all --force

format:
	isort app/
	black -l 79 app/
	black -l 79 tests/

lint:
	flake8 app/
	black -l 79 --check app/
	black -l 79 --check tests/

clean:
	@find ./ -name '*.pyc' -exec sudo rm -f {} \;
	@find ./ -name '__pycache__' -exec sudo rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec sudo rm -f {} \;
	@find ./ -name '*~' -exec sudo rm -f {} \;
	@sudo rm -rf .cache
	@sudo rm -rf .pytest_cache
	@sudo rm -rf .mypy_cache
	@sudo rm -rf build
	@sudo rm -rf dist
	@sudo rm -rf *.egg-info
	@sudo rm -rf htmlcov
	@sudo rm -rf .tox/
	@sudo rm -rf docs/_build