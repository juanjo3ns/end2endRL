build:
	docker-compose -f docker/docker-compose.yml build
run:
	docker-compose -f docker/docker-compose.yml up -d --build
dev:
	docker exec -it algorithmsrl bash
down:
	docker-compose -f docker/docker-compose.yml down -v
