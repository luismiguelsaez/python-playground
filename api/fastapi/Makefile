.PHONY: build test push

build:
	docker build -t fastapi:latest .

push:
	docker login -u luismiguelsaez
	docker tag fastapi:latest docker.io/luismiguelsaez/fastapi:latest
	docker push docker.io/luismiguelsaez/fastapi:latest

test:
	echo "Creating local environment ..."
	docker-compose up -d --build

	echo "Launching test commands"
	curl -XGET localhost:8000
	curl -XGET localhost:8000/list

helm-install:
	helm install fastapi helm/fastapi
