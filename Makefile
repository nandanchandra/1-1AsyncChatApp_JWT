build:
	docker compose -f docker-compose.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

show_logs:
	docker compose -f docker-compose.yml logs

migrate:
	docker compose -f docker-compose.yml run --rm chatappdjango python3 manage.py migrate

makemigrations:
	docker compose -f docker-compose.yml run --rm chatappdjango python3 manage.py makemigrations

collectstatic:
	docker compose -f docker-compose.yml run --rm chatappdjango python3 manage.py collectstatic --no-input --clear

superuser:
	docker compose -f docker-compose.yml run --rm chatappdjango python3 manage.py createsuperuser

down-v:
	docker compose -f docker-compose.yml down -v