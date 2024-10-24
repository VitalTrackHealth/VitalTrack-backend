up:
	docker run --env-file .env -d -p 8000:8000 --name api api:dev

down:
	docker stop api
	docker rm api

build:
	docker build -t api:dev .

