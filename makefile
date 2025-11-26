
docker:
	docker compose build
	docker compose up

run:
	fastapi dev main.py